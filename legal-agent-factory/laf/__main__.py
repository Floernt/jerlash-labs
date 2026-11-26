"""Ligne de commande de la chaîne du Lot 1.

  python -m laf runtime [--port 8765]
  python -m laf surveiller --entree D --sortie D --etat D [--intervalle 2] [--une-fois] [--runtime-url URL]
  python -m laf rejouer --evenement FICHIER --entree D --sortie D --etat D [--runtime-url URL]
  python -m laf demo
  python -m laf evaluer sonde [--fournisseur simulee] [--modele M]
  python -m laf evaluer executer --cas CSV --serie JSON --sortie D [--pieces D] [--variantes] [--confirmer-holdout]
  python -m laf evaluer rapport --cas CSV --sortie D [--references D] [--notes D]
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import time

from .banc.cas import charger_cas
from .banc.execution import SerieRefusee, executer_serie
from .banc.rapport import produire
from .banc.sonde import sonder
from .chaine import Chaine, compter, lire_evenement, verifier_repertoires
from .passerelle import PasserelleScaleway, PasserelleSimulee, PasserelleUmans
from .runtime import ClientRuntime, creer_serveur, demarrer_en_fond
from .surveillance import Surveillant

RACINE_LAF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DEMO = os.path.join(RACINE_LAF, "tests", "fixtures", "courrier-synthetique.txt")
DOSSIER_CONFIG_BANC = os.path.join(RACINE_LAF, "config", "banc")


def _chaine(args) -> Chaine:
    runtime = ClientRuntime(args.runtime_url) if args.runtime_url else None
    return Chaine(args.entree, args.sortie, args.etat, runtime=runtime)


def cmd_runtime(args) -> int:
    serveur = creer_serveur(args.port)
    print(f"Runtime à l'écoute sur http://127.0.0.1:{serveur.server_address[1]} (Ctrl+C pour arrêter)")
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def cmd_surveiller(args) -> int:
    verifier_repertoires(args.entree, args.sortie, args.etat)
    chaine = _chaine(args)
    surveillant = Surveillant(args.entree, os.path.join(args.etat, "surveillance.json"))
    passages = 0
    try:
        while True:
            for ev in surveillant.scruter():
                r = chaine.traiter(ev)
                print(f"{ev['type']:<12} {r['issue']:<16} {ev['id']}")
            passages += 1
            if args.une_fois and passages >= 3:  # 3 passages : apparition, stabilité, suppression confirmée
                return 0
            time.sleep(args.intervalle)
    except KeyboardInterrupt:
        return 0


def cmd_rejouer(args) -> int:
    r = _chaine(args).traiter(lire_evenement(args.evenement))
    print(r["issue"])
    return 0


def cmd_demo(args) -> int:
    """Dépose un fichier synthétique, traite, rejoue, et compte les sorties."""
    racine = tempfile.mkdtemp(prefix="laf-demo-")
    entree, sortie, etat = (os.path.join(racine, n) for n in ("entree", "sortie", "etat"))
    for d in (entree, sortie, etat):
        os.makedirs(d)
    serveur, url = demarrer_en_fond()
    try:
        chaine = Chaine(entree, sortie, etat, runtime=ClientRuntime(url))
        surveillant = Surveillant(entree, os.path.join(etat, "surveillance.json"))
        shutil.copy(FIXTURE_DEMO, os.path.join(entree, "courrier-synthetique.txt"))
        evenements = surveillant.scruter() + surveillant.scruter()
        for ev in evenements:
            print(f"{ev['type']}: {chaine.traiter(ev)['issue']}")
        print("Rejeu du même événement :", chaine.traiter(evenements[0])["issue"])
        print(f"Charges utiles Paperclip : {compter(sortie, 'taches-paperclip')}")
        print(f"Fichiers de résultat     : {compter(sortie, 'resultats')}")
        print(f"Répertoire de démonstration : {racine}")
    finally:
        serveur.shutdown()
        serveur.server_close()
    return 0


PASSERELLES = {"simulee": PasserelleSimulee, "scaleway": PasserelleScaleway, "umans": PasserelleUmans}


def charger_serie(chemin: str) -> dict:
    """Lit une série ; les chemins `instructions`, `schema` et `dossiers` sont relatifs à son fichier."""
    with open(chemin, encoding="utf-8") as f:
        serie = {k: v for k, v in json.load(f).items() if not k.startswith("$")}
    base = os.path.dirname(os.path.abspath(chemin))
    for cle in ("instructions", "schema", "dossiers"):
        if serie.get(cle):
            serie[cle] = os.path.normpath(os.path.join(base, serie[cle]))
    return serie


def cmd_evaluer_sonde(args) -> int:
    print(json.dumps(sonder(PASSERELLES[args.fournisseur](), args.modele, args.repetitions),
                     ensure_ascii=False, indent=2))
    return 0


def cmd_evaluer_executer(args) -> int:
    serie = charger_serie(args.serie)
    try:
        resume = executer_serie(serie, charger_cas(args.cas), args.cas, args.pieces, args.sortie,
                                PASSERELLES[serie["fournisseur"]](), args.confirmer_holdout, args.variantes)
    except SerieRefusee as e:
        print(f"Série refusée : {e}", file=sys.stderr)
        return 2
    print(json.dumps(resume, ensure_ascii=False))
    if resume["plafond"]:
        print("Plafond de dépense atteint : série arrêtée, à signaler.", file=sys.stderr)
    return 0


def cmd_evaluer_rapport(args) -> int:
    sentinelles = None
    if args.sentinelles and os.path.isfile(args.sentinelles):
        with open(args.sentinelles, encoding="utf-8") as f:
            sentinelles = json.load(f)
    texte = produire(charger_cas(args.cas), args.sortie, args.references, args.notes, sentinelles)
    chemin = os.path.join(args.sortie, "rapport.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    print(chemin)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="laf", description="Legal Agent Factory, Lot 1 (local, sans secrets)")
    sous = p.add_subparsers(dest="commande", required=True)

    r = sous.add_parser("runtime", help="démarre le runtime HTTP local")
    r.add_argument("--port", type=int, default=8765)
    r.set_defaults(fonction=cmd_runtime)

    for nom, fonction in (("surveiller", cmd_surveiller), ("rejouer", cmd_rejouer)):
        s = sous.add_parser(nom)
        s.add_argument("--entree", required=True, help="dossier surveillé")
        s.add_argument("--sortie", required=True, help="répertoire de sortie (distinct)")
        s.add_argument("--etat", required=True, help="répertoire d'état (distinct)")
        s.add_argument("--runtime-url", help="ex. http://127.0.0.1:8765 ; à défaut, runtime en processus")
        s.set_defaults(fonction=fonction)
        if nom == "surveiller":
            s.add_argument("--intervalle", type=float, default=2.0)
            s.add_argument("--une-fois", action="store_true", help="trois passages puis arrêt")
        else:
            s.add_argument("--evenement", required=True, help="fichier JSON d'un événement (sortie/evenements/)")

    d = sous.add_parser("demo", help="démonstration de bout en bout dans un dossier temporaire")
    d.set_defaults(fonction=cmd_demo)

    e = sous.add_parser("evaluer", help="banc d'évaluation du Lot 3 (benchmark faillite)")
    ev = e.add_subparsers(dest="etape", required=True)
    s = ev.add_parser("sonde", help="JSON contraint et appels d'outils, par modèle et endpoint")
    s.add_argument("--fournisseur", default="simulee", choices=sorted(PASSERELLES))
    s.add_argument("--modele", default="simule-deterministe")
    s.add_argument("--repetitions", type=int, default=3)
    s.set_defaults(fonction=cmd_evaluer_sonde)
    x = ev.add_parser("executer", help="exécute une série gelée")
    x.add_argument("--cas", required=True, help="fichier CSV du benchmark (hors dépôt)")
    x.add_argument("--serie", required=True, help="configuration de la série (JSON)")
    x.add_argument("--pieces", help="dossier des pièces synthétiques, un sous-dossier par cas")
    x.add_argument("--sortie", required=True, help="répertoire de la série (un par configuration)")
    x.add_argument("--variantes", action="store_true", help="ajoute injections et variations de pièces")
    x.add_argument("--confirmer-holdout", action="store_true", help="autorise le jeu de test final")
    x.set_defaults(fonction=cmd_evaluer_executer)
    r = ev.add_parser("rapport", help="produit le rapport Markdown d'une série")
    r.add_argument("--cas", required=True)
    r.add_argument("--sortie", required=True)
    r.add_argument("--references", help="réponses de référence signées, <id>.json")
    r.add_argument("--notes", help="notes humaines, <id>.json")
    r.add_argument("--sentinelles", default=os.path.join(DOSSIER_CONFIG_BANC, "sentinelles.json"))
    r.set_defaults(fonction=cmd_evaluer_rapport)

    args = p.parse_args(argv)
    return args.fonction(args)


if __name__ == "__main__":
    sys.exit(main())
