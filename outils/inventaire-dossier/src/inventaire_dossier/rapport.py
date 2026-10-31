"""Registre du dossier : Word (.docx), Markdown et JSON. Mêmes informations dans les trois formats.

Le registre contient les noms des pièces, des parties et des extraits d'indices : il est aussi
confidentiel que le dossier lui-même.
"""

from __future__ import annotations

import datetime
import io
import json
import re
import zipfile
from xml.sax.saxutils import escape

from . import __version__
from .analyse import Fiche, Inventaire

AVERTISSEMENT = ("Inventaire établi par règles, sans IA. Chaque type, statut ou rattachement est une "
                 "proposition fondée sur l'indice indiqué : vérifiez-la avant de vous y fier.")
COLONNES = ["N°", "Pièce", "Type", "Statut", "Date", "Parties", "Se rapporte à", "Fait foi"]


RE_INTERDITS = re.compile("[^\t\n\r -퟿-�\U00010000-\U0010ffff]")


def propre(texte: str) -> str:
    """Retire les caractères interdits en XML 1.0 et les demi-paires UTF-16 isolées (possibles dans un nom
    de fichier ou un en-tête de courriel) : sans cela, Word refuserait d'ouvrir le registre."""
    return RE_INTERDITS.sub("�", texte)


def fait_foi(f: Fiche) -> str:
    return {True: "oui", False: "non", None: "à vérifier"}[f.fait_foi]


def lignes(inventaire: Inventaire) -> list[list[str]]:
    numeros = {f.piece.chemin: str(i) for i, f in enumerate(inventaire.fiches, start=1)}
    return [[numeros[f.piece.chemin], f.piece.chemin, f.type, f.statut, f.date or "—", ", ".join(f.parties) or "—",
             f"n° {numeros[f.rattache_a]}" if f.rattache_a else "—", fait_foi(f)] for f in inventaire.fiches]


def en_dict(inventaire: Inventaire) -> dict:
    return {
        "outil": "inventaire-dossier (iavocat.be)", "version": __version__, "mode": "local, sans IA",
        "etabli_le": datetime.datetime.now().isoformat(timespec="seconds"), "dossier": inventaire.dossier,
        "avertissement": AVERTISSEMENT, "contrat_principal": inventaire.contrat_principal, "etat": inventaire.etat,
        "alertes": inventaire.alertes, "fichiers_ignores": inventaire.ignores,
        "pieces": [{"chemin": f.piece.chemin, "type": f.type, "statut": f.statut, "date": f.date,
                    "parties": f.parties, "rattache_a": f.rattache_a, "fait_foi": f.fait_foi,
                    "indices": f.indices, "alertes": f.alertes, "format": f.piece.format, "taille": f.piece.taille,
                    "sha256": f.piece.sha256, "modifie_le": f.piece.modifie_le, "auteur": f.piece.auteur,
                    "modifie_par": f.piece.modifie_par, "non_lu": f.piece.non_lu,
                    "pieces_jointes": f.piece.courriel.get("pieces_jointes", [])} for f in inventaire.fiches],
    }


def en_json(inventaire: Inventaire) -> str:
    return propre(json.dumps(en_dict(inventaire), ensure_ascii=False, indent=1)) + "\n"


def cellule_md(texte: str) -> str:
    return propre(texte).replace("|", "\\|").replace("\n", " ")


def en_markdown(inventaire: Inventaire) -> str:
    sortie = [f"# Inventaire du dossier {inventaire.dossier}", "",
              f"Établi le {datetime.date.today().isoformat()} par l'outil inventaire-dossier {__version__} (iavocat.be).",
              "", f"> {AVERTISSEMENT}", "", "## Synthèse", "",
              f"- Contrat principal : {inventaire.contrat_principal or 'non identifié'}",
              f"- État : {inventaire.etat}", f"- Pièces : {len(inventaire.fiches)}", "", "## Alertes", ""]
    sortie += [f"- {cellule_md(a)}" for a in inventaire.alertes] or ["Aucune."]
    sortie += ["", "## Pièces", "", "| " + " | ".join(COLONNES) + " |", "|" + "---|" * len(COLONNES)]
    sortie += ["| " + " | ".join(cellule_md(c) for c in ligne) + " |" for ligne in lignes(inventaire)]
    sortie += ["", "## Indices et empreintes", ""]
    for i, f in enumerate(inventaire.fiches, start=1):
        sortie.append(f"{i}. {cellule_md(f.piece.chemin)} — SHA-256 {f.piece.sha256 or '(non calculée)'}"
                      + (f" ; auteur : {cellule_md(f.piece.auteur)}" if f.piece.auteur else ""))
        sortie += [f"   - {cellule_md(x)}" for x in f.indices + jointes(f)]
    return propre("\n".join(sortie)) + "\n"


def jointes(f: Fiche) -> list[str]:
    noms = f.piece.courriel.get("pieces_jointes") or []
    return [f"pièces jointes (non inventoriées) : {', '.join(noms)}"] if noms else []


# --- Word ---------------------------------------------------------------------------------------

def p(texte: str, style: str | None = None, gras: bool = False, taille: int | None = None) -> str:
    proprietes = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    run = ("<w:rPr>" + ("<w:b/>" if gras else "") + (f'<w:sz w:val="{taille}"/>' if taille else "") + "</w:rPr>"
           if gras or taille else "")
    return f'<w:p>{proprietes}<w:r>{run}<w:t xml:space="preserve">{escape(propre(texte))}</w:t></w:r></w:p>'


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


def en_docx(inventaire: Inventaire) -> bytes:
    corps = [p("Inventaire du dossier", "Titre"), p(inventaire.dossier),
             p(f"Établi le {datetime.date.today().isoformat()} par l'outil inventaire-dossier {__version__} (iavocat.be)."),
             p(AVERTISSEMENT, gras=True), p("Synthèse", "Titre1"),
             p(f"Contrat principal : {inventaire.contrat_principal or 'non identifié'}"),
             p(f"État : {inventaire.etat}"), p(f"Pièces : {len(inventaire.fiches)}"), p("Alertes", "Titre1")]
    corps += [p(f"– {a}") for a in inventaire.alertes] or [p("Aucune.")]
    corps += [p("Pièces", "Titre1"), tableau(COLONNES, lignes(inventaire), [500, 3600, 1400, 1100, 1200, 2600, 1100, 900])]
    corps.append(p("Indices et empreintes", "Titre1"))
    for i, f in enumerate(inventaire.fiches, start=1):
        corps.append(p(f"{i}. {f.piece.chemin}", gras=True))
        corps.append(p(f"SHA-256 {f.piece.sha256 or '(non calculée)'}" + (f" ; auteur : {f.piece.auteur}" if f.piece.auteur else ""), taille=16))
        corps += [p(f"– {x}", taille=18) for x in f.indices + jointes(f)]
    section = ('<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
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
