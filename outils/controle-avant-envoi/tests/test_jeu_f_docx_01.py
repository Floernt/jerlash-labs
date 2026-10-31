"""Résultats attendus sur le jeu de test F-DOCX-01 (factory/jeux-de-test/F-DOCX-01/attendu/P05.json)."""

import json
import os
import tempfile
import unittest

import aide
from controle_avant_envoi.analyse import analyser, charger_configuration

with open(os.path.join(aide.JEU, "attendu", "P05.json"), encoding="utf-8") as f:
    ATTENDU = json.load(f)


def texte_controle(c) -> str:
    return "\n".join(f"{k.localisation} : {k.detail}" for k in c.constats) + "\n" + c.note


class JeuFDocx01(unittest.TestCase):
    def verifier_piece(self, cle: str, spec: dict) -> None:
        fichier = spec.get("fichier", cle)
        cfg = charger_configuration()
        cfg["termes_sensibles"] = spec.get("termes", [])
        rapport = analyser(os.path.join(aide.PIECES, fichier), cfg)
        self.assertEqual(rapport.niveau, spec["niveau"], rapport.verdict)
        if "erreur_contient" in spec:
            self.assertIn(spec["erreur_contient"], rapport.erreur)
            self.assertEqual(rapport.code_sortie, 2)
            return
        self.assertTrue(rapport.integre, "le fichier analysé doit rester inchangé")
        controles = {c.ident: c for c in rapport.controles}
        for ident, attendu in spec.get("controles", {}).items():
            c = controles[ident]
            with self.subTest(piece=cle, controle=ident):
                self.assertEqual(c.statut, attendu["statut"], texte_controle(c))
                texte = texte_controle(c)
                for fragment in attendu.get("contient", []):
                    self.assertIn(fragment, texte)
                for fragment in attendu.get("absent", []):
                    self.assertNotIn(fragment, texte)
                if "min" in attendu:
                    self.assertGreaterEqual(len(c.constats), attendu["min"])
        if "statut_par_defaut" in spec:
            for c in rapport.controles:
                with self.subTest(piece=cle, controle=c.ident):
                    self.assertEqual(c.statut, spec["tous_sauf"].get(c.ident, spec["statut_par_defaut"]),
                                     texte_controle(c))

    def test_pieces(self):
        for cle, spec in ATTENDU["pieces"].items():
            with self.subTest(piece=cle):
                self.verifier_piece(cle, spec)

    def test_pieces_versionnees_identiques_au_generateur(self):
        """Les pièces du dépôt sont exactement celles que produit generer.py."""
        with tempfile.TemporaryDirectory() as dossier:
            for chemin in aide.generateur().generer(dossier):
                nom = os.path.basename(chemin)
                with open(chemin, "rb") as a, open(os.path.join(aide.PIECES, nom), "rb") as b:
                    self.assertEqual(a.read(), b.read(), f"{nom} diffère du générateur : relancer generer.py")


if __name__ == "__main__":
    unittest.main()
