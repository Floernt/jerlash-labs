"""Garanties : pas de réseau, contrat intact, rapport jamais remplacé, entrées hostiles, rapport lisible."""

import io
import os
import pathlib
import shutil
import socket
import tempfile
import time
import unittest
import zipfile
from unittest import mock

import aide
from glossaire_definitions.__main__ import main as cli
from glossaire_definitions.analyse import analyser
from glossaire_definitions.lecture import Document, ErreurLecture, Paragraphe, lire_contrat
from glossaire_definitions.rapport import en_docx, en_json, en_markdown

CONTRAT = os.path.join(aide.PIECES, "Contrat de fourniture - Brasserie du Condroz.docx")


def interdit(*_a, **_k):
    raise AssertionError("tentative d'accès réseau")


def docx(document_xml: bytes, extra: dict | None = None) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", document_xml)
        for nom, contenu in (extra or {}).items():
            z.writestr(nom, contenu)
    return sortie.getvalue()


W = b'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>%s</w:body></w:document>'


class Garanties(unittest.TestCase):
    def test_parcours_complet_sans_reseau_et_contrat_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            contrat = shutil.copy(CONTRAT, tmp)
            avant = (pathlib.Path(contrat).read_bytes(), os.stat(contrat).st_mtime_ns)
            with mock.patch.object(socket.socket, "connect", interdit), \
                    mock.patch.object(socket, "create_connection", interdit), \
                    mock.patch.object(socket, "getaddrinfo", interdit):
                code = cli([contrat, "--sortie", os.path.join(tmp, "rapports")])
            self.assertEqual((pathlib.Path(contrat).read_bytes(), os.stat(contrat).st_mtime_ns), avant)
            self.assertEqual(code, 1)
            self.assertEqual(len(os.listdir(os.path.join(tmp, "rapports"))), 3)

    def test_aucun_rapport_remplace(self):
        with tempfile.TemporaryDirectory() as tmp:
            cli([CONTRAT, "--sortie", tmp])
            cli([CONTRAT, "--sortie", tmp])
            self.assertEqual(len(os.listdir(tmp)), 6)

    def test_liste_n_ecrit_rien(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch("glossaire_definitions.__main__.dossier_par_defaut",
                                                              return_value=os.path.join(tmp, "r")):
            cli([CONTRAT, "--liste"])
            self.assertFalse(os.path.exists(os.path.join(tmp, "r")))

    def test_aucun_module_reseau(self):
        self.assertEqual(aide.auditer_imports(aide.SRC), [])
        self.assertEqual(aide.auditer_imports(aide.OUTIL, recursif=False), [])

    def test_fichiers_hostiles_refuses_proprement(self):
        bombe = io.BytesIO()
        with zipfile.ZipFile(bombe, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("word/document.xml", b"<a>" + b" " * 50_000_000 + b"</a>")
        cas = {
            "entites.docx": docx(b'<?xml version="1.0"?><!DOCTYPE d [<!ENTITY a "aaaa">]><d>&a;</d>'),
            "bombe.docx": bombe.getvalue(),
            "faux.docx": b"ceci n'est pas un zip",
            "vide.docx": _sans_document(),
            "strict.docx": docx(b'<w:document xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main"/>'),
            "binaire.txt": b"abc\x00def",
            "contrat.pdf": b"%PDF-1.4",
        }
        with tempfile.TemporaryDirectory() as tmp:
            for nom, donnees in cas.items():
                chemin = os.path.join(tmp, nom)
                pathlib.Path(chemin).write_bytes(donnees)
                with self.subTest(nom):
                    debut = time.monotonic()
                    with self.assertRaises(ErreurLecture):
                        lire_contrat(chemin)
                    self.assertLess(time.monotonic() - debut, 5)
                    self.assertEqual(cli([chemin, "--liste"]), 2)

    def test_texte_masque_et_supprime_non_lus(self):
        corps = (b'<w:p><w:r><w:t xml:space="preserve">Article 1 \xe2\x80\x93 D\xc3\xa9finitions</w:t></w:r></w:p>'
                 b'<w:p><w:r><w:rPr><w:vanish/></w:rPr><w:t>\xc2\xab Cach\xc3\xa9 \xc2\xbb : masqu\xc3\xa9.</w:t></w:r></w:p>'
                 b'<w:p><w:del><w:r><w:delText>\xc2\xab Supprim\xc3\xa9 \xc2\xbb : supprim\xc3\xa9.</w:delText></w:r></w:del></w:p>'
                 b'<w:p><w:r><w:t>\xc2\xab Prix \xc2\xbb : le prix.</w:t></w:r></w:p>')
        with tempfile.TemporaryDirectory() as tmp:
            chemin = os.path.join(tmp, "c.docx")
            pathlib.Path(chemin).write_bytes(docx(W % corps))
            self.assertEqual([t.forme for t in analyser(lire_contrat(chemin)).termes], ["Prix"])

    def test_rapport_word_valide_malgre_caracteres_interdits(self):
        a = analyser(Document("c\x01\udcff.docx", [Paragraphe("Article 1 – Définitions"),
                                                   Paragraphe("« Prix\x0b » : le prix \x02.")]))
        donnees = en_docx(a)
        with zipfile.ZipFile(io.BytesIO(donnees)) as z:
            import xml.etree.ElementTree as ET
            ET.fromstring(z.read("word/document.xml"))
        en_markdown(a)
        en_json(a)

    def test_temps_borne_sur_texte_pathologique(self):
        paragraphes = [Paragraphe("Article 1 – Définitions")]
        paragraphes += [Paragraphe(f"« Terme Numéro {i} » : définition {i}.") for i in range(300)]
        paragraphes += [Paragraphe("le " + "Abc Def de " * 2000 + "fin")]
        paragraphes += [Paragraphe(" ".join(f"le Terme Numéro {i}" for i in range(300))) for _ in range(50)]
        debut = time.monotonic()
        analyser(Document("long.docx", paragraphes))
        self.assertLess(time.monotonic() - debut, 20)


def _sans_document() -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w") as z:
        z.writestr("autre.xml", b"<a/>")
    return sortie.getvalue()


if __name__ == "__main__":
    unittest.main()
