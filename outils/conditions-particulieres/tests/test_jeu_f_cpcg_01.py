"""Banc d'essai F-CPCG-01 : jeu de développement exact, jeu de contrôle au-dessus des planchers.

Les écarts du jeu de contrôle ne sont pas affichés (seulement les totaux) : il sert à mesurer, pas à régler.
"""

import json
import os
import unittest

import aide


class JeuFCpcg01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generer = aide.module_du_jeu("generer")
        cls.evaluer = aide.module_du_jeu("evaluer")
        with open(os.path.join(aide.JEU, "attendu", "P03-planchers.json"), encoding="utf-8") as f:
            cls.planchers = json.load(f)

    def test_pieces_conformes_aux_sources(self):
        self.assertEqual(self.generer.main(["--verifier"]), 0)

    def test_planchers(self):
        for jeu in ("developpement", "controle"):
            r = self.evaluer.evaluer(jeu)
            attendus = sum(n["attendus"] for n in r["donnees"].values())
            reperes = sum(n["reperes"] for n in r["donnees"].values())
            mesures = {"rappel": reperes / attendus,
                       "precision": r["signalements"]["exacts"] / max(1, r["signalements"]["total"]),
                       "articles": r["articles"]["exacts"] / r["articles"]["total"]}
            for mesure, seuil in self.planchers[jeu].items():
                with self.subTest(jeu=jeu, mesure=mesure):
                    self.assertGreaterEqual(round(mesures[mesure], 2), seuil)


if __name__ == "__main__":
    unittest.main()
