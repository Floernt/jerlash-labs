"""Génère le dossier fictif F-DOSSIER-01 à partir de sources/.

    python -I factory/jeux-de-test/F-DOSSIER-01/generer.py             régénère pieces/
    python -I factory/jeux-de-test/F-DOSSIER-01/generer.py --verifier  échoue si pieces/ diffère des sources

Chaque source commence par un en-tête (« fichier: », « auteur: », pour un courriel « de: », « a: »,
« date: », « objet: »), puis « --- » et le texte. L'extension du nom de fichier choisit le format :
.docx (avec propriétés du document), .eml (courriel), .txt. S'y ajoute un PDF sans couche texte,
comme un scan, que l'outil doit signaler comme non lu. Toutes les personnes et sociétés sont fictives.
"""

from __future__ import annotations

import io
import os
import sys
import zipfile
from email.message import EmailMessage
from email.policy import SMTP
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(ICI, "sources")
PIECES = os.path.join(ICI, "pieces")
# Dossier de contrôle : rédigé à part, sans accès à l'outil ; sert seulement à mesurer.
SOURCES_CONTROLE = os.path.join(ICI, "sources-controle")
PIECES_CONTROLE = os.path.join(ICI, "pieces-controle")
DATE_ZIP = (2026, 1, 1, 0, 0, 0)
SCAN = "Scan contrat signé 2023.pdf"


def lire_source(chemin: str) -> tuple[dict, str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().replace("\r\n", "\n")
    entete, texte = brut.split("\n---\n", 1)
    meta = dict(ligne.split(": ", 1) for ligne in entete.splitlines() if ligne.strip())
    return meta, texte


def docx(texte: str, auteur: str) -> bytes:
    paragraphes = "".join(
        f'<w:p><w:r><w:t xml:space="preserve">{escape(ligne)}</w:t></w:r></w:p>' if ligne else "<w:p/>"
        for ligne in texte.rstrip("\n").split("\n"))
    parties = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
            'Target="docProps/core.xml"/></Relationships>'),
        "docProps/core.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            f'<dc:creator>{escape(auteur)}</dc:creator></cp:coreProperties>'),
        "word/document.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{paragraphes}<w:sectPr/></w:body></w:document>'),
    }
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in parties.items():
            info = zipfile.ZipInfo(nom, DATE_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, contenu.encode("utf-8"))
    return sortie.getvalue()


def eml(meta: dict, texte: str) -> bytes:
    message = EmailMessage(policy=SMTP)
    message["From"] = meta["de"]
    message["To"] = meta["a"]
    message["Date"] = meta["date"]
    message["Subject"] = meta["objet"]
    # Identifiant déterministe (la date suffit à distinguer les courriels du jeu).
    message["Message-ID"] = f"<{meta['date'].replace(' ', '').replace(',', '').replace(':', '')}@f-dossier-01.example>"
    message.set_content(texte)
    return bytes(message)


def pdf_sans_texte() -> bytes:
    """PDF d'une page qui ne contient qu'un rectangle gris : aucune couche texte, comme un scan."""
    objets = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << >> >>",
    ]
    flux = b"0.8 g 50 50 495 742 re f"
    objets.append(b"<< /Length %d >>\nstream\n" % len(flux) + flux + b"\nendstream")
    sortie = io.BytesIO()
    sortie.write(b"%PDF-1.4\n")
    positions = []
    for i, objet in enumerate(objets, start=1):
        positions.append(sortie.tell())
        sortie.write(b"%d 0 obj\n" % i + objet + b"\nendobj\n")
    xref = sortie.tell()
    sortie.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objets) + 1))
    for p in positions:
        sortie.write(b"%010d 00000 n \n" % p)
    sortie.write(b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objets) + 1, xref))
    return sortie.getvalue()


def produire() -> dict[str, bytes]:
    fichiers = {os.path.join(PIECES, SCAN): pdf_sans_texte()}
    for sources, pieces in ((SOURCES, PIECES), (SOURCES_CONTROLE, PIECES_CONTROLE)):
        if not os.path.isdir(sources):
            continue
        for nom in sorted(os.listdir(sources)):
            meta, texte = lire_source(os.path.join(sources, nom))
            cible = os.path.join(pieces, meta["fichier"])
            if cible.endswith(".docx"):
                fichiers[cible] = docx(texte, meta.get("auteur", ""))
            elif cible.endswith(".eml"):
                fichiers[cible] = eml(meta, texte)
            elif cible.endswith(".pdf"):
                fichiers[cible] = pdf_sans_texte()
            else:
                fichiers[cible] = texte.encode("utf-8")
    return fichiers


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    verifier = "--verifier" in (argv if argv is not None else sys.argv[1:])
    attendus = produire()
    ecarts = 0
    if verifier:
        for pieces in (PIECES, PIECES_CONTROLE):
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
