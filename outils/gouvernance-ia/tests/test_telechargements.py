"""Contrôles des téléchargements de « Gouvernance de l'IA ».

    cd outils/gouvernance-ia && python -m unittest discover -s tests -v

Les fichiers sont construits en mémoire : rien n'est écrit dans le dépôt.
"""

import importlib.util
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO
from pathlib import Path

OUTIL = Path(__file__).resolve().parents[1]
SCRIPT = OUTIL / "telechargements" / "generer_telechargements.py"

_spec = importlib.util.spec_from_file_location("generer_telechargements", SCRIPT)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

PRODUITS = gen.generer()
VERSION = gen.json.loads(gen.REFERENTIEL.read_text(encoding="utf-8"))["version"]


def entrees(nom):
    return zipfile.ZipFile(BytesIO(PRODUITS[nom]))


class Reproductibilite(unittest.TestCase):
    def test_deux_constructions_donnent_les_memes_octets(self):
        self.assertEqual(PRODUITS, gen.generer())

    def test_dates_et_systeme_fixes(self):
        for nom in PRODUITS:
            if not nom.endswith((".zip", ".docx")):
                continue
            with self.subTest(fichier=nom):
                for info in entrees(nom).infolist():
                    self.assertEqual(info.date_time, gen.DATE_ZIP)
                    self.assertEqual(info.create_system, 3)

    def test_entrees_triees(self):
        for nom in PRODUITS:
            if not nom.endswith(".zip"):
                continue
            noms = entrees(nom).namelist()
            self.assertEqual(noms, sorted(noms), nom)


class Pack(unittest.TestCase):
    attendus = {
        "fr": (f"gouvernance-ia-{VERSION}.zip", "LISEZ-MOI.md", "kit-petit-cabinet",
               f"gouvernance-ia-charte-modele-{VERSION}.docx"),
        "en": (f"ai-governance-{VERSION}.zip", "READ-ME.md", "small-firm-kit",
               f"ai-governance-model-charter-{VERSION}.docx"),
    }

    def test_le_pack_contient_les_dix_pages_le_kit_la_charte_et_le_tableur(self):
        for langue, (archive, lisez_moi, kit, charte) in self.attendus.items():
            with self.subTest(langue=langue):
                prefixe = archive[:-4] + "/"
                noms = entrees(archive).namelist()
                pages = [n for n in noms if n.startswith(prefixe + "pages/")]
                self.assertEqual(len(pages), 10)
                self.assertIn(prefixe + lisez_moi, noms)
                self.assertIn(prefixe + "LICENCE.txt", noms)
                self.assertIn(prefixe + charte, noms)
                self.assertIn(prefixe + f"tableur/gouvernance-ia-matrices-{VERSION}.xlsx", noms)
                self.assertIn(prefixe + "referentiel/gouvernance-ia.json", noms)
                self.assertEqual(len([n for n in noms if n.startswith(prefixe + kit + "/")]), 9)
                self.assertEqual(len([n for n in noms if n.startswith(prefixe + "registres/")]), 4)

    def test_les_liens_des_pages_sont_utilisables_hors_du_site(self):
        for archive, *_ in self.attendus.values():
            z = entrees(archive)
            for nom in z.namelist():
                if not nom.endswith(".md"):
                    continue
                for lien in re.findall(r"\]\(([^)]+)\)", z.read(nom).decode("utf-8")):
                    self.assertTrue(lien.startswith(("http", "#")), f"{nom} : {lien}")

    def test_les_pages_portent_leur_titre(self):
        z = entrees(f"gouvernance-ia-{VERSION}.zip")
        page = z.read(f"gouvernance-ia-{VERSION}/pages/02-niveau-1.md").decode("utf-8")
        self.assertTrue(page.startswith("# Le niveau 1\n"))
        self.assertNotIn("draft:", page)


class Kit(unittest.TestCase):
    def test_les_six_elements_sont_la(self):
        for langue in ("fr", "en"):
            nom = gen.LANGUES[langue]["kit"].format(v=VERSION)
            noms = entrees(nom).namelist()
            with self.subTest(langue=langue):
                for numero in range(1, 7):
                    fichier = gen.NOMS_KIT[langue][numero]
                    self.assertIn(f"{nom[:-4]}/{fichier}", noms)

    def test_les_formulaires_sont_vides(self):
        for langue in ("fr", "en"):
            nom = gen.LANGUES[langue]["kit"].format(v=VERSION)
            z = entrees(nom)
            for fichier in z.namelist():
                if fichier.endswith(".csv"):
                    with self.subTest(fichier=fichier):
                        self.assertEqual(len(z.read(fichier).decode("utf-8").strip().split("\n")), 1)


class Registres(unittest.TestCase):
    def test_entetes_seules_et_colonnes_du_referentiel(self):
        ref = gen.json.loads(gen.REFERENTIEL.read_text(encoding="utf-8"))
        z = entrees(f"gouvernance-ia-{VERSION}.zip")
        prefixe = f"gouvernance-ia-{VERSION}/registres/"
        for fichier, colonnes in (("REGISTRE_INCIDENTS.csv", ref["registres"]["incidents"]),
                                  ("REGISTRE_HOMOLOGATIONS.csv", ref["registres"]["homologations"])):
            contenu = z.read(prefixe + fichier).decode("utf-8")
            self.assertEqual(contenu, ";".join(colonnes) + "\n")


class Charte(unittest.TestCase):
    def test_le_docx_a_les_parties_attendues_et_un_xml_valide(self):
        for langue in ("fr", "en"):
            nom = gen.LANGUES[langue]["charte"].format(v=VERSION)
            z = entrees(nom)
            with self.subTest(langue=langue):
                for partie in ("[Content_Types].xml", "_rels/.rels", "word/document.xml",
                               "word/_rels/document.xml.rels", "word/styles.xml"):
                    self.assertIn(partie, z.namelist())
                for partie in z.namelist():
                    ET.fromstring(z.read(partie))

    def test_les_seize_articles_sont_dans_le_document(self):
        z = entrees(gen.LANGUES["fr"]["charte"].format(v=VERSION))
        document = z.read("word/document.xml").decode("utf-8")
        for numero in range(1, 17):
            self.assertIn(f"Article {numero}.", document)
        self.assertIn("CC BY-NC 4.0", document)

    def test_aucun_lien_markdown_ne_subsiste(self):
        for langue in ("fr", "en"):
            document = entrees(gen.LANGUES[langue]["charte"].format(v=VERSION)).read("word/document.xml").decode("utf-8")
            self.assertNotRegex(document, r"\]\(")
            self.assertNotIn("**", document)


class Pages(unittest.TestCase):
    def test_un_intertitre_disparu_arrete_la_construction(self):
        page = gen.lire_pages("fr")["niveau-1"]
        with self.assertRaises(SystemExit):
            page.section("Intertitre qui n'existe pas")


if __name__ == "__main__":
    unittest.main()
