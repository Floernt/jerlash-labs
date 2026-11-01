"""Règles : données propres à l'opération, découpage en blocs, classement. Textes courts écrits pour le test."""

import unittest

import aide  # noqa: F401
from conditions_particulieres.analyse import analyser, bce_valide, detecter, iban_valide
from conditions_particulieres.lecture import Document, Paragraphe


def donnees(texte, noms=()):
    return [(d.categorie, d.texte) for d in detecter(texte, 0, list(noms))]


def analyse(*lignes):
    return analyser(Document("t.docx", [Paragraphe(l) for l in lignes]))


class Donnees(unittest.TestCase):
    def test_parties_adresses_identifiants(self):
        self.assertEqual(donnees("Alpha Bêta SRL, rue du Moulin 12 à 4560 Clavier, BCE 0712.345.630, représentée par "
                                 "Madame Claire Dumont"),
                         [("PARTIE", "Alpha Bêta SRL"), ("ADRESSE", "rue du Moulin 12 à 4560 Clavier"),
                          ("IDENTIFIANT", "0712.345.630"), ("PARTIE", "Madame Claire Dumont")])

    def test_iban_courriel_telephone_reference(self):
        self.assertEqual([c for c, _ in donnees("compte BE71 0961 2345 6769, à compta@exemple.test, au +32 87 12 34 56, "
                                                "référence HL-2025-0412")], ["IDENTIFIANT"] * 4)

    def test_montants_en_chiffres_et_en_lettres(self):
        self.assertEqual(donnees("fixés à dix-sept mille cinq cents euros (17.500 EUR) hors TVA, plafond de 25.000 euros, "
                                 "prix unitaire de 0,21 euro, ou € 300"),
                         [("MONTANT", "dix-sept mille cinq cents euros (17.500 EUR)"), ("MONTANT", "25.000 euros"),
                          ("MONTANT", "0,21 euro"), ("MONTANT", "€ 300")])

    def test_dates_hors_textes_normatifs(self):
        self.assertEqual(donnees("Le contrat prend effet le 1er mars 2023, conformément à la loi du 2 août 2002 et à "
                                 "l'arrêté royal du 12 janvier 2010 ; rapport remis le 15/12/2025."),
                         [("DATE", "1er mars 2023"), ("DATE", "15/12/2025")])

    def test_quantites_et_pieges(self):
        self.assertEqual(donnees("à raison de 40.000 bouteilles et de 18 jours-homme, payables dans les trente jours, "
                                 "en deux exemplaires, remise de 3 %, articles 4 et 5"),
                         [("QUANTITE", "40.000 bouteilles"), ("QUANTITE", "18 jours-homme")])

    def test_signataire_sans_civilite(self):
        a = analyse("Entre : Alpha SRL, représentée par Madame Claire Dumont.", "Article 1 – Objet", "La livraison.",
                    "Fait à Liège, le 15 février 2023.", "Pour Alpha, Claire Dumont, gérante")
        self.assertIn(("PARTIE", "Claire Dumont"), [(d.categorie, d.texte) for d in a.blocs[-1].donnees])

    def test_sommes_de_controle(self):
        self.assertTrue(bce_valide("0712345630"))
        self.assertFalse(bce_valide("0712345631"))
        self.assertTrue(iban_valide("BE71 0961 2345 6769"))
        self.assertFalse(iban_valide("BE72 0961 2345 6769"))
        self.assertEqual(donnees("le nombre 1712345631 n'est pas un numéro"), [])


class Blocs(unittest.TestCase):
    def test_decoupage_et_classement(self):
        a = analyse("CONTRAT DE SERVICES", "Entre Alpha SRL, rue Haute 5, 4000 Liège, et Bêta SA.",
                    "Préambule", "Les parties se sont rencontrées le 4 septembre 2025.",
                    "Article 1 – Prix", "Le prix est de 1.000 euros.",
                    "Article 2 – Confidentialité", "Chaque partie garde le secret.",
                    "Article 3 – Responsabilité", "La responsabilité est limitée.", "Elle est plafonnée à 5.000 euros.",
                    "Article 4 – Résiliation", "Chaque partie peut résilier.",
                    "Fait à Liège, le 1er octobre 2025.", "Pour Alpha, Jean Dupont")
        self.assertEqual([(b.titre, b.classement) for b in a.blocs], [
            ("comparution", "particulieres"), ("Préambule", "particulieres"), ("Article 1 – Prix", "particulieres"),
            ("Article 2 – Confidentialité", "generales"), ("Article 3 – Responsabilité", "mixte"),
            ("Article 4 – Résiliation", "generales"), ("signatures", "particulieres")])

    def test_titres_numerotes_et_renvois(self):
        a = analyse("Entre Alpha SRL et Bêta SA.", "1. Objet", "Voir l'article 3 et les articles 4 à 6.",
                    "2. Paiement", "Payable sur le compte BE71 0961 2345 6769.")
        self.assertEqual([b.titre for b in a.blocs], ["comparution", "1. Objet", "2. Paiement"])
        self.assertEqual(a.blocs[1].renvois, ["article 3", "articles 4 à 6"])
        self.assertEqual(a.blocs[2].classement, "mixte")

    def test_intitule_sans_donnees(self):
        a = analyse("Entre Alpha SRL et Bêta SA.", "Article 1 – Objet", "Le Prestataire réalise la mission décrite en annexe.",
                    "Article 2 – Obligations des parties", "Chaque partie collabore de bonne foi.")
        self.assertEqual(a.blocs[1].classement, "particulieres")   # un « Objet » est propre à l'opération par nature
        self.assertEqual(a.blocs[2].classement, "generales")


if __name__ == "__main__":
    unittest.main()
