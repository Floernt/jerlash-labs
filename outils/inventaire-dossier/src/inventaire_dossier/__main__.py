"""Ligne de commande.

    python -m inventaire_dossier                         ouvre la fenêtre
    python -m inventaire_dossier DOSSIER [--sortie DOSSIER] [--liste]

Écrit le registre en trois formats (.docx, .md, .json) dans le dossier de sortie, jamais dans le
dossier inventorié. Aucune pièce n'est modifiée. --liste affiche l'inventaire sans rien écrire.
Code de sortie : 0 aucune alerte, 1 alertes à examiner, 2 erreur.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

from . import __version__
from .analyse import inventorier
from .lecture import ErreurLecture, lire_dossier
from .rapport import AVERTISSEMENT, en_docx, en_json, en_markdown, lignes


def dossier_par_defaut() -> str:
    documents = pathlib.Path.home() / "Documents"
    return str((documents if documents.is_dir() else pathlib.Path.home()) / "Inventaire dossier")


def chemin_libre(dossier: str, nom: str) -> str:
    base, extension = os.path.splitext(nom)
    rang = 1
    while True:
        cible = os.path.join(dossier, f"{base}{f' ({rang})' if rang > 1 else ''}{extension}")
        if not os.path.exists(cible):
            return cible
        rang += 1


def reel(chemin: str) -> str:
    """Chemin réel et comparable : liens, jonctions, lecteurs substitués, noms courts 8.3 et casse résolus."""
    return os.path.normcase(os.path.realpath(chemin))


def dans(cible: str, source: str) -> bool:
    try:
        return os.path.commonpath([reel(cible), reel(source)]) == reel(source)
    except ValueError:   # lecteurs différents
        return False


def refuser_si_dans_le_dossier(cible: str, source: str) -> None:
    if dans(cible, source):
        raise ErreurLecture("Le registre doit être écrit hors du dossier inventorié (choisissez un autre dossier).")


def ecrire_registre(inventaire, sortie: str) -> list[str]:
    """Trois fichiers nommés d'après le dossier inventorié ; aucun fichier existant n'est remplacé.

    Le dossier de sortie est comparé au dossier inventorié par leur chemin réel, avant et après sa
    création, puis avant chaque fichier : aucune écriture ne peut aboutir dans le dossier inventorié."""
    source = os.path.abspath(inventaire.dossier)
    refuser_si_dans_le_dossier(sortie, source)
    os.makedirs(sortie, exist_ok=True)
    refuser_si_dans_le_dossier(sortie, source)
    cible = os.path.abspath(sortie)
    base = f"Inventaire - {os.path.basename(source.rstrip(os.sep)) or 'dossier'}"
    chemins = []
    for extension, contenu in ((".docx", en_docx(inventaire)), (".md", en_markdown(inventaire)),
                               (".json", en_json(inventaire))):
        refuser_si_dans_le_dossier(cible, source)
        chemin = chemin_libre(cible, base + extension)
        mode, donnees = ("xb", contenu) if isinstance(contenu, bytes) else ("x", contenu)
        with open(chemin, mode, **({} if "b" in mode else {"encoding": "utf-8", "newline": "\n"})) as f:
            f.write(donnees)
        chemins.append(chemin)
    return chemins


def afficher(inventaire) -> str:
    sortie = [f"Dossier : {inventaire.dossier}", f"Contrat principal : {inventaire.contrat_principal or 'non identifié'}",
              f"État : {inventaire.etat}", ""]
    for ligne in lignes(inventaire):
        sortie.append(f"{ligne[0]:>3}. {ligne[1]}\n      {ligne[2]} ; {ligne[3]} ; {ligne[4]} ; {ligne[5]} ; "
                      f"se rapporte à : {ligne[6]} ; fait foi : {ligne[7]}")
    sortie += ["", "Alertes :" if inventaire.alertes else "Alertes : aucune."]
    sortie += [f"  - {a}" for a in inventaire.alertes]
    sortie += ["", AVERTISSEMENT]
    return "\n".join(sortie)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="inventaire_dossier", description=(
        "Dresse l'inventaire d'un dossier contractuel sur cet ordinateur, sans IA ni réseau, sans modifier les pièces."))
    parser.add_argument("dossier", nargs="?", help="dossier à inventorier (sous-dossiers compris)")
    parser.add_argument("--sortie", metavar="DOSSIER", help="où écrire le registre (par défaut : Documents\\Inventaire dossier)")
    parser.add_argument("--liste", action="store_true", help="affiche l'inventaire sans rien écrire")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)
    if not args.dossier:
        from .interface import main as interface
        return interface()
    try:
        pieces, ignores = lire_dossier(args.dossier)
        inventaire = inventorier(args.dossier, pieces, ignores)
        print(afficher(inventaire))
        if not args.liste:
            for chemin in ecrire_registre(inventaire, args.sortie or dossier_par_defaut()):
                print(f"Registre : {chemin}")
    except (ErreurLecture, OSError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2
    except Exception as e:  # jamais le code 1, qui signifie « alertes à examiner »
        print(f"Erreur inattendue ({type(e).__name__}) : {e}", file=sys.stderr)
        return 2
    return 1 if inventaire.alertes else 0


if __name__ == "__main__":
    sys.exit(main())
