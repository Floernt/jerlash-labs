"""Garanties : réseau limité au fournisseur configuré, pièces intactes, registre hors du dossier,
entrées hostiles, registre lisible."""

import io
import os
import pathlib
import shutil
import tempfile
import unittest
import zipfile

import aide
from inventaire_dossier.lecture import lire_dossier


def empreinte_du_dossier(dossier):
    return {nom: (pathlib.Path(dossier, nom).read_bytes(), os.stat(os.path.join(dossier, nom)).st_mtime_ns)
            for nom in os.listdir(dossier)}


class Garanties(unittest.TestCase):
    def test_parcours_complet_reseau_limite_au_fournisseur_et_pieces_intactes(self):
        with tempfile.TemporaryDirectory() as tmp, aide.Fournisseur() as fournisseur:
            dossier = os.path.join(tmp, "dossier")
            shutil.copytree(aide.PIECES, dossier)
            avant = empreinte_du_dossier(dossier)
            with aide.reseau_local_seulement():
                code = aide.cli_ia([dossier, "--sortie", os.path.join(tmp, "registres")], fournisseur, tmp)
            self.assertEqual(empreinte_du_dossier(dossier), avant)
            self.assertEqual(code, 1)  # le jeu contient des alertes
            self.assertEqual(len(os.listdir(os.path.join(tmp, "registres"))), 3)
            self.assertEqual(len(fournisseur.recus), 1)  # un seul envoi pour tout le dossier

    def test_registre_refuse_dans_le_dossier_inventorie_avant_tout_envoi(self):
        with tempfile.TemporaryDirectory() as tmp, aide.Fournisseur() as fournisseur:
            dossier = os.path.join(tmp, "dossier")
            shutil.copytree(aide.PIECES, dossier)
            self.assertEqual(aide.cli_ia([dossier, "--sortie", os.path.join(dossier, "sous")], fournisseur, tmp), 2)
            self.assertFalse(os.path.exists(os.path.join(dossier, "sous")))
            self.assertEqual(fournisseur.recus, [])

    def test_aucun_registre_remplace(self):
        with tempfile.TemporaryDirectory() as tmp, aide.Fournisseur() as fournisseur:
            sortie = os.path.join(tmp, "r")
            aide.cli_ia([aide.PIECES, "--sortie", sortie], fournisseur, tmp)
            aide.cli_ia([aide.PIECES, "--sortie", sortie], fournisseur, tmp)
            self.assertEqual(len(os.listdir(sortie)), 6)

    def test_seul_le_connecteur_importe_des_modules_reseau(self):
        self.assertEqual(aide.auditer_imports(aide.SRC, exclus=("connecteur_ia",)), [])
        self.assertEqual(aide.auditer_imports(aide.OUTIL, recursif=False), [])
        reseau = aide.auditer_imports(os.path.join(aide.SRC, "connecteur_ia"))
        self.assertTrue(reseau and all(v.startswith("connecteur.py:") for v in reseau), reseau)

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
