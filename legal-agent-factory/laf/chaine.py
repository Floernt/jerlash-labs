"""Chaîne de bout en bout : événement -> qualification -> tâche Paperclip (simulée)
-> exécution par le runtime -> fichier de sortie.

Répertoire de sortie (distinct du dossier surveillé) :
  evenements/<id>.json        chaque événement reçu
  signalements/<id>.json      fichiers illisibles ou changés en cours de traitement
  qualifications/<id>.json    qualification validée (ou de repli)
  taches-paperclip/<id>.json  charge utile de création de tâche, dry run
  resultats/<id>.json         résultat du runtime

Répertoire d'état : surveillance.json, traites/<id>.json (idempotence), audit.jsonl.

Idempotence : un événement déjà traité (marqueur présent) est ignoré et journalisé
comme doublon. Tous les fichiers de sortie sont nommés d'après l'identifiant de
l'événement, si bien qu'une reprise après interruption réécrit les mêmes fichiers
au lieu d'en créer de nouveaux.
"""

import json
import os

from . import paperclip, qualification as qualif, securite
from .audit import Journal
from .outils_fichiers import ecrire_json, empreinte_fichier, est_dans, horodatage
from .runtime import POLITIQUE_LOT1, RuntimeLocal
from .passerelle import PasserelleSimulee
from .surveillance import identifiant_evenement

TAILLE_MAX_EXTRAIT = 20_000
MODELE_SIMULE = "simule-deterministe"
TYPES_AVEC_TACHE = {"creation", "modification"}

SKILL_SIMULE = {
    "nom": "accuse-reception-simule",
    "version": "0.1",
    "instructions": "Skill de démonstration du Lot 1 : produire un accusé de réception du document, "
                    "sans analyse juridique.",
}


def verifier_repertoires(entree: str, sortie: str, etat: str) -> None:
    """Le dossier surveillé, la sortie et l'état doivent être disjoints."""
    for a, b in ((entree, sortie), (entree, etat), (sortie, entree), (etat, entree)):
        if est_dans(a, b):
            raise ValueError("le dossier surveillé, la sortie et l'état doivent être des emplacements distincts")


class Chaine:
    def __init__(self, entree: str, sortie: str, etat: str, passerelle=None, runtime=None,
                 schema: dict | None = None):
        verifier_repertoires(entree, sortie, etat)
        self.entree, self.sortie, self.etat = (os.path.abspath(p) for p in (entree, sortie, etat))
        self.passerelle = passerelle or PasserelleSimulee()
        self.runtime = runtime or RuntimeLocal(self.passerelle)
        self.schema = schema or qualif.charger_schema()
        self.journal = Journal(os.path.join(self.etat, "audit.jsonl"))

    def _marqueur(self, ev_id: str) -> str:
        return os.path.join(self.etat, "traites", f"{ev_id}.json")

    def _ecrire(self, sous_dossier: str, ev_id: str, donnees) -> str:
        chemin = os.path.join(self.sortie, sous_dossier, f"{ev_id}.json")
        ecrire_json(chemin, donnees)
        return chemin

    def traiter(self, evenement: dict) -> dict:
        """Traite un événement. Renvoie {"issue": ..., ...}."""
        ev_id = identifiant_evenement(evenement)
        if evenement.get("id") != ev_id:
            raise ValueError("identifiant d'événement incohérent avec son contenu")
        base = {"evenement_id": ev_id, "type": evenement["type"]}
        if os.path.exists(self._marqueur(ev_id)):
            self.journal.ecrire(evenement.get("chemin"), issue="doublon_ignore", **base)
            return {"issue": "doublon_ignore", "evenement_id": ev_id}

        self._ecrire("evenements", ev_id, evenement)
        if evenement["type"] == "illisible":
            issue = self._signaler(evenement, "fichier_illisible")
        elif evenement["type"] in TYPES_AVEC_TACHE:
            issue = self._traiter_document(evenement)
        else:  # renommage, suppression : consignés, sans nouvelle tâche (Lot 1)
            issue = "consigne"
            self.journal.ecrire(evenement.get("chemin"), issue=issue, sha256=evenement.get("sha256"),
                                version=evenement.get("version"), **base)
        if issue != "contenu_change":
            ecrire_json(self._marqueur(ev_id), {"issue": issue, "horodatage": horodatage()})
        return {"issue": issue, "evenement_id": ev_id}

    def _signaler(self, evenement: dict, motif: str) -> str:
        self._ecrire("signalements", evenement["id"], {
            "motif": motif, "evenement_id": evenement["id"], "chemin": evenement["chemin"],
            "erreur": evenement.get("erreur"), "horodatage": horodatage(),
            "action_attendue": "vérification humaine du fichier"})
        self.journal.ecrire(evenement["chemin"], evenement_id=evenement["id"], type=evenement["type"],
                            issue=motif, erreur=evenement.get("erreur"))
        return motif

    def _traiter_document(self, evenement: dict) -> str:
        ev_id = evenement["id"]
        chemin = os.path.join(self.entree, evenement["chemin"].replace("/", os.sep))
        try:
            if empreinte_fichier(chemin) != evenement["sha256"]:
                # le fichier a changé depuis l'événement : la surveillance produira une modification
                self.journal.ecrire(evenement["chemin"], evenement_id=ev_id, type=evenement["type"],
                                    issue="contenu_change")
                return "contenu_change"
            texte = securite.lire_texte(chemin, TAILLE_MAX_EXTRAIT)
        except OSError as e:
            return self._signaler(dict(evenement, erreur=type(e).__name__), "fichier_illisible")

        q = qualif.qualifier(texte, self.passerelle, MODELE_SIMULE, self.schema, TAILLE_MAX_EXTRAIT)
        self._ecrire("qualifications", ev_id, {"evenement_id": ev_id, **q})

        tache = paperclip.charge_utile(evenement, q)
        self._ecrire("taches-paperclip", ev_id, tache)

        task = {"id": ev_id, "titre": tache["titre"], "description": tache["description"]}
        case_context = {"document": {"chemin": evenement["chemin"], "sha256": evenement["sha256"],
                                     "version": evenement["version"], "extrait": texte},
                        "qualification": q["qualification"]}
        resultat = self.runtime.execute(task, case_context, SKILL_SIMULE, dict(POLITIQUE_LOT1))
        self._ecrire("resultats", ev_id, resultat)

        self.journal.ecrire(
            evenement["chemin"], evenement_id=ev_id, type=evenement["type"], sha256=evenement["sha256"],
            version=evenement["version"], taille=evenement.get("taille"), issue="tache_creee",
            categorie=q["qualification"]["categorie"],
            triage_humain=q["qualification"]["requires_human_triage"],
            injection_suspectee=q["injection_suspectee"], sortie_modele_valide=q["valide"],
            statut_runtime=resultat.get("statut"), tours=resultat.get("tours"))
        return "tache_creee"


def compter(sortie: str, sous_dossier: str) -> int:
    dossier = os.path.join(sortie, sous_dossier)
    return len([n for n in os.listdir(dossier) if n.endswith(".json")]) if os.path.isdir(dossier) else 0


def lire_evenement(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)
