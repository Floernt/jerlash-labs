"""Compare l'inventaire produit par P01 à l'inventaire attendu (attendu/P01.json).

    python factory/jeux-de-test/F-DOSSIER-01/evaluer.py
    python factory/jeux-de-test/F-DOSSIER-01/evaluer.py --ia [--config FICHIER] [--executions 3]

Sans --ia : règles seules (référence, gratuit, reproductible ; c'est ce que vérifient les tests).
Avec --ia : mode IA de P01 0.2.0, avec la configuration et la clé de l'outil. Les pièces du jeu sont
fictives : l'envoi est confirmé d'office. Chaque exécution est payante et les réponses varient ; on
retient, champ par champ, le plus mauvais résultat des exécutions (projets/P01-mode-ia-spec.md, §6).

Pour chaque champ (type, statut, date, parties, rattachement, document qui fait foi), le nombre de pièces
où l'outil a la bonne valeur, puis les écarts. Les parties sont justes si l'ensemble est identique.
Les alertes attendues sur le dossier sont cherchées dans les alertes produites, par mot-clé.
"""

from __future__ import annotations

import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(DEPOT, "outils", "inventaire-dossier", "src"))

from inventaire_dossier import __version__  # noqa: E402
from inventaire_dossier import ia  # noqa: E402
from inventaire_dossier.analyse import classer, inventorier  # noqa: E402
from inventaire_dossier.lecture import lire_dossier  # noqa: E402

CHAMPS = ["type", "statut", "date", "parties", "rattache_a", "fait_foi"]
# Mot-clé qu'une alerte produite doit contenir pour couvrir l'alerte attendue de même rang.
ALERTES = {"pièce d'un autre client": ("Précédent - contrat distribution", "autre"),
           "PDF non lu": ("Scan contrat signé 2023.pdf", "non lu"),
           "avenant 2 non signé": ("Avenant 2", "non signé"),
           "preuve de l'envoi recommandé de la résiliation absente": ("recommandé", "preuve")}


JEUX = {"developpement": ("pieces", "P01.json", "dossier de développement (a servi à écrire les règles)"),
        "controle": ("pieces-controle", "P01-controle.json", "dossier de contrôle (rédigé à part, inconnu des règles)")}


def evaluer(jeu: str = "developpement", acces=None) -> dict:
    """acces : (configuration, clé) pour le mode IA ; None pour les règles seules."""
    dossier, fichier, _libelle = JEUX[jeu]
    with open(os.path.join(ICI, "attendu", fichier), encoding="utf-8") as f:
        attendu = json.load(f)
    pieces, ignores = lire_dossier(os.path.join(ICI, dossier))
    if acces is None:
        inventaire = inventorier(os.path.join(ICI, dossier), pieces, ignores)
    else:
        inventaire = classer(os.path.join(ICI, dossier), pieces, ignores)
        envoi = ia.preparer_envoi(inventaire)
        ia.completer(inventaire, envoi, envoi.texte, *acces)
    fiches = {f.piece.chemin: f for f in inventaire.fiches}
    justes = {c: 0 for c in CHAMPS}
    ecarts = []
    for nom, att in attendu["pieces"].items():
        f = fiches.get(nom)
        if f is None:
            ecarts.append(f"{nom} : pièce absente de l'inventaire")
            continue
        for champ in CHAMPS:
            obtenu = getattr(f, champ)
            voulu = att[champ]
            if champ == "parties":
                ok = set(obtenu) == set(voulu)
            else:
                ok = obtenu == voulu
            justes[champ] += ok
            if not ok:
                ecarts.append(f"{nom} : {champ} = {obtenu!r}, attendu {voulu!r}")
    alertes_couvertes = []
    # Les alertes attendues du dossier de contrôle sont rédigées librement : elles se relisent à la main.
    for libelle, (cle1, cle2) in (ALERTES.items() if jeu == "developpement" else ()):
        couverte = any(cle1 in a and cle2 in a for a in inventaire.alertes)
        alertes_couvertes.append((libelle, couverte))
    return {"version": __version__, "n": len(attendu["pieces"]), "justes": justes, "ecarts": ecarts, "ia": inventaire.ia,
            "alertes": alertes_couvertes, "etat": inventaire.etat, "etat_attendu": attendu["dossier"]["etat"],
            "principal_ok": inventaire.contrat_principal == attendu["dossier"]["contrat_principal"]}


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    if "--ia" in argv:
        return mesurer_ia(argv)
    for jeu, (_d, _f, libelle) in JEUX.items():
        r = evaluer(jeu)
        details = jeu != "controle" or "--details-controle" in argv
        print(f"P01 {r['version']} (règles seules) sur F-DOSSIER-01 v1.0, {libelle}, {r['n']} pièces\n")
        for champ, n in r["justes"].items():
            print(f"  {champ:<12} {n:>2}/{r['n']}")
        print(f"\nContrat principal identifié : {'oui' if r['principal_ok'] else 'non'}")
        if details:
            print(f"État du dossier : {r['etat']}\n  attendu : {r['etat_attendu']}")
        if r["alertes"]:
            print("\nAlertes attendues :")
            for libelle_alerte, ok in r["alertes"]:
                print(f"  [{'x' if ok else ' '}] {libelle_alerte}")
        if details:
            print("\nÉcarts :" if r["ecarts"] else "\nÉcarts : aucun.")
            for e in r["ecarts"]:
                print(f"- {e}")
        else:
            print(f"\n{len(r['ecarts'])} écart(s), non détaillés (--details-controle pour les afficher, "
                  "seulement pour archiver une mesure).")
        print()
    return 0


def mesurer_ia(argv) -> int:
    def option(nom, defaut=None):
        return argv[argv.index(nom) + 1] if nom in argv and argv.index(nom) + 1 < len(argv) else defaut

    executions = int(option("--executions", "3"))
    try:
        acces = ia.charger_acces(ia.dossier_outil(), option("--config"))
    except Exception as e:
        print(f"Mesure impossible : {e}", file=sys.stderr)
        return 2
    print(f"Mode IA : {acces[0].fournisseur}, modèle {acces[0].modele}, {executions} exécution(s) par dossier.\n")
    for jeu, (_d, _f, libelle) in JEUX.items():
        resultats = [evaluer(jeu, acces) for _ in range(executions)]
        n = resultats[0]["n"]
        print(f"P01 {resultats[0]['version']} (mode IA) sur F-DOSSIER-01 v1.0, {libelle}, {n} pièces")
        for champ in CHAMPS:
            valeurs = [r["justes"][champ] for r in resultats]
            print(f"  {champ:<12} pire {min(valeurs):>2}/{n}   exécutions : {', '.join(map(str, valeurs))}")
        couts = [r["ia"].get("cout_usd") for r in resultats if r["ia"]]
        if all(c is not None for c in couts):
            print(f"  coût total : {sum(couts):.4f} USD")
        if jeu != "controle" or "--details-controle" in argv:
            for e in resultats[-1]["ecarts"]:
                print(f"  - {e}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
