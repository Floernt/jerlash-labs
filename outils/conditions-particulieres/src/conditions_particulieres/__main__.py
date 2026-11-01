"""Ligne de commande.

    python -m conditions_particulieres                          ouvre la fenêtre
    python -m conditions_particulieres CONTRAT [--sortie DOSSIER] [--liste]

Écrit le rapport en trois formats (.docx, .md, .json) dans le dossier de sortie, sans jamais remplacer
un fichier. Le contrat n'est pas modifié. --liste affiche le rapport sans rien écrire.
Code de sortie : 0 aucune clause mixte, 1 clauses mixtes à épurer, 2 erreur.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

from . import __version__
from .analyse import analyser
from .lecture import ErreurLecture, lire_contrat
from .rapport import AVERTISSEMENT, a_epurer, en_docx, en_json, en_markdown, lignes, synthese


def dossier_par_defaut() -> str:
    documents = pathlib.Path.home() / "Documents"
    return str((documents if documents.is_dir() else pathlib.Path.home()) / "Conditions particulieres")


def base_libre(dossier: str, base: str, extensions: tuple[str, ...]) -> str:
    """Un seul numéro pour les trois fichiers d'un même rapport : « Glossaire - Bail (2).docx, .md, .json »."""
    rang = 1
    while True:
        cible = os.path.join(dossier, f"{base}{f' ({rang})' if rang > 1 else ''}")
        if not any(os.path.exists(cible + e) for e in extensions):
            return cible
        rang += 1


def ecrire_rapport(analyse, sortie: str) -> list[str]:
    """Trois fichiers nommés d'après le contrat ; aucun fichier existant n'est remplacé. Si l'un d'eux ne
    peut pas être écrit (disque plein…), ceux déjà écrits sont effacés : pas de rapport incomplet."""
    os.makedirs(sortie, exist_ok=True)
    base = f"Conditions - {os.path.splitext(analyse.document)[0] or 'contrat'}"
    chemins = []
    fichiers = ((".docx", en_docx(analyse)), (".md", en_markdown(analyse)), (".json", en_json(analyse)))
    libre = base_libre(sortie, base, tuple(e for e, _ in fichiers))
    try:
        for extension, contenu in fichiers:
            chemin = libre + extension
            if isinstance(contenu, bytes):
                with open(chemin, "xb") as f:
                    chemins.append(chemin)
                    f.write(contenu)
            else:
                with open(chemin, "x", encoding="utf-8", newline="\n") as f:
                    chemins.append(chemin)
                    f.write(contenu)
    except OSError:
        for chemin in chemins:   # uniquement les fichiers que cet appel vient de créer
            try:
                os.remove(chemin)
            except OSError:
                pass
        raise
    return chemins


def afficher(analyse) -> str:
    sortie = [f"Contrat : {analyse.document}", ""] + synthese(analyse)
    sortie += ["", "Clauses mixtes, données à extraire :"] + [f"  - {x}" for x in a_epurer(analyse)] if a_epurer(analyse) else []
    sortie += ["", "Proposition bloc par bloc :"] + [f"  - {b} : {c}" for b, c, _d in lignes(analyse)]
    sortie += ["", AVERTISSEMENT]
    return "\n".join(sortie)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="conditions_particulieres", description=(
        "Prépare la séparation d'un contrat en conditions particulières et générales, sur cet ordinateur, sans IA ni réseau, sans modifier le contrat."))
    parser.add_argument("contrat", nargs="?", help="contrat à analyser (.docx, .txt ou .md)")
    parser.add_argument("--sortie", metavar="DOSSIER", help="où écrire le rapport (par défaut : Documents\\Conditions particulieres)")
    parser.add_argument("--liste", action="store_true", help="affiche le rapport sans rien écrire")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)
    if not args.contrat:
        from .interface import main as interface
        return interface()
    try:
        analyse = analyser(lire_contrat(args.contrat))
        print(afficher(analyse))
        if not args.liste:
            for chemin in ecrire_rapport(analyse, args.sortie or dossier_par_defaut()):
                print(f"Rapport : {chemin}")
    except (ErreurLecture, OSError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2
    except Exception as e:  # jamais le code 1, qui signifie « points à examiner »
        print(f"Erreur inattendue ({type(e).__name__}) : {e}", file=sys.stderr)
        return 2
    return 1 if analyse.du_type("mixte") else 0


if __name__ == "__main__":
    sys.exit(main())
