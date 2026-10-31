"""Ligne de commande.

    python -m controle_avant_envoi contrat.docx [autre.docx ...] [--html DOSSIER] [--json DOSSIER]
                                    [--termes liste.txt] [--config config.json] [--interface]

Code de sortie : 0 rien détecté, 1 points à traiter, 2 analyse impossible ou incomplète.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__
from .analyse import ErreurConfiguration, analyser, charger_configuration
from .rapport import en_html, en_json, en_texte


def nom_rapport(chemin: str, extension: str, rang: int = 0) -> str:
    base = os.path.splitext(os.path.basename(chemin))[0]
    suffixe = f" ({rang + 1})" if rang else ""
    return f"{base} - controle avant envoi{suffixe}.{extension}"


def ecrire(dossier: str, chemin_source: str, extension: str, contenu: str, deja_ecrits: set | None = None) -> str:
    """Écrit un rapport sans écraser le fichier analysé ni un autre rapport de la même session.

    deja_ecrits : chemins produits pendant la session ; un nom déjà pris reçoit un numéro (2), (3)…
    Un rapport d'une session précédente portant le même nom est remplacé.
    """
    os.makedirs(dossier, exist_ok=True)
    deja_ecrits = deja_ecrits if deja_ecrits is not None else set()
    rang = 0
    while True:
        cible = os.path.abspath(os.path.join(dossier, nom_rapport(chemin_source, extension, rang)))
        if cible == os.path.abspath(chemin_source):
            raise ErreurConfiguration("Le rapport écraserait le fichier analysé.")
        if cible not in deja_ecrits:
            break
        rang += 1
    with open(cible, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenu)
    deja_ecrits.add(cible)
    return cible


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="controle_avant_envoi",
                                     description="Contrôle un document .docx avant envoi, sans le modifier, sans IA ni réseau.")
    parser.add_argument("fichiers", nargs="*", help="documents .docx à contrôler")
    parser.add_argument("--html", metavar="DOSSIER", help="écrit un rapport HTML par document dans DOSSIER")
    parser.add_argument("--json", metavar="DOSSIER", help="écrit un rapport JSON par document dans DOSSIER")
    parser.add_argument("--termes", metavar="FICHIER", help="liste de termes sensibles, un par ligne")
    parser.add_argument("--config", metavar="FICHIER", help="configuration JSON (voir config.example.json)")
    parser.add_argument("--silencieux", action="store_true", help="n'affiche que le verdict")
    parser.add_argument("--interface", action="store_true", help="ouvre la fenêtre graphique")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    if args.interface or not args.fichiers:
        if not args.fichiers and not args.interface and sys.stdin and sys.stdin.isatty():
            parser.print_help()
            return 2
        from .interface import main as interface
        return interface()

    try:
        cfg = charger_configuration(args.config, args.termes)
    except ErreurConfiguration as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2

    code = 0
    ecrits: set = set()
    for chemin in args.fichiers:
        rapport = analyser(chemin, cfg)
        print(f"{rapport.nom} : {rapport.verdict}" if args.silencieux else en_texte(rapport))
        try:
            if args.html:
                print(f"Rapport HTML : {ecrire(args.html, chemin, 'html', en_html(rapport), ecrits)}")
            if args.json:
                print(f"Rapport JSON : {ecrire(args.json, chemin, 'json', en_json(rapport), ecrits)}")
        except (OSError, ErreurConfiguration) as e:
            print(f"Erreur d'écriture du rapport : {e}", file=sys.stderr)
            code = 2
        code = max(code, rapport.code_sortie)
    return code


if __name__ == "__main__":
    sys.exit(main())
