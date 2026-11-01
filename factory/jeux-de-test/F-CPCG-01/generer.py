"""Génère les contrats fictifs F-CPCG-01 (.docx) à partir de sources/ et sources-controle/.

    python -I factory/jeux-de-test/F-CPCG-01/generer.py             régénère pieces/ et pieces-controle/
    python -I factory/jeux-de-test/F-CPCG-01/generer.py --verifier  échoue si les .docx diffèrent des sources

Chaque source commence par « fichier: <nom>.docx », puis « --- » et le texte, un paragraphe par ligne.
Une ligne qui commence par « | » est une ligne de tableau. Les données propres à l'opération sont balisées
[[CATÉGORIE:texte]] : le balisage est retiré des .docx et sert à la mesure (evaluer.py). Comme pour
F-DEF-01, le générateur place des espaces insécables dans les guillemets français et met les termes entre
guillemets dans un fragment (run) séparé. Toutes les personnes et sociétés sont fictives.
"""

from __future__ import annotations

import io
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
JEUX = ((os.path.join(ICI, "sources"), os.path.join(ICI, "pieces")),
        # Jeu de contrôle : rédigé à part, sans accès à l'outil ; sert seulement à mesurer.
        (os.path.join(ICI, "sources-controle"), os.path.join(ICI, "pieces-controle")))
DATE_ZIP = (2026, 1, 1, 0, 0, 0)
GUILLEMETS = re.compile(r'(«[^»]*»|"[^"]*"|“[^”]*”)')
BALISE = re.compile(r"\[\[([A-Z]+):(.*?)\]\]")


def lire_source(chemin: str, balise: bool = False) -> tuple[str, list[str]]:
    """Nom du .docx et lignes du texte, sans le balisage des données (sauf si balise=True)."""
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().replace("\r\n", "\n")
    entete, texte = brut.split("\n---\n", 1)
    nom = entete.split("fichier: ", 1)[1].strip()
    lignes = texte.rstrip("\n").split("\n")
    return nom, lignes if balise else [BALISE.sub(r"\2", l) for l in lignes]


def runs(texte: str) -> str:
    texte = texte.replace("« ", "« ").replace(" »", " »")
    xml = []
    for i, morceau in enumerate(GUILLEMETS.split(texte)):
        if morceau:
            gras = "<w:rPr><w:b/></w:rPr>" if i % 2 else ""
            xml.append(f'<w:r>{gras}<w:t xml:space="preserve">{escape(morceau)}</w:t></w:r>')
    return "".join(xml)


def paragraphe(texte: str) -> str:
    return f"<w:p>{runs(texte)}</w:p>" if texte else "<w:p/>"


def tableau(lignes: list[str]) -> str:
    rangs = []
    for ligne in lignes:
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        rangs.append("<w:tr>" + "".join(f"<w:tc>{paragraphe(c)}</w:tc>" for c in cellules) + "</w:tr>")
    return "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/></w:tblPr>" + "".join(rangs) + "</w:tbl>"


def corps(lignes: list[str]) -> str:
    xml, en_tableau = [], []
    for ligne in lignes + [""]:
        if ligne.startswith("|"):
            en_tableau.append(ligne)
            continue
        if en_tableau:
            xml.append(tableau(en_tableau))
            en_tableau = []
        xml.append(paragraphe(ligne))
    return "".join(xml[:-1])


def docx(lignes: list[str]) -> bytes:
    parties = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/></Relationships>'),
        "word/document.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{corps(lignes)}<w:sectPr/></w:body></w:document>'),
    }
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in parties.items():
            info = zipfile.ZipInfo(nom, DATE_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, contenu.encode("utf-8"))
    return sortie.getvalue()


def produire() -> dict[str, bytes]:
    fichiers = {}
    for sources, pieces in JEUX:
        if os.path.isdir(sources):
            for nom in sorted(os.listdir(sources)):
                fichier, lignes = lire_source(os.path.join(sources, nom))
                fichiers[os.path.join(pieces, fichier)] = docx(lignes)
    return fichiers


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    verifier = "--verifier" in (argv if argv is not None else sys.argv[1:])
    attendus = produire()
    ecarts = 0
    if verifier:
        for _sources, pieces in JEUX:
            presents = {os.path.join(pieces, n) for n in os.listdir(pieces)} if os.path.isdir(pieces) else set()
            for chemin in presents - set(attendus):
                ecarts += 1
                print(f"en trop : {os.path.relpath(chemin, ICI)}")
    for chemin, donnees in attendus.items():
        if verifier:
            try:
                with open(chemin, "rb") as f:
                    identique = f.read() == donnees
            except OSError:
                identique = False
            if not identique:
                ecarts += 1
                print(f"différent : {os.path.basename(chemin)}")
        else:
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            with open(chemin, "wb") as f:
                f.write(donnees)
            print(f"écrit : {os.path.basename(chemin)}")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
