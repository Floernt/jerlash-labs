"""Mesure l'outil glossaire-definitions (P02) sur F-DEF-01.

    python -I factory/jeux-de-test/F-DEF-01/evaluer.py                      les deux jeux, totaux seulement
    python -I factory/jeux-de-test/F-DEF-01/evaluer.py --details            écarts du jeu de développement
    python -I factory/jeux-de-test/F-DEF-01/evaluer.py --details-controle   écarts du jeu de contrôle aussi

Le jeu de contrôle sert à mesurer, jamais à régler les règles : ses écarts ne s'affichent que sur demande.
Pour chaque catégorie : rappel (défauts annotés que l'outil trouve) et précision (signalements exacts).
Un terme est comparé par sa clé : sans article, casse, accents ni marque du pluriel.
"""

from __future__ import annotations

import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(DEPOT, "outils", "glossaire-definitions", "src"))

from glossaire_definitions.analyse import analyser, cle  # noqa: E402
from glossaire_definitions.lecture import lire_contrat  # noqa: E402

JEUX = {"developpement": ("pieces", "P02.json"), "controle": ("pieces-controle", "P02-controle.json")}
CATEGORIES = ["definis", "doublons", "divergents", "inutilises", "non_definis", "variantes", "avant_definition"]


def trouve(analyse) -> dict[str, set[str]]:
    termes = lambda *cats: {cle(c.terme) for c in analyse.constats if c.categorie in cats}  # noqa: E731
    return {"definis": {t.cle for t in analyse.termes}, "doublons": termes("doublon", "divergent"),
            "divergents": termes("divergent"), "inutilises": termes("inutilise"),
            "non_definis": {cle(c.forme) for c in analyse.du_type("non_defini")},
            "variantes": termes("variante"), "avant_definition": termes("avant_definition")}


def attendu(entree: dict) -> dict[str, set[str]]:
    sortie = {c: {cle(x) for x in entree.get(c, [])} for c in CATEGORIES if c != "variantes"}
    sortie["variantes"] = {cle(v["terme"]) for v in entree.get("variantes", [])}
    return sortie


def evaluer(jeu: str) -> dict:
    pieces, fichier = JEUX[jeu]
    with open(os.path.join(ICI, "attendu", fichier), encoding="utf-8") as f:
        annotations = json.load(f)
    totaux = {c: {"attendus": 0, "trouves": 0, "exacts": 0} for c in CATEGORIES}
    ecarts = []
    for nom, entree in annotations.items():
        a = attendu(entree)
        t = trouve(analyser(lire_contrat(os.path.join(ICI, pieces, nom))))
        for c in CATEGORIES:
            totaux[c]["attendus"] += len(a[c])
            totaux[c]["trouves"] += len(t[c])
            totaux[c]["exacts"] += len(a[c] & t[c])
            ecarts += [f"{nom} : {c} manqué : {x}" for x in sorted(a[c] - t[c])]
            ecarts += [f"{nom} : {c} en trop : {x}" for x in sorted(t[c] - a[c])]
    for c in CATEGORIES:
        n = totaux[c]
        n["rappel"] = n["exacts"] / n["attendus"] if n["attendus"] else 1.0
        n["precision"] = n["exacts"] / n["trouves"] if n["trouves"] else 1.0
    return {"totaux": totaux, "ecarts": ecarts}


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    for jeu in JEUX:
        resultat = evaluer(jeu)
        print(f"== {jeu}")
        for c, n in resultat["totaux"].items():
            print(f"  {c:17} rappel {n['exacts']}/{n['attendus']}  précision {n['exacts']}/{n['trouves']}")
        if ("--details" in argv and jeu == "developpement") or "--details-controle" in argv:
            for e in resultat["ecarts"]:
                print("   ", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
