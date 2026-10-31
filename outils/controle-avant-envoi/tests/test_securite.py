"""Garanties de sécurité : pas de réseau, pas d'écriture du fichier, entrées hostiles, rapport inoffensif."""

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
from controle_avant_envoi.__main__ import main as cli
from controle_avant_envoi.analyse import analyser, charger_configuration
from controle_avant_envoi.rapport import en_html, en_json, en_texte

PIEGES = os.path.join(aide.PIECES, "contrat-pieges.docx")


def interdit(*_a, **_k):
    raise AssertionError("tentative d'accès réseau")


class AucunAccesReseau(unittest.TestCase):
    def test_analyse_et_rapports_sans_reseau(self):
        with mock.patch.object(socket.socket, "connect", interdit), \
                mock.patch.object(socket, "create_connection", interdit), \
                mock.patch.object(socket, "getaddrinfo", interdit):
            cfg = charger_configuration()
            cfg["termes_sensibles"] = ["Durand"]
            rapport = analyser(PIEGES, cfg)
            en_html(rapport), en_json(rapport), en_texte(rapport)
        self.assertEqual(rapport.niveau, "a_traiter")

    def test_aucun_module_reseau_dans_le_code(self):
        self.assertEqual(aide.auditer_imports(aide.SRC), [])

    def test_l_audit_detecte_un_import_reseau_plante(self):
        with tempfile.TemporaryDirectory() as dossier:
            with open(os.path.join(dossier, "piege.py"), "w", encoding="utf-8") as f:
                f.write("import urllib.request\nfrom socket import create_connection\n__import__('ssl')\n")
            violations = aide.auditer_imports(dossier)
        self.assertEqual(len(violations), 3, violations)


class FichierNonModifie(unittest.TestCase):
    def test_octets_et_date_inchanges(self):
        with tempfile.TemporaryDirectory() as dossier:
            copie = os.path.join(dossier, "copie.docx")
            shutil.copy2(PIEGES, copie)
            avant = (pathlib.Path(copie).read_bytes(), os.stat(copie).st_mtime_ns)
            rapport = analyser(copie)
            cli([copie, "--html", dossier, "--json", dossier, "--silencieux"])
            apres = (pathlib.Path(copie).read_bytes(), os.stat(copie).st_mtime_ns)
        self.assertEqual(avant, apres)
        self.assertTrue(rapport.integre)


def docx_avec(parties: dict, base: str = os.path.join(aide.PIECES, "contrat-propre.docx")) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(base) as source, zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for info in source.infolist():
            if info.filename not in parties:
                z.writestr(info, source.read(info.filename))
        for nom, contenu in parties.items():
            if contenu is not None:
                z.writestr(nom, contenu)
    return sortie.getvalue()


class EntreesHostiles(unittest.TestCase):
    def analyser_octets(self, donnees: bytes, nom="test.docx"):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, nom)
            with open(chemin, "wb") as f:
                f.write(donnees)
            return analyser(chemin)

    def test_declaration_d_entite_refusee(self):
        xxe = ('<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e SYSTEM "file:///c:/windows/win.ini">]>'
               '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               '<w:body><w:p><w:r><w:t>&e;</w:t></w:r></w:p></w:body></w:document>')
        rapport = self.analyser_octets(docx_avec({"word/document.xml": xxe}))
        self.assertEqual(rapport.niveau, "erreur")
        self.assertIn("piégé", rapport.erreur)

    def test_entite_dans_une_partie_secondaire_donne_un_controle_en_erreur(self):
        rapport = self.analyser_octets(docx_avec({"docProps/core.xml": '<!DOCTYPE a [<!ENTITY b "c">]><a/>'}))
        self.assertEqual(rapport.niveau, "incomplet")
        self.assertIn("incomplète", rapport.verdict)
        self.assertNotEqual(rapport.code_sortie, 0)

    def test_bombe_de_decompression(self):
        # Ratio de compression anormal (zéros : environ 1 000 pour 1).
        rapport = self.analyser_octets(docx_avec({"word/media/bombe.png": b"\x00" * (20 * 1024 * 1024)}))
        self.assertEqual(rapport.niveau, "erreur")
        # Partie au-delà de la taille maximale, quel que soit son taux de compression.
        aleatoire = os.urandom(1024 * 1024) * 61
        rapport = self.analyser_octets(docx_avec({"word/media/grande.png": aleatoire}))
        self.assertEqual(rapport.niveau, "erreur")

    def test_trop_d_elements(self):
        sortie = io.BytesIO()
        with zipfile.ZipFile(sortie, "w") as z:
            for i in range(5001):
                z.writestr(f"x/{i}", b"")
        self.assertEqual(self.analyser_octets(sortie.getvalue()).niveau, "erreur")

    def test_format_strict_non_pris_en_charge(self):
        strict = ('<w:document xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main"><w:body/></w:document>')
        rapport = self.analyser_octets(docx_avec({"word/document.xml": strict}))
        self.assertEqual(rapport.niveau, "erreur")
        self.assertIn("strict", rapport.erreur)

    def test_fichier_texte_renomme(self):
        self.assertEqual(self.analyser_octets(b"Ceci n'est pas un document Word.").niveau, "erreur")

    def test_archive_sans_document(self):
        self.assertEqual(self.analyser_octets(docx_avec({"word/document.xml": None})).niveau, "erreur")

    def test_fichier_absent(self):
        rapport = analyser(os.path.join(tempfile.gettempdir(), "inexistant-iavocat.docx"))
        self.assertEqual(rapport.niveau, "erreur")


class RapportInoffensif(unittest.TestCase):
    def test_contenu_du_document_echappe_dans_le_html(self):
        commentaire = ('<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                       '<w:comment w:id="0" w:author="&lt;script&gt;alert(1)&lt;/script&gt;"><w:p><w:r>'
                       '<w:t>&lt;img src=x onerror=alert(2)&gt;</w:t></w:r></w:p></w:comment></w:comments>')
        rels = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="a" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                '<Relationship Id="b" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>'
                '</Relationships>')
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "x.docx")
            with open(chemin, "wb") as f:
                f.write(docx_avec({"word/comments.xml": commentaire, "word/_rels/document.xml.rels": rels}))
            html = en_html(analyser(chemin))
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("default-src 'none'", html)


if __name__ == "__main__":
    unittest.main()
