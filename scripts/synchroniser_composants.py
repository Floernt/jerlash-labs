"""Copie les composants communs dans les outils qui les déclarent (ADR-021).

    python scripts/synchroniser_composants.py              met à jour les copies
    python scripts/synchroniser_composants.py --verifier   échoue si une copie diffère de sa source

Chaque outil reste autonome : il embarque, dans son propre src/, une copie des composants
qu'il utilise. Il les déclare dans outils/<slug>/COMPOSANTS.md, une ligne par composant :

    - connecteur-ia 0.1.0 (source : factory/composants/connecteur-ia)

Seul le nom compte à la lecture ; version et source sont réécrites par ce script.
Les copies ne se modifient jamais dans l'outil : on modifie la source, puis on synchronise.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import re
import shutil
import sys

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCES = {
    "connecteur-ia": ("factory/composants/connecteur-ia", "src/connecteur_ia"),
    "pseudonymisation": ("outils/pseudonymisation", "src/pseudonymisation"),
}

ENTETE = """# Composants intégrés

Cet outil fonctionne seul : il contient une copie des composants communs du projet jerlash.labs dont il a besoin. Ces copies ne se modifient pas ici ; la source est indiquée ci-dessous (scripts/synchroniser_composants.py, ADR-021).

"""
LIGNE = re.compile(r"^- ([a-z0-9-]+)\b", re.MULTILINE)
IGNORES = shutil.ignore_patterns("__pycache__", "*.pyc")


def version(paquet: str) -> str:
    with open(os.path.join(paquet, "__init__.py"), encoding="utf-8") as f:
        m = re.search(r'^__version__ = "([^"]+)"', f.read(), re.MULTILINE)
    return m.group(1) if m else "?"


def fichiers(dossier: str) -> dict[str, bytes]:
    contenu = {}
    for racine, sous, noms in os.walk(dossier):
        sous[:] = [s for s in sous if s != "__pycache__"]
        for nom in noms:
            if nom.endswith(".pyc"):
                continue
            chemin = os.path.join(racine, nom)
            with open(chemin, "rb") as f:
                contenu[os.path.relpath(chemin, dossier)] = f.read().replace(b"\r\n", b"\n")
    return contenu


def declarations() -> dict[str, list[str]]:
    resultat = {}
    racine = os.path.join(DEPOT, "outils")
    for slug in sorted(os.listdir(racine)):
        chemin = os.path.join(racine, slug, "COMPOSANTS.md")
        if os.path.isfile(chemin):
            with open(chemin, encoding="utf-8") as f:
                resultat[slug] = LIGNE.findall(f.read())
    return resultat


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", action="store_true", help="contrôle sans rien écrire")
    args = parser.parse_args(argv)
    ecarts, copies = [], 0
    for slug, noms in declarations().items():
        lignes = []
        for nom in noms:
            if nom not in SOURCES:
                ecarts.append(f"{slug} : composant inconnu « {nom} »")
                continue
            base, paquet = SOURCES[nom]
            if base == f"outils/{slug}":
                ecarts.append(f"{slug} : un outil ne peut pas s'embarquer lui-même ({nom})")
                continue
            source = os.path.join(DEPOT, base, paquet)
            cible = os.path.join(DEPOT, "outils", slug, "src", os.path.basename(paquet))
            lignes.append(f"- {nom} {version(source)} (source : {base})")
            copies += 1
            if args.verifier:
                if fichiers(source) != (fichiers(cible) if os.path.isdir(cible) else {}):
                    ecarts.append(f"{slug} : la copie de {nom} diffère de sa source")
            else:
                if os.path.isdir(cible):
                    shutil.rmtree(cible)
                shutil.copytree(source, cible, ignore=IGNORES)
        chemin = os.path.join(DEPOT, "outils", slug, "COMPOSANTS.md")
        texte = ENTETE + "\n".join(lignes) + "\n"
        if args.verifier:
            with open(chemin, encoding="utf-8") as f:
                if f.read().replace("\r\n", "\n") != texte:
                    ecarts.append(f"{slug} : COMPOSANTS.md n'est pas à jour")
        else:
            with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                f.write(texte)
    for e in ecarts:
        print(e)
    print(f"{copies} copie(s) de composant{', écarts : ' + str(len(ecarts)) if ecarts else ', conformes'}")
    if ecarts and args.verifier:
        print("Corriger la source, puis lancer : python scripts/synchroniser_composants.py")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
