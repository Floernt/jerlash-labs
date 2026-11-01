"""Génère les pièces du jeu de test F-DOCX-01 (entièrement fictives).

    python -I generer.py [dossier_sortie]     (par défaut : pieces/ à côté de ce script)

Les fichiers sont reproductibles octet par octet (dates d'archive fixes), ce qui permet
de vérifier que les pièces versionnées correspondent bien à ce générateur.
Aucune dépendance : bibliothèque standard uniquement.
"""

from __future__ import annotations

import os
import sys
import zipfile

DATE_ZIP = (2026, 1, 1, 0, 0, 0)

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
T_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
T_CORE = "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
T_APP = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
T_CUSTOM = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties"
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
NSDOC = (f'xmlns:w="{W}" xmlns:r="{R}" '
         'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
         'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
         'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
         'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"')


def ecrire_docx(chemin: str, parties: dict[str, str | bytes]) -> None:
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in sorted(parties, key=lambda n: (n != "[Content_Types].xml", n)):
            contenu = parties[nom]
            info = zipfile.ZipInfo(nom, DATE_ZIP)
            info.create_system = 3  # Unix partout : zipfile met 0 sous Windows, ce qui change les octets
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            z.writestr(info, contenu.encode("utf-8") if isinstance(contenu, str) else contenu)


def types(defauts: dict[str, str], surcharges: dict[str, str]) -> str:
    d = "".join(f'<Default Extension="{e}" ContentType="{t}"/>' for e, t in defauts.items())
    o = "".join(f'<Override PartName="/{p}" ContentType="{t}"/>' for p, t in surcharges.items())
    return f'{XML}<Types xmlns="{CT}">{d}{o}</Types>'


def rels(liste: list[tuple[str, str, str, bool]]) -> str:
    corps = "".join(
        f'<Relationship Id="{i}" Type="{t}" Target="{c}"' + (' TargetMode="External"' if ext else "") + "/>"
        for i, t, c, ext in liste)
    return f'{XML}<Relationships xmlns="{PR}">{corps}</Relationships>'


def p(*runs: str, style: str | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{''.join(runs)}</w:p>"


def r(texte: str, rpr: str = "") -> str:
    return f'<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{texte}</w:t></w:r>'


CT_DOC = "application/vnd.openxmlformats-officedocument.wordprocessingml"
DEFAUTS = {"rels": "application/vnd.openxmlformats-package.relationships+xml", "xml": "application/xml"}


def styles(avec_style_masque: bool) -> str:
    masque = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="NoteInterne"><w:name w:val="Note interne"/>'
              '<w:basedOn w:val="Normal"/><w:rPr><w:vanish/></w:rPr></w:style>') if avec_style_masque else ""
    return (f'{XML}<w:styles xmlns:w="{W}"><w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            f'<w:name w:val="Normal"/></w:style><w:style w:type="paragraph" w:styleId="Titre">'
            f'<w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>'
            f'{masque}</w:styles>')


def core(createur: str, modifie_par: str, titre: str = "", mots_cles: str = "", revision: str = "1",
         impression: str = "") -> str:
    imp = f"<cp:lastPrinted>{impression}</cp:lastPrinted>" if impression else ""
    return (f'{XML}<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{titre}</dc:title><dc:creator>{createur}</dc:creator><cp:keywords>{mots_cles}</cp:keywords>"
            f"<cp:lastModifiedBy>{modifie_par}</cp:lastModifiedBy><cp:revision>{revision}</cp:revision>{imp}"
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-09-01T09:00:00Z</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-10-15T17:30:00Z</dcterms:modified>'
            "</cp:coreProperties>")


def app(societe: str = "", responsable: str = "") -> str:
    return (f'{XML}<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            f"<Template>Normal.dotm</Template><TotalTime>95</TotalTime><Application>Microsoft Office Word</Application>"
            f"{'<Company>' + societe + '</Company>' if societe else ''}"
            f"{'<Manager>' + responsable + '</Manager>' if responsable else ''}</Properties>")


def settings(pieges: bool) -> str:
    if pieges:
        return (f'{XML}<w:settings xmlns:w="{W}" xmlns:r="{R}"><w:attachedTemplate r:id="rIdModele"/>'
                '<w:trackRevisions/><w:defaultTabStop w:val="708"/>'
                '<w:docVars><w:docVar w:name="ClientDossier" w:val="DURAND-2026-0123"/></w:docVars></w:settings>')
    return f'{XML}<w:settings xmlns:w="{W}" xmlns:r="{R}"><w:defaultTabStop w:val="708"/></w:settings>'


# Image JPEG minimale (1 x 1 pixel) précédée d'un segment EXIF fictif.
JPEG_EXIF = bytes.fromhex(
    "ffd8ffe1002245786966000049492a000800000001000f010200060000001a00000000000000"
    "000046494354494600"
    "ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720"
    "222c231c1c2837292c30313434341f27393d38323c2e333432ffc0000b080001000101011100ffc4001f0000"
    "010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d"
    "01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a2526272829"
    "2a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a"
    "92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3"
    "e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffda0008010100003f00fbd3ffd9")

DESSIN = ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="190500" cy="190500"/>'
          '<wp:docPr id="1" name="Photo chantier"/><a:graphic><a:graphicData '
          'uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr>'
          '<pic:cNvPr id="0" name="photo.jpeg"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill>'
          '<a:blip r:embed="rIdImage"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr>'
          '<a:xfrm><a:off x="0" y="0"/><a:ext cx="190500" cy="190500"/></a:xfrm><a:prstGeom prst="rect">'
          '<a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


def contrat_pieges() -> dict[str, str | bytes]:
    a1 = 'w:author="Anne Dupont (fictif)" w:date="2026-10-14T10:00:00Z"'
    a2 = 'w:author="Jean Martin (fictif)" w:date="2026-10-15T16:00:00Z"'
    corps = "".join([
        p(r("CONTRAT DE PRESTATION DE SERVICES"), style="Titre"),
        p(r("Entre la société Fictivia SRL, ci-après « le Prestataire », et la société Durand Fictif SA, "
            "ci-après « le Client », il est convenu ce qui suit.")),
        # Commentaire ancré sur l'article 7
        p('<w:commentRangeStart w:id="0"/>', r("Article 7. Responsabilité. La responsabilité du Prestataire est "
                                                "limitée au montant des honoraires perçus."),
          '<w:commentRangeEnd w:id="0"/><w:r><w:commentReference w:id="0"/></w:r>'),
        # Modifications suivies
        p(r("Article 8. Prix. Le prix forfaitaire s'élève à "),
          f'<w:del w:id="10" {a2}><w:r><w:delText>15.000 EUR</w:delText></w:r></w:del>',
          f'<w:ins w:id="11" {a2}>{r("18.000 EUR")}</w:ins>', r(" hors TVA.")),
        p(r("Article 9. Durée. Le contrat est conclu pour une durée d'un an.",
            f'<w:b/><w:rPrChange w:id="12" {a1}><w:rPr/></w:rPrChange>')),
        # Texte masqué, en blanc, minuscule
        p(r("Article 10. Confidentialité. Chaque partie garde confidentielles les informations reçues. "),
          r("Note interne : le client acceptera jusqu'à 20.000 EUR.", "<w:vanish/>")),
        p(r("Ne pas révéler la marge de négociation.", '<w:color w:val="FFFFFF"/>')),
        p(r("Dossier 2026-0123", '<w:sz w:val="2"/>')),
        p(r("Paragraphe de travail masqué par son style."), style="NoteInterne"),
        # Marqueurs à compléter et surlignage
        p(r("Article 11. Entrée en vigueur. Le présent contrat entre en vigueur le [●]. "
            "Signé à [À COMPLÉTER : lieu], le XXX.")),
        p(r("Article 12. Litiges. "), r("à revoir avec le client", '<w:highlight w:val="yellow"/>'),
          r(" Les tribunaux de Liège sont seuls compétents.")),
        # Champs révélateurs : complexe (FILENAME \p) et simple (AUTHOR)
        p(r("Référence du fichier : "), '<w:r><w:fldChar w:fldCharType="begin"/></w:r>',
          '<w:r><w:instrText xml:space="preserve"> FILENAME </w:instrText></w:r>',
          '<w:r><w:instrText xml:space="preserve">\\p </w:instrText></w:r>',
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r>',
          r("C:\\Dossiers\\Durand\\contrat v3.docx"), '<w:r><w:fldChar w:fldCharType="end"/></w:r>'),
        p(r("Rédigé par : "), f'<w:fldSimple w:instr=" AUTHOR "><w:r><w:t>Anne Dupont (fictif)</w:t></w:r></w:fldSimple>'),
        p(r("Page "), '<w:fldSimple w:instr=" PAGE "><w:r><w:t>1</w:t></w:r></w:fldSimple>'),
        # Liens : interne (SharePoint) et public
        p(r("Pièces : "), '<w:hyperlink r:id="rIdLienInterne">' + r("dossier partagé") + "</w:hyperlink>",
          r(" ; législation : "), '<w:hyperlink r:id="rIdLienPublic">' + r("Moniteur belge") + "</w:hyperlink>"),
        # Nom d'un autre dossier
        p(r("Modèle repris du contrat Autre-Client SA (ne pas diffuser).")),
        # Note de bas de page
        p(r("Annexe 1. Description des services."), '<w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr>'
          '<w:footnoteReference w:id="1"/></w:r>'),
        p(DESSIN),
        '<w:sectPr><w:headerReference w:type="default" r:id="rIdEntete"/>'
        '<w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1417" w:right="1417" w:bottom="1417" w:left="1417" w:header="708" w:footer="708" w:gutter="0"/>'
        '</w:sectPr>',
    ])
    document = f'{XML}<w:document {NSDOC}><w:body>{corps}</w:body></w:document>'
    commentaires = (f'{XML}<w:comments xmlns:w="{W}"><w:comment w:id="0" {a1} w:initials="AD">'
                    + p(r("Ne pas céder sur ce plafond : le client accepte jusqu'à 50.000 EUR.")) + "</w:comment></w:comments>")
    entete = (f'{XML}<w:hdr xmlns:w="{W}">' + p(r("Projet confidentiel – v3 – "),
              f'<w:ins w:id="20" {a1}>{r("relu par A. Dupont")}</w:ins>') + "</w:hdr>")
    notes = (f'{XML}<w:footnotes xmlns:w="{W}">'
             '<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>'
             '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
             '<w:footnote w:id="1">' + p(r("Voir le courriel interne du 3 octobre 2026.")) + "</w:footnote></w:footnotes>")
    personnes = (f'{XML}<w15:people xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml">'
                 '<w15:person w15:author="Anne Dupont (fictif)"><w15:presenceInfo w15:providerId="None" '
                 'w15:userId="Anne Dupont (fictif)"/></w15:person></w15:people>')
    custom = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
              'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
              '<property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="NumeroDossier">'
              '<vt:lpwstr>2026/0123-DURAND</vt:lpwstr></property></Properties>')
    return {
        "[Content_Types].xml": types({**DEFAUTS, "jpeg": "image/jpeg"}, {
            "word/document.xml": f"{CT_DOC}.document.main+xml",
            "word/styles.xml": f"{CT_DOC}.styles+xml",
            "word/settings.xml": f"{CT_DOC}.settings+xml",
            "word/comments.xml": f"{CT_DOC}.comments+xml",
            "word/header1.xml": f"{CT_DOC}.header+xml",
            "word/footnotes.xml": f"{CT_DOC}.footnotes+xml",
            "word/people.xml": f"{CT_DOC}.people+xml",
            "docProps/core.xml": "application/vnd.openxmlformats-package.core-properties+xml",
            "docProps/app.xml": "application/vnd.openxmlformats-officedocument.extended-properties+xml",
            "docProps/custom.xml": "application/vnd.openxmlformats-officedocument.custom-properties+xml",
        }),
        "_rels/.rels": rels([("rId1", T_DOC, "word/document.xml", False), ("rId2", T_CORE, "docProps/core.xml", False),
                             ("rId3", T_APP, "docProps/app.xml", False), ("rId4", T_CUSTOM, "docProps/custom.xml", False)]),
        "word/_rels/document.xml.rels": rels([
            ("rIdStyles", RT + "styles", "styles.xml", False),
            ("rIdSettings", RT + "settings", "settings.xml", False),
            ("rIdComments", RT + "comments", "comments.xml", False),
            ("rIdEntete", RT + "header", "header1.xml", False),
            ("rIdNotes", RT + "footnotes", "footnotes.xml", False),
            ("rIdPeople", "http://schemas.microsoft.com/office/2011/relationships/people", "people.xml", False),
            ("rIdImage", RT + "image", "media/image1.jpeg", False),
            ("rIdLienInterne", RT + "hyperlink", "https://cabinet-fictif.sharepoint.com/sites/dossiers/Durand", True),
            ("rIdLienPublic", RT + "hyperlink", "https://www.ejustice.just.fgov.be/", True),
        ]),
        "word/_rels/settings.xml.rels": rels([
            ("rIdModele", RT + "attachedTemplate", "file:///\\\\serveur-fictif\\Modeles\\Cabinet.dotm", True)]),
        "word/document.xml": document,
        "word/styles.xml": styles(True),
        "word/settings.xml": settings(True),
        "word/comments.xml": commentaires,
        "word/header1.xml": entete,
        "word/footnotes.xml": notes,
        "word/people.xml": personnes,
        "word/media/image1.jpeg": JPEG_EXIF,
        "docProps/core.xml": core("Anne Dupont (fictif)", "Stagiaire Cabinet Fictif", "Projet - Durand c/ Fictivia",
                                  "dossier 2026/0123", "14", "2026-10-15T08:00:00Z"),
        "docProps/app.xml": app("Cabinet Fictif SRL", "Associé fictif"),
        "docProps/custom.xml": custom,
    }


def contrat_propre() -> dict[str, str | bytes]:
    corps = "".join([
        p(r("CONTRAT DE PRESTATION DE SERVICES"), style="Titre"),
        p(r("Entre la société Fictivia SRL et la société Durand Fictif SA, il est convenu ce qui suit.")),
        p(r("Article 1. Objet. Le Prestataire fournit au Client les services décrits en annexe.")),
        p(r("Article 2. Prix. Le prix forfaitaire s'élève à 18.000 EUR hors TVA.")),
        p(r("Page "), '<w:fldSimple w:instr=" PAGE "><w:r><w:t>1</w:t></w:r></w:fldSimple>'),
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1417" w:bottom="1417" '
        'w:left="1417" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>',
    ])
    return {
        "[Content_Types].xml": types(DEFAUTS, {
            "word/document.xml": f"{CT_DOC}.document.main+xml",
            "word/styles.xml": f"{CT_DOC}.styles+xml",
            "word/settings.xml": f"{CT_DOC}.settings+xml",
            "docProps/core.xml": "application/vnd.openxmlformats-package.core-properties+xml",
            "docProps/app.xml": "application/vnd.openxmlformats-officedocument.extended-properties+xml",
        }),
        "_rels/.rels": rels([("rId1", T_DOC, "word/document.xml", False), ("rId2", T_CORE, "docProps/core.xml", False),
                             ("rId3", T_APP, "docProps/app.xml", False)]),
        "word/_rels/document.xml.rels": rels([("rIdStyles", RT + "styles", "styles.xml", False),
                                               ("rIdSettings", RT + "settings", "settings.xml", False)]),
        "word/document.xml": f'{XML}<w:document {NSDOC}><w:body>{corps}</w:body></w:document>',
        "word/styles.xml": styles(False),
        "word/settings.xml": settings(False),
        "docProps/core.xml": core("", ""),
        "docProps/app.xml": app(),
    }


def contrat_macros() -> dict[str, str | bytes]:
    parties = contrat_propre()
    parties["word/vbaProject.bin"] = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 56
    parties["word/embeddings/Feuille_de_calcul_Microsoft_Excel.xlsx"] = b"PK\x05\x06" + b"\x00" * 18
    parties["word/_rels/document.xml.rels"] = rels([
        ("rIdStyles", RT + "styles", "styles.xml", False), ("rIdSettings", RT + "settings", "settings.xml", False),
        ("rIdVba", "http://schemas.microsoft.com/office/2006/relationships/vbaProject", "vbaProject.bin", False),
        ("rIdObjet", RT + "package", "embeddings/Feuille_de_calcul_Microsoft_Excel.xlsx", False)])
    parties["[Content_Types].xml"] = types({**DEFAUTS, "bin": "application/vnd.ms-office.vbaProject",
                                            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}, {
        "word/document.xml": "application/vnd.ms-word.document.macroEnabled.main+xml",
        "word/styles.xml": f"{CT_DOC}.styles+xml", "word/settings.xml": f"{CT_DOC}.settings+xml",
        "docProps/core.xml": "application/vnd.openxmlformats-package.core-properties+xml",
        "docProps/app.xml": "application/vnd.openxmlformats-officedocument.extended-properties+xml"})
    return parties


PIECES = {
    "contrat-pieges.docx": contrat_pieges,
    "contrat-propre.docx": contrat_propre,
    "contrat-macros.docm": contrat_macros,
}


def generer(dossier: str) -> list[str]:
    os.makedirs(dossier, exist_ok=True)
    produits = []
    for nom, fabrique in PIECES.items():
        chemin = os.path.join(dossier, nom)
        ecrire_docx(chemin, fabrique())
        produits.append(chemin)
    # Pièces non lisibles : le contrôle doit conclure à l'impossibilité, jamais à l'absence de risque.
    chemin = os.path.join(dossier, "contrat-protege.docx")
    with open(chemin, "wb") as f:
        f.write(bytes.fromhex("D0CF11E0A1B11AE1") + b"\x00" * 504)
    produits.append(chemin)
    chemin = os.path.join(dossier, "contrat-tronque.docx")
    with open(os.path.join(dossier, "contrat-propre.docx"), "rb") as f:
        debut = f.read()[:400]
    with open(chemin, "wb") as f:
        f.write(debut)
    produits.append(chemin)
    return produits


if __name__ == "__main__":
    sortie = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "pieces")
    for chemin in generer(sortie):
        print(chemin)
