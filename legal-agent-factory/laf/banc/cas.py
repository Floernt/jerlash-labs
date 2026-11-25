"""Chargement des cas, des réponses de référence signées et des notes humaines.

Le fichier de cas est lu tel quel : la répartition entre jeu de conception
(`design`) et jeu de test final (`holdout`) est celle de la colonne `jeu`, jamais
recalculée. La colonne `attendu` n'est pas une réponse de référence : seul un
fichier signé par Florian l'est (voir `charger_references`).
"""

import csv
import hashlib
import json
import os

COLONNES = ("id", "axe", "scenario", "canal", "acteur", "attendu", "sources_a_verifier",
            "erreur_critique", "jeu", "statut_gold")
JEUX = ("design", "holdout")

# Dimensions de la fiche §14 (reprises du ticket FLO-66 ; libellés à aligner sur la fiche [À VÉRIFIER]).
DIMENSIONS_AUTO = ("orchestration", "ingestion", "actions_risque", "efficience")
DIMENSIONS_JURIDIQUES = ("faits_critiques", "droit_temporel", "sources_decisives")
NOTES_ADMISES = ("reussi", "partiel", "echec")


class CasInvalides(ValueError):
    pass


def charger_cas(chemin: str) -> list[dict]:
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f)
        entete = tuple(lecteur.fieldnames or ())
        if entete != COLONNES:
            raise CasInvalides(f"colonnes attendues {list(COLONNES)}, trouvées {list(entete)}")
        lignes = list(lecteur)
    cas, vus = [], set()
    for n, ligne in enumerate(lignes, start=2):
        if ligne["id"] in vus:
            raise CasInvalides(f"ligne {n} : identifiant en double {ligne['id']}")
        if ligne["erreur_critique"] not in ("oui", "non"):
            raise CasInvalides(f"ligne {n} : erreur_critique doit valoir oui ou non")
        if ligne["jeu"] not in JEUX:
            raise CasInvalides(f"ligne {n} : jeu doit valoir {' ou '.join(JEUX)}")
        vus.add(ligne["id"])
        cas.append(dict(ligne, erreur_critique=ligne["erreur_critique"] == "oui",
                        sources_a_verifier=[s for s in ligne["sources_a_verifier"].split(";") if s]))
    return cas


def empreinte_fichier(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def empreinte_dossier(dossier: str | None, suffixe: str = "") -> str | None:
    """Empreinte des chemins relatifs et des contenus ; None si le dossier n'existe pas.

    `__pycache__` est ignoré ; `suffixe` restreint aux fichiers de cette extension.
    """
    if not dossier or not os.path.isdir(dossier):
        return None
    h = hashlib.sha256()
    for racine, dossiers, fichiers in os.walk(dossier):
        dossiers[:] = sorted(d for d in dossiers if d != "__pycache__")
        for nom in sorted(f for f in fichiers if f.endswith(suffixe)):
            chemin = os.path.join(racine, nom)
            h.update(os.path.relpath(chemin, dossier).replace(os.sep, "/").encode("utf-8") + b"\0")
            h.update(empreinte_fichier(chemin).encode("ascii"))
    return h.hexdigest()


def _lire_json_par_cas(dossier: str | None, ids) -> dict:
    trouves = {}
    if not dossier or not os.path.isdir(dossier):
        return trouves
    for id_ in ids:
        chemin = os.path.join(dossier, f"{id_}.json")
        if os.path.isfile(chemin):
            with open(chemin, encoding="utf-8") as f:
                trouves[id_] = json.load(f)
    return trouves


def charger_references(dossier: str | None, ids) -> tuple[dict, list[str]]:
    """Références signées : `<id>.json` avec `signe_par` et `date_signature` non vides.

    Une référence sans signature est écartée et signalée : le cas reste « non évalué »
    sur les dimensions juridiques.
    """
    retenues, ecartees = {}, []
    for id_, ref in _lire_json_par_cas(dossier, ids).items():
        if str(ref.get("signe_par", "")).strip() and str(ref.get("date_signature", "")).strip():
            retenues[id_] = ref
        else:
            ecartees.append(id_)
    return retenues, ecartees


def charger_notes(dossier: str | None, ids, references: dict) -> tuple[dict, list[str]]:
    """Notes humaines `<id>.json` : {"note_par", "dimensions": {dimension: reussi|partiel|echec}}.

    Une note sur un cas sans référence signée est ignorée (et signalée).
    """
    retenues, ignorees = {}, []
    for id_, note in _lire_json_par_cas(dossier, ids).items():
        dims = note.get("dimensions") or {}
        if id_ not in references or not str(note.get("note_par", "")).strip():
            ignorees.append(id_)
            continue
        retenues[id_] = {d: v for d, v in dims.items() if d in DIMENSIONS_JURIDIQUES and v in NOTES_ADMISES}
    return retenues, ignorees
