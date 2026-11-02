"""Remplacement des détections par des marqueurs, et rétablissement des données dans la réponse de l'IA.

Une même donnée reçoit toujours le même marqueur ([PERSONNE_1], [IBAN_2]…), ce qui permet à l'IA de
suivre les personnes d'un bout à l'autre du texte. La table de correspondance contient les données
d'origine : elle reste sur l'ordinateur et ne s'envoie jamais avec le texte.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re
from dataclasses import dataclass, field

from . import __version__
from .detection import CATEGORIES, Entite

_CATS = "|".join(CATEGORIES)
# Forme exacte [PERSONNE_1], et formes qu'une IA produit parfois : [Personne_1], [PERSONNE 1], PERSONNE_1,
# PERSONNE 1. Hors crochets, seules les capitales sont admises : « la personne 1 » reste du texte ordinaire.
RE_MARQUEUR = re.compile(rf"\[(?i:({_CATS}))[ _-]?(\d{{1,4}})\]|\b({_CATS})[ _](\d{{1,4}})\b")
RE_MARQUEUR_EXACT = re.compile(rf"\[(?:{_CATS})_\d{{1,4}}\]")


def lire_marqueur(m: re.Match) -> str:
    """Forme exacte d'un marqueur trouvé par RE_MARQUEUR : [personne 01] -> [PERSONNE_1]."""
    categorie = (m.group(1) or m.group(3)).upper()
    return f"[{categorie}_{int(m.group(2) or m.group(4))}]"


def marqueurs_presents(texte: str) -> list[str]:
    """Marqueurs déjà présents dans un texte, y compris sous une forme approchée."""
    return sorted({m.group() for m in RE_MARQUEUR.finditer(texte)})


@dataclass
class Resultat:
    texte: str
    table: dict
    marqueurs_preexistants: list[str] = field(default_factory=list)


def attribuer_marqueurs(entites: list[Entite], texte: str = "") -> dict[str, str]:
    """Clé de détection -> marqueur, numéroté par catégorie dans l'ordre d'apparition.

    La numérotation commence après le plus grand numéro déjà présent dans le texte d'origine :
    le rétablissement ne confond jamais un marqueur préexistant avec une donnée."""
    compteurs: dict[str, int] = {}
    for m in RE_MARQUEUR.finditer(texte):
        categorie, numero = lire_marqueur(m)[1:-1].rsplit("_", 1)
        compteurs[categorie] = max(compteurs.get(categorie, 0), int(numero))
    marqueurs: dict[str, str] = {}
    for e in sorted(entites, key=lambda e: e.debut):
        if not e.actif or e.cle in marqueurs:
            continue
        compteurs[e.categorie] = compteurs.get(e.categorie, 0) + 1
        marqueurs[e.cle] = f"[{e.categorie}_{compteurs[e.categorie]}]"
    return marqueurs


def pseudonymiser(texte: str, entites: list[Entite], source: str = "") -> Resultat:
    actives = sorted((e for e in entites if e.actif), key=lambda e: e.debut)
    marqueurs = attribuer_marqueurs(actives, texte)
    morceaux, curseur = [], 0
    formes: dict[str, list[str]] = {}
    for e in actives:
        if e.debut < curseur:
            raise ValueError("Détections qui se chevauchent : appeler detecter() pour les résoudre.")
        if texte[e.debut:e.fin] != e.texte:
            raise ValueError("Détections calculées sur un autre texte : relancer la détection.")
        morceaux.append(texte[curseur:e.debut])
        morceaux.append(marqueurs[e.cle])
        curseur = e.fin
        liste = formes.setdefault(marqueurs[e.cle], [])
        if e.texte not in liste:
            liste.append(e.texte)
    morceaux.append(texte[curseur:])
    resultat = "".join(morceaux)
    correspondances = []
    for marqueur, originaux in formes.items():
        categorie = marqueur[1:].rsplit("_", 1)[0]
        correspondances.append({"marqueur": marqueur, "categorie": categorie,
                                "retablir_par": max(originaux, key=len), "formes": originaux})
    table = {
        "outil": "pseudonymisation (jerlash.labs)",
        "version": __version__,
        "avertissement": "Cette table contient les données d'origine. Gardez-la sur votre ordinateur ; "
                         "ne l'envoyez jamais avec le texte pseudonymisé.",
        "cree_le": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "sha256_texte_pseudonymise": hashlib.sha256(resultat.encode("utf-8")).hexdigest(),
        "correspondances": correspondances,
    }
    return Resultat(resultat, table, marqueurs_presents(texte))


@dataclass
class Retablissement:
    texte: str
    remplaces: dict[str, int]
    inconnus: list[str]
    absents: list[str]
    approches: list[str] = field(default_factory=list)   # formes déformées par l'IA, remplacées quand même


def retablir(texte: str, table: dict) -> Retablissement:
    """Remet les données d'origine à la place des marqueurs, y compris s'ils ont été un peu déformés
    par l'IA ([Personne_1], [PERSONNE 1], PERSONNE_1 sans crochets) ; ces formes sont signalées."""
    valeurs = {c["marqueur"].upper(): c["retablir_par"] for c in table.get("correspondances", [])}
    remplaces: dict[str, int] = {}
    inconnus: list[str] = []
    approches: list[str] = []

    def remplacer(m: re.Match) -> str:
        marqueur = lire_marqueur(m)
        if marqueur in valeurs:
            remplaces[marqueur] = remplaces.get(marqueur, 0) + 1
            if m.group() != marqueur and m.group() not in approches:
                approches.append(m.group())
            return valeurs[marqueur]
        if m.group() not in inconnus:
            inconnus.append(m.group())
        return m.group()

    resultat = RE_MARQUEUR.sub(remplacer, texte)
    absents = [m for m in valeurs if m not in remplaces]
    return Retablissement(resultat, remplaces, inconnus, absents, approches)


def lire_table(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        table = json.load(f)
    if not isinstance(table, dict) or not isinstance(table.get("correspondances"), list) or not all(
            isinstance(c, dict) and isinstance(c.get("marqueur"), str) and isinstance(c.get("retablir_par"), str)
            for c in table["correspondances"]):
        raise ValueError("Ce fichier n'est pas une table de correspondance de l'outil.")
    return table
