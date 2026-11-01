"""Garanties : pas de réseau, contrat intact, rapport jamais remplacé, entrées hostiles, temps borné, rapport lisible."""

import io
import os
import pathlib
import shutil
import socket
import tempfile
import time
import unittest
import zipfile
import xml.etree.ElementTree as ET
from unittest import mock

import aide
from conditions_particulieres.__main__ import main as cli
from conditions_particulieres.analyse import analyser, detecter
from conditions_particulieres.lecture import Document, ErreurLecture, Paragraphe, lire_contrat
from conditions_particulieres.rapport import en_docx, en_json, en_markdown

CONTRAT = os.path.join(aide.PIECES, "Contrat de fourniture - Brasserie du Condroz.docx")


def interdit(*_a, **_k):
    raise AssertionError("tentative d'accès réseau")


def zip_avec(nom: str, contenu: bytes) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(nom, contenu)
    return sortie.getvalue()


class Garanties(unittest.TestCase):
    def test_parcours_complet_sans_reseau_et_contrat_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            contrat = shutil.copy(CONTRAT, tmp)
            avant = (pathlib.Path(contrat).read_bytes(), os.stat(contrat).st_mtime_ns)
            with mock.patch.object(socket.socket, "connect", interdit), \
                    mock.patch.object(socket, "create_connection", interdit), \
                    mock.patch.object(socket, "getaddrinfo", interdit):
                code = cli([contrat, "--sortie", os.path.join(tmp, "rapports")])
            self.assertEqual((pathlib.Path(contrat).read_bytes(), os.stat(contrat).st_mtime_ns), avant)
            self.assertEqual(code, 1)   # le contrat contient des clauses mixtes
            self.assertEqual(len(os.listdir(os.path.join(tmp, "rapports"))), 3)

    def test_aucun_rapport_remplace_et_numero_commun(self):
        with tempfile.TemporaryDirectory() as tmp:
            cli([CONTRAT, "--sortie", tmp])
            cli([CONTRAT, "--sortie", tmp])
            noms = sorted(os.listdir(tmp))
            self.assertEqual(len(noms), 6)
            self.assertEqual(sum(" (2)." in n for n in noms), 3)

    def test_aucun_module_reseau(self):
        self.assertEqual(aide.auditer_imports(aide.SRC), [])
        self.assertEqual(aide.auditer_imports(aide.OUTIL, recursif=False), [])

    def test_fichiers_hostiles_refuses_proprement(self):
        cas = {
            "entites.docx": zip_avec("word/document.xml", b'<?xml version="1.0"?><!DOCTYPE d [<!ENTITY a "aaaa">]><d>&a;</d>'),
            "bombe.docx": zip_avec("word/document.xml", b"<a>" + b" " * 50_000_000 + b"</a>"),
            "faux.docx": b"ceci n'est pas un zip",
            "sans_corps.docx": zip_avec("autre.xml", b"<a/>"),
            "binaire.txt": b"abc\x00def",
            "contrat.pdf": b"%PDF-1.4",
        }
        with tempfile.TemporaryDirectory() as tmp:
            for nom, donnees in cas.items():
                chemin = os.path.join(tmp, nom)
                pathlib.Path(chemin).write_bytes(donnees)
                with self.subTest(nom):
                    debut = time.monotonic()
                    with self.assertRaises(ErreurLecture):
                        lire_contrat(chemin)
                    self.assertLess(time.monotonic() - debut, 5)
                    self.assertEqual(cli([chemin, "--liste"]), 2)

    def test_temps_borne_sur_textes_hostiles(self):
        for texte in ("A" * 20000, "1" * 20000, "1.000 " * 5000, "rue " * 5000 + "12", "Madame " * 5000,
                      "x@" * 10000, "BE71 " * 5000, "dix " * 5000 + "euros", "le 1er " * 5000, "a.b@c." * 5000):
            debut = time.perf_counter()
            detecter(texte, 0, ["Claire Dumont"])
            self.assertLess(time.perf_counter() - debut, 2, repr(texte[:20]))

    def test_contrat_long(self):
        lignes = ["Entre Alpha SRL, rue Haute 5, 4000 Liège, et Bêta SA."]
        for n in range(1, 301):
            lignes += [f"Article {n} – Paiement", f"Le montant de {n}.000 euros est payé le 1er mars 2026 sur le compte "
                       "BE71 0961 2345 6769 de Madame Claire Dumont, rue Haute 5, 4000 Liège."] * 1
            lignes += ["Chaque partie respecte ses obligations dans les trente jours."] * 10
        debut = time.perf_counter()
        analyser(Document("long.docx", [Paragraphe(l) for l in lignes]))
        self.assertLess(time.perf_counter() - debut, 10)

    def test_rapport_word_valide_malgre_caracteres_interdits(self):
        a = analyser(Document("c\x01\udcff.docx", [Paragraphe("Entre Alpha\x0b SRL et Bêta SA, <img src=x> ![i](https://x.test)"),
                                                   Paragraphe("Article 1 – Paiement"), Paragraphe("Compte BE71 0961 2345 6769 \x02.")]))
        with zipfile.ZipFile(io.BytesIO(en_docx(a))) as z:
            ET.fromstring(z.read("word/document.xml"))
        md = en_markdown(a)
        self.assertNotIn("<img", md)
        self.assertNotIn("![", md)
        en_json(a)


if __name__ == "__main__":
    unittest.main()
