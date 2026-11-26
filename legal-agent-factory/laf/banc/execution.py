"""Exécution d'une série gelée, sur la chaîne du Lot 1 (qualification puis runtime) ou,
si la série porte `"chaine": "lot2"`, sur celle du Lot 2 (voir `lot2.py`).

Ce que voit le système évalué : les pièces du cas et son canal. Jamais le scénario,
ni la colonne `attendu`, ni une référence.

Gel. Au démarrage, la configuration de la série et les empreintes (cas, pièces,
instructions, schéma, code) sont écrites dans `gel.json`. Une reprise n'est
acceptée qu'à l'identique ; toute modification impose une nouvelle série dans un
autre répertoire. Le jeu `holdout` demande une confirmation explicite.

Dépense. Avec un fournisseur réel, la série est refusée sans plafond et sans
tarifs. Le coût est estimé à partir des tokens déclarés par l'API et des tarifs
de la configuration [À VÉRIFIER : tarifs publiés du fournisseur] ; il ne remplace
pas la facture. Au plafond, la série s'arrête et les cas restants sont marqués.
"""

import glob
import json
import os
import time

from .. import runtime
from ..qualification import charger_schema, qualifier
from ..securite import lire_texte
from . import lot2 as mod_lot2
from . import variantes as mod_variantes
from .cas import empreinte_dossier, empreinte_fichier

TAILLE_MAX = 20_000
DOSSIER_CODE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SerieRefusee(RuntimeError):
    pass


class _Compteur:
    """Enveloppe d'une passerelle : compte appels et tokens d'un cas."""

    def __init__(self, passerelle):
        self.passerelle = passerelle
        self.nom = passerelle.nom
        self.appels = self.entree = self.sortie = 0

    def chat_completions(self, model, messages, **options):
        reponse = self.passerelle.chat_completions(model, messages, **options)
        self.appels += 1
        usage = reponse.get("usage") or {}
        self.entree += int(usage.get("prompt_tokens") or 0)
        self.sortie += int(usage.get("completion_tokens") or 0)
        return reponse


def cout(entree: int, sortie: int, tarifs: dict | None) -> float | None:
    if not tarifs:
        return None
    return (entree * tarifs["entree_par_million"] + sortie * tarifs["sortie_par_million"]) / 1_000_000


def lire_pieces(dossier_pieces: str | None, id_: str) -> list[tuple[str, str]] | None:
    dossier = os.path.join(dossier_pieces, id_) if dossier_pieces else None
    if not dossier or not os.path.isdir(dossier):
        return None
    chemins = sorted(p for p in glob.glob(os.path.join(dossier, "*")) if os.path.isfile(p))
    return [(os.path.basename(p), lire_texte(p, TAILLE_MAX)) for p in chemins] or None


def _assembler(pieces: list[tuple[str, str]]) -> str:
    return "\n\n".join(f"--- pièce : {nom} ---\n{texte}" for nom, texte in pieces)


def empreinte_code() -> str:
    return empreinte_dossier(DOSSIER_CODE, ".py")


def chaine_de(config: dict) -> str:
    return config.get("chaine", "lot1")


def _empreintes_lot2(config: dict) -> dict:
    """Tout ce qui détermine le comportement de la chaîne du Lot 2, hors code."""
    config_laf = os.path.join(os.path.dirname(DOSSIER_CODE), "config")
    return {
        "dossiers": empreinte_fichier(config["dossiers"]),
        "skills": empreinte_dossier(os.path.join(os.path.dirname(DOSSIER_CODE), "skills")),
        **{f"config {n}": empreinte_fichier(os.path.join(config_laf, f"{n}.json"))
           for n in ("schema-routage", "schema-courriel", "niveaux-action", "registre-sources")},
    }


def geler(config: dict, chemin_cas: str, dossier_pieces: str | None, sortie: str) -> dict:
    empreintes = {"cas": empreinte_fichier(chemin_cas), "pieces": empreinte_dossier(dossier_pieces),
                  "code": empreinte_code()}
    if chaine_de(config) == "lot2":
        empreintes.update(_empreintes_lot2(config))
    else:
        empreintes.update(instructions=empreinte_fichier(config["instructions"]),
                          schema=empreinte_fichier(config["schema"]))
    gel = {
        # Le plafond n'est pas gelé : le relever permet de reprendre la même série.
        "serie": {k: v for k, v in config.items() if k != "plafond"},
        "empreintes": empreintes,
    }
    chemin = os.path.join(sortie, "gel.json")
    if os.path.isfile(chemin):
        with open(chemin, encoding="utf-8") as f:
            existant = json.load(f)
        if existant != gel:
            raise SerieRefusee("série déjà gelée dans ce répertoire avec une autre configuration "
                               "ou d'autres empreintes : utiliser un nouveau répertoire de sortie")
    else:
        os.makedirs(sortie, exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(gel, f, ensure_ascii=False, indent=2, sort_keys=True)
    return gel


def _executer_un(id_, canal, pieces, passerelle, config, schema, instructions) -> dict:
    compteur = _Compteur(passerelle)
    debut = time.perf_counter()
    q = qualifier(_assembler(pieces), compteur, config["modele"], schema, TAILLE_MAX)
    r = runtime.execute({"id": id_, "type": "analyse_cas"},
                        {"canal": canal, "qualification": q["qualification"],
                         "pieces": [{"nom": nom, "texte": texte} for nom, texte in pieces]},
                        {"nom": config.get("skill", "instructions-provisoires"), "instructions": instructions},
                        runtime.POLITIQUE_LOT1, passerelle=compteur, modele=config["modele"])
    return {
        "statut_execution": "execute",
        "pieces": len(pieces),
        "qualification_valide": q["valide"],
        "erreurs_schema": q["erreurs"],
        "injection_suspectee": q["injection_suspectee"],
        "triage_force": q["triage_force"],
        "triage_humain": q["qualification"]["requires_human_triage"],
        "runtime_statut": r["statut"],
        "tours": r["tours"],
        "demandes_outils_refusees": r.get("demandes_outils_refusees", 0),
        "actions_effectuees": r["actions_effectuees"],
        "corrections": 0 if q["valide"] else 1,
        "duree_s": round(time.perf_counter() - debut, 4),
        "appels_modele": compteur.appels,
        "tokens_entree": compteur.entree,
        "tokens_sortie": compteur.sortie,
        "cout": cout(compteur.entree, compteur.sortie, config.get("tarifs")),
        "sortie": r["sortie"],
    }


def _executer_un_lot2(id_unite, id_cas, canal, pieces, passerelle, config, sortie) -> dict:
    compteur = _Compteur(passerelle)
    debut = time.perf_counter()
    mesures = mod_lot2.executer_un(id_unite, id_cas, canal, pieces, compteur, config,
                                   os.path.join(sortie, "chaine", id_unite))
    return dict(mesures, statut_execution="execute", duree_s=round(time.perf_counter() - debut, 4),
                appels_modele=compteur.appels, tokens_entree=compteur.entree, tokens_sortie=compteur.sortie,
                cout=cout(compteur.entree, compteur.sortie, config.get("tarifs")))


def executer_serie(config: dict, cas: list[dict], chemin_cas: str, dossier_pieces: str | None,
                   sortie: str, passerelle, confirmer_holdout: bool = False,
                   avec_variantes: bool = False) -> dict:
    """Exécute les cas du jeu `config["jeu"]`. Renvoie un résumé de l'exécution."""
    jeu = config["jeu"]
    if jeu == "holdout" and not confirmer_holdout:
        raise SerieRefusee("jeu de test final : relancer avec la confirmation explicite, "
                           "une fois prompts, skills, sources et modèle figés sur le jeu de conception")
    reel = passerelle.nom != "simulee"
    if reel and (config.get("plafond") is None or not config.get("tarifs")):
        raise SerieRefusee("fournisseur réel : plafond de dépense et tarifs obligatoires dans la série")

    geler(config, chemin_cas, dossier_pieces, sortie)
    lot2 = chaine_de(config) == "lot2"
    schema = instructions = None
    if not lot2:
        schema = charger_schema(config["schema"])
        with open(config["instructions"], encoding="utf-8") as f:
            instructions = f.read()
    dossier_res = os.path.join(sortie, "resultats")
    os.makedirs(dossier_res, exist_ok=True)

    depense = 0.0
    for chemin in glob.glob(os.path.join(dossier_res, "*.json")):
        with open(chemin, encoding="utf-8") as f:
            depense += json.load(f).get("cout") or 0.0

    resume = {"executes": 0, "repris": 0, "pieces_manquantes": 0, "plafond": 0}
    for c in (c for c in cas if c["jeu"] == jeu):
        pieces = lire_pieces(dossier_pieces, c["id"])
        unites = [(c["id"], pieces)]
        if avec_variantes and pieces:
            unites += [(f"{c['id']}~{s}", p) for s, p in mod_variantes.variantes(pieces)]
        for id_unite, pieces_unite in unites:
            chemin = os.path.join(dossier_res, f"{id_unite}.json")
            if os.path.isfile(chemin):
                resume["repris"] += 1
                continue
            base = {"id": id_unite, "cas": c["id"], "variante": id_unite.partition("~")[2] or None}
            if pieces_unite is None:
                res = dict(base, statut_execution="non_execute", motif="pieces_manquantes")
                resume["pieces_manquantes"] += 1
            elif config.get("plafond") is not None and depense >= config["plafond"]:
                res = dict(base, statut_execution="non_execute", motif="plafond_atteint")
                resume["plafond"] += 1
            else:
                if lot2:
                    res = dict(base, **_executer_un_lot2(id_unite, c["id"], c["canal"], pieces_unite,
                                                         passerelle, config, sortie))
                else:
                    res = dict(base, **_executer_un(id_unite, c["canal"], pieces_unite, passerelle,
                                                    config, schema, instructions))
                depense += res["cout"] or 0.0
                resume["executes"] += 1
            if res.get("motif") != "plafond_atteint":  # rejouable une fois le plafond relevé
                with open(chemin, "w", encoding="utf-8") as f:
                    json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
    resume["depense_estimee"] = depense if config.get("tarifs") else None
    return resume
