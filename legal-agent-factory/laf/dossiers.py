"""Rapprochement d'un événement à un dossier connu, ou dossier d'attente.

Règle : aucune attribution sur une déduction non contrôlée. Seuls trois liens
sont admis, tous vérifiables :

1. courriel en réponse à un message déjà rattaché (In-Reply-To ou References) ;
2. référence exacte d'un dossier dans l'objet, ET expéditeur inscrit comme
   contact de ce dossier ;
3. fichier déposé dans le sous-dossier qui porte la référence exacte d'un dossier.

Tout le reste (nom du débiteur, ressemblance, expéditeur seul, plusieurs
références, contradiction avec le fil) va au dossier d'attente, avec son motif.
"""

import json
import re

from .outils_fichiers import ecrire_json, lire_json

ATTENTE = "ATTENTE"
RE_REFERENCE = re.compile(r"\bSYN-\d{4}-\d{3}\b")


def charger_registre(chemin: str) -> dict:
    """Registre des dossiers (synthétiques) : référence -> fiche."""
    with open(chemin, encoding="utf-8") as f:
        donnees = json.load(f)
    return {d["reference"]: dict(d, contacts=[c.lower() for c in d.get("contacts", [])])
            for d in donnees["dossiers"]}


def _resultat(dossier, lien, motif=None) -> dict:
    return {"dossier": dossier or ATTENTE, "rattache": bool(dossier), "lien": lien, "motif": motif}


class IndexFils:
    """message_id -> dossier, conservé dans l'état (fils.json)."""

    def __init__(self, chemin: str):
        self.chemin = chemin
        self.fils: dict = lire_json(chemin, {})

    def dossier_de(self, message_ids) -> set:
        return {self.fils[m] for m in message_ids if m in self.fils}

    def inscrire(self, message_id: str, dossier: str) -> None:
        self.fils[message_id] = dossier
        ecrire_json(self.chemin, self.fils)


def rapprocher_courriel(fil: dict, objet: str, registre: dict, index: IndexFils) -> dict:
    precedents = [m for m in [fil.get("in_reply_to")] + fil.get("references", []) if m]
    par_fil = index.dossier_de(precedents) - {ATTENTE}
    refs = set(RE_REFERENCE.findall(objet))

    if len(par_fil) > 1:
        return _resultat(None, None, "fil_contradictoire")
    if par_fil:
        dossier = par_fil.pop()
        if refs and refs != {dossier}:
            return _resultat(None, None, "objet_contredit_le_fil")
        return _resultat(dossier, "fil")
    if not refs:
        return _resultat(None, None, "aucune_reference")
    if len(refs) > 1:
        return _resultat(None, None, "plusieurs_references")
    ref = refs.pop()
    if ref not in registre:
        return _resultat(None, None, "reference_inconnue")
    if fil["de"] not in registre[ref]["contacts"]:
        return _resultat(None, None, "expediteur_non_inscrit")
    return _resultat(ref, "reference_et_expediteur")


def rapprocher_fichier(chemin_relatif: str, registre: dict) -> dict:
    morceaux = chemin_relatif.split("/")
    if len(morceaux) < 2:
        return _resultat(None, None, "fichier_hors_sous_dossier")
    if morceaux[0] not in registre:
        return _resultat(None, None, "sous_dossier_inconnu")
    return _resultat(morceaux[0], "sous_dossier")
