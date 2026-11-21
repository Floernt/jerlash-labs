"""Entrée par courriel : normalisation d'un message vers un événement source.

Le format exact des messages livrés par AgentMail n'a pas été consulté [À VÉRIFIER].
On travaille donc sur un format intermédiaire explicite, `laf-courriel/0.1`
(config/schema-courriel.json) ; un futur adaptateur AgentMail devra le produire.

Le message normalisé devient un événement de même forme que celui du dossier
surveillé (type, chemin, sha256, version, horodatage, id dérivé du contenu), avec
en plus le fil (identifiants, référence au précédent, expéditeur, destinataires,
date) et la liste des pièces (nom, type, empreinte, taille), sans leur texte.

Un courriel est une donnée. Il n'est jamais une instruction d'administration ni
une autorisation d'engager le cabinet : rien de ce qu'il demande n'est exécuté.
"""

import hashlib
import json
import os

from .outils_fichiers import empreinte_texte, horodatage
from .schema import valider
from .surveillance import identifiant_evenement

DOSSIER_CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
FORMAT = "laf-courriel/0.1"


class CourrielInvalide(ValueError):
    pass


def charger_schema() -> dict:
    with open(os.path.join(DOSSIER_CONFIG, "schema-courriel.json"), encoding="utf-8") as f:
        return json.load(f)


def _canonique(message: dict) -> bytes:
    return json.dumps(message, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def empreinte(message) -> str:
    try:
        return hashlib.sha256(_canonique(message)).hexdigest()
    except (TypeError, ValueError):
        return hashlib.sha256(repr(message).encode("utf-8", "replace")).hexdigest()


def normaliser(message: dict, schema: dict | None = None) -> tuple[dict, str]:
    """Renvoie (événement, texte à examiner). Lève CourrielInvalide si le format n'est pas respecté."""
    if not isinstance(message, dict):
        raise CourrielInvalide("$ : objet attendu")
    erreurs = valider(message, schema or charger_schema())
    if erreurs:
        raise CourrielInvalide("; ".join(erreurs[:5]))
    pieces = [{"nom": p["nom"], "type_mime": p["type_mime"],
               "sha256": hashlib.sha256(p["texte"].encode("utf-8")).hexdigest(),
               "taille": len(p["texte"].encode("utf-8"))} for p in message["pieces"]]
    evenement = {
        "type": "courriel",
        # un message = un chemin stable, dérivé de son identifiant (pas de l'heure de réception)
        "chemin": "courriel/" + empreinte_texte(message["message_id"], 24),
        "sha256": empreinte(message),
        "version": 1,
        "horodatage": horodatage(),
        "fil": {"message_id": message["message_id"], "in_reply_to": message["in_reply_to"],
                "references": list(message["references"]), "de": message["de"].lower(),
                "a": [x.lower() for x in message["a"]], "cc": [x.lower() for x in message["cc"]],
                "date": message["date"]},
        "objet": message["objet"],
        "pieces": pieces,
    }
    evenement["id"] = identifiant_evenement(evenement)
    return evenement, texte(message)


def texte(message: dict) -> str:
    """Texte examiné : objet, corps puis pièces, chacune annoncée par son nom."""
    morceaux = [f"Objet : {message['objet']}", "", message["corps_texte"]]
    for p in message["pieces"]:
        morceaux += ["", f"--- Pièce jointe : {p['nom']} ---", p["texte"]]
    return "\n".join(morceaux)


def lire(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)
