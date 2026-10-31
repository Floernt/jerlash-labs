"""Lecture prudente d'un paquet .docx (OOXML), sans extraction sur disque.

Le fichier est lu une seule fois, en lecture seule, puis traité en mémoire.
Les limites ci-dessous protègent contre les archives piégées (bombes de
décompression, nombre d'entrées démesuré) et contre les déclarations XML
d'entités (DOCTYPE), qu'un .docx légitime ne contient pas.
"""

from __future__ import annotations

import hashlib
import io
import posixpath
import re
import zipfile
import zlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from xml.parsers import expat

TAILLE_MAX_FICHIER = 150 * 1024 * 1024
TAILLE_MAX_PARTIE = 60 * 1024 * 1024
TAILLE_MAX_TOTALE = 400 * 1024 * 1024
NOMBRE_MAX_ENTREES = 5000
# Un document légitime très répétitif atteint environ 300 (mesuré) ; une bombe de décompression dépasse 1 000.
RATIO_MAX_COMPRESSION = 1000

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
    "cust": "http://schemas.openxmlformats.org/officeDocument/2006/custom-properties",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
}
NS_STRICT_W = "http://purl.oclc.org/ooxml/wordprocessingml/main"

SIGNATURE_ZIP = b"PK\x03\x04"
SIGNATURE_CFB = bytes.fromhex("D0CF11E0A1B11AE1")


def q(prefixe: str, nom: str) -> str:
    """Nom qualifié ElementTree, par exemple q("w", "t") -> "{...}t"."""
    return "{%s}%s" % (NS[prefixe], nom)


class ErreurLecture(Exception):
    """Le fichier ne peut pas être analysé. Jamais transformée en résultat rassurant."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass
class Relation:
    source: str
    ident: str
    type: str
    cible: str
    externe: bool

    @property
    def type_court(self) -> str:
        return self.type.rsplit("/", 1)[-1]


@dataclass
class PaquetDocx:
    chemin: str
    taille: int
    sha256: str
    _zip: zipfile.ZipFile = field(repr=False)
    noms: list[str] = field(default_factory=list)
    _cache: dict = field(default_factory=dict, repr=False)

    # --- ouverture -------------------------------------------------------

    @classmethod
    def ouvrir(cls, chemin: str) -> "PaquetDocx":
        try:
            with open(chemin, "rb") as f:
                donnees = f.read(TAILLE_MAX_FICHIER + 1)
        except OSError as e:
            raise ErreurLecture("lecture", f"Le fichier n'a pas pu être lu : {e.strerror or e}.")
        if len(donnees) > TAILLE_MAX_FICHIER:
            raise ErreurLecture("taille", "Le fichier dépasse la taille maximale analysée (150 Mo).")
        return cls.depuis_octets(chemin, donnees)

    @classmethod
    def depuis_octets(cls, chemin: str, donnees: bytes) -> "PaquetDocx":
        empreinte = hashlib.sha256(donnees).hexdigest()
        if donnees.startswith(SIGNATURE_CFB):
            raise ErreurLecture(
                "protege",
                "Le fichier est un conteneur chiffré ou au format Word 97-2003. "
                "Un document protégé par mot de passe ne peut pas être contrôlé : "
                "retirez la protection sur une copie, ou enregistrez-le au format .docx.",
            )
        if not donnees.startswith(SIGNATURE_ZIP):
            raise ErreurLecture("format", "Le fichier n'est pas un document Word au format .docx.")
        try:
            archive = zipfile.ZipFile(io.BytesIO(donnees))
            infos = archive.infolist()
        except (zipfile.BadZipFile, ValueError, NotImplementedError) as e:
            raise ErreurLecture("corrompu", f"Le fichier .docx est endommagé ({e}).")
        if len(infos) > NOMBRE_MAX_ENTREES:
            raise ErreurLecture("archive", "Le fichier contient un nombre anormal d'éléments internes.")
        total = 0
        for info in infos:
            if info.flag_bits & 0x1:
                raise ErreurLecture("protege", "Une partie du fichier est chiffrée.")
            if info.file_size > TAILLE_MAX_PARTIE:
                raise ErreurLecture("archive", f"Élément interne trop volumineux : {info.filename}.")
            if info.compress_size and info.file_size / info.compress_size > RATIO_MAX_COMPRESSION:
                raise ErreurLecture("archive", f"Taux de compression anormal : {info.filename}.")
            total += info.file_size
        if total > TAILLE_MAX_TOTALE:
            raise ErreurLecture("archive", "Le contenu décompressé du fichier est anormalement volumineux.")
        paquet = cls(chemin=chemin, taille=len(donnees), sha256=empreinte, _zip=archive,
                     noms=[i.filename for i in infos])
        paquet._verifier_structure()
        return paquet

    def _verifier_structure(self) -> None:
        if "[Content_Types].xml" not in self.noms:
            raise ErreurLecture("format", "Le fichier n'est pas un paquet Office valide.")
        principal = self.partie_principale()
        if principal is None or principal not in self.noms:
            raise ErreurLecture("format", "Le fichier ne contient pas de document Word.")
        racine = self.xml(principal)
        if racine is not None and racine.tag.startswith("{%s}" % NS_STRICT_W):
            raise ErreurLecture(
                "strict",
                "Le document est enregistré au format « Open XML strict », qui n'est pas pris en charge. "
                "Enregistrez une copie au format « Document Word (.docx) » standard.",
            )

    # --- accès aux parties --------------------------------------------------

    def resoudre(self, nom: str) -> str | None:
        """Nom réel d'une partie, sans tenir compte de la casse (les relations ne la respectent pas toujours)."""
        if nom in self.noms:
            return nom
        bas = nom.lower()
        return next((n for n in self.noms if n.lower() == bas), None)

    def octets(self, nom: str) -> bytes | None:
        nom = self.resoudre(nom)
        if nom is None:
            return None
        try:
            with self._zip.open(nom) as f:
                donnees = f.read(TAILLE_MAX_PARTIE + 1)
        except (zipfile.BadZipFile, NotImplementedError, zlib.error, EOFError, OSError, RuntimeError) as e:
            raise ErreurLecture("corrompu", f"Élément interne illisible : {nom} ({e}).")
        if len(donnees) > TAILLE_MAX_PARTIE:
            raise ErreurLecture("archive", f"Élément interne trop volumineux : {nom}.")
        return donnees

    def xml(self, nom: str) -> ET.Element | None:
        if nom in self._cache:
            return self._cache[nom]
        brut = self.octets(nom)
        if brut is None:
            return None
        _refuser_declarations(nom, brut)
        try:
            racine = ET.fromstring(brut)
        except ET.ParseError as e:
            raise ErreurLecture("xml", f"Contenu XML illisible dans {nom} ({e}).")
        self._cache[nom] = racine
        return racine

    def parties_xml(self) -> list[str]:
        return [n for n in self.noms if n.lower().endswith((".xml", ".rels", ".psmdcp"))]

    def partie_paquet(self, type_court: str) -> str | None:
        """Partie déclarée au niveau du paquet (propriétés), quel que soit son chemin."""
        for rel in self.relations(""):
            if rel.type_court == type_court and not rel.externe and self.resoudre(rel.cible):
                return self.resoudre(rel.cible)
        return None

    def relations(self, partie: str) -> list[Relation]:
        """Relations déclarées par une partie ('' pour le paquet lui-même)."""
        dossier, nom = posixpath.split(partie)
        chemin_rels = posixpath.join(dossier, "_rels", nom + ".rels") if partie else "_rels/.rels"
        racine = self.xml(chemin_rels)
        if racine is None:
            return []
        resultat = []
        for el in racine.findall(q("rel", "Relationship")):
            externe = el.get("TargetMode", "") == "External"
            cible = el.get("Target", "")
            if not externe:
                cible = posixpath.normpath(posixpath.join(dossier, cible)).lstrip("/")
            resultat.append(Relation(partie, el.get("Id", ""), el.get("Type", ""), cible, externe))
        return resultat

    def fichiers_relations(self) -> list[str]:
        return [n for n in self.noms if n.endswith(".rels")]

    def partie_principale(self) -> str | None:
        for rel in self.relations(""):
            if rel.type.endswith("/officeDocument"):
                return self.resoudre(rel.cible) or rel.cible
        return "word/document.xml" if "word/document.xml" in self.noms else None

    def parties_texte(self) -> list[str]:
        """Parties contenant du texte rédigé : corps, en-têtes, pieds de page, notes, commentaires.

        Les parties de commentaires présentes dans l'archive mais non référencées sont incluses.
        """
        principal = self.partie_principale()
        parties = [principal] if principal else []
        for rel in self.relations(principal or ""):
            cible = None if rel.externe else self.resoudre(rel.cible)
            if cible and rel.type_court in ("header", "footer", "footnotes", "endnotes", "comments") \
                    and cible not in parties:
                parties.append(cible)
        for nom in self.parties_commentaires():
            if nom not in parties:
                parties.append(nom)
        return parties

    def parties_commentaires(self) -> list[str]:
        trouvees = []
        lie = self.partie_liee("comments")
        if lie:
            trouvees.append(lie)
        for nom in self.noms:
            if re.fullmatch(r"word/comments\d*\.xml", nom, re.IGNORECASE) and nom not in trouvees:
                trouvees.append(nom)
        return trouvees

    def partie_liee(self, type_court: str) -> str | None:
        principal = self.partie_principale() or ""
        for rel in self.relations(principal):
            if rel.type_court == type_court and not rel.externe and self.resoudre(rel.cible):
                return self.resoudre(rel.cible)
        return None


def libelle_partie(nom: str) -> str:
    base = posixpath.basename(nom)
    if base == "document.xml":
        return "Corps du document"
    if base.startswith("header"):
        return f"En-tête ({base})"
    if base.startswith("footer"):
        return f"Pied de page ({base})"
    if base == "footnotes.xml":
        return "Notes de bas de page"
    if base == "endnotes.xml":
        return "Notes de fin"
    if base == "comments.xml":
        return "Commentaires"
    if base == "settings.xml":
        return "Réglages du document"
    return nom


def _refuser_declarations(nom: str, brut: bytes) -> None:
    """Refuse toute déclaration DOCTYPE ou ENTITY, quel que soit l'encodage du document.

    Un .docx légitime n'en contient pas. L'analyse préalable passe par expat, qui détecte
    lui-même l'encodage (UTF-8, UTF-16…), ce qu'une recherche d'octets ne ferait pas.
    """
    def refuser(*_args):
        raise ErreurLecture("xml", f"Déclaration XML inattendue dans {nom} (fichier potentiellement piégé).")

    analyseur = expat.ParserCreate()
    analyseur.StartDoctypeDeclHandler = refuser
    analyseur.EntityDeclHandler = refuser
    try:
        analyseur.Parse(brut, True)
    except expat.ExpatError as e:
        raise ErreurLecture("xml", f"Contenu XML illisible dans {nom} ({e}).")


def texte_element(el: ET.Element) -> str:
    """Texte d'un élément : w:t, w:delText, w:instrText exclus, tabulations et sauts rendus en espace."""
    morceaux = []
    for sous in el.iter():
        if sous.tag in (q("w", "t"), q("w", "delText")):
            morceaux.append(sous.text or "")
        elif sous.tag in (q("w", "tab"), q("w", "br"), q("w", "cr")):
            morceaux.append(" ")
        elif sous.tag == q("w", "noBreakHyphen"):
            morceaux.append("-")
    return "".join(morceaux)


def extrait(texte: str, longueur: int = 160) -> str:
    texte = " ".join(texte.split())
    return texte if len(texte) <= longueur else texte[: longueur - 1] + "…"
