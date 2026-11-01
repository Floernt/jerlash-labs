"""Banc d'essai F-DEF-01 : jeu de développement exact, jeu de contrôle au-dessus des planchers.

Les écarts du jeu de contrôle ne sont pas affichés (seulement les totaux) : il sert à mesurer, pas à régler.
"""

import json
import os
import unittest

import aide


class JeuFDef01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generer = aide.module_du_jeu("generer")
        cls.evaluer = aide.module_du_jeu("evaluer")
        with open(os.path.join(aide.JEU, "attendu", "P02-planchers.json"), encoding="utf-8") as f:
            cls.planchers = json.load(f)

    def test_pieces_conformes_aux_sources(self):
        self.assertEqual(self.generer.main(["--verifier"]), 0)

    def test_planchers(self):
        for jeu in ("developpement", "controle"):
            totaux = self.evaluer.evaluer(jeu)["totaux"]
            for categorie, seuils in self.planchers[jeu].items():
                for mesure, seuil in seuils.items():
                    with self.subTest(jeu=jeu, categorie=categorie, mesure=mesure):
                        n = totaux[categorie]
                        self.assertGreaterEqual(round(n[mesure], 2), seuil,
                                                f"{n['exacts']} exacts, {n['attendus']} attendus, {n['trouves']} trouvés")


if __name__ == "__main__":
    unittest.main()
