"""Mesure la détection de l'outil de pseudonymisation (P09) sur le jeu F-IDENT-01.

    python factory/jeux-de-test/F-IDENT-01/evaluer.py              tableau par catégorie, oublis et fausses alertes
    python factory/jeux-de-test/F-IDENT-01/evaluer.py --markdown   même résultat, au format du dossier resultats/

Pour le jeu de contrôle, seuls les taux sont affichés. --details-controle affiche aussi ses oublis et fausses
alertes : à n'utiliser que pour archiver une mesure, jamais pour régler une règle.

Définitions retenues :
- une entité attendue est « masquée » si chacun de ses caractères alphanumériques est couvert par une détection,
  quelle qu'en soit la catégorie (c'est ce qui compte pour ne rien laisser partir) ;
- elle est « partiellement masquée » si une partie seulement est couverte : une fuite, comptée comme un oubli ;
- une détection est « correcte » si elle chevauche une entité attendue ; sinon c'est une fausse alerte.
Rappel = entités masquées / entités attendues. Précision = détections correctes / détections.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(DEPOT, "outils", "pseudonymisation", "src"))

from pseudonymisation import __version__  # noqa: E402
from pseudonymisation.detection import detecter  # noqa: E402

PIECES = os.path.join(ICI, "pieces")


JEUX = {"developpement": "jeu de développement (a servi à écrire les règles)",
        "controle": "jeu de contrôle (rédigé à part, inconnu des règles)"}
FICHIERS = {"developpement": "annotations.json", "controle": "annotations-controle.json"}


def charger(jeu: str) -> dict:
    with open(os.path.join(ICI, "attendu", FICHIERS[jeu]), encoding="utf-8") as f:
        return json.load(f)


def evaluer(jeu: str = "controle") -> dict:
    annotations = charger(jeu)
    par_categorie = defaultdict(lambda: {"attendues": 0, "masquees": 0, "partielles": 0})
    oublis, fausses_alertes, detections_total, detections_correctes = [], [], 0, 0
    for nom, attendues in annotations["pieces"].items():
        if not nom.endswith(".txt"):
            continue
        with open(os.path.join(PIECES, nom), encoding="utf-8") as f:
            texte = f.read()
        detections = detecter(texte)
        couvert = [False] * len(texte)
        for d in detections:
            for i in range(d.debut, d.fin):
                couvert[i] = True
        for a in attendues:
            stats = par_categorie[a["categorie"]]
            stats["attendues"] += 1
            positions = [i for i in range(a["debut"], a["fin"]) if texte[i].isalnum()]
            n = sum(couvert[i] for i in positions)
            if n == len(positions):
                stats["masquees"] += 1
            else:
                if n:
                    stats["partielles"] += 1
                oublis.append(f"{nom} : {a['categorie']} « {a['texte']} »" + (" (partiel)" if n else ""))
        for d in detections:
            detections_total += 1
            if any(d.debut < a["fin"] and a["debut"] < d.fin for a in attendues):
                detections_correctes += 1
            else:
                fausses_alertes.append(f"{nom} : {d.categorie} « {d.texte} » ({d.raison})")
    attendues = sum(s["attendues"] for s in par_categorie.values())
    masquees = sum(s["masquees"] for s in par_categorie.values())
    return {"jeu": jeu, "version_outil": __version__, "version_jeu": annotations["version"],
            "categories": dict(sorted(par_categorie.items())), "attendues": attendues, "masquees": masquees,
            "rappel": masquees / attendues if attendues else 1.0,
            "detections": detections_total, "detections_correctes": detections_correctes,
            "precision": detections_correctes / detections_total if detections_total else 1.0,
            "oublis": oublis, "fausses_alertes": fausses_alertes}


def pourcentage(x: float) -> str:
    return f"{100 * x:.0f} %"


def en_texte(r: dict, markdown: bool = False, details: bool = True) -> str:
    lignes = []
    if markdown:
        lignes += ["| Catégorie | Attendues | Masquées | Rappel |", "|---|---|---|---|"]
    for categorie, s in r["categories"].items():
        rappel = pourcentage(s["masquees"] / s["attendues"])
        lignes.append(f"| {categorie} | {s['attendues']} | {s['masquees']} | {rappel} |" if markdown
                      else f"  {categorie:<18} {s['masquees']:>3}/{s['attendues']:<3} {rappel}")
    lignes.append("")
    lignes.append(f"Rappel global : {r['masquees']}/{r['attendues']} entités entièrement masquées ({pourcentage(r['rappel'])}).")
    lignes.append(f"Précision : {r['detections_correctes']}/{r['detections']} détections correctes ({pourcentage(r['precision'])}).")
    lignes.append("")
    if not details:
        lignes.append(f"{len(r['oublis'])} oubli(s) et {len(r['fausses_alertes'])} fausse(s) alerte(s), non détaillés : "
                      "les lire revient à consommer le jeu de contrôle (--details-controle pour les afficher).")
        return "\n".join(lignes)
    lignes.append("Oublis :" if r["oublis"] else "Oublis : aucun.")
    lignes += [f"- {o}" for o in r["oublis"]]
    lignes.append("")
    lignes.append("Fausses alertes :" if r["fausses_alertes"] else "Fausses alertes : aucune.")
    lignes += [f"- {o}" for o in r["fausses_alertes"]]
    return "\n".join(lignes)


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    for jeu, libelle in JEUX.items():
        r = evaluer(jeu)
        titre = f"P09 {r['version_outil']} sur F-IDENT-01 v{r['version_jeu']}, {libelle}"
        print(f"## {titre}\n" if "--markdown" in argv else f"{titre}\n")
        details = jeu != "controle" or "--details-controle" in argv
        print(en_texte(r, markdown="--markdown" in argv, details=details))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
