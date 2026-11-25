"""Sonde des capacités d'un modèle sur un endpoint : JSON contraint et appels d'outils.

Les capacités ne sont pas présumées : chaque essai est répété et son issue
consignée (observé, non observé, erreur). La forme des options envoyées
(`response_format`, `tools`) suit l'API OpenAI ; leur prise en charge par chaque
fournisseur est [À VÉRIFIER] dans sa documentation, et c'est précisément ce que
la sonde observe. L'outil proposé est fictif et n'est jamais exécuté.
"""

import json

from ..passerelle import appels_outils, contenu
from ..schema import valider

SCHEMA_SONDE = {
    "type": "object", "additionalProperties": False, "required": ["statut", "nombre"],
    "properties": {"statut": {"type": "string", "enum": ["ok"]},
                   "nombre": {"type": "integer", "minimum": 3, "maximum": 3}},
}

OUTIL_SONDE = {
    "type": "function",
    "function": {
        "name": "enregistrer_sonde",
        "description": "Outil fictif de test. N'a aucun effet.",
        "parameters": {"type": "object", "additionalProperties": False, "required": ["valeur"],
                       "properties": {"valeur": {"type": "integer"}}},
    },
}


def _essai_json(passerelle, modele):
    messages = [{"role": "system", "content": "Réponds uniquement par un objet JSON."},
                {"role": "user", "content": 'Renvoie {"statut": "ok", "nombre": 3}.'}]
    reponse = passerelle.chat_completions(
        modele, messages, temperature=0,
        response_format={"type": "json_schema",
                         "json_schema": {"name": "sonde", "strict": True, "schema": SCHEMA_SONDE}})
    try:
        valeur = json.loads(contenu(reponse) or "")
    except json.JSONDecodeError:
        return "non_observe", "réponse non JSON"
    erreurs = valider(valeur, SCHEMA_SONDE)
    return ("observe", None) if not erreurs else ("non_observe", "; ".join(erreurs))


def _essai_outils(passerelle, modele):
    messages = [{"role": "system", "content": "Utilise l'outil fourni."},
                {"role": "user", "content": "Appelle enregistrer_sonde avec valeur = 7."}]
    reponse = passerelle.chat_completions(modele, messages, temperature=0,
                                          tools=[OUTIL_SONDE], tool_choice="auto")
    appels = appels_outils(reponse)
    if not appels:
        return "non_observe", "aucun appel d'outil"
    fonction = (appels[0] or {}).get("function") or {}
    if fonction.get("name") != "enregistrer_sonde":
        return "non_observe", "nom d'outil inattendu"
    try:
        arguments = json.loads(fonction.get("arguments") or "")
    except (json.JSONDecodeError, TypeError):
        return "non_observe", "arguments non JSON"
    return ("observe", None) if arguments == {"valeur": 7} else ("non_observe", "arguments inattendus")


def sonder(passerelle, modele: str, repetitions: int = 3) -> dict:
    resultat = {"fournisseur": passerelle.nom, "modele": modele, "repetitions": repetitions}
    for nom, essai in (("json_contraint", _essai_json), ("appels_outils", _essai_outils)):
        issues = []
        for _ in range(repetitions):
            try:
                issue, detail = essai(passerelle, modele)
            except Exception as e:  # noqa: BLE001 - toute erreur d'endpoint est une observation
                issue, detail = "erreur", type(e).__name__
            issues.append({"issue": issue, "detail": detail})
        observes = sum(i["issue"] == "observe" for i in issues)
        erreurs = sum(i["issue"] == "erreur" for i in issues)
        resultat[nom] = {"observe": observes, "sur": repetitions, "essais": issues,
                         "conclusion": "observe" if observes == repetitions
                         else "instable" if observes
                         else "erreur" if erreurs == repetitions else "non_observe"}
    return resultat
