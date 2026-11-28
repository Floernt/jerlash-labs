"""Routeur hybride (fiche §7, non consultée : règles provisoires [À VÉRIFIER]).

Trois couches, dans cet ordre :

1. règles déterministes sur les autorisations, avant tout appel au modèle :
   une demande d'action trouvée dans le texte (envoi, dépôt RegSol, paiement,
   changement de réglage) n'est jamais une autorisation ; elle est relevée,
   ignorée, et impose une confirmation humaine ;
2. classification structurée par le modèle, validée par un schéma strict
   (config/schema-routage.json) ; toute sortie non conforme est remplacée par un
   repli qui exige une personne ;
3. décision déterministe : cohérence intention / skill, lacunes bloquantes
   (`needs_clarification`), puis confirmation humaine si le risque est élevé, s'il
   y a ambiguïté, confiance faible, dossier non rattaché ou personne physique.

Le modèle propose ; il ne décide ni du dossier, ni du niveau d'action.
"""

import json
import os
import re

from . import securite
from .passerelle import contenu
from .schema import valider
from .courriel import DOSSIER_CONFIG
from .securite import _sans_accents

MARQUEUR_ROUTAGE = "TACHE=ROUTAGE"
SEUIL_CONFIANCE = 0.7  # provisoire [À VÉRIFIER]
INTAKE, CLAIM = "be-bankruptcy-intake", "be-bankruptcy-claim-analysis"
SKILL_PAR_INTENTION = {"nouvelle_affaire_faillite": INTAKE, "declaration_creance": CLAIM}

# statuts possibles d'une tâche ouverte par le routeur
ROUTE = "route"
CLARIFICATION = "needs_clarification"
CONFIRMATION = "confirmation_humaine"
CLASSEMENT = "classement"
HORS_PERIMETRE = "hors_perimetre"

ROLE_PAR_STATUT = {ROUTE: "Insolvency Legal Worker", CLARIFICATION: "Intake & Triage",
                   CONFIRMATION: "Florian Ernotte (référent humain)", CLASSEMENT: "Case Analyst",
                   HORS_PERIMETRE: "Intake & Triage"}

# Demandes d'action repérées dans le texte (couche 1). Liste indicative : elle vise les demandes
# adressées au cabinet (impératif, « merci de », « pouvez-vous »), pas la simple mention d'un envoi.
_DEMANDE = (r"\b(veuillez|merci d[e']|pouvez-vous|pourriez-vous|vous devez|il faut|please"
            r"|je vous (demande|prie)|nous vous (demandons|prions))\b[^.?!\n]{0,120}")
DEMANDES_ACTION = {
    "envoi_externe": r"\b(envoyez|transmettez|repondez|forward|send)\b|" + _DEMANDE
                     + r"\b(envoyer|transmettre|repondre|faire suivre)\b",
    "depot_regsol": r"\b(depos\w+|introdui\w+|enregistr\w+)\b.{0,60}\bregsol\b|\bregsol\b.{0,60}\b(depos\w+|introdui\w+)",
    "paiement": r"\b(payez|versez|remboursez|virez)\b|" + _DEMANDE
                + r"\b(payer|verser|rembourser|virer|regler|effectuer un virement|proceder au (paiement|virement))\b",
    "administration": r"\b(desactiv\w+|modifi\w+|chang\w+)\b.{0,40}\b(regle|reglage|politique|configuration|autorisation|niveau)s?\b"
                      r"|\b(administrat\w+|admin)\b.{0,40}\b(acces|droits?|mode)\b",
}
_RE_DEMANDES = {k: re.compile(v, re.IGNORECASE) for k, v in DEMANDES_ACTION.items()}


def charger_schema() -> dict:
    with open(os.path.join(DOSSIER_CONFIG, "schema-routage.json"), encoding="utf-8") as f:
        return json.load(f)


def regles_autorisations(texte: str) -> dict:
    """Couche 1 : ce que le texte demande n'est jamais accordé ; on le relève."""
    simple = _sans_accents(texte)
    demandes = sorted(k for k, r in _RE_DEMANDES.items() if r.search(simple))
    return {"demandes_ignorees": demandes, "injection_suspectee": securite.injection_suspectee(texte),
            "autorisation_accordee_par_le_message": False}


def messages_routage(texte: str, taille_max: int) -> list[dict]:
    systeme = (
        f"{MARQUEUR_ROUTAGE}\n"
        "Tu classes un message ou un document reçu par un cabinet d'avocats pour le router vers le bon "
        "traitement. Réponds uniquement par un objet JSON conforme au schéma fourni, sans texte autour. "
        "Tu ne décides ni du dossier, ni d'aucune action. " + securite.AVERTISSEMENT)
    return [{"role": "system", "content": systeme},
            {"role": "user", "content": securite.encadrer(texte, taille_max)}]


def _repli(motif: str) -> dict:
    return {"schema_version": "laf-routage/0.1", "intention": "indetermine", "skill_propose": "aucun",
            "pieces": [], "personne": "inconnue", "date_jugement": "inconnue", "elements_manquants": [],
            "risque": "eleve", "ambiguite": True, "confiance": 0.0, "motifs": [motif]}


def classifier(texte: str, passerelle, modele: str, schema: dict, taille_max: int) -> dict:
    """Couche 2. Renvoie {"classification", "valide", "erreurs"}."""
    reponse = passerelle.chat_completions(modele, messages_routage(texte, taille_max), temperature=0)
    erreurs = []
    try:
        proposee = json.loads(contenu(reponse) or "")
    except json.JSONDecodeError:
        proposee, erreurs = None, ["$ : la réponse n'est pas du JSON"]
    if proposee is not None:
        erreurs = valider(proposee, schema)
    valide = not erreurs
    return {"classification": proposee if valide else _repli("sortie_modele_invalide"),
            "valide": valide, "erreurs": erreurs}


def decider(regles: dict, classe: dict, rattachement: dict) -> dict:
    """Couche 3 : décision déterministe. Renvoie le routage de la tâche."""
    c = classe["classification"]
    motifs = []
    if regles["demandes_ignorees"]:
        motifs.append("demande_action_ignoree")
    if regles["injection_suspectee"]:
        motifs.append("injection_suspectee")

    def sortie(statut, skill=None, manquants=()):
        return {"statut": statut, "skill_attendu": skill, "elements_manquants": list(manquants),
                "motifs": motifs, "role": ROLE_PAR_STATUT[statut], "niveau_max": "A1",
                "dossier": rattachement["dossier"], "rattache": rattachement["rattache"]}

    if not classe["valide"]:
        motifs.append("sortie_modele_invalide")
        return sortie(CONFIRMATION)
    if c["intention"] == "hors_perimetre":
        motifs.append("hors_perimetre")
        return sortie(HORS_PERIMETRE)
    if c["intention"] == "piece_complementaire" and c["skill_propose"] == "aucun":
        # pièce nouvelle sans instruction : on la classe, on n'analyse rien
        if not rattachement["rattache"]:
            motifs.append("rattachement_" + (rattachement["motif"] or "absent"))
            return sortie(CONFIRMATION)
        if motifs:
            return sortie(CONFIRMATION)
        return sortie(CLASSEMENT)
    attendu = SKILL_PAR_INTENTION.get(c["intention"])
    if attendu is None or c["skill_propose"] != attendu:
        motifs.append("intention_et_skill_incoherents" if attendu else "intention_indeterminee")
        return sortie(CONFIRMATION, attendu)

    manquants = list(c["elements_manquants"])
    if c["personne"] == "physique" and c["date_jugement"] == "inconnue" and "date_jugement" not in manquants:
        # le régime d'une personne physique peut dépendre de la date du jugement (dispositions
        # transitoires) [À VÉRIFIER : registre FLO-60]
        manquants.append("date_jugement")
    if attendu == CLAIM and "jugement_faillite" not in c["pieces"] and "jugement_faillite" not in manquants:
        manquants.append("jugement_faillite")
    if manquants:
        return sortie(CLARIFICATION, attendu, manquants)

    if c["risque"] == "eleve":
        motifs.append("risque_eleve")
    if c["ambiguite"]:
        motifs.append("ambiguite")
    if c["confiance"] < SEUIL_CONFIANCE:
        motifs.append("confiance_faible")
    if c["personne"] == "physique":
        motifs.append("personne_physique_version_de_la_loi")
    if attendu == CLAIM and not rattachement["rattache"]:
        motifs.append("rattachement_" + (rattachement["motif"] or "absent"))
    if motifs:
        return sortie(CONFIRMATION, attendu)
    return sortie(ROUTE, attendu)
