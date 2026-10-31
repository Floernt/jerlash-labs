"""Remplacement cohérent, rétablissement, et fichiers produits."""

import json
import os
import tempfile
import unittest

import aide  # noqa: F401
from pseudonymisation.__main__ import enregistrer
from pseudonymisation.detection import detecter
from pseudonymisation.remplacement import lire_table, pseudonymiser, retablir

TEXTE = ("M. Thomas Wilmotte (thomas@exemple.example) loue à Mme Nadia Bensalem. "
         "Wilmotte réclame 850 EUR sur le compte BE14 0631 2345 6783.")


class Remplacement(unittest.TestCase):
    def test_marqueurs_coherents(self):
        r = pseudonymiser(TEXTE, detecter(TEXTE))
        self.assertEqual(r.texte, "M. [PERSONNE_1] ([EMAIL_1]) loue à Mme [PERSONNE_2]. "
                                  "[PERSONNE_1] réclame 850 EUR sur le compte [IBAN_1].")
        self.assertNotIn("Wilmotte", r.texte)

    def test_aller_retour(self):
        r = pseudonymiser(TEXTE, detecter(TEXTE))
        reponse = "Selon [PERSONNE_1], [Personne_2] doit payer sur IBAN_1. PERSONNE 1 a raison."
        retour = retablir(reponse, r.table)
        self.assertEqual(retour.texte, "Selon Thomas Wilmotte, Nadia Bensalem doit payer sur BE14 0631 2345 6783. "
                                       "Thomas Wilmotte a raison.")
        self.assertEqual(retour.absents, ["[EMAIL_1]"])

    def test_marqueur_inconnu_laisse_tel_quel(self):
        r = pseudonymiser(TEXTE, detecter(TEXTE))
        retour = retablir("Voir [PERSONNE_7].", r.table)
        self.assertEqual(retour.texte, "Voir [PERSONNE_7].")
        self.assertEqual(retour.inconnus, ["[PERSONNE_7]"])

    def test_donnee_desactivee_conservee(self):
        entites = detecter(TEXTE)
        for e in entites:
            if e.categorie == "IBAN":
                e.actif = False
        self.assertIn("BE14 0631 2345 6783", pseudonymiser(TEXTE, entites).texte)

    def test_marqueur_deja_present_signale(self):
        texte = "Le modèle cite [PERSONNE_1]. M. Jean Dupont signe."
        self.assertEqual(pseudonymiser(texte, detecter(texte)).marqueurs_preexistants, ["[PERSONNE_1]"])

    def test_table_avertit_et_ne_contient_que_le_necessaire(self):
        r = pseudonymiser(TEXTE, detecter(TEXTE), "bail.txt")
        self.assertIn("ne l'envoyez jamais", r.table["avertissement"])
        self.assertEqual({c["marqueur"] for c in r.table["correspondances"]},
                         {"[PERSONNE_1]", "[PERSONNE_2]", "[EMAIL_1]", "[IBAN_1]"})


class Fichiers(unittest.TestCase):
    def test_rien_n_est_jamais_remplace(self):
        with tempfile.TemporaryDirectory() as dossier:
            premiers = enregistrer(dossier, "bail", "texte 1", {"correspondances": []})
            seconds = enregistrer(dossier, "bail", "texte 2", {"correspondances": []})
            self.assertEqual([os.path.basename(c) for c in premiers], ["bail - pseudonymise.txt", "bail - table.json"])
            self.assertEqual([os.path.basename(c) for c in seconds],
                             ["bail - pseudonymise (2).txt", "bail - table (2).json"])
            with open(premiers[0], encoding="utf-8") as f:
                self.assertEqual(f.read(), "texte 1")

    def test_table_invalide_refusee(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "x.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump({"correspondances": [{"marqueur": 1}]}, f)
            with self.assertRaises(ValueError):
                lire_table(chemin)


if __name__ == "__main__":
    unittest.main()
