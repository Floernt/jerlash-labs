"""Ligne de commande.

    python -m pseudonymisation                                    ouvre la fenêtre
    python -m pseudonymisation pseudonymiser piece.docx [--termes liste.txt] [--exclure liste.txt]
                                             [--sortie DOSSIER] [--liste]
    python -m pseudonymisation retablir reponse.txt --table "piece - table.json" [--sortie FICHIER]

pseudonymiser écrit deux fichiers dans DOSSIER : le texte pseudonymisé et la table de correspondance.
Aucun fichier existant n'est remplacé. --liste affiche les détections sans rien écrire.
Code de sortie : 0 réussi, 2 erreur.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

from . import __version__
from .detection import CATEGORIES, detecter, lire_termes
from .lecture import ErreurLecture, lire_fichier
from .remplacement import attribuer_marqueurs, lire_table, pseudonymiser, retablir

AVERTISSEMENT = (
    "Pseudonymisation, et non anonymisation : l'outil ne trouve pas tout, et le contexte (fonction, lieu, faits) "
    "peut suffire à reconnaître une personne. Relisez le texte pseudonymisé avant de l'envoyer. "
    "La table de correspondance contient les données d'origine : gardez-la sur cet ordinateur.")


def dossier_par_defaut() -> str:
    documents = pathlib.Path.home() / "Documents"
    return str((documents if documents.is_dir() else pathlib.Path.home()) / "Pseudonymisation")


def chemin_libre(dossier: str, nom: str) -> str:
    """Premier chemin inexistant : « nom.txt », puis « nom (2).txt »… Rien n'est jamais remplacé."""
    base, extension = os.path.splitext(nom)
    rang = 1
    while True:
        cible = os.path.join(dossier, f"{base}{f' ({rang})' if rang > 1 else ''}{extension}")
        if not os.path.exists(cible):
            return cible
        rang += 1


def enregistrer(dossier: str, base: str, texte: str, table: dict) -> tuple[str, str]:
    os.makedirs(dossier, exist_ok=True)
    chemin_texte = chemin_libre(dossier, f"{base} - pseudonymise.txt")
    suffixe = os.path.splitext(os.path.basename(chemin_texte))[0].removeprefix(f"{base} - pseudonymise")
    chemin_table = chemin_libre(dossier, f"{base} - table{suffixe}.json")
    with open(chemin_texte, "x", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    with open(chemin_table, "x", encoding="utf-8", newline="\n") as f:
        json.dump(table, f, ensure_ascii=False, indent=1)
    return chemin_texte, chemin_table


def lire_liste(chemin: str | None) -> str:
    if not chemin:
        return ""
    with open(chemin, encoding="utf-8-sig") as f:
        return f.read()


def decrire(entites, marqueurs) -> str:
    groupes: dict[str, list] = {}
    for e in entites:
        groupes.setdefault(marqueurs[e.cle], []).append(e)
    lignes = []
    for marqueur, liste in groupes.items():
        formes = sorted({e.texte for e in liste}, key=len, reverse=True)
        lignes.append(f"  {marqueur:<22} {' / '.join(formes)}  ({len(liste)} occurrence{'s' if len(liste) > 1 else ''} ;"
                      f" {liste[0].raison})")
    return "\n".join(lignes) if lignes else "  aucune donnée détectée"


def commande_pseudonymiser(args) -> int:
    try:
        texte = lire_fichier(args.fichier)
        termes = lire_termes(lire_liste(args.termes))
        exclus = [x.strip() for x in lire_liste(args.exclure).splitlines() if x.strip() and not x.startswith("#")]
        entites = detecter(texte, termes, exclus)
    except (ErreurLecture, OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2
    resultat = pseudonymiser(texte, entites, os.path.basename(args.fichier))
    print(f"{os.path.basename(args.fichier)} : {len(entites)} remplacement(s), "
          f"{len(resultat.table['correspondances'])} donnée(s) distincte(s)\n")
    print(decrire(entites, attribuer_marqueurs(entites, texte)))
    if not entites and texte.strip():
        print("\nAttention : aucune donnée détectée. Vérifiez que le texte affiché ci-dessus est lisible "
              "et relisez-le : l'absence de détection ne prouve pas l'absence de données personnelles.")
    if resultat.marqueurs_preexistants:
        print(f"\nAttention : le texte d'origine contient déjà des marqueurs ({', '.join(resultat.marqueurs_preexistants)}). "
              "Ils resteront tels quels au rétablissement ; la numérotation des nouveaux marqueurs commence après eux.")
    print(f"\n{AVERTISSEMENT}")
    if args.liste:
        return 0
    try:
        base = os.path.splitext(os.path.basename(args.fichier))[0]
        chemin_texte, chemin_table = enregistrer(args.sortie or dossier_par_defaut(), base, resultat.texte, resultat.table)
    except OSError as e:
        print(f"Erreur d'écriture : {e}", file=sys.stderr)
        return 2
    print(f"\nTexte pseudonymisé : {chemin_texte}\nTable de correspondance : {chemin_table}")
    return 0


def commande_retablir(args) -> int:
    try:
        table = lire_table(args.table)
        with open(args.fichier, encoding="utf-8-sig") as f:
            texte = f.read()
    except (OSError, ValueError) as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2
    r = retablir(texte, table)
    if args.sortie:
        if os.path.exists(args.sortie):
            print(f"Erreur : {args.sortie} existe déjà ; choisissez un autre nom.", file=sys.stderr)
            return 2
        with open(args.sortie, "x", encoding="utf-8", newline="\n") as f:
            f.write(r.texte)
        print(f"Texte rétabli : {args.sortie}", file=sys.stderr)
    else:
        print(r.texte)
    print(f"{sum(r.remplaces.values())} marqueur(s) remplacé(s).", file=sys.stderr)
    if r.approches:
        print(f"Formes approchées remplacées (vérifiez-les) : {', '.join(r.approches)}", file=sys.stderr)
    if r.inconnus:
        print(f"Marqueurs absents de la table, laissés tels quels : {', '.join(r.inconnus)}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="pseudonymisation", description=(
        "Pseudonymise un texte sur cet ordinateur avant de l'envoyer à une IA, puis rétablit les données "
        "dans la réponse. Sans réseau. " + AVERTISSEMENT))
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sous = parser.add_subparsers(dest="commande")
    p = sous.add_parser("pseudonymiser", help="remplace les données détectées par des marqueurs")
    p.add_argument("fichier", help="fichier .txt, .md ou .docx")
    p.add_argument("--termes", metavar="FICHIER",
                   help="termes à pseudonymiser en tout cas, un par ligne (« PERSONNE | Jean Dupont » pour choisir "
                        f"la catégorie ; catégories : {', '.join(CATEGORIES)})")
    p.add_argument("--exclure", metavar="FICHIER", help="textes à ne jamais remplacer, un par ligne")
    p.add_argument("--sortie", metavar="DOSSIER", help="dossier où écrire le texte et la table")
    p.add_argument("--liste", action="store_true", help="affiche les détections sans rien écrire")
    r = sous.add_parser("retablir", help="remet les données d'origine dans la réponse de l'IA")
    r.add_argument("fichier", help="réponse de l'IA (texte)")
    r.add_argument("--table", required=True, help="table de correspondance produite lors de la pseudonymisation")
    r.add_argument("--sortie", metavar="FICHIER", help="fichier à écrire (sinon : affichage)")
    args = parser.parse_args(argv)
    if args.commande == "pseudonymiser":
        return commande_pseudonymiser(args)
    if args.commande == "retablir":
        return commande_retablir(args)
    from .interface import main as interface
    return interface()


if __name__ == "__main__":
    sys.exit(main())
