"""Revue qualité (rôle Quality Reviewer), partie déterministe.

Contrôles appliqués à la sortie d'un skill, avant toute décision humaine :

- conformité : JSON valide contre le schéma de sortie du skill ;
- cohérence : même skill et même dossier que la tâche, statut « brouillon » ;
- références : chaque source citée existe au registre ; une source
  `source_unverified` est signalée (avertissement), une source inconnue est une
  erreur ; un constat sans source est signalé ;
- confidentialité : la sortie ne contient ni référence d'un autre dossier, ni
  adresse électronique, IBAN ou numéro de registre national absents des pièces
  reçues ;
- actions : le niveau vient de config/niveaux-action.json et non de la sortie ;
  une action inconnue ou un niveau déclaré différent est une erreur ; A3 est
  marqué bloqué.

La revue ne valide rien juridiquement. Elle prépare la décision humaine.
"""

import json
import os
import re

from .dossiers import RE_REFERENCE
from .schema import valider

DOSSIER_CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")

MOTIFS_CONFIDENTIELS = {
    "adresse_electronique": re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,4})?\b"),
    "registre_national": re.compile(r"\b\d{2}[.\s]?\d{2}[.\s]?\d{2}[-\s]?\d{3}[.\s]?\d{2}\b"),
}


def charger_niveaux() -> dict:
    with open(os.path.join(DOSSIER_CONFIG, "niveaux-action.json"), encoding="utf-8") as f:
        return json.load(f)


def _texte_sortie(sortie: dict) -> str:
    return json.dumps(sortie, ensure_ascii=False)


def niveaux_des_actions(actions: list[dict], niveaux: dict) -> tuple[list[dict], list[str]]:
    resultat, erreurs = [], []
    for a in actions:
        niveau = niveaux["actions"].get(a["action"])
        if niveau is None:
            erreurs.append(f"action_inconnue:{a['action']}")
            continue
        if a["niveau"] != niveau:
            erreurs.append(f"niveau_declare_incorrect:{a['action']}")
        if niveau in niveaux["niveaux_bloques"]:
            etat = "bloquee"
        elif niveau in niveaux["niveaux_sur_approbation"]:
            etat = "soumise_approbation"
        else:
            etat = "interne"
        resultat.append({"action": a["action"], "niveau": niveau, "etat": etat})
    return resultat, erreurs


def reviser(sortie_brute, skill: dict, routage: dict, texte_source: str, registre: dict,
            niveaux: dict | None = None) -> dict:
    niveaux = niveaux or charger_niveaux()
    erreurs, avertissements = [], []
    if skill.get("mention"):
        avertissements.append("skill_non_verifie_juridiquement")

    if isinstance(sortie_brute, str):
        try:
            sortie = json.loads(sortie_brute)
        except json.JSONDecodeError:
            sortie = None
    else:
        sortie = sortie_brute
    if not isinstance(sortie, dict):
        return {"conforme": False, "erreurs": ["sortie_non_json"], "avertissements": avertissements,
                "actions": [], "sortie": None}
    erreurs_schema = valider(sortie, skill["schema_sortie"])
    if erreurs_schema:
        return {"conforme": False, "erreurs": ["sortie_hors_schema"] + erreurs_schema[:5],
                "avertissements": avertissements, "actions": [], "sortie": sortie}

    # cohérence
    if sortie["skill"] != skill["nom"] or sortie["skill"] != routage["skill_attendu"]:
        erreurs.append("skill_incoherent")
    if sortie["dossier"] != routage["dossier"]:
        erreurs.append("dossier_incoherent")

    # références
    for i, constat in enumerate(sortie["constats"]):
        if not constat["sources"]:
            avertissements.append(f"constat_sans_source:{i}")
        for s in constat["sources"]:
            if s not in registre:
                erreurs.append(f"source_inconnue:{s}")
            elif registre[s]["statut"] == "source_unverified":
                avertissements.append(f"source_unverified:{s}")

    # confidentialité
    texte = _texte_sortie(sortie)
    autres = set(RE_REFERENCE.findall(texte)) - {routage["dossier"]}
    if autres:
        erreurs.append("reference_autre_dossier")
    for nom, motif in MOTIFS_CONFIDENTIELS.items():
        absents = {m.group(0) for m in motif.finditer(texte)} - {m.group(0) for m in motif.finditer(texte_source)}
        if absents:
            erreurs.append(f"confidentialite:{nom}")

    actions, erreurs_actions = niveaux_des_actions(sortie["actions_proposees"], niveaux)
    erreurs += erreurs_actions
    if any(a["etat"] == "bloquee" for a in actions):
        avertissements.append("action_a3_bloquee")
    return {"conforme": not erreurs, "erreurs": sorted(set(erreurs)),
            "avertissements": sorted(set(avertissements)), "actions": actions, "sortie": sortie}
