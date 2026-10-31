"""Règles de détection, cas par cas."""

import unittest

import aide  # noqa: F401  (chemin vers src)
from pseudonymisation.detection import (bce_valide, detecter, iban_valide, lire_termes, luhn_valide,
                                        nn_valide)


def trouves(texte, **options):
    return [(e.categorie, e.texte) for e in detecter(texte, **options)]


class SommesDeControle(unittest.TestCase):
    def test_numero_national(self):
        self.assertTrue(nn_valide("78.03.12-047.88"))
        self.assertTrue(nn_valide("03.06.17-081.28"))   # naissance après 2000
        self.assertFalse(nn_valide("78.03.12-047.89"))
        self.assertFalse(nn_valide("12.34.56-789.01"))  # mois impossible

    def test_numero_entreprise(self):
        self.assertTrue(bce_valide("0456.712.325"))
        self.assertFalse(bce_valide("0456.712.326"))
        self.assertFalse(bce_valide("BE 0123 456 789"))

    def test_iban(self):
        self.assertTrue(iban_valide("BE14 0631 2345 6783"))
        self.assertTrue(iban_valide("FR76 3000 6000 0112 3456 7890 189"))
        self.assertFalse(iban_valide("BE14 0631 2345 6784"))

    def test_luhn(self):
        self.assertTrue(luhn_valide("4111 1111 1111 1111"))
        self.assertFalse(luhn_valide("4111 1111 1111 1112"))


class Identifiants(unittest.TestCase):
    def test_numero_national_faux_ignore_sauf_s_il_est_annonce(self):
        self.assertEqual(trouves("Code 78.03.12-047.89."), [])
        self.assertEqual(trouves("Registre national : 78.03.12-047.89."),
                         [("NUMERO_NATIONAL", "78.03.12-047.89")])

    def test_iban_n_avale_pas_le_mot_suivant(self):
        self.assertEqual(trouves("Compte BE14 0631 2345 6783 au nom de"), [("IBAN", "BE14 0631 2345 6783")])

    def test_telephones(self):
        self.assertEqual(trouves("Tél. 04 223 45 67, gsm 0475/12.34.56, +32 (0)4 223 45 67."),
                         [("TELEPHONE", "04 223 45 67"), ("TELEPHONE", "0475/12.34.56"),
                          ("TELEPHONE", "+32 (0)4 223 45 67")])

    def test_dates_et_montants_ne_sont_pas_des_telephones(self):
        self.assertEqual(trouves("Le 04.05.2021, la somme de 1.250.000,00 EUR, facture 0123 456 789."), [])

    def test_date_de_naissance_seule(self):
        self.assertEqual(trouves("née à Huy le 5 janvier 1962, mariée le 3 mai 1990"),
                         [("DATE_NAISSANCE", "5 janvier 1962")])


class Personnes(unittest.TestCase):
    def test_civilite_hors_du_nom(self):
        self.assertEqual(trouves("M. Jean Dupont et Mme Van den Bossche."),
                         [("PERSONNE", "Jean Dupont"), ("PERSONNE", "Van den Bossche")])

    def test_fonctions_ne_sont_pas_des_noms(self):
        self.assertEqual(trouves("Monsieur le Président et Mme la Juge ; publié au M.B. le 3 mars."), [])

    def test_representee_par_avec_civilite(self):
        self.assertEqual(trouves("représentée par Mme Sophie Lemaire, administratrice"),
                         [("PERSONNE", "Sophie Lemaire")])

    def test_nom_retrouve_ailleurs_avec_le_meme_marqueur(self):
        entites = detecter("M. Thomas Wilmotte loue. Plus tard, Wilmotte et THOMAS WILMOTTE signent.")
        self.assertEqual([e.texte for e in entites], ["Thomas Wilmotte", "Wilmotte", "THOMAS WILMOTTE"])
        self.assertEqual(len({e.cle for e in entites}), 1)

    def test_nom_de_famille_partage_reste_distinct(self):
        entites = detecter("Mme Martine Vanderheyden et M. Luc Vanderheyden. Décharge à Mme Vanderheyden.")
        self.assertEqual(len({e.cle for e in entites}), 3)

    def test_titres_en_capitales_ne_sont_pas_des_noms(self):
        self.assertEqual(trouves("ARTICLE PREMIER. Les PARTIES conviennent. RPM Liège."), [])


class Societes(unittest.TestCase):
    def test_forme_avant_et_apres(self):
        self.assertEqual(trouves("Garage Derouaux SRL et la SA Immo Condroz, ainsi que l'ASBL Les Amis du Val."),
                         [("ORGANISATION", "Garage Derouaux"), ("ORGANISATION", "Immo Condroz"),
                          ("ORGANISATION", "Les Amis du Val")])

    def test_mot_qui_precede_exclu(self):
        self.assertEqual(trouves("Pour Atelier Numérique Meuse SRL : le gérant"),
                         [("ORGANISATION", "Atelier Numérique Meuse")])


class Adresses(unittest.TestCase):
    def test_adresse_complete(self):
        self.assertEqual(trouves("domicilié avenue de l'Observatoire 7 bte 3, 4000 Liège, depuis"),
                         [("ADRESSE", "avenue de l'Observatoire 7 bte 3, 4000 Liège")])

    def test_mise_en_place_n_est_pas_une_adresse(self):
        self.assertEqual(trouves("la mise en place de 3 dispositifs"), [])


class ListesUtilisateur(unittest.TestCase):
    def test_terme_impose_et_exclusion(self):
        texte = "Le dossier Brasserie du Pont concerne M. Jean Dupont."
        self.assertEqual(trouves(texte, termes=[("ORGANISATION", "brasserie du pont")], exclus=["Jean Dupont"]),
                         [("ORGANISATION", "Brasserie du Pont")])

    def test_nom_fourni_retrouve_seul(self):
        texte = "Réunion avec Jean Dupont. Ensuite, Dupont a signé."
        entites = detecter(texte, termes=[("PERSONNE", "Jean Dupont")])
        self.assertEqual([e.texte for e in entites], ["Jean Dupont", "Dupont"])
        self.assertEqual(len({e.cle for e in entites}), 1)

    def test_lecture_de_la_liste(self):
        self.assertEqual(lire_termes("# commentaire\nDurand\nPERSONNE | Jean Dupont\n"),
                         [("TERME", "Durand"), ("PERSONNE", "Jean Dupont")])
        with self.assertRaises(ValueError):
            lire_termes("INCONNUE | x")


if __name__ == "__main__":
    unittest.main()
