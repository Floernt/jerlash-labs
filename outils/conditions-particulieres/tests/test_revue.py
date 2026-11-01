"""Un test par défaut relevé lors de la relecture indépendante du 2026-11-01 (verifications/2026-11-01-revue.md)."""

import os
import pathlib
import tempfile
import time
import unittest
from unittest import mock

import aide  # noqa: F401
from conditions_particulieres.__main__ import ecrire_rapport
from conditions_particulieres.analyse import RE_MONTANT, RE_QUANTITE, analyser, detecter
from conditions_particulieres.lecture import Document, Paragraphe

COMPARUTION = "Entre Alpha SRL, rue Haute 5, 4000 Liège, et Bêta SA."


def analyse(*lignes, numerotes=()):
    return analyser(Document("t.docx", [Paragraphe(l, numerote=l in numerotes) for l in lignes]))


def classes(a):
    return {b.titre: b.classement for b in a.blocs}


def categories(texte, noms=()):
    return [d.categorie for d in detecter(texte, 0, list(noms))]


class FauxNegatifs(unittest.TestCase):
    def test_b1_montants_et_dates_belges(self):
        for texte in ("EUR 12.500", "EUR 12500", "12.500,- EUR", "1,5 million d'euros", "12k€", "USD 10.000", "10.000 USD",
                      "12 500 € HTVA", "1.250,00 €"):
            with self.subTest(texte):
                self.assertEqual(categories(f"Le plafond est de {texte}."), ["MONTANT"])
        for texte in ("le premier mars deux mille vingt-six", "le 1/3/26", "en mars 2026", "le 2026-03-01", "le 01.03.2026"):
            with self.subTest(texte):
                self.assertEqual(categories(f"Le contrat prend fin {texte}."), ["DATE"])
        self.assertEqual(categories("conformément à la loi du 2 août 2002"), [])

    def test_b2_nom_propage_apres_entre(self):
        a = analyse("Entre Brasserie du Condroz SRL, dont le siège est établi à Ciney, et Bêta SA (ci-après « BDC »).",
                    "Article 5 – Confidentialité", "Brasserie du Condroz ne divulgue aucune information.",
                    "Article 6 – Responsabilité", "BRASSERIE DU CONDROZ et BDC répondent de leurs préposés.",
                    "Article 7 – Divers", "Alpha et Bêta restent tenus.")
        self.assertEqual(classes(a)["Article 5 – Confidentialité"], "mixte")
        self.assertEqual(classes(a)["Article 6 – Responsabilité"], "mixte")
        self.assertNotIn("Entre", " ".join(d.texte for d in a.blocs[0].donnees))

    def test_b3_donnees_dans_l_intitule_et_clause_en_capitales(self):
        a = analyse(COMPARUTION, "Article 2 – Garantie de 12.500 euros consentie par Jean-Marc Lenoir SRL",
                    "La garantie est irrévocable.", "Article 7 – Responsabilité",
                    "LA RESPONSABILITÉ DE BÊTA EST LIMITÉE À 12.500 EUROS PAR SINISTRE ENVERS ALPHA SRL, SAUF FAUTE LOURDE.")
        self.assertEqual(classes(a)["Article 2 – Garantie de 12.500 euros consentie par Jean-Marc Lenoir SRL"], "mixte")
        self.assertEqual(classes(a)["Article 7 – Responsabilité"], "mixte")

    def test_b4_signatures_en_capitales(self):
        a = analyse(COMPARUTION, "Article 1 – Objet", "La vente.", "Fait à Liège, le 1er mars 2026.",
                    "POUR LE FOURNISSEUR", "Jean Dupont, gérant", "POUR LE CLIENT", "Annexe 1 – Tarifs", "Bouteille : 1,20 €")
        self.assertEqual([b.titre for b in a.blocs][-2:], ["signatures", "Annexe 1 – Tarifs"])

    def test_b5_prix_sans_donnee_reconnue(self):
        a = analyse(COMPARUTION, "Article 3 – Prix", "Le prix est fixé à l'annexe 2.")
        self.assertEqual(classes(a)["Article 3 – Prix"], "particulieres")

    def test_c1_identifiants(self):
        for texte in ("be71 0961 2345 6769", "BE71-0961-2345-6769", "712.345.630", "0475123456", "commande n° 4500012345",
                      "dossier n° 2025/123", "référence dossier 25-0412", "TVA BE0712345630"):
            with self.subTest(texte):
                self.assertEqual(categories(f"Voir {texte}."), ["IDENTIFIANT"])

    def test_c2_adresses(self):
        for texte in ("Rue de la Loi, 16 à Bruxelles", "Rue de la Loi, 16, 1000 Bruxelles", "Mont des Arts 1, 1000 Bruxelles",
                      "Steenweg op Brussel 10, 3000 Leuven", "Kerkstraat 10, 9000 Gent", "Avenue Louise 54 bte 3, 1050 Ixelles"):
            with self.subTest(texte):
                self.assertEqual(categories(f"Les notifications sont faites {texte}."), ["ADRESSE"])

    def test_c3_formes_sociales_et_societe_nommee(self):
        for texte in ("Acme srl", "ACME s.r.l.", "Acme S.R.L.", "la société Hesbaye Logistique"):
            with self.subTest(texte):
                self.assertEqual(categories(f"Toute réclamation est adressée à {texte}."), ["PARTIE"])
        self.assertEqual(categories("Le Prestataire et sa sous-traitante."), [])

    def test_c4_date_d_une_convention_entre_parties(self):
        self.assertEqual(categories("la convention du 12 janvier 2025 et le jugement du 4 mars 2025"), ["DATE", "DATE"])

    def test_c7_intitules_et_signatures(self):
        a = analyse(COMPARUTION, "Article 1 – Objet", "La vente.", "Article 4bis – Résiliation", "Chaque partie peut résilier.",
                    "§ 5. Droit applicable", "Le droit belge.", "7) Juridiction", "Les tribunaux de Liège.",
                    "Établi à Liège, le 1er mars 2026.")
        self.assertEqual([b.titre for b in a.blocs], ["comparution", "Article 1 – Objet", "Article 4bis – Résiliation",
                                                      "§ 5. Droit applicable", "7) Juridiction", "signatures"])
        self.assertEqual(classes(a)["7) Juridiction"], "generales")

    def test_c8_clause_generale_avec_mot_de_l_operation(self):
        a = analyse(COMPARUTION, "Article 4 – Obligations des parties", "Chaque partie collabore.", "Elle informe l'autre.",
                    "Elle respecte les délais.", "Une pénalité de 500 euros est due par jour de retard.")
        self.assertEqual(classes(a)["Article 4 – Obligations des parties"], "mixte")


class Temps(unittest.TestCase):
    def test_c5_groupes_de_chiffres_sans_fin(self):
        texte = "100 " * 64000
        debut = time.perf_counter()
        list(RE_MONTANT.finditer(texte))
        list(RE_QUANTITE.finditer(texte))
        detecter(texte, 0, [])
        self.assertLess(time.perf_counter() - debut, 3)

    def test_c6_nombreux_noms(self):
        lignes = [f"Entre Societe{i} Nom{i} SRL et autre." for i in range(1000)]
        debut = time.perf_counter()
        analyser(Document("x", [Paragraphe(l) for l in lignes]))
        self.assertLess(time.perf_counter() - debut, 5)


class Sorties(unittest.TestCase):
    def test_m2_pas_de_rapport_incomplet(self):
        a = analyse(COMPARUTION, "Article 1 – Objet", "La vente.")
        vrai_open = open

        def echoue_au_json(chemin, *args, **kwargs):
            if str(chemin).endswith(".json"):
                raise OSError("disque plein")
            return vrai_open(chemin, *args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("builtins.open", echoue_au_json), self.assertRaises(OSError):
                ecrire_rapport(a, tmp)
            self.assertEqual(os.listdir(tmp), [])
            pathlib.Path(tmp, "Conditions - t.docx").write_bytes(b"")
            self.assertEqual(len(ecrire_rapport(a, tmp)), 3)


if __name__ == "__main__":
    unittest.main()
