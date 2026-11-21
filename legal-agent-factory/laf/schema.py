"""Validation stricte d'un JSON contre un schéma (sous-ensemble de JSON Schema).

Mots-clés pris en charge : type, enum, required, properties, additionalProperties
(false uniquement), items, minItems, maxItems, minLength, maxLength, pattern,
minimum, maximum. Tout mot-clé inconnu dans le schéma est une erreur : on préfère
refuser un schéma que l'on ne sait pas appliquer.
"""

import re

MOTS_CLES = {"$comment", "type", "enum", "required", "properties", "additionalProperties", "items",
             "minItems", "maxItems", "minLength", "maxLength", "pattern", "minimum", "maximum"}

TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


class SchemaInvalide(ValueError):
    pass


def valider(valeur, schema: dict, chemin: str = "$") -> list[str]:
    """Renvoie la liste des erreurs (vide si la valeur est conforme)."""
    inconnus = set(schema) - MOTS_CLES
    if inconnus:
        raise SchemaInvalide(f"{chemin} : mots-clés non pris en charge {sorted(inconnus)}")
    if schema.get("additionalProperties", False) is not False:
        raise SchemaInvalide(f"{chemin} : seul additionalProperties=false est accepté")

    erreurs = []
    type_ = schema.get("type")
    if type_ is not None and not TYPES[type_](valeur):
        return [f"{chemin} : type attendu {type_}"]
    if "enum" in schema and valeur not in schema["enum"]:
        erreurs.append(f"{chemin} : valeur hors liste")

    if isinstance(valeur, dict) and type_ == "object":
        proprietes = schema.get("properties", {})
        for cle in schema.get("required", []):
            if cle not in valeur:
                erreurs.append(f"{chemin} : champ requis manquant « {cle} »")
        for cle, sous_valeur in valeur.items():
            if cle not in proprietes:
                erreurs.append(f"{chemin} : champ non autorisé « {cle} »")
            else:
                erreurs += valider(sous_valeur, proprietes[cle], f"{chemin}.{cle}")

    if isinstance(valeur, list) and type_ == "array":
        if len(valeur) < schema.get("minItems", 0):
            erreurs.append(f"{chemin} : trop peu d'éléments")
        if "maxItems" in schema and len(valeur) > schema["maxItems"]:
            erreurs.append(f"{chemin} : trop d'éléments")
        if "items" in schema:
            for i, element in enumerate(valeur):
                erreurs += valider(element, schema["items"], f"{chemin}[{i}]")

    if isinstance(valeur, str):
        if len(valeur) < schema.get("minLength", 0):
            erreurs.append(f"{chemin} : texte trop court")
        if "maxLength" in schema and len(valeur) > schema["maxLength"]:
            erreurs.append(f"{chemin} : texte trop long")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], valeur):
            erreurs.append(f"{chemin} : format non conforme")

    if TYPES["number"](valeur):
        if "minimum" in schema and valeur < schema["minimum"]:
            erreurs.append(f"{chemin} : valeur trop petite")
        if "maximum" in schema and valeur > schema["maximum"]:
            erreurs.append(f"{chemin} : valeur trop grande")
    return erreurs
