"""Petites fonctions partagées : empreintes, horodatage, écriture atomique de JSON."""

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone

TAILLE_BLOC = 65536


def empreinte_fichier(chemin: str) -> str:
    """SHA-256 du contenu d'un fichier, lu par blocs."""
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(TAILLE_BLOC), b""):
            h.update(bloc)
    return h.hexdigest()


def empreinte_texte(texte: str, longueur: int = 64) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:longueur]


def horodatage() -> str:
    """Horodatage UTC ISO 8601 à la seconde."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ecrire_json(chemin: str, donnees) -> None:
    """Écrit un JSON de façon atomique (fichier temporaire puis remplacement)."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(chemin), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, chemin)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def lire_json(chemin: str, defaut=None):
    if not os.path.exists(chemin):
        return defaut
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def est_dans(chemin: str, parent: str) -> bool:
    """Vrai si `chemin` est `parent` ou se trouve sous `parent`."""
    chemin, parent = os.path.realpath(chemin), os.path.realpath(parent)
    try:
        return os.path.commonpath([chemin, parent]) == parent
    except ValueError:  # lecteurs différents sous Windows
        return False
