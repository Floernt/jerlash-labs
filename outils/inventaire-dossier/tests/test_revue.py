"""Défauts relevés par la relecture indépendante du 2026-10-31 : un test par défaut corrigé."""

import io
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
import xml.etree.ElementTree as ET
from email.message import EmailMessage
from unittest import mock

import aide
from inventaire_dossier.__main__ import main as cli
from inventaire_dossier.analyse import inventorier
from inventaire_dossier.lecture import Piece, lire_dossier
from inventaire_dossier.rapport import en_docx

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def piece(nom, texte, format_=".docx", courriel=None):
    return Piece(nom, format_, len(texte), nom, "2026-10-31", texte=texte, courriel=courriel or {})


def une(nom, texte, **k):
    return inventorier(".", [piece(nom, texte, **k)], []).fiches[0]


def docx(corps_xml: str) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", f'<w:document xmlns:w="{W}"><w:body>{corps_xml}</w:body></w:document>')
    return sortie.getvalue()


class SortieHorsDuDossier(unittest.TestCase):
    """B1 : le registre ne peut pas aboutir dans le dossier inventorié, quel que soit le chemin."""

    def setUp(self):
        self.tmp = self.enterContext(tempfile.TemporaryDirectory())
        self.dossier = os.path.join(self.tmp, "Dossier Client")
        os.makedirs(self.dossier)
        pathlib.Path(self.dossier, "piece.txt").write_text("Note", encoding="utf-8")

    def contenu(self):
        return sorted(os.listdir(self.dossier))

    @unittest.skipUnless(sys.platform == "win32", "casse indifférente : Windows")
    def test_autre_casse(self):
        self.assertEqual(cli([self.dossier, "--sortie", os.path.join(self.tmp, "dossier client", "registres")]), 2)
        self.assertEqual(self.contenu(), ["piece.txt"])

    @unittest.skipUnless(sys.platform == "win32", "jonction : Windows")
    def test_jonction_vers_le_dossier(self):
        lien = os.path.join(self.tmp, "raccourci")
        subprocess.run(["cmd", "/c", "mklink", "/J", lien, self.dossier], check=True, capture_output=True)
        self.assertEqual(cli([self.dossier, "--sortie", lien]), 2)
        self.assertEqual(cli([self.dossier, "--sortie", os.path.join(lien, "sous")]), 2)
        self.assertEqual(self.contenu(), ["piece.txt"])


class SignatureEtFaitFoi(unittest.TestCase):
    """B2 : « signé » et « fait foi » jamais tirés d'indices contraires ou trop faibles."""

    def test_non_signe_dans_le_nom(self):
        f = une("Contrat de bail - NON signé.docx", "CONTRAT DE BAIL\nEntre Alpha SRL et Beta SA.")
        self.assertNotEqual(f.statut, "signé")
        self.assertIsNot(f.fait_foi, True)

    def test_verbe_signer(self):
        self.assertNotEqual(une("Contrat que le client signe demain.docx", "CONTRAT\nEntre Alpha SRL et Beta SA.").statut, "signé")

    def test_mention_citee_au_milieu_du_texte(self):
        texte = "AVENANT N° 3\nEntre Alpha SRL et Beta SA.\nL'avenant 1 (signé) reste applicable.\n" + "Article.\n" * 30 + "Sera soumis à la signature."
        self.assertNotEqual(une("Avenant 3.docx", texte).statut, "signé")

    def test_nom_seul_ne_suffit_pas_pour_faire_foi(self):
        f = une("Contrat - signé.docx", "CONTRAT\nEntre Alpha SRL et Beta SA.")
        self.assertEqual(f.statut, "signé")
        self.assertIsNone(f.fait_foi)

    def test_texte_masque_ignore(self):
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, "Contrat de pret.docx").write_bytes(docx(
                '<w:p><w:r><w:t>CONTRAT DE PRET</w:t></w:r></w:p>'
                '<w:p><w:r><w:rPr><w:vanish/></w:rPr><w:t>(signé)</w:t></w:r></w:p>'))
            pieces, _ = lire_dossier(tmp)
        self.assertNotIn("signé", pieces[0].texte)


class CourrierEtResiliation(unittest.TestCase):
    def test_courrier_qui_cite_un_contrat(self):
        f = une("Courrier.docx", "Liège, le 2 mai 2025\nConcerne : contrat du 15 mars 2023\n\nMadame,\nTexte.\nJ. Martin (signé)")
        self.assertEqual(f.type, "courrier")

    def test_contestation_n_est_pas_une_resiliation(self):
        contrat = piece("c.docx", "CONTRAT DE SERVICES\nEntre Alpha SRL et Beta SA.\nFait à Liège, le 1er avril 2023.\n(signé)")
        lettre = piece("l.docx", "Liège, le 2 mai 2025\nConcerne : contrat du 1er avril 2023\n\nMadame,\n"
                                 "Alpha SRL n'entend pas mettre fin au contrat du 1er avril 2023 et conteste toute résiliation. "
                                 "Le contrat prendra fin le 31 mars 2026 à son terme normal.\nJ. Martin (signé)")
        inv = inventorier(".", [contrat, lettre], [])
        self.assertNotIn("résiliation notifiée", inv.etat)
        self.assertIn("à vérifier", inv.etat)


class Dates(unittest.TestCase):
    def test_date_impossible(self):
        self.assertIsNone(une("2025-02-30 Avenant 4 - signé.docx", "AVENANT N° 4").date)
        self.assertIsNone(une("Contrat 5.docx", "CONTRAT\nFait à Liège, le 31/02/2024.").date)

    def test_courriel_date_de_l_en_tete(self):
        f = une("m.eml", "Objet : x\n\nVoir la version du 20 février 2023.", format_=".eml",
                courriel={"date": "2025-03-03", "de": "", "a": "", "objet": "x"})
        self.assertEqual(f.date, "2025-03-03")


class PiecesEchappees(unittest.TestCase):
    def test_pieces_jointes_signalees_et_reprises(self):
        f = une("m.eml", "Objet : x\n\ntexte", format_=".eml",
                courriel={"date": "2025-03-03", "de": "", "a": "", "objet": "x", "pieces_jointes": ["Contrat SIGNE.pdf"]})
        self.assertTrue(any("Contrat SIGNE.pdf" in a for a in f.alertes))

    def test_dossier_cache_et_fichier_illisible_signales(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, ".archives"))
            pathlib.Path(tmp, ".archives", "Contrat - signé.txt").write_text("x", encoding="utf-8")
            pathlib.Path(tmp, "note.txt").write_text("x", encoding="utf-8")
            pathlib.Path(tmp, "verrou.txt").write_text("x", encoding="utf-8")
            original = open

            def ouvrir(chemin, *a, **k):
                if str(chemin).endswith("verrou.txt"):
                    raise PermissionError(13, "Permission denied")
                return original(chemin, *a, **k)

            with mock.patch("builtins.open", ouvrir):
                pieces, ignores = lire_dossier(tmp)
        self.assertTrue(any(".archives" in i for i in ignores))
        verrou = next(p for p in pieces if p.chemin == "verrou.txt")
        self.assertIn("inaccessible", verrou.non_lu)

    @unittest.skipUnless(sys.platform == "win32", "jonction : Windows")
    def test_jonction_non_suivie(self):
        with tempfile.TemporaryDirectory() as tmp:
            autre = os.path.join(tmp, "AUTRE CLIENT")
            dossier = os.path.join(tmp, "dossier")
            os.makedirs(autre)
            os.makedirs(dossier)
            pathlib.Path(autre, "secret.txt").write_text("x", encoding="utf-8")
            subprocess.run(["cmd", "/c", "mklink", "/J", os.path.join(dossier, "lien"), autre], check=True, capture_output=True)
            pieces, ignores = lire_dossier(dossier)
        self.assertEqual(pieces, [])
        self.assertTrue(any("lien" in i and "non suivi" in i for i in ignores))

    def test_docx_au_flux_corrompu(self):
        donnees = bytearray(docx('<w:p><w:r><w:t>' + "contrat " * 2000 + '</w:t></w:r></w:p>'))
        debut = donnees.find(b"word/document.xml") + len(b"word/document.xml")
        for i in range(debut + 10, debut + 60):
            donnees[i] ^= 0xFF
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, "abime.docx").write_bytes(bytes(donnees))
            pieces, _ = lire_dossier(tmp)
            self.assertTrue(pieces[0].non_lu)
            self.assertIn(cli([tmp, "--liste"]), (0, 1))

    def test_dossier_vide(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cli([tmp, "--liste"]), 1)

    def test_texte_utf16(self):
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, "n.txt").write_bytes("Réunion du 2 juin 2025".encode("utf-16"))
            pieces, _ = lire_dossier(tmp)
        self.assertEqual(pieces[0].texte, "Réunion du 2 juin 2025")


class RegistreToujoursValide(unittest.TestCase):
    def test_caracteres_interdits(self):
        for nom in ("Ma\x0btre.eml", "fichier￿.docx", "demi\ud800.docx"):
            inv = inventorier(".", [piece(nom, "CONTRAT\nEntre Alpha SRL et Beta SA.", courriel={"de": "x\x0cy"})], [])
            with zipfile.ZipFile(io.BytesIO(en_docx(inv))) as z:
                ET.fromstring(z.read("word/document.xml"))  # lève une erreur si le XML est mal formé

    def test_ecriture_complete_avec_nom_etrange(self):
        inv = inventorier("dossier\ud800", [piece("a\x0b.txt", "texte", format_=".txt")], [])
        with tempfile.TemporaryDirectory() as tmp:
            from inventaire_dossier.__main__ import ecrire_registre
            self.assertEqual(len(ecrire_registre(inv, tmp)), 3)


class TempsDeCalcul(unittest.TestCase):
    def test_entrees_hostiles(self):
        for texte in ("\n" * 50000, "fait à " * 50000, "fait à Liège " * 20000, "Liège " * 30000 + ", le"):
            debut = time.perf_counter()
            inventorier(".", [piece("x.txt", texte, format_=".txt")], [])
            self.assertLess(time.perf_counter() - debut, 2, repr(texte[:20]))


class Fenetre(unittest.TestCase):
    def setUp(self):
        try:
            import tkinter as tk
            from tkinter import messagebox
            self.racine = tk.Tk()
        except Exception as e:
            self.skipTest(f"fenêtre indisponible : {e}")
        self.racine.withdraw()
        self.erreurs = []
        self.ancien = messagebox.showerror
        messagebox.showerror = lambda *a, **k: self.erreurs.append(a)
        from inventaire_dossier.interface import Application
        self.app = Application(self.racine)

    def tearDown(self):
        from tkinter import messagebox
        messagebox.showerror = self.ancien
        self.racine.destroy()

    def test_erreur_affichee_et_rien_de_melange(self):
        from tkinter import filedialog
        with tempfile.TemporaryDirectory() as sortie:
            self.app.sortie = sortie
            with mock.patch.object(filedialog, "askdirectory", return_value=aide.PIECES):
                self.app.choisir()
            self.assertIsNotNone(self.app.registre)
            with mock.patch.object(filedialog, "askdirectory", return_value=aide.PIECES), \
                    mock.patch("inventaire_dossier.interface.ecrire_registre", side_effect=RuntimeError("panne")):
                self.app.choisir()
        self.assertTrue(self.erreurs)
        self.assertIsNone(self.app.registre)
        self.assertEqual(self.app.liste.get_children(), ())


if __name__ == "__main__":
    unittest.main()
