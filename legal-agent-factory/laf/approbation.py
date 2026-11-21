"""Décision humaine sur une sortie revue (fiche §12, non consultée : provisoire [À VÉRIFIER]).

La décision vient d'une personne, par l'appel local `ChaineLot2.decider` ; jamais
d'un courriel ni d'un fichier déposé. Trois décisions :

- `refuse` : rien n'est autorisé ;
- `corrige` : la sortie corrigée remplace celle du skill, puis repasse la revue ;
  elle n'est approuvée que si la revue est conforme ;
- `approuve` : impossible si la revue n'est pas conforme (il faut corriger).

Effet par niveau : A0 et A1 restent internes ; A2 est autorisé mais seulement
consigné (« exécution simulée », Lot 2) ; A3 reste bloqué quelle que soit la
décision. Aucune fonction d'envoi n'existe.
"""

from .outils_fichiers import horodatage
from .revue import reviser

DECISIONS = {"approuve", "refuse", "corrige"}


class DecisionInvalide(ValueError):
    pass


def appliquer(revue: dict, decision: dict, skill: dict, routage: dict, texte_source: str,
              registre: dict, niveaux: dict) -> dict:
    nature = decision.get("decision")
    relecteur = decision.get("relecteur")
    if nature not in DECISIONS:
        raise DecisionInvalide("décision inconnue")
    if relecteur not in niveaux["referents_humains"]:
        raise DecisionInvalide("relecteur non inscrit comme référent humain")
    trace = {"decision": nature, "relecteur": relecteur, "motif": decision.get("motif", ""),
             "horodatage": horodatage(), "actions_executees": []}

    if nature == "refuse":
        return dict(trace, statut="refuse", actions=[], revue=revue)
    if nature == "corrige":
        if "sortie_corrigee" not in decision:
            raise DecisionInvalide("correction sans sortie corrigée")
        revue = reviser(decision["sortie_corrigee"], skill, routage, texte_source, registre, niveaux)
        if not revue["conforme"]:
            return dict(trace, statut="correction_non_conforme", actions=[], revue=revue)
    elif not revue["conforme"]:
        return dict(trace, statut="approbation_impossible_revue_non_conforme", actions=[], revue=revue)

    actions = []
    for a in revue["actions"]:
        if a["niveau"] in niveaux["niveaux_bloques"]:
            effet = "bloquee"
        elif a["niveau"] in niveaux["niveaux_sur_approbation"]:
            effet = "autorisee_execution_simulee"
        else:
            effet = "interne"
        actions.append(dict(a, effet=effet))
    statut = "corrige_approuve" if nature == "corrige" else "approuve"
    return dict(trace, statut=statut, actions=actions, revue=revue)
