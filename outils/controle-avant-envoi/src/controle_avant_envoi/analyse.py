"""Point d'entrée de l'analyse : configuration, exécution des contrôles, synthèse."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from importlib import resources

from . import __version__
from .controles import A_EXAMINER, DETECTE, ERREUR, IMPORTANT, INFORMATION, NON_VERIFIE, Controle, executer
from .ooxml import ErreurLecture, PaquetDocx


class ErreurConfiguration(Exception):
    pass


def charger_configuration(chemin_config: str | None = None, chemin_termes: str | None = None) -> dict:
    cfg = json.loads(resources.files(__package__).joinpath("defaut.json").read_text(encoding="utf-8"))
    if chemin_config:
        try:
            with open(chemin_config, encoding="utf-8") as f:
                cfg.update(json.load(f))
        except (OSError, json.JSONDecodeError) as e:
            raise ErreurConfiguration(f"Configuration illisible ({chemin_config}) : {e}")
    if chemin_termes:
        try:
            with open(chemin_termes, encoding="utf-8-sig") as f:
                lignes = [l.strip() for l in f]
        except (OSError, UnicodeDecodeError) as e:
            raise ErreurConfiguration(f"Liste de termes illisible ({chemin_termes}) : {e}")
        cfg["termes_sensibles"] = list(cfg.get("termes_sensibles", [])) + \
            [l for l in lignes if l and not l.startswith("#")]
    for m in cfg.get("marqueurs", []):
        try:
            re.compile(m["motif"])
        except (re.error, KeyError, TypeError) as e:
            raise ErreurConfiguration(f"Motif de marqueur invalide ({m!r}) : {e}")
    return cfg


@dataclass
class Rapport:
    chemin: str
    date: str
    version: str = __version__
    taille: int | None = None
    sha256: str | None = None
    integre: bool | None = None
    erreur: str | None = None
    controles: list[Controle] = field(default_factory=list)

    @property
    def nom(self) -> str:
        return os.path.basename(self.chemin)

    def detectes(self, gravite: str) -> list[Controle]:
        return [c for c in self.controles if c.statut == DETECTE and c.gravite == gravite]

    @property
    def en_erreur(self) -> list[Controle]:
        return [c for c in self.controles if c.statut == ERREUR]

    @property
    def niveau(self) -> str:
        """erreur | incomplet | a_traiter | rien_detecte"""
        if self.erreur:
            return "erreur"
        if self.en_erreur or self.integre is False:
            return "incomplet"
        if self.detectes(IMPORTANT) or self.detectes(A_EXAMINER):
            return "a_traiter"
        return "rien_detecte"

    @property
    def verdict(self) -> str:
        if self.niveau == "erreur":
            return f"Analyse impossible. {self.erreur} Aucune conclusion ne peut être tirée sur ce document."
        if self.integre is False:
            return "Le fichier a changé pendant l'analyse. Relancez le contrôle sur une copie stable."
        n_imp, n_exa = len(self.detectes(IMPORTANT)), len(self.detectes(A_EXAMINER))
        parties = []
        if n_imp:
            parties.append(f"{n_imp} point{'s' if n_imp > 1 else ''} important{'s' if n_imp > 1 else ''}")
        if n_exa:
            parties.append(f"{n_exa} point{'s' if n_exa > 1 else ''} à examiner")
        texte = (" et ".join(parties) + " avant envoi.") if parties else \
            ("Aucun des éléments recherchés n'a été détecté. Cela ne garantit pas que le document peut être "
             "envoyé : seuls les contrôles listés ont été réalisés, et la relecture reste nécessaire.")
        if not parties and any(c.ident == "termes" and c.statut == NON_VERIFIE for c in self.controles):
            texte += " Les noms d'autres dossiers n'ont pas été recherchés : aucune liste de termes fournie."
        if self.en_erreur:
            texte = (f"Analyse incomplète : {len(self.en_erreur)} contrôle(s) n'ont pas pu être réalisés. "
                     + (texte if parties else "Ne considérez pas le document comme vérifié."))
        return texte

    @property
    def code_sortie(self) -> int:
        return {"rien_detecte": 0, "a_traiter": 1}.get(self.niveau, 2)

    def en_dict(self) -> dict:
        return {
            "outil": "controle-avant-envoi", "version": self.version, "date": self.date,
            "fichier": self.nom, "taille": self.taille, "sha256": self.sha256,
            "fichier_inchange": self.integre, "niveau": self.niveau, "verdict": self.verdict,
            "erreur": self.erreur,
            "controles": [{
                "id": c.ident, "titre": c.titre, "statut": c.statut, "gravite": c.gravite, "note": c.note,
                "constats": [{"localisation": k.localisation, "detail": k.detail} for k in c.constats],
                "constats_non_affiches": c.omis,
            } for c in self.controles],
        }


def _empreinte(chemin: str) -> str | None:
    h = hashlib.sha256()
    try:
        with open(chemin, "rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
    except OSError:
        return None
    return h.hexdigest()


def analyser(chemin: str, cfg: dict | None = None) -> Rapport:
    """Analyse un fichier. Le fichier est ouvert en lecture seule et n'est jamais écrit."""
    cfg = cfg if cfg is not None else charger_configuration()
    rapport = Rapport(chemin=os.path.abspath(chemin), date=datetime.now().astimezone().isoformat(timespec="seconds"))
    try:
        paquet = PaquetDocx.ouvrir(chemin)
    except ErreurLecture as e:
        rapport.erreur = e.message
        return rapport
    except Exception as e:  # toute autre erreur de lecture : jamais un résultat rassurant
        rapport.erreur = f"Le fichier n'a pas pu être lu ({type(e).__name__} : {e})."
        return rapport
    rapport.taille, rapport.sha256 = paquet.taille, paquet.sha256
    rapport.controles = executer(paquet, cfg)
    rapport.integre = _empreinte(chemin) == paquet.sha256
    return rapport


__all__ = ["analyser", "charger_configuration", "Rapport", "ErreurConfiguration", "INFORMATION"]
