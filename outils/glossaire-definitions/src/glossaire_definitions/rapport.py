"""Rapport : Word (.docx), Markdown et JSON. Mêmes informations dans les trois formats.

Le rapport reprend les définitions du contrat : il est aussi confidentiel que le contrat lui-même.
"""

from __future__ import annotations

import datetime
import io
import json
import re
import zipfile
from xml.sax.saxutils import escape

from . import __version__
from .analyse import ORDRE, Analyse, abreger, lister

AVERTISSEMENT = ("Rapport établi par règles, sans IA. Il signale des points à vérifier ; il ne dit pas si une "
                 "définition est juridiquement correcte. Relisez chaque point dans le contrat avant de le corriger.")
TITRES = {
    "divergent": "Définitions divergentes",
    "non_defini": "Termes écrits comme des termes définis, sans définition",
    "variante": "Graphies différentes d'un terme défini",
    "avant_definition": "Termes employés avant leur définition",
    "doublon": "Définitions répétées",
    "inutilise": "Termes définis jamais employés",
}
COLONNES = ["Terme", "Définition", "Où", "Emplois"]
RE_INTERDITS = re.compile("[^\t\n\r\u0020-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]")


def propre(texte: str) -> str:
    """Retire les caractères interdits en XML 1.0 : sans cela, Word refuserait d'ouvrir le rapport."""
    return RE_INTERDITS.sub("\ufffd", texte)


def lignes(analyse: Analyse) -> list[list[str]]:
    sortie = []
    for t in analyse.termes:
        definitions = [abreger(d.libelle, 300) for d in t.definitions]
        sortie.append([t.forme, "\n".join(f"{i}) {x}" for i, x in enumerate(definitions, 1)) if len(definitions) > 1
                       else definitions[0], ", ".join(dict.fromkeys(d.lieu for d in t.definitions)),
                       str(len(t.emplois))])
    return sortie


def en_dict(analyse: Analyse) -> dict:
    return {
        "outil": "glossaire-definitions (jerlash.labs)", "version": __version__, "mode": "local, sans IA",
        "etabli_le": datetime.datetime.now().isoformat(timespec="seconds"), "document": analyse.document,
        "avertissement": AVERTISSEMENT,
        "constats": [{"categorie": c.categorie, "terme": c.terme, "forme": c.forme, "message": c.message}
                     for c in analyse.constats],
        "termes": [{"terme": t.forme, "emplois": len(t.emplois), "premier_emploi": analyse.lieux[t.emplois[0]] if t.emplois else None,
                    "variantes": {f: lister(ou, analyse.lieux) for f, ou in t.variantes.items()},
                    "definitions": [{"forme": d.forme, "lieu": d.lieu, "libelle": d.libelle,
                                     "article_des_definitions": d.glossaire} for d in t.definitions]}
                   for t in analyse.termes],
    }


def en_json(analyse: Analyse) -> str:
    return propre(json.dumps(en_dict(analyse), ensure_ascii=False, indent=1)) + "\n"


def synthese(analyse: Analyse) -> list[str]:
    sortie = [f"Termes définis : {len(analyse.termes)}"]
    sortie += [f"{TITRES[c]} : {len(analyse.du_type(c))}" for c in ORDRE if analyse.du_type(c)]
    if not analyse.constats:
        sortie.append("Aucun point relevé.")
    return sortie


def cellule_md(texte: str) -> str:
    """Le HTML et les images du contrat sont neutralisés : un aperçu Markdown n'ira rien chercher sur le réseau."""
    texte = propre(texte).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("![", "!\\[")
    return texte.replace("|", "\\|").replace("\n", "<br>")


def en_markdown(analyse: Analyse) -> str:
    sortie = [f"# Glossaire des définitions : {cellule_md(analyse.document)}", "",
              f"Établi le {datetime.date.today().isoformat()} par l'outil glossaire-definitions {__version__} (jerlash.labs).",
              "", f"> {AVERTISSEMENT}", "", "## Synthèse", ""]
    sortie += [f"- {x}" for x in synthese(analyse)]
    sortie += ["", "## Points à examiner", ""]
    for c in ORDRE:
        if analyse.du_type(c):
            sortie += [f"### {TITRES[c]}", ""] + [f"- {cellule_md(x.message)}" for x in analyse.du_type(c)] + [""]
    if not analyse.constats:
        sortie += ["Aucun.", ""]
    sortie += ["## Glossaire", "", "| " + " | ".join(COLONNES) + " |", "|" + "---|" * len(COLONNES)]
    sortie += ["| " + " | ".join(cellule_md(x) for x in ligne) + " |" for ligne in lignes(analyse)]
    return propre("\n".join(sortie)) + "\n"


# --- Word ---------------------------------------------------------------------------------------

def p(texte: str, style: str | None = None, gras: bool = False, taille: int | None = None) -> str:
    proprietes = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    run = ("<w:rPr>" + ("<w:b/>" if gras else "") + (f'<w:sz w:val="{taille}"/>' if taille else "") + "</w:rPr>"
           if gras or taille else "")
    morceaux = propre(texte).split("\n")
    contenu = "<w:br/>".join(f'<w:t xml:space="preserve">{escape(m)}</w:t>' for m in morceaux)
    return f'<w:p>{proprietes}<w:r>{run}{contenu}</w:r></w:p>'


def tableau(entetes: list[str], contenu: list[list[str]], largeurs: list[int]) -> str:
    bord = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
    bords = "".join(bord.format(c) for c in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(largeurs)}" w:type="dxa"/><w:tblBorders>{bords}</w:tblBorders>'
           '<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>'
           + "".join(f'<w:gridCol w:w="{l}"/>' for l in largeurs) + "</w:tblGrid>"]
    for rang, ligne in enumerate([entetes] + contenu):
        entete = '<w:trPr><w:tblHeader/></w:trPr>' if rang == 0 else ""
        cellules = "".join(f'<w:tc><w:tcPr><w:tcW w:w="{l}" w:type="dxa"/></w:tcPr>{p(c, gras=rang == 0, taille=18)}</w:tc>'
                           for c, l in zip(ligne, largeurs))
        xml.append(f"<w:tr>{entete}{cellules}</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


def en_docx(analyse: Analyse) -> bytes:
    corps = [p("Glossaire des définitions", "Titre"), p(analyse.document),
             p(f"Établi le {datetime.date.today().isoformat()} par l'outil glossaire-definitions {__version__} (jerlash.labs)."),
             p(AVERTISSEMENT, gras=True), p("Synthèse", "Titre1")]
    corps += [p(f"– {x}") for x in synthese(analyse)]
    corps.append(p("Points à examiner", "Titre1"))
    for c in ORDRE:
        if analyse.du_type(c):
            corps.append(p(TITRES[c], "Titre2"))
            corps += [p(f"– {x.message}") for x in analyse.du_type(c)]
    if not analyse.constats:
        corps.append(p("Aucun."))
    corps += [p("Glossaire", "Titre1"), tableau(COLONNES, lignes(analyse), [2200, 4700, 1700, 900])]
    section = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
               '<w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000" w:header="500" w:footer="500" w:gutter="0"/></w:sectPr>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f'<w:body>{"".join(corps)}{section}</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
              '<w:sz w:val="20"/><w:lang w:val="fr-BE"/></w:rPr></w:rPrDefault>'
              '<w:pPrDefault><w:pPr><w:spacing w:after="80"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              '<w:style w:type="paragraph" w:styleId="Titre"><w:name w:val="Title"/><w:basedOn w:val="Normal"/>'
              '<w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Titre1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
              '<w:pPr><w:keepNext/><w:spacing w:before="240"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Titre2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
              '<w:pPr><w:keepNext/><w:spacing w:before="160"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>'
              '</w:styles>')
    parties = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>'),
        "word/_rels/document.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>'),
        "word/document.xml": document,
        "word/styles.xml": styles,
    }
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in parties.items():
            z.writestr(nom, contenu.encode("utf-8"))
    return sortie.getvalue()
