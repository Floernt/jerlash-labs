"""Mesure sur le jeu F-IDENT-01 : aucune régression sous les planchers de attendu/P09.json.

Un échec sur le jeu de contrôle n'affiche que des taux et des comptes, jamais son contenu :
le lire reviendrait à régler l'outil sur ce jeu et à lui retirer sa valeur de mesure.
"""

import json
import os
import unittest

import aide

evaluation = aide.module_du_jeu("evaluer")
generation = aide.module_du_jeu("generer")

with open(os.path.join(aide.JEU, "attendu", "P09.json"), encoding="utf-8") as f:
    ATTENDU = json.load(f)


class JeuAJour(unittest.TestCase):
    def test_pieces_conformes_aux_sources(self):
        self.assertEqual(generation.main(["--verifier"]), 0, "lancer : python -I factory/jeux-de-test/F-IDENT-01/generer.py")


class Planchers(unittest.TestCase):
    def verifier(self, jeu):
        r = evaluation.evaluer(jeu)
        planchers = ATTENDU["planchers"][jeu]
        detail = jeu != "controle"
        self.assertGreaterEqual(r["rappel"], planchers["rappel"],
                                "\n".join(r["oublis"]) if detail else f"{len(r['oublis'])} oublis")
        self.assertGreaterEqual(r["precision"], planchers["precision"],
                                "\n".join(r["fausses_alertes"]) if detail else f"{len(r['fausses_alertes'])} fausses alertes")
        for categorie, plancher in planchers.get("rappel_par_categorie", {}).items():
            s = r["categories"][categorie]
            self.assertGreaterEqual(s["masquees"] / s["attendues"], plancher, categorie)
        return r

    def test_jeu_de_developpement(self):
        self.verifier("developpement")

    def test_jeu_de_controle(self):
        self.verifier("controle")

    def test_textes_sans_donnees(self):
        for jeu in ("developpement", "controle"):
            r = evaluation.evaluer(jeu)
            for nom, admis in ATTENDU["faux_positifs_admis"].items():
                alertes = [a for a in r["fausses_alertes"] if a.startswith(nom + " :")]
                inattendues = [a for a in alertes if not any(f"« {x} »" in a for x in admis)]
                self.assertEqual(len(inattendues), 0,
                                 f"{nom} : {inattendues if jeu != 'controle' else len(inattendues)} fausse(s) alerte(s) nouvelle(s)")


if __name__ == "__main__":
    unittest.main()
