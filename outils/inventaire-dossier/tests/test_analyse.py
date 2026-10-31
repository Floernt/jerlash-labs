"""Règles de classement, cas par cas, sur des pièces construites en mémoire."""

import unittest

import aide  # noqa: F401  (chemin vers src)
from inventaire_dossier.analyse import inventorier
from inventaire_dossier.lecture import Piece


def piece(nom, texte, format_=".docx", courriel=None):
    return Piece(nom, format_, len(texte), str(hash(nom)), "2026-10-31", texte=texte, courriel=courriel or {})


def fiche(inv, nom):
    return next(f for f in inv.fiches if f.piece.chemin == nom)


class Classement(unittest.TestCase):
    def test_intitule_et_statut(self):
        inv = inventorier(".", [
            piece("a.docx", "CONTRAT DE BAIL COMMERCIAL\n\nEntre Immo Sud SA et Café Central SRL.\n\n"
                            "Fait à Namur, le 3 mai 2024.\nPour Immo Sud SA : J. Martin (signé)"),
            piece("b.docx", "PROJET\nAVENANT N° 1 AU CONTRAT DE BAIL COMMERCIAL DU 3 MAI 2024\n"
                            "Entre Immo Sud SA et Café Central SRL.\nFait à ......, le ......"),
        ], [])
        a, b = fiche(inv, "a.docx"), fiche(inv, "b.docx")
        self.assertEqual((a.type, a.statut, a.date, a.fait_foi), ("contrat", "signé", "2024-05-03", True))
        self.assertEqual((b.type, b.statut, b.date, b.fait_foi), ("avenant", "projet", None, False))
        self.assertEqual(b.rattache_a, "a.docx")
        self.assertIn("avenant non signé", " ".join(inv.alertes))

    def test_sans_indice_le_statut_reste_a_verifier(self):
        inv = inventorier(".", [piece("x.docx", "CONVENTION DE COLLABORATION\nEntre Alpha SRL et Beta SA.")], [])
        self.assertEqual(fiche(inv, "x.docx").statut, "à vérifier")
        self.assertIn("statut à vérifier", " ".join(inv.alertes))

    def test_puce_qui_cite_un_avenant_ne_change_pas_le_type(self):
        inv = inventorier(".", [piece("notes réunion.txt", "Réunion du 2 juin 2025\n\n- Avenant 2 à revoir\n- Contrat à résilier", ".txt")], [])
        self.assertEqual(fiche(inv, "notes réunion.txt").type, "note interne")

    def test_modele_reconnu_a_ses_champs(self):
        inv = inventorier(".", [piece("Document1.docx", "CONTRAT\nENTRE [NOM] [FORME] et [NOM]\nPrix : [●] EUR\nDate : [●]")], [])
        self.assertEqual(fiche(inv, "Document1.docx").type, "modèle")

    def test_partie_d_un_courriel_reconnue_par_le_domaine(self):
        inv = inventorier(".", [
            piece("c.docx", "CONTRAT DE LICENCE\nEntre Logiciels Hesbaye SRL et Cabinet Comptable Mosan SA. (signé)"),
            piece("m.eml", "Objet : licence\n\nBonjour, voir notre contrat.", ".eml",
                  {"de": "a@logiciels-hesbaye.example", "a": "b@autre.example", "date": "2025-01-02", "objet": "licence"}),
        ], [])
        self.assertIn("Logiciels Hesbaye SRL", fiche(inv, "m.eml").parties)

    def test_piece_sans_partie_commune_signalee(self):
        inv = inventorier(".", [
            piece("1.docx", "CONTRAT\nEntre Alpha SRL et Beta SA. (signé)"),
            piece("2.docx", "AVENANT N° 1\nEntre Alpha SRL et Beta SA. (signé)"),
            piece("3.docx", "CONTRAT\nEntre Gamma SRL et Delta NV. (signé)"),
        ], [])
        self.assertTrue(any("3.docx" in a and "aucune partie commune" in a for a in inv.alertes))

    def test_piece_non_lue_jamais_devinee(self):
        p = Piece("Scan contrat signé.pdf", ".pdf", 10, "x", "2026-10-31", non_lu="PDF")
        f = fiche(inventorier(".", [p], []), "Scan contrat signé.pdf")
        self.assertEqual((f.type, f.statut, f.fait_foi, f.date), ("non lu", "inconnu", None, None))

    def test_doublons_signales(self):
        a = piece("a.docx", "CONTRAT\nEntre Alpha SRL et Beta SA. (signé)")
        b = piece("copie de a.docx", a.texte)
        b.sha256 = a.sha256
        self.assertTrue(any("même empreinte" in x for x in inventorier(".", [a, b], []).alertes))


if __name__ == "__main__":
    unittest.main()
