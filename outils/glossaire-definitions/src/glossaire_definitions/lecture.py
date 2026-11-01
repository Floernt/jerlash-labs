"""Lecture d'un contrat en lecture seule : .docx (corps du texte, tableaux compris), .txt et .md.

Le texte masqué et le texte supprimé en suivi des modifications ne sont pas lus : ils ne figurent pas
dans le contrat tel qu'il se lit. Les notes de bas de page, en-têtes et pieds de page ne sont pas lus
dans cette version. Protections reprises des autres outils : limites de taille et de compression,
refus des déclarations XML (entités, DOCTYPE).
"""

from __future__ import annotations

import io
import os
import re
import unicodedata
import zipfile
import zlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from xml.parsers import expat

TAILLE_MAX_FICHIER = 20 * 1024 * 1024
TAILLE_MAX_PARTIE = 15 * 1024 * 1024   # un contrat de 300 pages en fait moins de 5 ; borne la mémoire
RATIO_MAX_COMPRESSION = 1000
NOMBRE_MAX_ENTREES = 5000
NOMBRE_MAX_PARAGRAPHES = 20000
TAILLE_MAX_TEXTE = 2 * 1024 * 1024
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
# Non lus dans le paragraphe : variante de repli d'un objet, ancien emplacement d'un déplacement suivi,
# zone de texte (lue à part, comme un paragraphe distinct).
IGNORES = {FALLBACK, W + "moveFrom", W + "txbxContent"}
FORMATS = (".docx", ".txt", ".md")
# Espaces insécables et apostrophes typographiques remplacées caractère pour caractère :
# les positions restent les mêmes et les règles n'ont qu'une forme à reconnaître.
EQUIVALENTS = str.maketrans({" ": " ", " ": " ", " ": " ", " ": " ",
                             "’": "'", "ʼ": "'", "‘": "'"})


class ErreurLecture(Exception):
    pass


@dataclass
class Paragraphe:
    texte: str
    cellule: tuple[int, int, int] | None = None   # (tableau, rangée, colonne) si le paragraphe est dans un tableau
    titre: bool = False                            # style de titre Word, ou paragraphe numéroté automatiquement
    numerote: bool = False


@dataclass
class Document:
    nom: str
    paragraphes: list[Paragraphe]


def preparer(texte: str) -> str:
    return unicodedata.normalize("NFC", texte).translate(EQUIVALENTS)


def refuser_declarations(xml: bytes) -> None:
    analyseur = expat.ParserCreate()

    def refuser(*_args):
        raise ErreurLecture("déclaration XML (DOCTYPE ou entité) : fichier piégé, refusé")

    analyseur.StartDoctypeDeclHandler = refuser
    analyseur.EntityDeclHandler = refuser
    try:
        analyseur.Parse(xml, True)
    except expat.ExpatError as e:
        raise ErreurLecture(f"document Word endommagé ({e})") from e


def lire_partie(z: zipfile.ZipFile, nom: str) -> bytes | None:
    info = next((i for i in z.infolist() if i.filename.lower() == nom), None)
    if info is None:
        return None
    if info.file_size > TAILLE_MAX_PARTIE or (
            info.compress_size and info.file_size / info.compress_size > RATIO_MAX_COMPRESSION):
        raise ErreurLecture("archive anormale : taux de compression ou taille démesurés")
    with z.open(info) as f:
        donnees = f.read(TAILLE_MAX_PARTIE + 1)
    if len(donnees) > TAILLE_MAX_PARTIE:
        raise ErreurLecture("archive anormale : partie démesurée")
    refuser_declarations(donnees)
    return donnees


def masque(run: ET.Element) -> bool:
    v = run.find(f"{W}rPr/{W}vanish")
    return v is not None and v.get(f"{W}val", "true") not in ("0", "false", "off")


def runs(el: ET.Element):
    for enfant in el:
        if enfant.tag in IGNORES:
            continue
        if enfant.tag == W + "r":
            yield enfant
        else:
            yield from runs(enfant)


def zones_de_texte(el: ET.Element):
    for enfant in el:
        if enfant.tag == FALLBACK:
            continue
        if enfant.tag == W + "txbxContent":
            yield enfant
        else:
            yield from zones_de_texte(enfant)


def texte_paragraphe(p: ET.Element) -> str:
    morceaux = []
    for run in runs(p):
        if masque(run):
            continue
        for el in run:
            if el.tag == W + "t":
                morceaux.append(el.text or "")
            elif el.tag in (W + "tab", W + "br", W + "cr"):
                morceaux.append(" ")
            elif el.tag == W + "noBreakHyphen":
                morceaux.append("-")
    return "".join(morceaux)


class Lecteur:
    def __init__(self):
        self.paragraphes: list[Paragraphe] = []
        self.tableaux = 0
        self.taille = 0

    def ajouter(self, texte: str, cellule=None, titre=False, numerote=False) -> None:
        texte = preparer(texte)
        self.taille += len(texte)
        if len(self.paragraphes) >= NOMBRE_MAX_PARAGRAPHES or self.taille > TAILLE_MAX_TEXTE:
            raise ErreurLecture("document trop long pour cette version (plus de 20 000 paragraphes ou 2 millions de caractères)")
        self.paragraphes.append(Paragraphe(texte, cellule, titre, numerote))

    def parcourir(self, el: ET.Element, cellule=None) -> None:
        """Paragraphes dans l'ordre du document, chacun une seule fois ; la variante de repli
        (mc:Fallback) d'un objet n'est pas relue ; un tableau est lu rangée par rangée."""
        for enfant in el:
            if enfant.tag == W + "p":
                style = (enfant.find(f"{W}pPr/{W}pStyle") is not None
                         and re.search(r"heading|titre|title", enfant.find(f"{W}pPr/{W}pStyle").get(W + "val", ""), re.I))
                plan = enfant.find(f"{W}pPr/{W}outlineLvl") is not None
                self.ajouter(texte_paragraphe(enfant), cellule, bool(style or plan),
                             enfant.find(f"{W}pPr/{W}numPr") is not None)
                for zone in zones_de_texte(enfant):
                    self.parcourir(zone, cellule)
            elif enfant.tag == W + "tbl":
                numero = self.tableaux
                self.tableaux += 1
                for r, rangee in enumerate(enfant.findall(W + "tr")):
                    for c, case in enumerate(rangee.findall(W + "tc")):
                        self.parcourir(case, (numero, r, c))
            elif enfant.tag != FALLBACK:
                self.parcourir(enfant, cellule)


def lire_docx(donnees: bytes) -> list[Paragraphe]:
    if not donnees.startswith(b"PK\x03\x04"):
        raise ErreurLecture("pas un document .docx valide (protégé par mot de passe, ancien format ou fichier renommé)")
    try:
        with zipfile.ZipFile(io.BytesIO(donnees)) as z:
            if len(z.infolist()) > NOMBRE_MAX_ENTREES:
                raise ErreurLecture("archive anormale : trop d'éléments")
            document = lire_partie(z, "word/document.xml")
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error) as e:
        raise ErreurLecture(f"document Word illisible ({e})") from e
    if document is None:
        raise ErreurLecture("document Word sans corps de texte")
    racine = ET.fromstring(document)
    if racine.tag != W + "document":
        raise ErreurLecture("format Word non pris en charge (format strict ou inconnu)")
    lecteur = Lecteur()
    try:
        lecteur.parcourir(racine)
    except RecursionError as e:
        raise ErreurLecture("document Word anormal (imbrication excessive)") from e
    return lecteur.paragraphes


def lire_texte(donnees: bytes) -> list[Paragraphe]:
    """Une ligne par paragraphe. Les lignes « | a | b | » forment un tableau (Markdown)."""
    if donnees.startswith((b"\xff\xfe", b"\xfe\xff")):
        texte = donnees.decode("utf-16", errors="replace")
    else:
        try:
            texte = donnees.decode("utf-8-sig")
        except UnicodeDecodeError:
            texte = donnees.decode("cp1252", errors="replace")
    if "\x00" in texte:
        raise ErreurLecture("fichier binaire : ce n'est pas un texte")
    lecteur = Lecteur()
    rangee, tableau, dans_tableau = 0, -1, False
    for ligne in texte.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        brut = ligne.strip()
        if brut.startswith("|"):
            if not dans_tableau:
                tableau, rangee, dans_tableau = tableau + 1, 0, True
            cellules = [c.strip() for c in brut.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cellules):   # ligne de séparation Markdown
                continue
            for c, contenu in enumerate(cellules):
                lecteur.ajouter(contenu, (tableau, rangee, c))
            rangee += 1
        else:
            dans_tableau = False
            lecteur.ajouter(ligne)
    return lecteur.paragraphes


def lire_contrat(chemin: str) -> Document:
    extension = os.path.splitext(chemin)[1].lower()
    if extension not in FORMATS:
        raise ErreurLecture(f"format {extension or 'inconnu'} non pris en charge : enregistrez le contrat en .docx")
    if os.path.getsize(chemin) > TAILLE_MAX_FICHIER:
        raise ErreurLecture("fichier de plus de 20 Mo : trop volumineux pour un contrat")
    with open(chemin, "rb") as f:
        donnees = f.read(TAILLE_MAX_FICHIER + 1)
    try:
        paragraphes = lire_docx(donnees) if extension == ".docx" else lire_texte(donnees)
    except ET.ParseError as e:
        raise ErreurLecture(f"document Word endommagé ({e})") from e
    return Document(os.path.basename(chemin), paragraphes)
