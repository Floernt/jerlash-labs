"""Importe dans le blog les articles marqués « statuts: à publier » (ADR-022).

    python scripts/importer_articles.py                    importe depuis ../articles
    python scripts/importer_articles.py --source DOSSIER   autre dossier source
    python scripts/importer_articles.py --verifier         échoue si le blog diffère de la source

Le dossier source reste hors du dépôt : les brouillons ne sont jamais publiés. Seuls les fichiers .md
placés directement dans le dossier source et dont l'en-tête contient « statuts: à publier » sont repris.
Pour corriger un article, on corrige la source, puis on relance l'import : on ne modifie pas la copie.

Titre : champ « title » de l'en-tête, sinon nom du fichier. Date : champ « date », sinon date de
modification du fichier. Description : champ « description », sinon première phrase du texte.
Les champs internes (statuts, projet, type, tags, tldr) ne sont pas repris.
Sans dossier source (par exemple sur le serveur de publication), --verifier ne contrôle rien et réussit.
"""

from __future__ import annotations

import argparse
import datetime
import io
import os
import re
import sys
import unicodedata

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(os.path.dirname(DEPOT), "articles")
BLOG = os.path.join(DEPOT, "site", "content", "blog")
MARQUE = "Importé par scripts/importer_articles.py : ne pas modifier ici, corriger la source."

sys.path.insert(0, os.path.join(DEPOT, "scripts"))
from typographie import corriger_markdown  # noqa: E402


def lire(chemin: str) -> tuple[dict, str]:
    texte = io.open(chemin, encoding="utf-8").read().replace("\r\n", "\n").lstrip("﻿")
    entete = {}
    m = re.match(r"---\n(.*?)\n---\n?", texte, re.S)
    if m:
        for ligne in m.group(1).splitlines():
            cle, sep, valeur = ligne.partition(":")
            if sep and not ligne.startswith((" ", "\t", "-")):
                entete[cle.strip()] = valeur.strip().strip('"').strip("'")
        texte = texte[m.end():]
    return entete, texte.strip("\n")


def a_publier(entete: dict) -> bool:
    return unicodedata.normalize("NFC", entete.get("statuts", "")).strip().lower() == "à publier"


def slug(titre: str) -> str:
    s = unicodedata.normalize("NFKD", titre).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s if len(s) <= 80 else s[:81].rsplit("-", 1)[0]  # coupe entre deux mots


def premiere_phrase(corps: str) -> str:
    for paragraphe in re.split(r"\n\s*\n", corps):
        p = paragraphe.strip()
        if p and not p.startswith(("#", ">", "-", "*", "|", "!")):
            p = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", r"\1", " ".join(p.split()))
            phrase = re.match(r"(.+?[.!?…])(\s|$)", p)
            phrase = phrase.group(1) if phrase else p
            return phrase if len(phrase) <= 220 else phrase[:217].rsplit(" ", 1)[0] + "…"
    return ""


def yaml(valeur: str) -> str:
    return '"' + valeur.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convertir(chemin: str) -> tuple[str, str]:
    """Nom du fichier de blog et son contenu."""
    entete, corps = lire(chemin)
    titre = entete.get("title") or unicodedata.normalize("NFC", os.path.splitext(os.path.basename(chemin))[0])
    titre = re.sub(r"\s+", " ", titre).strip()
    lignes = corps.split("\n")
    if lignes and re.match(r"#\s+", lignes[0]) and lignes[0].lstrip("# ").strip().lower() == titre.lower():
        corps = "\n".join(lignes[1:]).strip("\n")
    date = entete.get("date") or datetime.date.fromtimestamp(os.path.getmtime(chemin)).isoformat()
    description = entete.get("description") or premiere_phrase(corps)
    # Alias : l'adresse sans préfixe de langue, publiée avant le site bilingue, redirige vers /fr/ (ADR-023).
    contenu = (f"---\ntitle: {yaml(titre)}\ndate: {date}\ndescription: {yaml(description)}\n"
               f"aliases: [\"/blog/{slug(titre)}/\"]\n# {MARQUE}\n---\n\n{corps}\n")
    return f"{slug(titre)}.md", corriger_markdown(contenu)


def attendus(source: str) -> dict[str, str]:
    resultat = {}
    for nom in sorted(os.listdir(source)):
        chemin = os.path.join(source, nom)
        if nom.endswith(".md") and os.path.isfile(chemin) and a_publier(lire(chemin)[0]):
            fichier, contenu = convertir(chemin)
            if fichier in resultat:
                raise SystemExit(f"Deux articles donnent le même nom de fichier : {fichier}")
            resultat[fichier] = contenu
    return resultat


def presents() -> dict[str, str]:
    resultat = {}
    for nom in sorted(os.listdir(BLOG)):
        # Les traductions (x.en.md, ADR-023) ne viennent pas de la source : jamais retirées ni comparées ici.
        if nom.endswith(".md") and nom != "_index.md" and not re.search(r"\.[a-z]{2}\.md$", nom):
            texte = io.open(os.path.join(BLOG, nom), encoding="utf-8").read()
            if MARQUE in texte:
                resultat[nom] = texte
    return resultat


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", default=SOURCE)
    parser.add_argument("--verifier", action="store_true")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.source):
        if args.verifier:
            print(f"Dossier source absent ({args.source}) : contrôle non effectué")
            return 0
        print(f"Dossier source introuvable : {args.source}", file=sys.stderr)
        return 2
    voulus, actuels = attendus(args.source), presents()
    if args.verifier:
        ecarts = sorted(n for n in set(voulus) | set(actuels) if voulus.get(n) != actuels.get(n))
        for n in ecarts:
            print(f"écart : {n}")
        print(f"{len(voulus)} article(s) à publier, " + (f"{len(ecarts)} écart(s) : relancer l'import" if ecarts else "blog conforme"))
        return 1 if ecarts else 0
    for nom in set(actuels) - set(voulus):
        os.remove(os.path.join(BLOG, nom))
        print(f"retiré : {nom}")
    for nom, contenu in voulus.items():
        with open(os.path.join(BLOG, nom), "w", encoding="utf-8", newline="\n") as f:
            f.write(contenu)
        date = re.search(r"^date: (.*)$", contenu, re.M).group(1)
        print(f"{date}  {nom}")
    print(f"{len(voulus)} article(s) importé(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
