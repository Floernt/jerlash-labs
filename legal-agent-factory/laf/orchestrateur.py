"""Chaîne du Lot 2 : courriel ou dépôt -> rapprochement -> routeur -> tâche -> skill
-> revue qualité -> décision humaine.

Deux entrées, un seul événement source :
- `traiter(evenement)` pour les événements du dossier surveillé (Lot 1) ;
- `recevoir_courriel(message)` pour un message au format intermédiaire laf-courriel/0.1.

Chaque événement ouvre exactement une tâche (charge utile Paperclip en dry run),
nommée d'après son identifiant ; le rejeu est sans effet. Le skill n'est exécuté
que si le routeur a statué `route`, ou après confirmation par une personne.

Répertoire de sortie (en plus de ceux du Lot 1) :
  routages/<id>.json      règles, classification validée, décision du routeur
  contextes/<id>.json     contexte transmis au skill (texte encadré au moment de l'appel)
  revues/<id>.json        sortie du skill et revue qualité
  decisions/<id>.json     décision humaine et effet par niveau d'action
Répertoire d'état : fils.json (message -> dossier), traites/, audit.jsonl.
"""

import os

from . import approbation, courriel, dossiers, paperclip, routeur, securite, skills
from .audit import Journal
from .chaine import TAILLE_MAX_EXTRAIT, verifier_repertoires
from .outils_fichiers import ecrire_json, empreinte_fichier, horodatage, lire_json
from .passerelle import PasserelleSimulee
from .revue import charger_niveaux, reviser
from .runtime import POLITIQUE_LOT1, RuntimeLocal
from .surveillance import identifiant_evenement

MODELE_SIMULE = "simule-deterministe"


class ChaineLot2:
    def __init__(self, entree: str, sortie: str, etat: str, registre_dossiers: str,
                 passerelle=None, runtime=None):
        verifier_repertoires(entree, sortie, etat)
        self.entree, self.sortie, self.etat = (os.path.abspath(p) for p in (entree, sortie, etat))
        self.dossiers = dossiers.charger_registre(registre_dossiers)
        self.passerelle = passerelle or PasserelleSimulee()
        self.runtime = runtime or RuntimeLocal(self.passerelle)
        self.schema_routage = routeur.charger_schema()
        self.schema_courriel = courriel.charger_schema()
        self.sources = skills.charger_registre()
        self.niveaux = charger_niveaux()
        self.fils = dossiers.IndexFils(os.path.join(self.etat, "fils.json"))
        self.journal = Journal(os.path.join(self.etat, "audit.jsonl"))

    # --- utilitaires -------------------------------------------------------------------------
    def _chemin(self, sous_dossier: str, ev_id: str) -> str:
        return os.path.join(self.sortie, sous_dossier, f"{ev_id}.json")

    def _ecrire(self, sous_dossier: str, ev_id: str, donnees) -> None:
        ecrire_json(self._chemin(sous_dossier, ev_id), donnees)

    def lire(self, sous_dossier: str, ev_id: str):
        return lire_json(self._chemin(sous_dossier, ev_id))

    def _deja_traite(self, evenement: dict) -> bool:
        if os.path.exists(os.path.join(self.etat, "traites", f"{evenement['id']}.json")):
            self.journal.ecrire(evenement.get("chemin"), evenement_id=evenement["id"],
                                type=evenement["type"], issue="doublon_ignore")
            return True
        return False

    def _marquer(self, ev_id: str, issue: str) -> None:
        ecrire_json(os.path.join(self.etat, "traites", f"{ev_id}.json"), {"issue": issue, "horodatage": horodatage()})

    def _signaler(self, evenement: dict, motif: str) -> dict:
        self._ecrire("signalements", evenement["id"], {
            "motif": motif, "evenement_id": evenement["id"], "chemin": evenement.get("chemin"),
            "erreur": evenement.get("erreur"), "horodatage": horodatage(),
            "action_attendue": "vérification humaine"})
        self.journal.ecrire(evenement.get("chemin"), evenement_id=evenement["id"], type=evenement["type"],
                            issue=motif, erreur=evenement.get("erreur"))
        self._marquer(evenement["id"], motif)
        return {"issue": motif, "evenement_id": evenement["id"]}

    # --- entrées -----------------------------------------------------------------------------
    def traiter(self, evenement: dict) -> dict:
        """Événement du dossier surveillé (même forme qu'au Lot 1)."""
        if evenement.get("id") != identifiant_evenement(evenement):
            raise ValueError("identifiant d'événement incohérent avec son contenu")
        if self._deja_traite(evenement):
            return {"issue": "doublon_ignore", "evenement_id": evenement["id"]}
        self._ecrire("evenements", evenement["id"], evenement)
        if evenement["type"] == "illisible":
            return self._signaler(evenement, "fichier_illisible")
        if evenement["type"] not in ("creation", "modification"):
            self.journal.ecrire(evenement["chemin"], evenement_id=evenement["id"], type=evenement["type"],
                                issue="consigne")
            self._marquer(evenement["id"], "consigne")
            return {"issue": "consigne", "evenement_id": evenement["id"]}
        chemin = os.path.join(self.entree, evenement["chemin"].replace("/", os.sep))
        try:
            if empreinte_fichier(chemin) != evenement["sha256"]:
                return {"issue": "contenu_change", "evenement_id": evenement["id"]}
            texte = securite.lire_texte(chemin, TAILLE_MAX_EXTRAIT)
        except OSError as e:
            return self._signaler(dict(evenement, erreur=type(e).__name__), "fichier_illisible")
        rattachement = dossiers.rapprocher_fichier(evenement["chemin"], self.dossiers)
        return self._ouvrir(evenement, texte, rattachement)

    def recevoir_courriel(self, message: dict) -> dict:
        """Message au format intermédiaire. Jamais une instruction ni une autorisation."""
        try:
            evenement, texte = courriel.normaliser(message, self.schema_courriel)
        except courriel.CourrielInvalide:
            brut = {"type": "courriel_invalide", "chemin": "courriel/invalide",
                    "sha256": courriel.empreinte(message), "version": 1}
            brut["id"] = identifiant_evenement(brut)
            if self._deja_traite(brut):
                return {"issue": "doublon_ignore", "evenement_id": brut["id"]}
            return self._signaler(dict(brut, erreur="format_non_conforme"), "courriel_invalide")
        if self._deja_traite(evenement):
            return {"issue": "doublon_ignore", "evenement_id": evenement["id"]}
        self._ecrire("evenements", evenement["id"], evenement)
        rattachement = dossiers.rapprocher_courriel(evenement["fil"], evenement["objet"], self.dossiers, self.fils)
        # le fil est conservé : une réponse ultérieure suivra le même dossier, ou restera en attente
        self.fils.inscrire(evenement["fil"]["message_id"], rattachement["dossier"])
        return self._ouvrir(evenement, texte, rattachement)

    # --- routage et tâche --------------------------------------------------------------------
    def _ouvrir(self, evenement: dict, texte: str, rattachement: dict) -> dict:
        ev_id = evenement["id"]
        regles = routeur.regles_autorisations(texte)
        classe = routeur.classifier(texte, self.passerelle, MODELE_SIMULE, self.schema_routage, TAILLE_MAX_EXTRAIT)
        decision = routeur.decider(regles, classe, rattachement)
        self._ecrire("routages", ev_id, {"evenement_id": ev_id, "rattachement": rattachement, "regles": regles,
                                         "classification": classe, "routage": decision})
        self._ecrire("contextes", ev_id, {"evenement_id": ev_id, "texte": texte,
                                          "pieces": classe["classification"]["pieces"]})
        self._ecrire("taches-paperclip", ev_id, paperclip.charge_utile_lot2(evenement, decision))
        self.journal.ecrire(evenement["chemin"], evenement_id=ev_id, type=evenement["type"],
                            sha256=evenement["sha256"], issue="tache_creee",
                            statut_routage=decision["statut"], skill=decision["skill_attendu"],
                            rattache=rattachement["rattache"], lien_rattachement=rattachement["lien"],
                            motifs=decision["motifs"], demandes_ignorees=regles["demandes_ignorees"],
                            sortie_modele_valide=classe["valide"])
        self._marquer(ev_id, "tache_creee")
        resultat = {"issue": "tache_creee", "evenement_id": ev_id, "statut": decision["statut"],
                    "skill": decision["skill_attendu"], "dossier": decision["dossier"]}
        if decision["statut"] == routeur.ROUTE:
            resultat["revue"] = self._executer(ev_id)
        return resultat

    def _executer(self, ev_id: str) -> dict:
        routage = self.lire("routages", ev_id)["routage"]
        contexte = self.lire("contextes", ev_id)
        skill = skills.charger(routage["skill_attendu"], self.sources)
        task = {"id": ev_id, "dossier": routage["dossier"], "skill": skill["nom"], "statut": routage["statut"]}
        case_context = {"dossier": routage["dossier"], "rattache": routage["rattache"],
                        "pieces_detectees": contexte["pieces"], "document": contexte["texte"]}
        bundle = {"nom": skill["nom"], "instructions": skill["instructions"]}
        resultat = self.runtime.execute(task, case_context, bundle, dict(POLITIQUE_LOT1))
        revue = reviser(resultat.get("sortie"), skill, routage, contexte["texte"], self.sources, self.niveaux)
        self._ecrire("revues", ev_id, {"evenement_id": ev_id, "skill": skill["nom"], "skill_version": skill["version"],
                                       "mention": skill["mention"], "runtime": {k: resultat.get(k) for k in
                                       ("statut", "tours", "demandes_outils_refusees", "actions_effectuees")},
                                       "revue": revue, "statut": "en_attente_decision_humaine"})
        self.journal.ecrire(None, evenement_id=ev_id, issue="revue", skill=skill["nom"],
                            statut_runtime=resultat.get("statut"), revue_conforme=revue["conforme"])
        return revue

    # --- interventions humaines (appels locaux, jamais déclenchés par un message) -------------
    def _verifier_relecteur(self, relecteur: str) -> None:
        if relecteur not in self.niveaux["referents_humains"]:
            raise approbation.DecisionInvalide("relecteur non inscrit comme référent humain")

    def confirmer(self, ev_id: str, relecteur: str, skill: str | None = None, dossier: str | None = None) -> dict:
        """Confirmation humaine d'une tâche en `confirmation_humaine` : la personne fixe le skill et,
        au besoin, le dossier. C'est un rattachement contrôlé, consigné avec son auteur."""
        self._verifier_relecteur(relecteur)
        donnees = self.lire("routages", ev_id)
        routage = donnees["routage"]
        if routage["statut"] != routeur.CONFIRMATION:
            raise approbation.DecisionInvalide("cette tâche n'attend pas de confirmation")
        skill = skill or routage["skill_attendu"]
        if skill not in (routeur.INTAKE, routeur.CLAIM):
            raise approbation.DecisionInvalide("skill inconnu")
        if dossier is not None and dossier not in self.dossiers:
            raise approbation.DecisionInvalide("dossier inconnu")
        if skill == routeur.CLAIM and dossier is None and not routage["rattache"]:
            raise approbation.DecisionInvalide("l'analyse d'une créance exige un dossier rattaché")
        if dossier is not None:
            routage.update(dossier=dossier, rattache=True)
        routage.update(statut=routeur.ROUTE, skill_attendu=skill, role=routeur.ROLE_PAR_STATUT[routeur.ROUTE],
                       confirme_par=relecteur, confirme_le=horodatage())
        self._ecrire("routages", ev_id, donnees)
        self.journal.ecrire(None, evenement_id=ev_id, issue="route_confirmee", skill=skill,
                            rattache=routage["rattache"])
        return self._executer(ev_id)

    def decider(self, ev_id: str, decision: dict) -> dict:
        """Décision humaine sur la sortie revue : approuve, refuse ou corrige."""
        revue_enr = self.lire("revues", ev_id)
        if revue_enr is None:
            raise approbation.DecisionInvalide("aucune sortie revue pour cette tâche")
        if self.lire("decisions", ev_id) is not None:
            raise approbation.DecisionInvalide("décision déjà prise")
        routage = self.lire("routages", ev_id)["routage"]
        skill = skills.charger(routage["skill_attendu"], self.sources)
        texte = self.lire("contextes", ev_id)["texte"]
        resultat = approbation.appliquer(revue_enr["revue"], decision, skill, routage, texte,
                                         self.sources, self.niveaux)
        self._ecrire("decisions", ev_id, dict(resultat, evenement_id=ev_id))
        self.journal.ecrire(None, evenement_id=ev_id, issue="decision_humaine", decision=resultat["decision"],
                            statut_decision=resultat["statut"])
        return resultat
