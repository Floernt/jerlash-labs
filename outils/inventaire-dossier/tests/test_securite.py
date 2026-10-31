"""Garanties : pas de réseau, pièces intactes, registre hors du dossier, entrées hostiles, registre lisible."""

import io
import os
import pathlib
import shutil
import socket
import tempfile
import unittest
import zipfile
from unittest import mock

import aide
from inventaire_dossier.__main__ import main as cli
from inventaire_dossier.lecture import lire_dossier


def interdit(*_a, **_k):
    raise AssertionError("tentative d'accès réseau")


def empreinte_du_dossier(dossier):
    return {nom: (pathlib.Path(dossier, nom).read_bytes(), os.stat(os.path.join(dossier, nom)).st_mtime_ns)
            for nom in os.listdir(dossier)}


class Garanties(unittest.TestCase):
    def test_parcours_complet_sans_reseau_et_pieces_intactes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dossier = os.path.join(tmp, "dossier")
            shutil.copytree(aide.PIECES, dossier)
            avant = empreinte_du_dossier(dossier)
            with mock.patch.object(socket.socket, "connect", interdit), \
                    mock.patch.object(socket, "create_connection", interdit), \
                    mock.patch.object(socket, "getaddrinfo", interdit):
                code = cli([dossier, "--sortie", os.path.join(tmp, "registres")])
            self.assertEqual(empreinte_du_dossier(dossier), avant)
            self.assertEqual(code, 1)  # le jeu contient des alertes
            self.assertEqual(len(os.listdir(os.path.join(tmp, "registres"))), 3)

    def test_registre_refuse_dans_le_dossier_inventorie(self):
        with tempfile.TemporaryDirectory() as tmp:
            dossier = os.path.join(tmp, "dossier")
            shutil.copytree(aide.PIECES, dossier)
            self.assertEqual(cli([dossier, "--sortie", os.path.join(dossier, "sous")]), 2)
            self.assertFalse(os.path.exists(os.path.join(dossier, "sous")))

    def test_aucun_registre_remplace(self):
        with tempfile.TemporaryDirectory() as tmp:
            sortie = os.path.join(tmp, "r")
            cli([aide.PIECES, "--sortie", sortie])
            cli([aide.PIECES, "--sortie", sortie])
            self.assertEqual(len(os.listdir(sortie)), 6)

    def test_aucun_module_reseau(self):
        self.assertEqual(aide.auditer_imports(aide.SRC), [])
        self.assertEqual(aide.auditer_imports(aide.OUTIL, recursif=False), [])

    def test_fichiers_hostiles_non_lus_sans_planter(self):
        with tempfile.TemporaryDirectory() as tmp:
            sortie = io.BytesIO()
            with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr("word/document.xml", '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e "x">]><w:document '
                           'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
            pathlib.Path(tmp, "piege.docx").write_bytes(sortie.getvalue())
            sortie = io.BytesIO()
            with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr("word/document.xml", b" " * (20 * 1024 * 1024))
            pathlib.Path(tmp, "bombe.docx").write_bytes(sortie.getvalue())
            pathlib.Path(tmp, "faux.docx").write_bytes(b"pas un zip")
            pathlib.Path(tmp, "~$verrou.docx").write_bytes(b"x")
            pieces, ignores = lire_dossier(tmp)
        self.assertEqual(ignores, ["~$verrou.docx (fichier technique)"])
        self.assertTrue(all(p.texte is None and p.non_lu for p in pieces), [(p.chemin, p.non_lu) for p in pieces])


if __name__ == "__main__":
    unittest.main()
