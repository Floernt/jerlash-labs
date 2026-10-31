"""Ligne de commande : codes de sortie et fichiers produits."""

import contextlib
import io
import json
import os
import tempfile
import unittest

import aide
from controle_avant_envoi.__main__ import main as cli


def executer(*args):
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(io.StringIO()):
        code = cli(list(args))
    return code, sortie.getvalue()


class LigneDeCommande(unittest.TestCase):
    def test_codes_de_sortie(self):
        self.assertEqual(executer(os.path.join(aide.PIECES, "contrat-propre.docx"))[0], 0)
        self.assertEqual(executer(os.path.join(aide.PIECES, "contrat-pieges.docx"))[0], 1)
        self.assertEqual(executer(os.path.join(aide.PIECES, "contrat-protege.docx"))[0], 2)
        # Plusieurs fichiers : le code le plus grave l'emporte.
        self.assertEqual(executer(os.path.join(aide.PIECES, "contrat-propre.docx"),
                                  os.path.join(aide.PIECES, "contrat-tronque.docx"))[0], 2)

    def test_rapports_html_et_json(self):
        with tempfile.TemporaryDirectory() as dossier:
            termes = os.path.join(dossier, "termes.txt")
            with open(termes, "w", encoding="utf-8") as f:
                f.write("# commentaire ignoré\nAutre-Client\n\n")
            code, _ = executer(os.path.join(aide.PIECES, "contrat-pieges.docx"), "--html", dossier,
                               "--json", dossier, "--termes", termes, "--silencieux")
            base = os.path.join(dossier, "contrat-pieges - controle avant envoi")
            with open(base + ".json", encoding="utf-8") as f:
                donnees = json.load(f)
            with open(base + ".html", encoding="utf-8") as f:
                html = f.read()
        self.assertEqual(code, 1)
        termes_ctrl = next(c for c in donnees["controles"] if c["id"] == "termes")
        self.assertEqual(termes_ctrl["statut"], "detecte")
        self.assertTrue(donnees["fichier_inchange"])
        self.assertIn("Contrôle avant envoi", html)

    def test_configuration_invalide(self):
        with tempfile.TemporaryDirectory() as dossier:
            cfg = os.path.join(dossier, "cfg.json")
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump({"marqueurs": [{"libelle": "x", "motif": "(("}]}, f)
            code, _ = executer(os.path.join(aide.PIECES, "contrat-propre.docx"), "--config", cfg)
        self.assertEqual(code, 2)


class Interface(unittest.TestCase):
    def test_la_fenetre_se_construit(self):
        try:
            import tkinter
            racine = tkinter.Tk()
        except Exception as e:  # pas d'affichage disponible (serveur d'intégration continue)
            self.skipTest(f"affichage indisponible : {e}")
        try:
            racine.withdraw()
            from controle_avant_envoi.interface import Application
            Application(racine)
            racine.update_idletasks()
        finally:
            racine.destroy()


if __name__ == "__main__":
    unittest.main()
