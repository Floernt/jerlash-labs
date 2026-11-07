"""Espaces insécables du français dans les textes du site (charte éditoriale, « Typographie »).

    python scripts/typographie.py              corrige les fichiers de site/content et le texte de site/layouts
    python scripts/typographie.py --verifier   n'écrit rien ; code 1 si une correction est nécessaire

Règles : espace fine insécable (U+202F) avant ; ! ?, espace insécable (U+00A0) avant : et à
l'intérieur des guillemets « ». Le code (blocs ``` et `code`), les URL, les balises HTML et les
instructions de gabarit {{ }} ne sont jamais modifiés.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINE, INSECABLE = " ", " "

REGLES = [
    (re.compile(r"(?<=[^\s\[(])[   ]?([;!?])(?=\s|$|[\"»)*_])"), FINE + r"\1"),
    (re.compile(r"(?<=[^\s\[(:/])[   ]?:(?=\s|$)"), INSECABLE + ":"),
    (re.compile(r"«[   ]?"), "«" + INSECABLE),
    (re.compile(r"[   ]?»"), INSECABLE + "»"),
]
PROTEGE_MD = re.compile(r"(`[^`]*`|\]\([^)]*\)|<[^>]+>|https?://\S+|\{\{.*?\}\})")
PROTEGE_HTML = re.compile(r"(\{\{.*?\}\}|<[^>]+>|https?://\S+)", re.DOTALL)


def corriger_segment(texte: str) -> str:
    for motif, remplacement in REGLES:
        texte = motif.sub(remplacement, texte)
    return texte


def corriger_ligne(ligne: str, protege: re.Pattern) -> str:
    morceaux = protege.split(ligne)
    return "".join(m if i % 2 else corriger_segment(m) for i, m in enumerate(morceaux))


def corriger_markdown(texte: str) -> str:
    lignes, sortie, dans_code, front = texte.split("\n"), [], False, 0
    for i, ligne in enumerate(lignes):
        if ligne.strip() == "---" and front < 2 and (i == 0 or front == 1):
            front += 1
            sortie.append(ligne)
            continue
        if ligne.lstrip().startswith("```"):
            dans_code = not dans_code
            sortie.append(ligne)
            continue
        if dans_code:
            sortie.append(ligne)
        elif front == 1:
            # Front matter YAML : seules les valeurs entre guillemets sont corrigées.
            m = re.match(r'^(\s*-?\s*[\w-]+:\s*")(.*)("\s*)$', ligne)
            sortie.append(m.group(1) + corriger_ligne(m.group(2), PROTEGE_MD) + m.group(3) if m else ligne)
        else:
            sortie.append(corriger_ligne(ligne, PROTEGE_MD))
    return "\n".join(sortie)


def corriger_html(texte: str) -> str:
    morceaux = PROTEGE_HTML.split(texte)
    return "".join(m if i % 2 else corriger_segment(m) for i, m in enumerate(morceaux))


def corriger_i18n(texte: str) -> str:
    """Libellés i18n (YAML « clé: "valeur" ») : seules les valeurs entre guillemets sont corrigées."""
    def ligne(l: str) -> str:
        m = re.match(r'^(\s*[\w-]+:\s*")(.*)("\s*)$', l)
        return m.group(1) + corriger_ligne(m.group(2), PROTEGE_MD) + m.group(3) if m else l
    return "\n".join(ligne(l) for l in texte.split("\n"))


def fichiers():
    for racine, _d, noms in os.walk(os.path.join(DEPOT, "site", "content")):
        for nom in noms:
            # Les traductions (x.en.md, ADR-023) suivent la typographie de leur langue.
            if nom.endswith(".md") and not re.search(r"\.[a-z]{2}\.md$", nom):
                yield os.path.join(racine, nom), corriger_markdown
    yield os.path.join(DEPOT, "site", "i18n", "fr.yaml"), corriger_i18n
    for racine, _d, noms in os.walk(os.path.join(DEPOT, "site", "layouts")):
        for nom in noms:
            if nom.endswith(".html") and not nom.endswith(("rss.xml",)):
                yield os.path.join(racine, nom), corriger_html


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", action="store_true")
    args = parser.parse_args(argv)
    a_corriger = []
    for chemin, corriger in fichiers():
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
        nouveau = corriger(texte)
        if nouveau != texte:
            a_corriger.append(os.path.relpath(chemin, DEPOT))
            if args.verifier:
                # Montrer où se trouvent les corrections, pour qu'on sache quoi reprendre.
                avant, apres = texte.splitlines(), nouveau.splitlines()
                lignes = [n for n, (a, b) in enumerate(zip(avant, apres), 1) if a != b]
                for n in lignes[:3]:
                    print(f"  {os.path.relpath(chemin, DEPOT)}:{n} : {avant[n - 1].strip()[:90]}")
                if len(lignes) > 3:
                    print(f"  … et {len(lignes) - 3} autre(s) ligne(s)")
            if not args.verifier:
                with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                    f.write(nouveau)
    for c in a_corriger:
        print(("à corriger : " if args.verifier else "corrigé : ") + c)
    if args.verifier and a_corriger:
        print("Lancer : python scripts/typographie.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
