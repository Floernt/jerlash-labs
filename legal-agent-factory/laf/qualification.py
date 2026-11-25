"""Qualification structurée d'un document, validée contre un schéma strict.

Toute sortie du modèle non conforme (JSON invalide, champ en trop, valeur hors
liste) est rejetée et remplacée par une qualification de repli qui exige un
triage humain. `requires_human_triage` à false n'ouvre aucune action : c'est une
indication de tri, jamais une permission d'agir (voir runtime.POLITIQUE_LOT1).
"""

import json
import os

from . import securite
from .passerelle import MARQUEUR_QUALIFICATION, contenu
from .schema import valider

DOSSIER_CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")


def charger_schema(chemin: str | None = None) -> dict:
    with open(chemin or os.path.join(DOSSIER_CONFIG, "schema-qualification.json"), encoding="utf-8") as f:
        return json.load(f)


def _repli(motif: str) -> dict:
    return {"schema_version": "laf-qualification/0.1", "categorie": "a_trier",
            "requires_human_triage": True, "confiance": 0.0, "motifs": [motif]}


def messages_qualification(texte: str, taille_max: int) -> list[dict]:
    systeme = (
        f"{MARQUEUR_QUALIFICATION}\n"
        "Tu qualifies un document déposé dans un dossier. Réponds uniquement par un objet JSON "
        "conforme au schéma fourni, sans texte autour. " + securite.AVERTISSEMENT)
    return [{"role": "system", "content": systeme},
            {"role": "user", "content": securite.encadrer(texte, taille_max)}]


def qualifier(texte: str, passerelle, modele: str, schema: dict, taille_max: int) -> dict:
    """Renvoie {"qualification", "valide", "erreurs", "injection_suspectee", "triage_force"}."""
    reponse = passerelle.chat_completions(modele, messages_qualification(texte, taille_max),
                                          temperature=0)
    brut = contenu(reponse) or ""
    erreurs = []
    try:
        proposee = json.loads(brut)
    except json.JSONDecodeError:
        proposee, erreurs = None, ["$ : la réponse n'est pas du JSON"]
    if proposee is not None:
        erreurs = valider(proposee, schema)
    valide = not erreurs
    qualification = proposee if valide else _repli("sortie_modele_invalide")

    injection = securite.injection_suspectee(texte)
    triage_force = False
    if injection and not qualification["requires_human_triage"]:
        qualification = dict(qualification, requires_human_triage=True)
        triage_force = True
    if injection and "injection_suspectee" not in qualification["motifs"]:
        qualification["motifs"] = qualification["motifs"][:4] + ["injection_suspectee"]
    return {"qualification": qualification, "valide": valide, "erreurs": erreurs,
            "injection_suspectee": injection, "triage_force": triage_force}
