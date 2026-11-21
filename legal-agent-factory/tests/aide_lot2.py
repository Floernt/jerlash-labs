"""Outils des tests du Lot 2 : fixtures synthétiques et modèle à réponses enregistrées."""

import json
import os
import shutil

from aide import FIXTURES, CasAvecDossiers

from laf import courriel, securite
from laf.chaine import TAILLE_MAX_EXTRAIT
from laf.orchestrateur import ChaineLot2
from laf.passerelle import PasserelleEnregistree, cle_routage
from laf.runtime import ClientRuntime, demarrer_en_fond
from laf.surveillance import Surveillant

LOT2 = os.path.join(FIXTURES, "lot2")
REGISTRE_DOSSIERS = os.path.join(LOT2, "dossiers-synthetiques.json")
INTAKE, CLAIM = "be-bankruptcy-intake", "be-bankruptcy-claim-analysis"


def reponses() -> dict:
    with open(os.path.join(LOT2, "reponses-enregistrees.json"), encoding="utf-8") as f:
        return json.load(f)


def message(nom: str) -> dict:
    return courriel.lire(os.path.join(LOT2, "courriels", nom))


def chemin_depot(nom: str) -> str:
    return os.path.join(LOT2, "depots", nom)


def texte_de(cle: str) -> str:
    genre, nom = cle.split(":", 1)
    if genre == "courriel":
        return courriel.texte(message(nom))
    return securite.lire_texte(chemin_depot(nom), TAILLE_MAX_EXTRAIT)


def passerelle_enregistree() -> PasserelleEnregistree:
    r = reponses()
    routages = {cle_routage(securite.encadrer(texte_de(cle), TAILLE_MAX_EXTRAIT)): dict(r["defaut"], **partiel)
                for cle, partiel in r["routages"].items()}
    return PasserelleEnregistree(routages, {})


def sortie_skill(skill: str, dossier: str, **champs) -> dict:
    return dict(reponses()["sortie_skill_simulee"], skill=skill, dossier=dossier, **champs)


class BaseLot2(CasAvecDossiers):
    """Chaîne du Lot 2 avec runtime HTTP local et modèle à réponses enregistrées."""

    def setUp(self):
        super().setUp()
        self.passerelle = passerelle_enregistree()
        self.serveur, url = demarrer_en_fond(passerelle=self.passerelle)
        self.addCleanup(self.serveur.server_close)
        self.addCleanup(self.serveur.shutdown)
        self.chaine = ChaineLot2(self.entree, self.sortie, self.etat, REGISTRE_DOSSIERS,
                                 passerelle=self.passerelle, runtime=ClientRuntime(url))
        self.surveillant = Surveillant(self.entree, os.path.join(self.etat, "surveillance.json"))

    def skill_repond(self, skill: str, dossier: str, **champs) -> None:
        self.passerelle.sorties_skills[skill] = sortie_skill(skill, dossier, **champs)

    def deposer_depot(self, nom: str, sous_dossier: str | None = None) -> list[dict]:
        cible = os.path.join(self.entree, sous_dossier, nom) if sous_dossier else os.path.join(self.entree, nom)
        os.makedirs(os.path.dirname(cible), exist_ok=True)
        shutil.copy(chemin_depot(nom), cible)
        evs = self.surveillant.scruter() + self.surveillant.scruter()
        return [self.chaine.traiter(e) for e in evs]

    def fichiers(self, sous_dossier: str) -> list[str]:
        d = os.path.join(self.sortie, sous_dossier)
        return sorted(os.listdir(d)) if os.path.isdir(d) else []

    def audit(self) -> str:
        with open(os.path.join(self.etat, "audit.jsonl"), encoding="utf-8") as f:
            return f.read()
