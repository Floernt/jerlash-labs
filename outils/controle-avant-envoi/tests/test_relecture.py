"""Non-régression : défauts relevés par la relecture indépendante du 2026-10-31.

Chaque test reproduit un cas où la version initiale concluait à tort « rien détecté »
ou s'arrêtait sur une exception.
"""

import io
import os
import tempfile
import unittest
import zipfile

import aide
from controle_avant_envoi.__main__ import ecrire
from controle_avant_envoi.analyse import analyser, charger_configuration
from test_securite import docx_avec

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
RT = R + "/"
PROPRE = os.path.join(aide.PIECES, "contrat-propre.docx")


def document(corps: str, ns_extra: str = "") -> str:
    return (f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="{W}" xmlns:r="{R}" {ns_extra}>'
            f"<w:body>{corps}<w:sectPr/></w:body></w:document>")


def rels(*extra: str) -> str:
    base = (f'<Relationship Id="rIdStyles" Type="{RT}styles" Target="styles.xml"/>'
            f'<Relationship Id="rIdSettings" Type="{RT}settings" Target="settings.xml"/>')
    return ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + base + "".join(extra) + "</Relationships>")


def para(texte: str, rpr: str = "", ppr: str = "") -> str:
    return (f"<w:p>{'<w:pPr>' + ppr + '</w:pPr>' if ppr else ''}<w:r>{'<w:rPr>' + rpr + '</w:rPr>' if rpr else ''}"
            f'<w:t xml:space="preserve">{texte}</w:t></w:r></w:p>')


class Cas(unittest.TestCase):
    def analyser(self, parties: dict, termes=(), donnees: bytes | None = None):
        cfg = charger_configuration()
        cfg["termes_sensibles"] = list(termes)
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "cas.docx")
            with open(chemin, "wb") as f:
                f.write(donnees if donnees is not None else docx_avec(parties))
            rapport = analyser(chemin, cfg)
        return rapport, {c.ident: c for c in rapport.controles}

    def assertDetecte(self, controles, ident, fragment=""):
        c = controles[ident]
        texte = "\n".join(f"{k.localisation} : {k.detail}" for k in c.constats)
        self.assertEqual(c.statut, "detecte", f"{ident} : {c.note}")
        self.assertIn(fragment, texte)


class LiensSensibles(Cas):
    def test_lien_relatif_vers_un_fichier(self):
        rapport, c = self.analyser({
            "word/document.xml": document(para("Voir la note.")),
            "word/_rels/document.xml.rels": rels(
                f'<Relationship Id="rL" Type="{RT}hyperlink" Target="../Clients/Dupont%20SA/note.docx" TargetMode="External"/>')})
        self.assertDetecte(c, "liens", "chemin local, réseau ou relatif")
        self.assertEqual(c["liens"].gravite, "a_examiner")
        self.assertEqual(rapport.niveau, "a_traiter")

    def test_serveur_intranet_a_nom_court(self):
        rapport, c = self.analyser({
            "word/document.xml": document(para("x")),
            "word/_rels/document.xml.rels": rels(
                f'<Relationship Id="rL" Type="{RT}hyperlink" Target="http://srv-dms/worksite/Dupont/123" TargetMode="External"/>')})
        self.assertDetecte(c, "liens", "serveur interne")
        self.assertEqual(rapport.niveau, "a_traiter")

    def test_lien_public_reste_information(self):
        _, c = self.analyser({
            "word/document.xml": document(para("x")),
            "word/_rels/document.xml.rels": rels(
                f'<Relationship Id="rL" Type="{RT}hyperlink" Target="https://www.ejustice.just.fgov.be/" TargetMode="External"/>')})
        self.assertEqual(c["liens"].gravite, "information")


class TermesSensibles(Cas):
    def test_trait_d_union_insecable(self):
        corps = '<w:p><w:r><w:t>Societe Dupont</w:t></w:r><w:r><w:noBreakHyphen/></w:r><w:r><w:t>Durand</w:t></w:r></w:p>'
        _, c = self.analyser({"word/document.xml": document(corps)}, termes=["Dupont-Durand"])
        self.assertDetecte(c, "termes", "Dupont-Durand")

    def test_apostrophe_typographique(self):
        _, c = self.analyser({"word/document.xml": document(para("Garage D’Ieteren"))}, termes=["D'Ieteren"])
        self.assertDetecte(c, "termes", "D'Ieteren")

    def test_code_de_champ(self):
        corps = ('<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve">'
                 ' HYPERLINK "file:///\\\\srv\\clients\\Dupont\\memo.docx" </w:instrText></w:r>'
                 '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>memo</w:t></w:r>'
                 '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        _, c = self.analyser({"word/document.xml": document(corps)}, termes=["Dupont"])
        self.assertDetecte(c, "termes", "Dupont")
        self.assertDetecte(c, "champs", "HYPERLINK")

    def test_texte_alternatif_d_image(self):
        corps = ('<w:p><w:r><w:drawing><wp:inline><wp:docPr id="1" name="Image" descr="Signature de Me Dupont"/>'
                 '</wp:inline></w:drawing></w:r></w:p>')
        ns = 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"'
        _, c = self.analyser({"word/document.xml": document(corps, ns)}, termes=["Dupont"])
        self.assertDetecte(c, "termes", "Dupont")

    def test_custom_xml_de_gestion_documentaire(self):
        _, c = self.analyser({"customXml/item1.xml": "<dms><client>Dupont SA</client><dossier>2026-0123</dossier></dms>"},
                             termes=["Dupont"])
        self.assertDetecte(c, "termes", "Dupont")

    def test_smartart(self):
        _, c = self.analyser({"word/diagrams/data1.xml": '<dgm:dataModel xmlns:dgm="urn:x"><dgm:t>Dupont</dgm:t></dgm:dataModel>'},
                             termes=["Dupont"])
        self.assertDetecte(c, "termes", "Dupont")


class ArchivesEndommagees(Cas):
    def test_crc_incorrecte(self):
        sortie = io.BytesIO()
        with zipfile.ZipFile(PROPRE) as source, zipfile.ZipFile(sortie, "w", zipfile.ZIP_STORED) as z:
            for info in source.infolist():
                z.writestr(info.filename, source.read(info.filename), compress_type=zipfile.ZIP_STORED)
        donnees = bytearray(sortie.getvalue())
        position = donnees.find(b"Article 1. Objet")
        donnees[position] = ord("B")  # contenu altéré, CRC inchangée
        rapport, _ = self.analyser({}, donnees=bytes(donnees))
        self.assertEqual(rapport.niveau, "erreur")
        self.assertEqual(rapport.code_sortie, 2)


class TexteMasqueHerite(Cas):
    STYLES = (f'<w:styles xmlns:w="{W}">'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              '<w:style w:type="character" w:styleId="Cache"><w:rPr><w:vanish/></w:rPr></w:style>'
              '<w:style w:type="character" w:styleId="CacheHerite"><w:basedOn w:val="Cache"/></w:style>'
              '<w:style w:type="character" w:styleId="Blanc"><w:rPr><w:color w:val="FFFFFF"/></w:rPr></w:style>'
              "</w:styles>")

    def test_style_de_caractere_herite(self):
        _, c = self.analyser({"word/styles.xml": self.STYLES,
                              "word/document.xml": document(para("secret", '<w:rStyle w:val="CacheHerite"/>'))})
        self.assertDetecte(c, "texte_masque", "Texte masqué (par style")

    def test_blanc_par_style(self):
        _, c = self.analyser({"word/styles.xml": self.STYLES,
                              "word/document.xml": document(para("invisible", '<w:rStyle w:val="Blanc"/>'))})
        self.assertDetecte(c, "texte_masque", "Texte écrit en blanc")

    def test_valeurs_par_defaut_du_document(self):
        styles = (f'<w:styles xmlns:w="{W}"><w:docDefaults><w:rPrDefault><w:rPr><w:vanish/></w:rPr></w:rPrDefault>'
                  "</w:docDefaults></w:styles>")
        _, c = self.analyser({"word/styles.xml": styles, "word/document.xml": document(para("tout est masqué"))})
        self.assertDetecte(c, "texte_masque", "valeurs par défaut")

    def test_annulation_explicite(self):
        _, c = self.analyser({"word/styles.xml": self.STYLES, "word/document.xml": document(
            para("visible", '<w:rStyle w:val="Cache"/><w:vanish w:val="0"/>'))})
        self.assertEqual(c["texte_masque"].statut, "non_detecte")


class ProprietesAilleurs(Cas):
    def test_proprietes_psmdcp(self):
        chemin = "package/services/metadata/core-properties/abc.psmdcp"
        core = ('<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>Anne Dupont</dc:creator></cp:coreProperties>')
        paquet = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  f'<Relationship Id="r1" Type="{RT}officeDocument" Target="word/document.xml"/>'
                  '<Relationship Id="r2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/'
                  f'core-properties" Target="/{chemin}"/></Relationships>')
        rapport, c = self.analyser({chemin: core, "_rels/.rels": paquet, "docProps/core.xml": None,
                                    "docProps/app.xml": None}, termes=["Dupont"])
        self.assertDetecte(c, "proprietes", "Anne Dupont")
        self.assertDetecte(c, "personnes", "Anne Dupont")
        self.assertDetecte(c, "termes", "Dupont")


class NomsDeRapport(unittest.TestCase):
    def test_deux_documents_de_meme_nom(self):
        with tempfile.TemporaryDirectory() as dossier:
            ecrits = set()
            a = ecrire(dossier, os.path.join("a", "contrat.docx"), "html", "A", ecrits)
            b = ecrire(dossier, os.path.join("b", "contrat.docx"), "html", "B", ecrits)
            self.assertNotEqual(a, b)
            with open(a, encoding="utf-8") as f:
                self.assertEqual(f.read(), "A")


class DeclarationsXml(Cas):
    def test_doctype_en_utf16(self):
        xml = ('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE d [<!ENTITY s "x">]>'
               f'<w:document xmlns:w="{W}"><w:body><w:p><w:r><w:t>&s;</w:t></w:r></w:p></w:body></w:document>')
        rapport, _ = self.analyser({"word/document.xml": xml.encode("utf-16")})
        self.assertEqual(rapport.niveau, "erreur")

    def test_doctype_apres_un_long_commentaire(self):
        xml = (f'<?xml version="1.0"?><!--{"x" * 5000}--><!DOCTYPE d SYSTEM "http://exemple.invalid/d.dtd">'
               f'<w:document xmlns:w="{W}"><w:body/></w:document>')
        rapport, _ = self.analyser({"word/document.xml": xml})
        self.assertEqual(rapport.niveau, "erreur")


class ObjetsEtChamps(Cas):
    def test_alt_chunk(self):
        _, c = self.analyser({
            "word/afchunk.htm": "<html><body>client Dupont accepterait 50.000</body></html>",
            "word/_rels/document.xml.rels": rels(f'<Relationship Id="rA" Type="{RT}aFChunk" Target="afchunk.htm"/>')},
            termes=["Inexistant"])
        self.assertDetecte(c, "objets", "altChunk")
        self.assertIn("non analysés", c["termes"].note)

    def test_champ_info(self):
        corps = f'<w:p><w:fldSimple w:instr=" INFO LastSavedBy "><w:r><w:t>Anne</w:t></w:r></w:fldSimple></w:p>'
        _, c = self.analyser({"word/document.xml": document(corps)})
        self.assertDetecte(c, "champs", "INFO")

    def test_macro_renommee(self):
        _, c = self.analyser({
            "word/code.bin": b"\x00" * 16,
            "word/_rels/document.xml.rels": rels(
                '<Relationship Id="rV" Type="http://schemas.microsoft.com/office/2006/relationships/vbaProject" '
                'Target="code.bin"/>')})
        self.assertDetecte(c, "macros", "code.bin")

    def test_commentaires_casse_et_orphelins(self):
        commentaire = (f'<w:comments xmlns:w="{W}"><w:comment w:id="0" w:author="X"><w:p><w:r><w:t>interne</w:t>'
                       "</w:r></w:p></w:comment></w:comments>")
        _, c = self.analyser({"word/Comments.xml": commentaire})
        self.assertDetecte(c, "commentaires", "interne")


class VerdictSansListe(Cas):
    def test_le_verdict_signale_l_absence_de_liste(self):
        rapport, _ = self.analyser({})
        self.assertEqual(rapport.niveau, "rien_detecte")
        self.assertIn("aucune liste de termes fournie", rapport.verdict)


if __name__ == "__main__":
    unittest.main()
