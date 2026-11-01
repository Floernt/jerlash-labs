"""Lecture du texte à pseudonymiser : fichier texte ou corps d'un document Word (.docx).

Pour un .docx, seul le corps du document est repris (paragraphes et tableaux, modifications
suivies acceptées). Les en-têtes, pieds de page, notes, commentaires et propriétés ne le sont pas :
ils ne figureront donc pas dans le texte pseudonymisé. Les protections reprennent celles de
l'outil Contrôle avant envoi : limites de taille et de compression, refus des déclarations XML.
"""

from __future__ import annotations

import io
import os
import zipfile
import xml.etree.ElementTree as ET
from xml.parsers import expat

from .detection import preparer

TAILLE_MAX_FICHIER = 50 * 1024 * 1024
TAILLE_MAX_PARTIE = 60 * 1024 * 1024
RATIO_MAX_COMPRESSION = 1000
NOMBRE_MAX_ENTREES = 5000
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
EXTENSIONS_TEXTE = (".txt", ".md", ".text")


class ErreurLecture(Exception):
    pass


def lire_fichier(chemin: str) -> str:
    extension = os.path.splitext(chemin)[1].lower()
    try:
        taille = os.path.getsize(chemin)
        if taille > TAILLE_MAX_FICHIER:
            raise ErreurLecture(f"Fichier trop volumineux ({taille // (1024 * 1024)} Mo ; maximum 50 Mo).")
        with open(chemin, "rb") as f:
            donnees = f.read()
    except OSError as e:
        raise ErreurLecture(f"Lecture impossible : {e.strerror or e}") from e
    if extension in (".docx", ".docm"):
        return texte_docx(donnees)
    if extension in EXTENSIONS_TEXTE:
        return texte_brut(donnees)
    raise ErreurLecture("Format non pris en charge : seuls les fichiers .txt, .md et .docx sont lus. "
                        "Pour un PDF ou un .doc, copiez le texte et collez-le dans la fenêtre.")


def texte_brut(donnees: bytes) -> str:
    if donnees.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        encodages = ("utf-32",)
    elif donnees.startswith((b"\xff\xfe", b"\xfe\xff")):
        encodages = ("utf-16",)
    else:
        encodages = ("utf-8-sig", "cp1252")
    for encodage in encodages:
        try:
            texte = donnees.decode(encodage)
        except UnicodeDecodeError:
            continue
        if "\x00" in texte:
            break
        return preparer(texte)
    # Un texte mal décodé ne contiendrait aucune donnée reconnaissable : il serait « pseudonymisé » sans
    # qu'aucun nom ne soit remplacé. Mieux vaut refuser.
    raise ErreurLecture("Encodage du fichier non reconnu : enregistrez-le en UTF-8, ou copiez le texte "
                        "et collez-le dans la fenêtre.")


def refuser_declarations(xml: bytes) -> None:
    """Un .docx légitime ne contient ni DOCTYPE ni entité : leur présence signale un fichier piégé."""
    analyseur = expat.ParserCreate()

    def refuser(*_args):
        raise ErreurLecture("Le document contient une déclaration XML (DOCTYPE ou entité) : fichier piégé, refusé.")

    analyseur.StartDoctypeDeclHandler = refuser
    analyseur.EntityDeclHandler = refuser
    try:
        analyseur.Parse(xml, True)
    except expat.ExpatError as e:
        raise ErreurLecture(f"Document Word endommagé ({e}).") from e


def texte_docx(donnees: bytes) -> str:
    if not donnees.startswith(b"PK\x03\x04"):
        raise ErreurLecture("Ce fichier n'est pas un document Word .docx valide (document protégé par mot de "
                            "passe, ancien format .doc ou fichier renommé).")
    try:
        with zipfile.ZipFile(io.BytesIO(donnees)) as z:
            infos = z.infolist()
            if len(infos) > NOMBRE_MAX_ENTREES:
                raise ErreurLecture("Archive anormale : trop d'éléments.")
            info = next((i for i in infos if i.filename.lower() == "word/document.xml"), None)
            if info is None:
                raise ErreurLecture("Document Word sans corps de texte (word/document.xml absent).")
            if info.file_size > TAILLE_MAX_PARTIE or (
                    info.compress_size and info.file_size / info.compress_size > RATIO_MAX_COMPRESSION):
                raise ErreurLecture("Archive anormale : taux de compression ou taille démesurés.")
            with z.open(info) as f:
                xml = f.read(TAILLE_MAX_PARTIE + 1)
            if len(xml) > TAILLE_MAX_PARTIE:
                raise ErreurLecture("Archive anormale : partie démesurée.")
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError) as e:
        raise ErreurLecture(f"Document Word illisible ({e}).") from e
    refuser_declarations(xml)
    racine = ET.fromstring(xml)
    if racine.tag != W + "document":
        raise ErreurLecture("Format Word non pris en charge (document au format strict ou inconnu).")
    corps = racine.find(W + "body")
    paragraphes = []
    for p in corps.iter(W + "p") if corps is not None else []:
        morceaux = []
        for el in p.iter():
            if el.tag == W + "t":
                morceaux.append(el.text or "")
            elif el.tag == W + "tab":
                morceaux.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                morceaux.append("\n")
        paragraphes.append("".join(morceaux))
    return preparer("\n".join(paragraphes))
