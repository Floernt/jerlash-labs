"""Règles : formes de définition, emplois, défauts. Textes courts écrits pour le test."""

import unittest

import aide  # noqa: F401
from glossaire_definitions.analyse import analyser, cle
from glossaire_definitions.lecture import Document, Paragraphe, lire_texte


def analyse(*lignes, tableau=None):
    paragraphes = [Paragraphe(l) for l in lignes]
    for r, rangee in enumerate(tableau or []):
        paragraphes += [Paragraphe(c, (0, r, i)) for i, c in enumerate(rangee)]
    return analyser(Document("test.docx", paragraphes))


def termes(a):
    return [t.forme for t in a.termes]


def categorie(a, nom):
    return sorted(c.forme for c in a.du_type(nom))


class Definitions(unittest.TestCase):
    def test_formes_courantes(self):
        a = analyse(
            "Société Alpha SRL (ci-après « le Client ») et Bêta SA, ci-après dénommée « la Société ».",
            "(ensemble, les « Parties » et individuellement une « Partie »)",
            "Article 1 – Définitions",
            "« Prix » : le prix fixé à l'annexe.",
            "a) le terme « Logiciel » vise le programme.",
            "b) on entend par “Livrable” tout document remis.",
            'c) "Jour Ouvrable" désigne un jour de semaine.',
            "Informations Confidentielles : toute information.",
            "Article 2 – Objet",
            "Le prix global est de 100 euros (le « Prix Global »).",
        )
        self.assertEqual(set(termes(a)), {"Client", "Société", "Parties", "Prix", "Logiciel", "Livrable",
                                          "Jour Ouvrable", "Informations Confidentielles", "Prix Global"})

    def test_pas_de_definition_sans_formule(self):
        a = analyse("Article 2 – Signature", "La mention « Lu et approuvé » précède la signature.",
                    "Les parties conviennent du « prix du marché ».", "Pour l'application de la présente convention :")
        self.assertEqual(termes(a), [])

    def test_ligne_sans_guillemets_seulement_dans_les_definitions(self):
        hors = analyse("Article 3 – Livraison", "Lieu de Livraison : le siège du client.")
        dans = analyse("Article 1 – Définitions", "Lieu de Livraison : le siège du client.",
                       "Pour l'application du contrat : voir ci-dessous.")
        self.assertEqual(termes(hors), [])
        self.assertEqual(termes(dans), ["Lieu de Livraison"])

    def test_tableau_de_definitions(self):
        a = analyse("Annexe A – Glossaire", tableau=[["Terme", "Définition"], ["Date de Closing", "le 30 juin 2025."],
                                                     ["« Garanties »", "les garanties de l'article 5."]])
        self.assertEqual(set(termes(a)), {"Date de Closing", "Garanties"})

    def test_tableau_ordinaire_ignore(self):
        a = analyse("Article 4 – Prix", tableau=[["Produit", "Prix unitaire"], ["Bouteille", "0,40 euro"]])
        self.assertEqual(termes(a), [])

    def test_tableau_markdown(self):
        paragraphes = lire_texte("Annexe 1 – Définitions\n| Terme | Définition |\n|---|---|\n| Cédant | le vendeur |\n".encode())
        a = analyser(Document("t.md", paragraphes))
        self.assertEqual(termes(a), ["Cédant"])


class Emplois(unittest.TestCase):
    BASE = ["Article 1 – Définitions", "« Jour Ouvrable » désigne un jour de semaine.", "« Prix » : le prix.",
            "« Prix de Cession » : le prix des parts."]

    def test_pluriel_et_terme_le_plus_long(self):
        a = analyse(*self.BASE, "Le paiement intervient dans les dix Jours Ouvrables. Le Prix de Cession est ferme.")
        emplois = {t.forme: len(t.emplois) for t in a.termes}
        self.assertEqual(emplois, {"Jour Ouvrable": 1, "Prix": 0, "Prix de Cession": 1})
        self.assertEqual(categorie(a, "inutilise"), ["Prix"])

    def test_minuscules_ni_emploi_ni_variante(self):
        a = analyse(*self.BASE, "Le prix du marché sert de référence. Le Prix de Cession et les Jours Ouvrables aussi.")
        self.assertEqual(categorie(a, "variante"), [])
        self.assertEqual(categorie(a, "inutilise"), ["Prix"])

    def test_variante_de_casse(self):
        a = analyse(*self.BASE, "Le Prix de cession est payé en deux Jours ouvrables. Le Prix aussi.")
        self.assertEqual(categorie(a, "variante"), ["Jours ouvrables", "Prix de cession"])

    def test_majuscule_de_debut_de_phrase_n_est_pas_une_variante(self):
        a = analyse("Article 1 – Définitions", "« Droits de propriété » : les droits.",
                    "Les Droits de propriété sont cédés. Droits de propriété exclus : aucun.")
        self.assertEqual(categorie(a, "variante"), [])

    def test_titre_n_est_pas_un_emploi(self):
        a = analyse("Article 1 – Définitions", "« Force Majeure » : tout événement imprévisible.", "Article 9 – Force Majeure",
                    "FORCE MAJEURE", "Aucune partie n'est responsable.")
        self.assertEqual(categorie(a, "inutilise"), ["Force Majeure"])


class Defauts(unittest.TestCase):
    def test_divergent_et_repete(self):
        a = analyse("Article 1 – Définitions", "« Durée » : cinq ans.", "« Prix » : le prix fixé.",
                    "Article 4 – Durée", "La « Durée » s'entend de trois ans. Le Prix est ferme pendant la Durée.",
                    "Article 5", "On entend par « Prix » le prix fixé.")
        self.assertEqual(categorie(a, "divergent"), ["Durée"])
        self.assertEqual(categorie(a, "doublon"), ["Prix"])

    def test_singulier_et_pluriel_definis_ensemble_ne_sont_pas_un_doublon(self):
        a = analyse("Alpha SRL et Bêta SA (ensemble, les « Parties » et individuellement une « Partie »).",
                    "Chaque Partie signe.")
        self.assertEqual(a.constats, [])

    def test_avant_definition_en_cours_de_texte_seulement(self):
        a = analyse("Le Contrat lie les parties.", "Article 1 – Définitions", "« Contrat » : la présente convention.",
                    "Article 2", "Les factures vont à l'Adresse de Facturation.",
                    "Article 9", "Les factures sont envoyées à compta@exemple.test (l'« Adresse de Facturation »).")
        self.assertEqual(categorie(a, "avant_definition"), ["Adresse de Facturation"])

    def test_non_definis_et_pieges(self):
        a = analyse(
            "Alpha Bêta SRL, rue du Moulin 12 à 4000 Liège, représentée par Madame Claire Dumont (ci-après « le Client »).",
            "Le Client respecte le Calendrier de Livraison et les Spécifications Techniques de l'Annexe 1.",
            "Le droit belge s'applique ; le Tribunal de l'entreprise de Liège est compétent, conformément au Code civil.",
            "La Banque-Carrefour des Entreprises, la TVA et le Règlement (UE) 2016/679 ne sont pas des termes.",
            "Les activités en Belgique et au Grand-Duché de Luxembourg, et l'Alpha Bêta SRL elle-même, non plus.",
            "Les obligations courent pendant quinze Jours Ouvrables.")
        self.assertEqual(categorie(a, "non_defini"), ["Calendrier de Livraison", "Jours Ouvrables", "Spécifications Techniques"])

    def test_cle(self):
        self.assertEqual(cle("les Jours Ouvrables"), cle("Jour Ouvrable"))
        self.assertEqual(cle("l'Adresse de Facturation"), cle("Adresse de facturation"))
        self.assertNotEqual(cle("Prix"), cle("Prix de Cession"))


if __name__ == "__main__":
    unittest.main()
