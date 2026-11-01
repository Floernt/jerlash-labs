"""État des traductions anglaises du site (ADR-023) : le français est la version maître.

    python scripts/traductions.py                     état de chaque page (code 1 s'il reste du travail)
    python scripts/traductions.py --etat CHEMIN...    idem, limité à des fichiers ou dossiers de site/content
    python scripts/traductions.py --diff FICHIER.md   ce qui a changé en français depuis la dernière traduction
    python scripts/traductions.py --marquer FICHIER.en.md...
                                                      enregistre que la traduction suit le français actuel

Chaque page française content/x.md a sa traduction content/x.en.md. Le front matter de la traduction
porte l'empreinte git du texte français traduit :

    traduction:
      source: "<empreinte>"

États : « à jour », « à traduire » (pas de traduction), « obsolète » (le français a changé depuis),
« non marqué » (traduction sans empreinte), « brouillon divergent » (draft différent), « orphelin »
(traduction sans page française). On corrige le français, jamais l'anglais : /traduire répercute.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENU = os.path.join(DEPOT, "site", "content")
LANGUE = "en"
TRADUCTION = re.compile(r"\.[a-z]{2}\.md$")
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SOURCE = re.compile(r'^traduction:\s*\n[ \t]+source:\s*"?([0-9a-f]{40})"?\s*$', re.M)
BROUILLON = re.compile(r"^draft:\s*(true|false)\s*$", re.M)


def git(*args: str, entree: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=DEPOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", input=entree)


def relatif(chemin: str) -> str:
    return os.path.relpath(chemin, DEPOT).replace(os.sep, "/")


def empreinte(chemin: str, ecrire: bool = False) -> str:
    """Empreinte git du fichier ; avec ecrire, le contenu est conservé dans le dépôt pour --diff."""
    r = git("hash-object", *(["-w"] if ecrire else []), "--", relatif(chemin))
    if r.returncode:
        raise SystemExit(r.stderr.strip())
    return r.stdout.strip()


def front_matter(chemin: str) -> str:
    with open(chemin, encoding="utf-8") as f:
        m = FRONT.match(f.read().replace("\r\n", "\n"))
    return m.group(1) + "\n" if m else ""


def brouillon(chemin: str) -> bool:
    m = BROUILLON.search(front_matter(chemin))
    return bool(m) and m.group(1) == "true"


def traduction_de(francais: str) -> str:
    return francais[:-3] + f".{LANGUE}.md"


def francais_de(traduction: str) -> str:
    return TRADUCTION.sub(".md", traduction)


def fichiers(racines: list[str]) -> tuple[list[str], list[str]]:
    francais, traductions = [], []
    for racine in racines:
        chemins = [racine] if os.path.isfile(racine) else \
            [os.path.join(r, n) for r, _d, ns in os.walk(racine) for n in ns]
        for c in chemins:
            if c.endswith(f".{LANGUE}.md"):
                traductions.append(c)
            elif c.endswith(".md") and not TRADUCTION.search(c):
                francais.append(c)
    return sorted(set(francais)), sorted(set(traductions))


def etat(francais: str) -> str:
    cible = traduction_de(francais)
    if not os.path.isfile(cible):
        return "à traduire"
    m = SOURCE.search(front_matter(cible))
    if not m:
        return "non marqué"
    if m.group(1) != empreinte(francais):
        return "obsolète"
    if brouillon(francais) != brouillon(cible):
        return "brouillon divergent"
    return "à jour"


def afficher_etat(racines: list[str]) -> int:
    francais, traductions = fichiers(racines)
    lignes = [(etat(f), relatif(f)) for f in francais]
    lignes += [("orphelin", relatif(t)) for t in traductions if not os.path.isfile(francais_de(t))]
    a_faire = [(e, c) for e, c in lignes if e != "à jour"]
    for e, c in sorted(a_faire):
        print(f"{e:<20} {c}")
    total = sum(1 for e, _ in lignes if e != "orphelin")
    print(f"{total - len([1 for e, _ in a_faire if e != 'orphelin'])}/{total} page(s) à jour"
          + (f", {len(a_faire)} à traiter : /traduire" if a_faire else ""))
    return 1 if a_faire else 0


def afficher_diff(francais: str) -> int:
    francais = os.path.abspath(francais)
    if TRADUCTION.search(francais):
        francais = francais_de(francais)
    cible = traduction_de(francais)
    if not os.path.isfile(cible):
        print(f"Pas de traduction : {relatif(cible)} est à créer entièrement.")
        return 1
    m = SOURCE.search(front_matter(cible))
    if not m:
        print(f"{relatif(cible)} ne porte pas d'empreinte : comparer le texte entier.")
        return 1
    ancienne, actuelle = m.group(1), empreinte(francais, ecrire=True)
    if ancienne == actuelle:
        print("Aucun changement en français depuis la dernière traduction.")
        return 0
    if git("cat-file", "-e", ancienne).returncode:
        print(f"Version traduite introuvable dans git ({ancienne[:12]}) : comparer le texte entier.")
        return 1
    r = git("diff", "--no-color", "--unified=3", ancienne, actuelle)
    print(r.stdout or r.stderr)
    return 0


def marquer(traduction: str) -> None:
    traduction = os.path.abspath(traduction)
    francais = francais_de(traduction)
    if not (traduction.endswith(f".{LANGUE}.md") and os.path.isfile(traduction) and os.path.isfile(francais)):
        raise SystemExit(f"Traduction ou page française introuvable : {relatif(traduction)}")
    bloc = f'traduction:\n  source: "{empreinte(francais, ecrire=True)}"\n'
    with open(traduction, encoding="utf-8") as f:
        texte = f.read().replace("\r\n", "\n")
    m = FRONT.match(texte)
    if not m:
        raise SystemExit(f"Front matter absent : {relatif(traduction)}")
    entete = re.sub(r"^traduction:\s*\n(?:[ \t]+.*\n)*", "", m.group(1) + "\n", flags=re.M)
    texte = f"---\n{entete}{bloc}---\n" + texte[m.end():]
    with open(traduction, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    print(f"marqué : {relatif(traduction)}")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    groupe = parser.add_mutually_exclusive_group()
    groupe.add_argument("--etat", nargs="*", metavar="CHEMIN")
    groupe.add_argument("--diff", metavar="FICHIER")
    groupe.add_argument("--marquer", nargs="+", metavar="FICHIER")
    args = parser.parse_args(argv)
    if args.diff:
        return afficher_diff(args.diff)
    if args.marquer:
        for t in args.marquer:
            marquer(t)
        return 0
    return afficher_etat([os.path.abspath(c) for c in args.etat] if args.etat else [CONTENU])


if __name__ == "__main__":
    sys.exit(main())
