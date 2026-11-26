"""Exécution d'un cas du benchmark sur la chaîne du Lot 2 (rapprochement, routeur,
skill, revue qualité), à la place de la qualification seule du Lot 1.

Entrée selon le canal du cas :
- `email` : la pièce `*courriel.txt` est convertie au format intermédiaire
  laf-courriel/0.1 (en-têtes De, À, Cc, Date, Objet ; le reste fait le corps) et
  les autres pièces deviennent ses pièces jointes, sans leur préfixe numérique ;
- `folder` : chaque pièce est déposée dans `<entrée>/<id du cas>/` et produit un
  événement de création, comme le ferait le dossier surveillé ; un dépôt de
  plusieurs fichiers ouvre donc plusieurs tâches, comme dans la chaîne réelle.

Les pièces de contexte (`00-contexte*`) ne sont pas des pièces reçues : elles ne
sont pas transmises. Au Lot 2, c'est le registre des dossiers qui joue ce rôle
(série : clé `dossiers`, vide par défaut, si bien que rien n'est rattaché).

Aucune intervention humaine n'est simulée : une tâche en `confirmation_humaine`,
`needs_clarification`, `classement` ou `hors_perimetre` s'arrête là, et c'est ce
statut qui est mesuré. Le skill n'est exécuté que pour une tâche `route`.

Chaque unité (cas ou variante) a ses propres répertoires sous
`<série>/chaine/<unité>/` ; les traces de la chaîne y restent pour l'audit.
"""

import hashlib
import os
import re
import shutil

from ..orchestrateur import ChaineLot2
from ..outils_fichiers import horodatage
from ..surveillance import identifiant_evenement

NOM_COURRIEL = re.compile(r"courriel\.txt$")
NOM_CONTEXTE = re.compile(r"^00-contexte")
PREFIXE = re.compile(r"^\d{2}-")
RE_ENTETE = re.compile(r"^(De|À|Cc|Date|Objet|Pièces jointes)\s?:\s?(.*)$")
RE_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})(?::(\d{2}))?$")
# Fuseau des dates des pièces non précisé : UTC par convention du banc [À VÉRIFIER si un cas en dépend].
FUSEAU = "Z"


def separer_contexte(pieces: list[tuple[str, str]]) -> tuple[list, list[str]]:
    recues = [(n, t) for n, t in pieces if not NOM_CONTEXTE.match(n)]
    return recues, [n for n, _ in pieces if NOM_CONTEXTE.match(n)]


def _adresses(valeur: str) -> list[str]:
    return [a.strip() for a in re.split(r"[,;]", valeur) if a.strip()]


def message_depuis_pieces(id_unite: str, pieces: list[tuple[str, str]]) -> dict:
    """Construit un message laf-courriel/0.1. Un courriel mal formé produit un message que la
    chaîne refusera (courriel_invalide) : c'est alors ce refus qui est mesuré."""
    courriels = [i for i, (n, _) in enumerate(pieces) if NOM_COURRIEL.search(n)]
    entetes, corps = {}, []
    if courriels:
        _, texte = pieces[courriels[0]]
        en_tete = True
        for ligne in texte.splitlines():
            m = RE_ENTETE.match(ligne) if en_tete else None
            if m:
                entetes[m.group(1)] = m.group(2).strip()
                continue
            if entetes and not ligne.strip():
                en_tete = False  # fin du bloc d'en-têtes : tout le reste est le corps
            corps.append(ligne)
    m = RE_DATE.match(entetes.get("Date", ""))
    date = f"{m.group(1)}T{m.group(2)}:{m.group(3) or '00'}{FUSEAU}" if m else entetes.get("Date", "")
    jointes = [{"nom": PREFIXE.sub("", n), "type_mime": "text/plain", "texte": t}
               for i, (n, t) in enumerate(pieces) if i not in courriels[:1]]
    return {
        "format": "laf-courriel/0.1",
        # identifiant stable, dérivé de l'unité : la variante d'un cas est un autre message
        "message_id": f"<{hashlib.sha256(id_unite.encode('utf-8')).hexdigest()[:24]}@banc.invalid>",
        "in_reply_to": "", "references": [],
        "de": entetes.get("De", ""), "a": _adresses(entetes.get("À", "")), "cc": _adresses(entetes.get("Cc", "")),
        "date": date, "objet": entetes.get("Objet", ""),
        "corps_texte": "\n".join(corps).strip(), "pieces": jointes,
    }


def _evenements_depot(entree: str, id_cas: str, pieces: list[tuple[str, str]]) -> list[dict]:
    """Dépose les pièces et renvoie les événements de création qu'en tirerait la surveillance."""
    evenements = []
    for nom, texte in pieces:
        relatif = f"{id_cas}/{nom}"
        chemin = os.path.join(entree, id_cas, nom)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        donnees = texte.encode("utf-8")
        with open(chemin, "wb") as f:
            f.write(donnees)
        ev = {"type": "creation", "chemin": relatif, "sha256": hashlib.sha256(donnees).hexdigest(),
              "version": 1, "taille": len(donnees), "horodatage": horodatage()}
        ev["id"] = identifiant_evenement(ev)
        evenements.append(ev)
    return evenements


def _tache(chaine: ChaineLot2, resultat: dict) -> dict:
    ev_id = resultat["evenement_id"]
    if resultat["issue"] != "tache_creee":
        return {"evenement": ev_id, "issue": resultat["issue"]}
    enr = chaine.lire("routages", ev_id)
    routage, classe, regles = enr["routage"], enr["classification"], enr["regles"]
    t = {
        "evenement": ev_id, "issue": "tache_creee", "statut": routage["statut"],
        "skill": routage["skill_attendu"], "dossier": routage["dossier"], "rattache": routage["rattache"],
        "motif_rattachement": enr["rattachement"]["motif"], "motifs": routage["motifs"],
        "elements_manquants": routage["elements_manquants"], "demandes_ignorees": regles["demandes_ignorees"],
        "injection_suspectee": regles["injection_suspectee"], "routage_valide": classe["valide"],
        "erreurs_routage": len(classe["erreurs"]), "skill_execute": False,
    }
    revue = chaine.lire("revues", ev_id)
    if revue is not None:
        rt = revue["runtime"]
        t.update(skill_execute=True, runtime_statut=rt["statut"], tours=rt["tours"],
                 demandes_outils_refusees=rt.get("demandes_outils_refusees") or 0,
                 actions_effectuees=rt.get("actions_effectuees") or [],
                 revue_conforme=revue["revue"]["conforme"], revue_erreurs=revue["revue"]["erreurs"],
                 revue_avertissements=revue["revue"]["avertissements"])
    return t


def executer_un(id_unite: str, id_cas: str, canal: str, pieces: list[tuple[str, str]], compteur,
                config: dict, dossier_unite: str) -> dict:
    """Passe une unité dans une chaîne neuve. Renvoie les mesures brutes (sans durée ni coût)."""
    if os.path.isdir(dossier_unite):  # reprise après interruption : on repart d'un état vide
        shutil.rmtree(dossier_unite)
    entree, sortie, etat = (os.path.join(dossier_unite, n) for n in ("entree", "sortie", "etat"))
    for d in (entree, sortie, etat):
        os.makedirs(d)
    chaine = ChaineLot2(entree, sortie, etat, config["dossiers"], passerelle=compteur, modele=config["modele"])
    recues, contexte = separer_contexte(pieces)
    if canal == "email":
        resultats = [chaine.recevoir_courriel(message_depuis_pieces(id_unite, recues))]
    else:
        resultats = [chaine.traiter(ev) for ev in _evenements_depot(entree, id_cas, recues)]
    taches = [_tache(chaine, r) for r in resultats]
    creees = [t for t in taches if t["issue"] == "tache_creee"]
    executees = [t for t in creees if t["skill_execute"]]
    return {
        "chaine": "lot2",
        "pieces": len(recues),
        "pieces_contexte_ignorees": contexte,
        "taches": taches,
        "statuts": sorted(t["statut"] for t in creees),
        "issues_sans_tache": sorted(t["issue"] for t in taches if t["issue"] != "tache_creee"),
        "routage_valide": bool(creees) and all(t["routage_valide"] for t in creees),
        "injection_suspectee": any(t["injection_suspectee"] for t in creees),
        "demandes_ignorees": sorted({d for t in creees for d in t["demandes_ignorees"]}),
        "skills_executes": len(executees),
        "runtime_termine": all(t["runtime_statut"] == "termine" for t in executees),
        "revues_conformes": sum(bool(t.get("revue_conforme")) for t in executees),
        "demandes_outils_refusees": sum(t.get("demandes_outils_refusees", 0) for t in executees),
        "actions_effectuees": [a for t in executees for a in t.get("actions_effectuees", [])],
        "corrections": sum(not t["routage_valide"] for t in creees),
    }
