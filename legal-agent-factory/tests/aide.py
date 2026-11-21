"""Outils communs aux tests : dossiers temporaires et fixtures synthétiques."""

import os
import shutil
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RACINE not in sys.path:
    sys.path.insert(0, RACINE)

FIXTURES = os.path.join(RACINE, "tests", "fixtures")


def fixture(nom: str) -> str:
    return os.path.join(FIXTURES, nom)


class CasAvecDossiers(unittest.TestCase):
    def setUp(self):
        self.racine = tempfile.mkdtemp(prefix="laf-test-")
        self.entree, self.sortie, self.etat = (os.path.join(self.racine, n) for n in ("entree", "sortie", "etat"))
        for d in (self.entree, self.sortie, self.etat):
            os.makedirs(d)

    def tearDown(self):
        shutil.rmtree(self.racine, ignore_errors=True)

    def deposer(self, nom: str, contenu: bytes | str) -> str:
        chemin = os.path.join(self.entree, nom)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "wb") as f:
            f.write(contenu.encode("utf-8") if isinstance(contenu, str) else contenu)
        return chemin

    def deposer_fixture(self, nom_fixture: str, nom: str | None = None) -> str:
        with open(fixture(nom_fixture), "rb") as f:
            return self.deposer(nom or nom_fixture, f.read())
