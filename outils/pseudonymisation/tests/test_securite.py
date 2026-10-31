"""Garanties de sécurité : pas de réseau, fichier d'origine intact, entrées hostiles refusées."""

import io
import os
import pathlib
import shutil
import socket
import tempfile
import unittest
import zipfile
from unittest import mock

import aide
from pseudonymisation.__main__ import main as cli
from pseudonymisation.lecture import ErreurLecture, lire_fichier

DOCX = os.path.join(aide.PIECES, "contrat-prestation.docx")


def interdit(*_a, **_k):
    raise AssertionError("tentative d'accès réseau")


class AucunAccesReseau(unittest.TestCase):
    def test_parcours_complet_sans_reseau(self):
        with tempfile.TemporaryDirectory() as dossier, \
                mock.patch.object(socket.socket, "connect", interdit), \
                mock.patch.object(socket, "create_connection", interdit), \
                mock.patch.object(socket, "getaddrinfo", interdit):
            self.assertEqual(cli(["pseudonymiser", DOCX, "--sortie", dossier]), 0)
            reponse = os.path.join(dossier, "reponse.txt")
            pathlib.Path(reponse).write_text("[PERSONNE_1] signe.", encoding="utf-8")
            table = os.path.join(dossier, "contrat-prestation - table.json")
            self.assertEqual(cli(["retablir", reponse, "--table", table, "--sortie", os.path.join(dossier, "r.txt")]), 0)
            self.assertEqual(pathlib.Path(dossier, "r.txt").read_text(encoding="utf-8"), "Julien Dethier signe.")

    def test_aucun_module_reseau_dans_le_code(self):
        self.assertEqual(aide.auditer_imports(aide.SRC), [])
        self.assertEqual(aide.auditer_imports(aide.OUTIL, recursif=False), [])  # lanceur .pyw

    def test_l_audit_detecte_un_import_reseau_plante(self):
        with tempfile.TemporaryDirectory() as dossier:
            with open(os.path.join(dossier, "piege.py"), "w", encoding="utf-8") as f:
                f.write("import urllib.request\nfrom socket import create_connection\nimport webbrowser\n")
            self.assertEqual(len(aide.auditer_imports(dossier)), 3)


class FichierOrigineIntact(unittest.TestCase):
    def test_octets_et_date_inchanges(self):
        with tempfile.TemporaryDirectory() as dossier:
            copie = os.path.join(dossier, "copie.docx")
            shutil.copy2(DOCX, copie)
            avant = (pathlib.Path(copie).read_bytes(), os.stat(copie).st_mtime_ns)
            cli(["pseudonymiser", copie, "--sortie", dossier])
            cli(["pseudonymiser", copie, "--sortie", dossier])
            apres = (pathlib.Path(copie).read_bytes(), os.stat(copie).st_mtime_ns)
        self.assertEqual(avant, apres)


def docx_avec(parties: dict) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(DOCX) as source, zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for info in source.infolist():
            if info.filename not in parties:
                z.writestr(info, source.read(info.filename))
        for nom, contenu in parties.items():
            if contenu is not None:
                z.writestr(nom, contenu)
    return sortie.getvalue()


class EntreesHostiles(unittest.TestCase):
    def lire_octets(self, donnees: bytes, nom="test.docx"):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, nom)
            with open(chemin, "wb") as f:
                f.write(donnees)
            return lire_fichier(chemin)

    def test_declaration_d_entite_refusee(self):
        xxe = ('<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e SYSTEM "file:///c:/windows/win.ini">]>'
               '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               '<w:body><w:p><w:r><w:t>&e;</w:t></w:r></w:p></w:body></w:document>')
        with self.assertRaisesRegex(ErreurLecture, "piégé"):
            self.lire_octets(docx_avec({"word/document.xml": xxe}))

    def test_bombe_de_decompression(self):
        corps = ('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
                 + " " * (20 * 1024 * 1024) + '</w:body></w:document>')
        with self.assertRaisesRegex(ErreurLecture, "anormale"):
            self.lire_octets(docx_avec({"word/document.xml": corps}))

    def test_fichier_texte_renomme(self):
        with self.assertRaises(ErreurLecture):
            self.lire_octets(b"Ceci n'est pas un document Word.")

    def test_archive_sans_document(self):
        with self.assertRaises(ErreurLecture):
            self.lire_octets(docx_avec({"word/document.xml": None}))

    def test_format_non_pris_en_charge(self):
        with self.assertRaisesRegex(ErreurLecture, "non pris en charge"):
            self.lire_octets(b"%PDF-1.7", nom="piece.pdf")

    def test_texte_ancien_encodage(self):
        self.assertEqual(self.lire_octets("Liège".encode("cp1252"), nom="a.txt"), "Liège")


class LectureDocx(unittest.TestCase):
    def test_texte_supprime_ignore_texte_insere_repris(self):
        corps = ('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p>'
                 '<w:r><w:t xml:space="preserve">M. </w:t></w:r><w:del><w:r><w:delText>Jean Ancien</w:delText></w:r></w:del>'
                 '<w:ins><w:r><w:t>Paul Nouveau</w:t></w:r></w:ins></w:p></w:body></w:document>')
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "x.docx")
            with open(chemin, "wb") as f:
                f.write(docx_avec({"word/document.xml": corps}))
            self.assertEqual(lire_fichier(chemin), "M. Paul Nouveau")


if __name__ == "__main__":
    unittest.main()
