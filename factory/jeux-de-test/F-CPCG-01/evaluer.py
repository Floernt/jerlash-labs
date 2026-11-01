"""Mesure l'outil conditions-particulieres (P03) sur F-CPCG-01.

    python -I factory/jeux-de-test/F-CPCG-01/evaluer.py                      les deux jeux, totaux seulement
    python -I factory/jeux-de-test/F-CPCG-01/evaluer.py --details            écarts du jeu de développement
    python -I factory/jeux-de-test/F-CPCG-01/evaluer.py --details-controle   écarts du jeu de contrôle aussi

Le jeu de contrôle sert à mesurer, jamais à régler les règles : ses écarts ne s'affichent que sur demande.
Données : une donnée balisée est « repérée » si un signalement de l'outil la chevauche, quelle que soit la
catégorie proposée ; un signalement est exact s'il chevauche une donnée balisée.
Articles : classement exact (conditions particulières, générales, clause mixte).
"""

from __future__ import annotations

import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(DEPOT, "outils", "conditions-particulieres", "src"))
sys.path.insert(0, ICI)

from conditions_particulieres.analyse import CATEGORIES, analyser  # noqa: E402
from conditions_particulieres.lecture import lire_contrat, preparer  # noqa: E402
from generer import BALISE, lire_source  # noqa: E402

JEUX = {"developpement": ("sources", "pieces", "P03.json"),
        "controle": ("sources-controle", "pieces-controle", "P03-controle.json")}


def paragraphes_balises(lignes: list[str]) -> list[tuple[str, list[tuple[int, int, str]]]]:
    """Texte de chaque paragraphe, dans l'ordre du .docx, avec les données balisées (début, fin, catégorie)."""
    sortie = []
    for ligne in lignes:
        morceaux = [c.strip() for c in ligne.strip().strip("|").split("|")] if ligne.startswith("|") else [ligne]
        for morceau in morceaux:
            texte, balises, pos = "", [], 0
            for m in BALISE.finditer(morceau):
                texte += morceau[pos:m.start()]
                balises.append((len(texte), len(texte) + len(m.group(2)), m.group(1)))
                texte += m.group(2)
                pos = m.end()
            sortie.append((preparer(texte + morceau[pos:]), balises))
    return sortie


def cle_titre(texte: str) -> str:
    return " ".join(preparer(texte).split())


def evaluer(jeu: str) -> dict:
    sources, pieces, fichier = JEUX[jeu]
    with open(os.path.join(ICI, "attendu", fichier), encoding="utf-8") as f:
        attendus = json.load(f)
    noms = {}
    for nom in sorted(os.listdir(os.path.join(ICI, sources))):
        docx, lignes = lire_source(os.path.join(ICI, sources, nom), balise=True)
        noms[docx] = lignes
    totaux = {c: {"attendus": 0, "reperes": 0} for c in CATEGORIES}
    signalements = {"total": 0, "exacts": 0}
    articles = {"total": 0, "exacts": 0}
    confusion: dict[str, int] = {}
    ecarts = []
    for docx, entree in attendus.items():
        analyse = analyser(lire_contrat(os.path.join(ICI, pieces, docx)))
        reference = paragraphes_balises(noms[docx])
        if [t for t, _ in reference] != analyse.paragraphes:
            raise SystemExit(f"{docx} : paragraphes du .docx et de la source désalignés")
        trouvees = {}
        for d in analyse.donnees:
            trouvees.setdefault(d.paragraphe, []).append(d)
        for i, (texte, balises) in enumerate(reference):
            for debut, fin, categorie in balises:
                totaux[categorie]["attendus"] += 1
                if any(d.debut < fin and debut < d.fin for d in trouvees.get(i, [])):
                    totaux[categorie]["reperes"] += 1
                else:
                    ecarts.append(f"{docx} : donnée manquée {categorie} « {texte[debut:fin]} »")
            for d in trouvees.get(i, []):
                signalements["total"] += 1
                if any(d.debut < fin and debut < d.fin for debut, fin, _ in balises):
                    signalements["exacts"] += 1
                else:
                    ecarts.append(f"{docx} : signalement en trop {d.categorie} « {d.texte} »")
        classes = {cle_titre(b.titre): b.classement for b in analyse.blocs}
        for titre, attendu in entree["articles"].items():
            articles["total"] += 1
            obtenu = classes.get(cle_titre(titre), "absent")
            if obtenu == attendu:
                articles["exacts"] += 1
            else:
                confusion[f"{attendu} → {obtenu}"] = confusion.get(f"{attendu} → {obtenu}", 0) + 1
                ecarts.append(f"{docx} : « {titre} » attendu {attendu}, obtenu {obtenu}")
    return {"donnees": totaux, "signalements": signalements, "articles": articles, "confusion": confusion,
            "ecarts": ecarts}


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    for jeu in JEUX:
        r = evaluer(jeu)
        print(f"== {jeu}")
        attendus = sum(n["attendus"] for n in r["donnees"].values())
        reperes = sum(n["reperes"] for n in r["donnees"].values())
        print(f"  données repérées   {reperes}/{attendus}  signalements exacts {r['signalements']['exacts']}/{r['signalements']['total']}")
        for c, n in r["donnees"].items():
            print(f"    {c:12} {n['reperes']}/{n['attendus']}")
        print(f"  articles bien classés {r['articles']['exacts']}/{r['articles']['total']}  " +
              "  ".join(f"{k} : {v}" for k, v in sorted(r["confusion"].items())))
        if ("--details" in argv and jeu == "developpement") or "--details-controle" in argv:
            for e in r["ecarts"]:
                print("   ", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
