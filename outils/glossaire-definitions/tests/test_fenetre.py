"""Fenêtre : un contrat analysé s'affiche ; une erreur est montrée et ne laisse rien de l'essai précédent."""

import os
import tempfile
import unittest
from unittest import mock

import aide

CONTRAT = os.path.join(aide.PIECES, "Contrat de fourniture - Brasserie du Condroz.docx")


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
        from glossaire_definitions.interface import Application
        self.app = Application(self.racine)

    def tearDown(self):
        from tkinter import messagebox
        messagebox.showerror = self.ancien
        self.racine.destroy()

    def test_analyse_puis_erreur_sans_melange(self):
        from tkinter import filedialog
        with tempfile.TemporaryDirectory() as sortie:
            self.app.sortie = sortie
            with mock.patch.object(filedialog, "askopenfilename", return_value=CONTRAT):
                self.app.choisir()
            self.assertIsNotNone(self.app.rapport)
            self.assertEqual(len(self.app.liste.get_children()), 12)
            self.app.liste.selection_set("0")
            self.app.afficher_terme()
            self.assertIn("art. 10.1", self.app.details.get("1.0", "end"))
            with mock.patch.object(filedialog, "askopenfilename", return_value=CONTRAT), \
                    mock.patch("glossaire_definitions.interface.ecrire_rapport", side_effect=RuntimeError("panne")):
                self.app.choisir()
        self.assertTrue(self.erreurs)
        self.assertIsNone(self.app.rapport)
        self.assertEqual(self.app.liste.get_children(), ())
        self.assertEqual(self.app.points.get("1.0", "end").strip(), "")


if __name__ == "__main__":
    unittest.main()
