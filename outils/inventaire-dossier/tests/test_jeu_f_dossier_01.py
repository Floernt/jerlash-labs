"""Mesure sur le dossier fictif F-DOSSIER-01 : aucune régression sous les planchers de attendu/P01-planchers.json.

Comme pour F-IDENT-01, un échec sur le dossier de contrôle n'affiche que des comptes.
"""

import json
import os
import unittest

import aide

evaluation = aide.module_du_jeu("evaluer")
generation = aide.module_du_jeu("generer")
PLANCHERS = os.path.join(aide.JEU, "attendu", "P01-planchers.json")


class Jeu(unittest.TestCase):
    def test_pieces_conformes_aux_sources(self):
        self.assertEqual(generation.main(["--verifier"]), 0, "lancer : python -I factory/jeux-de-test/F-DOSSIER-01/generer.py")

    def test_planchers(self):
        with open(PLANCHERS, encoding="utf-8") as f:
            planchers = json.load(f)["planchers"]
        for jeu, seuils in planchers.items():
            r = evaluation.evaluer(jeu)
            for champ, seuil in seuils.items():
                if champ == "alertes":
                    obtenu = sum(ok for _l, ok in r["alertes"]) / max(1, len(r["alertes"]))
                else:
                    obtenu = r["justes"][champ] / r["n"]
                detail = "\n".join(r["ecarts"]) if jeu == "developpement" else f"{len(r['ecarts'])} écarts"
                self.assertGreaterEqual(obtenu, seuil, f"{jeu} / {champ}\n{detail}")


if __name__ == "__main__":
    unittest.main()
