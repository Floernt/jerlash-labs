"""Un test par défaut relevé lors de la relecture indépendante du 2026-11-01 (verifications/2026-11-01-revue.md)."""

import io
import os
import pathlib
import sys
import tempfile
import time
import unittest
import zipfile
from unittest import mock

import aide  # noqa: F401
from glossaire_definitions.__main__ import main as cli
from glossaire_definitions.analyse import RE_SOCIETE, analyser
from glossaire_definitions.lecture import Document, ErreurLecture, Paragraphe, lire_contrat, lire_texte
from glossaire_definitions.rapport import en_markdown

NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def p(texte, num=False, style=None):
    ppr = ""
    if num or style:
        ppr = ("<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "")
               + ('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>' if num else "") + "</w:pPr>")
    return f'<w:p>{ppr}<w:r><w:t xml:space="preserve">{texte}</w:t></w:r></w:p>'


def lire_docx(corps: str):
    with tempfile.TemporaryDirectory() as tmp:
        chemin = os.path.join(tmp, "c.docx")
        tampon = io.BytesIO()
        with zipfile.ZipFile(tampon, "w") as z:
            z.writestr("word/document.xml", f"<w:document {NS}><w:body>{corps}</w:body></w:document>".encode())
        pathlib.Path(chemin).write_bytes(tampon.getvalue())
        return analyser(lire_contrat(chemin))


def analyse(*lignes, tableau=None):
    paragraphes = [Paragraphe(l) for l in lignes]
    for r, rangee in enumerate(tableau or []):
        paragraphes += [Paragraphe(c, (0, r, i)) for i, c in enumerate(rangee)]
    return analyser(Document("t.docx", paragraphes))


def categorie(a, nom):
    return sorted(c.forme for c in a.du_type(nom))


class Temps(unittest.TestCase):
    def test_c1_mot_en_capitales(self):
        debut = time.perf_counter()
        list(RE_SOCIETE.finditer("A" * 20000))
        analyse("Le Contrat " + "A" * 20000)
        self.assertLess(time.perf_counter() - debut, 1)

    def test_m2_nombreuses_citations(self):
        texte = " ".join(f"« Terme {i} » est cité." for i in range(4000))
        debut = time.perf_counter()
        analyse("Article 2 – Objet", texte)
        self.assertLess(time.perf_counter() - debut, 2)

    def test_c2_contrat_long(self):
        mots = ["Cession", "Garantie", "Action", "Prix", "Société", "Compte", "Dette", "Passif", "Actif", "Bilan"]
        termes = sorted({f"{a} {b}" for a in mots for b in mots if a != b})[:80]
        lignes = ["Article 1 – Définitions"] + [f"« {t} » désigne la chose {i}." for i, t in enumerate(termes)]
        lignes += [f"{i}.1 Le {termes[i % 80]} et la {termes[(i * 7) % 80]} sont dus, sans préjudice du {termes[(i * 3) % 80]}."
                   for i in range(3000)]
        debut = time.perf_counter()
        analyse(*lignes)
        self.assertLess(time.perf_counter() - debut, 5)


class Word(unittest.TestCase):
    def test_c3_deplacement_suivi_lu_une_fois(self):
        a = lire_docx(p("Article 1 – Définitions")
                      + f'<w:p><w:moveFrom w:id="1" w:author="x"><w:r><w:t>« Prix » : le prix convenu.</w:t></w:r></w:moveFrom></w:p>'
                      + f'<w:p><w:moveTo w:id="2" w:author="x"><w:r><w:t>« Prix » : le prix convenu.</w:t></w:r></w:moveTo></w:p>'
                      + p("Article 2 – Paiement") + p("Le Prix est payé comptant."))
        self.assertEqual(a.constats, [])

    def test_m6_zone_de_texte_lue_a_part(self):
        zone = ('<w:r><mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
                '<mc:Choice Requires="wps"><w:drawing><w:txbxContent>' + p("« Prix » : le prix convenu.")
                + '</w:txbxContent></w:drawing></mc:Choice><mc:Fallback><w:pict><w:txbxContent>'
                + p("« Prix » : le prix convenu.") + '</w:txbxContent></w:pict></mc:Fallback></mc:AlternateContent></w:r>')
        a = lire_docx(p("Article 1 – Définitions") + f"<w:p>{zone}</w:p>" + p("Article 2 – Paiement") + p("Le Prix est dû."))
        self.assertEqual([t.forme for t in a.termes], ["Prix"])
        self.assertEqual(len(a.termes[0].emplois), 1)
        self.assertEqual(a.constats, [])

    def test_c4_titres_numerotes_automatiquement(self):
        a = lire_docx(p("Définitions", num=True) + p("Fonds de Commerce : le fonds exploité.")
                      + p("Objet", num=True) + p("Le Fonds de Commerce est cédé."))
        self.assertEqual([t.forme for t in a.termes], ["Fonds de Commerce"])
        self.assertIn("« Objet »", a.lieux)
        self.assertEqual(a.constats, [])

    def test_c4_titres_numerotes_a_la_main_et_style(self):
        a = analyse("1. Définitions", "Fonds de Commerce : le fonds exploité.", "2. Objet",
                    "2.1 Le Fonds de Commerce est cédé. Lieu de Livraison : le siège.")
        self.assertEqual([t.forme for t in a.termes], ["Fonds de Commerce"])
        self.assertIn("article 2", a.lieux)
        b = lire_docx(p("Définitions et interprétation", style="Heading1") + p("Prix : le prix.")
                      + p("Paiement", style="Titre1") + p("Le Prix est payé."))
        self.assertEqual(b.constats, [])

    def test_m4_imbrication_excessive(self):
        corps = "<w:sdt><w:sdtContent>" * 3000 + p("x") + "</w:sdtContent></w:sdt>" * 3000
        with self.assertRaises(ErreurLecture):
            lire_docx(corps)


class Formules(unittest.TestCase):
    def test_c5_formules_belges(self):
        for phrase in ("Par « Données », il faut entendre toute information transmise.",
                       "Il y a lieu d'entendre par « Données » toute information transmise.",
                       "Par « Données », on entend toute information transmise.",
                       "Toute information transmise, ci-après désignée par « les Données », reste confidentielle."):
            with self.subTest(phrase):
                a = analyse("Article 3 – Confidentialité", phrase, "Les Données restent secrètes.")
                self.assertEqual([t.forme for t in a.termes], ["Données"])

    def test_c6_pluriels_en_aux(self):
        a = analyse("Article 1 – Définitions", "« Accord Commercial » : tout accord conclu avec un client.",
                    "« Locaux » : les bureaux loués.", "« Bureau » : le siège.", "Article 2 – Cession",
                    "Les Accords Commerciaux sont cédés ; le Local du rez-de-chaussée et les Bureaux aussi.")
        self.assertEqual(categorie(a, "inutilise"), [])
        self.assertEqual(categorie(a, "non_defini"), [])

    def test_c7_ligne_courte_sans_point(self):
        a = analyse("Article 1 – Définitions", "« Prix » : le prix.", "« Garant » : la caution.", "Article 2 – Paiement",
                    "Le Prix est payable comptant", "Pour le Garant")
        self.assertEqual(categorie(a, "inutilise"), [])

    def test_c8_tableau_a_trois_colonnes(self):
        a = analyse("Annexe A – Définitions", "Les Garanties courent jusqu'à la Date de Closing.",
                    tableau=[["N°", "Terme", "Définition"], ["1", "Date de Closing", "le 30 juin."],
                             ["2", "Garanties", "les garanties de l'article 5."]])
        self.assertEqual(sorted(t.forme for t in a.termes), ["Date de Closing", "Garanties"])
        self.assertEqual(a.constats, [])

    def test_m7_renvoi_a_un_intitule(self):
        a = analyse("Article 4 – Obligations", "Les obligations visées à l'article 7 (« Confidentialité ») survivent.")
        self.assertEqual(a.termes, [])

    def test_m8_singulier_et_pluriel_sur_deux_lignes(self):
        a = analyse("Article 1 – Définitions", "« Partie » : chacun des signataires.", "« Parties » : les signataires.",
                    "Article 2", "Chaque Partie signe.")
        self.assertEqual(categorie(a, "divergent") + categorie(a, "doublon"), [])


class Sorties(unittest.TestCase):
    def test_m1_limite_de_taille_sur_un_seul_paragraphe(self):
        with self.assertRaises(ErreurLecture):
            lire_texte(("x " * 1_100_000).encode())

    def test_m5_utf16_tronque(self):
        donnees = "﻿« Prix » : le prix.".encode("utf-16-le")
        self.assertTrue(lire_texte(b"\xff\xfe" + donnees[2:] + b"\x41"))

    def test_m9_meme_numero_et_markdown_neutralise(self):
        with tempfile.TemporaryDirectory() as tmp:
            contrat = os.path.join(tmp, "Bail.txt")
            pathlib.Path(contrat).write_text('Article 1 – Définitions\n« Prix » : le prix <img src="https://x.test/p.png"> '
                                             '![x](https://x.test/i.png).\nLe Prix.\n', encoding="utf-8")
            sortie = os.path.join(tmp, "r")
            os.makedirs(sortie)
            pathlib.Path(sortie, "Glossaire - Bail.docx").write_bytes(b"")
            cli([contrat, "--sortie", sortie])
            self.assertEqual(sorted(os.listdir(sortie)), ["Glossaire - Bail (2).docx", "Glossaire - Bail (2).json",
                                                          "Glossaire - Bail (2).md", "Glossaire - Bail.docx"])
            md = pathlib.Path(sortie, "Glossaire - Bail (2).md").read_text(encoding="utf-8")
            self.assertNotIn("<img", md)
            self.assertNotIn("![", md)

    @unittest.skipUnless(sys.platform == "win32", "os.startfile : Windows")
    def test_c9_rapport_introuvable_signale(self):
        try:
            import tkinter as tk
            racine = tk.Tk()
        except Exception as e:
            self.skipTest(f"fenêtre indisponible : {e}")
        racine.withdraw()
        try:
            from glossaire_definitions.interface import Application
            app = Application(racine)
            app.rapport = os.path.join(tempfile.gettempdir(), "rapport-inexistant-p02.docx")
            with mock.patch("tkinter.messagebox.showerror") as erreur:
                app.ouvrir()
            erreur.assert_called_once()
        finally:
            racine.destroy()


if __name__ == "__main__":
    unittest.main()
