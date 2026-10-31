"""Ligne de commande : codes de sortie, mode --liste, erreurs."""

import contextlib
import io
import os
import tempfile
import unittest

import aide
from pseudonymisation.__main__ import main as cli

PIECE = os.path.join(aide.PIECES, "conclusions-bail.txt")


def executer(*args):
    sortie, erreurs = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreurs):
        code = cli(list(args))
    return code, sortie.getvalue(), erreurs.getvalue()


class LigneDeCommande(unittest.TestCase):
    def test_liste_n_ecrit_rien(self):
        with tempfile.TemporaryDirectory() as dossier:
            code, sortie, _ = executer("pseudonymiser", PIECE, "--sortie", dossier, "--liste")
            self.assertEqual(code, 0)
            self.assertEqual(os.listdir(dossier), [])
        self.assertIn("[PERSONNE_1]", sortie)
        self.assertIn("Pseudonymisation, et non anonymisation", sortie)

    def test_termes_et_exclusions(self):
        with tempfile.TemporaryDirectory() as dossier:
            termes = os.path.join(dossier, "termes.txt")
            exclus = os.path.join(dossier, "exclus.txt")
            with open(termes, "w", encoding="utf-8") as f:
                f.write("REFERENCE | Chambre des baux\n")
            with open(exclus, "w", encoding="utf-8") as f:
                f.write("Fabrice Lonneux\n")
            code, _, _ = executer("pseudonymiser", PIECE, "--sortie", dossier, "--termes", termes, "--exclure", exclus)
            with open(os.path.join(dossier, "conclusions-bail - pseudonymise.txt"), encoding="utf-8") as f:
                texte = f.read()
        self.assertEqual(code, 0)
        self.assertIn("[REFERENCE_1]", texte.split("\n")[1])
        self.assertIn("Fabrice Lonneux", texte)

    def test_fichier_absent(self):
        code, _, erreurs = executer("pseudonymiser", os.path.join(tempfile.gettempdir(), "absent-iavocat.txt"))
        self.assertEqual(code, 2)
        self.assertIn("Erreur", erreurs)

    def test_retablir_refuse_d_ecraser(self):
        with tempfile.TemporaryDirectory() as dossier:
            executer("pseudonymiser", PIECE, "--sortie", dossier)
            table = os.path.join(dossier, "conclusions-bail - table.json")
            existant = os.path.join(dossier, "conclusions-bail - pseudonymise.txt")
            code, _, erreurs = executer("retablir", existant, "--table", table, "--sortie", existant)
        self.assertEqual(code, 2)
        self.assertIn("existe déjà", erreurs)

    def test_retablir_avec_une_table_invalide(self):
        code, _, erreurs = executer("retablir", PIECE, "--table", PIECE)
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
