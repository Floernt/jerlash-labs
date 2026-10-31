"""Lecture des pièces d'un dossier, en lecture seule.

Formats lus : .docx (corps du texte et propriétés), .eml (en-têtes, texte, noms des pièces jointes),
.txt et .md. Les autres formats (PDF, .doc, .msg, tableurs, images) sont inventoriés mais signalés
« non lus » : l'outil ne devine jamais le contenu d'une pièce qu'il n'a pas lue.
Protections reprises des autres outils : limites de taille et de compression, refus des déclarations XML.
"""

from __future__ import annotations

import datetime
import hashlib
import io
import os
import stat
import unicodedata
import zipfile
import zlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from xml.parsers import expat

TAILLE_MAX_FICHIER = 50 * 1024 * 1024
TAILLE_MAX_PARTIE = 60 * 1024 * 1024
RATIO_MAX_COMPRESSION = 1000
NOMBRE_MAX_ENTREES = 5000
NOMBRE_MAX_PIECES = 2000
TAILLE_MAX_TEXTE = 2 * 1024 * 1024   # caractères retenus par pièce : les règles n'ont pas besoin de plus
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CP = {"cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
      "dc": "http://purl.org/dc/elements/1.1/", "dcterms": "http://purl.org/dc/terms/"}
RAISONS_NON_LU = {
    ".pdf": "PDF : non lu dans cette version (le texte d'un PDF ne peut pas être extrait sans bibliothèque tierce)",
    ".doc": "ancien format Word (.doc) : à enregistrer en .docx",
    ".msg": "courriel Outlook (.msg) : à enregistrer en .eml",
    ".odt": "format OpenDocument : à enregistrer en .docx",
}


class ErreurLecture(Exception):
    pass


@dataclass
class Piece:
    chemin: str                     # chemin relatif au dossier inventorié
    format: str
    taille: int
    sha256: str
    modifie_le: str                 # date du fichier sur le disque
    texte: str | None = None        # None : pièce non lue
    non_lu: str = ""                # raison, si la pièce n'est pas lue
    auteur: str = ""                # propriété « auteur » du .docx ou expéditeur du courriel
    modifie_par: str = ""
    cree_le: str = ""               # propriété du document
    courriel: dict = field(default_factory=dict)   # de, a, date, objet, pieces_jointes
    tronque: bool = False           # texte limité à TAILLE_MAX_TEXTE caractères

    @property
    def nom(self) -> str:
        return os.path.basename(self.chemin)


def preparer(texte: str) -> str:
    return unicodedata.normalize("NFC", texte.replace("\r\n", "\n"))


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


FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"


def masque(run: ET.Element) -> bool:
    """Texte masqué (w:vanish) : invisible dans Word, il ne doit pas servir d'indice (« (signé) » caché…)."""
    v = run.find(f"{W}rPr/{W}vanish")
    return v is not None and v.get(f"{W}val", "true") not in ("0", "false", "off")


def texte_paragraphe(p: ET.Element) -> str:
    morceaux = []
    for run in p.iter(W + "r"):
        if masque(run):
            continue
        for el in run:
            if el.tag == W + "t":
                morceaux.append(el.text or "")
            elif el.tag == W + "tab":
                morceaux.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                morceaux.append("\n")
    return "".join(morceaux)


def parcourir(el: ET.Element, paragraphes: list[str]) -> None:
    """Paragraphes dans l'ordre du document, chacun une seule fois : une zone de texte incluse dans un
    paragraphe est lue avec lui, et la variante de repli (mc:Fallback) d'un objet n'est pas relue."""
    for enfant in el:
        if enfant.tag == W + "p":
            paragraphes.append(texte_paragraphe(enfant))
        elif enfant.tag != FALLBACK:
            parcourir(enfant, paragraphes)


def lire_docx(donnees: bytes, piece: Piece) -> None:
    if not donnees.startswith(b"PK\x03\x04"):
        raise ErreurLecture("pas un document .docx valide (protégé par mot de passe, ancien format ou fichier renommé)")
    try:
        with zipfile.ZipFile(io.BytesIO(donnees)) as z:
            if len(z.infolist()) > NOMBRE_MAX_ENTREES:
                raise ErreurLecture("archive anormale : trop d'éléments")
            document = lire_partie(z, "word/document.xml")
            proprietes = lire_partie(z, "docprops/core.xml")
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error) as e:
        raise ErreurLecture(f"document Word illisible ({e})") from e
    if document is None:
        raise ErreurLecture("document Word sans corps de texte")
    racine = ET.fromstring(document)
    if racine.tag != W + "document":
        raise ErreurLecture("format Word non pris en charge (format strict ou inconnu)")
    paragraphes: list[str] = []
    parcourir(racine, paragraphes)
    piece.texte = preparer("\n".join(paragraphes))
    if proprietes:
        core = ET.fromstring(proprietes)
        piece.auteur = (core.findtext("dc:creator", "", CP) or "").strip()
        piece.modifie_par = (core.findtext("cp:lastModifiedBy", "", CP) or "").strip()
        piece.cree_le = (core.findtext("dcterms:created", "", CP) or "").strip()[:10]


class TexteHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.morceaux = []

    def handle_data(self, data):
        self.morceaux.append(data)


def lire_eml(donnees: bytes, piece: Piece) -> None:
    message = BytesParser(policy=policy.default).parsebytes(donnees)
    corps = message.get_body(preferencelist=("plain", "html"))
    texte = ""
    if corps is not None:
        texte = corps.get_content()
        if corps.get_content_type() == "text/html":
            analyseur = TexteHTML()
            analyseur.feed(texte)
            texte = "".join(analyseur.morceaux)
    date = ""
    if message["Date"]:
        try:
            date = parsedate_to_datetime(str(message["Date"])).date().isoformat()
        except (TypeError, ValueError):
            date = ""
    piece.courriel = {"de": str(message["From"] or ""), "a": str(message["To"] or ""), "date": date,
                      "objet": str(message["Subject"] or ""),
                      "pieces_jointes": [p.get_filename() or "(sans nom)" for p in message.iter_attachments()]}
    piece.auteur = piece.courriel["de"]
    piece.texte = preparer(f"Objet : {piece.courriel['objet']}\n\n{texte}")


def lire_texte(donnees: bytes, piece: Piece) -> None:
    encodages = ("utf-16",) if donnees.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "cp1252")
    for encodage in encodages:
        try:
            texte = donnees.decode(encodage)
        except UnicodeDecodeError:
            continue
        if "\x00" not in texte:
            piece.texte = preparer(texte)
            return
    raise ErreurLecture("encodage du fichier non reconnu")


LECTEURS = {".docx": lire_docx, ".docm": lire_docx, ".eml": lire_eml, ".txt": lire_texte, ".md": lire_texte}


def ignorer(nom: str) -> bool:
    """Fichiers techniques à ne pas inventorier : verrous de Word, fichiers cachés du système."""
    return nom.startswith(("~$", ".")) or nom.lower() in ("thumbs.db", "desktop.ini")


def lire_piece(dossier: str, chemin: str) -> Piece:
    """Une pièce ; ne lève jamais d'exception : un fichier inaccessible ou corrompu devient « non lu »."""
    complet = os.path.join(dossier, chemin)
    extension = os.path.splitext(chemin)[1].lower()
    try:
        taille = os.path.getsize(complet)
        modifie = datetime.datetime.fromtimestamp(os.path.getmtime(complet)).date().isoformat()
        if taille > TAILLE_MAX_FICHIER:
            return Piece(chemin, extension, taille, "", modifie, non_lu="fichier trop volumineux (plus de 50 Mo)")
        with open(complet, "rb") as f:
            donnees = f.read()
    except OSError as e:
        return Piece(chemin, extension, 0, "", "", non_lu=f"inaccessible : {e.strerror or e}")
    piece = Piece(chemin, extension, taille, hashlib.sha256(donnees).hexdigest(), modifie)
    lecteur = LECTEURS.get(extension)
    if lecteur is None:
        piece.non_lu = RAISONS_NON_LU.get(extension, f"format {extension or 'sans extension'} non lu")
        return piece
    try:
        lecteur(donnees, piece)
    except Exception as e:  # toute pièce malformée devient « non lue », sans arrêter l'inventaire
        piece.texte = None
        piece.non_lu = f"illisible : {e}"
    if piece.texte is not None and len(piece.texte) > TAILLE_MAX_TEXTE:
        piece.texte = piece.texte[:TAILLE_MAX_TEXTE]
        piece.tronque = True
    return piece


def est_un_lien(chemin: str) -> bool:
    """Lien symbolique ou jonction Windows : suivre l'un ou l'autre ferait lire hors du dossier."""
    if os.path.islink(chemin) or (hasattr(os.path, "isjunction") and os.path.isjunction(chemin)):
        return True
    try:
        return bool(getattr(os.lstat(chemin), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
    except OSError:
        return False


def lire_dossier(dossier: str) -> tuple[list[Piece], list[str]]:
    """Toutes les pièces du dossier et de ses sous-dossiers, triées par chemin ; et ce qui n'a pas été
    inventorié (fichiers techniques, dossiers cachés, liens, dossiers illisibles), avec la raison."""
    if not os.path.isdir(dossier):
        raise ErreurLecture(f"dossier introuvable : {dossier}")
    chemins, ignores = [], []

    def erreur(e: OSError) -> None:
        ignores.append(f"{os.path.relpath(e.filename or dossier, dossier)} (dossier illisible : {e.strerror or e})")

    for racine, dossiers, fichiers in os.walk(dossier, onerror=erreur, followlinks=False):
        gardes = []
        for d in sorted(dossiers):
            relatif = os.path.relpath(os.path.join(racine, d), dossier)
            if d.startswith("."):
                ignores.append(f"{relatif}{os.sep} (dossier caché)")
            elif est_un_lien(os.path.join(racine, d)):
                ignores.append(f"{relatif}{os.sep} (lien ou jonction vers un autre emplacement, non suivi)")
            else:
                gardes.append(d)
        dossiers[:] = gardes
        for nom in sorted(fichiers):
            relatif = os.path.relpath(os.path.join(racine, nom), dossier)
            if ignorer(nom):
                ignores.append(f"{relatif} (fichier technique)")
            elif est_un_lien(os.path.join(racine, nom)):
                ignores.append(f"{relatif} (lien vers un autre emplacement, non suivi)")
            else:
                chemins.append(relatif)
    if len(chemins) > NOMBRE_MAX_PIECES:
        raise ErreurLecture(f"{len(chemins)} fichiers : au-delà de {NOMBRE_MAX_PIECES}, découpez le dossier")
    return [lire_piece(dossier, c) for c in chemins], ignores
