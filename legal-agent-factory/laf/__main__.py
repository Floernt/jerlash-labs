"""Ligne de commande de la chaîne du Lot 1.

  python -m laf runtime [--port 8765]
  python -m laf surveiller --entree D --sortie D --etat D [--intervalle 2] [--une-fois] [--runtime-url URL]
  python -m laf rejouer --evenement FICHIER --entree D --sortie D --etat D [--runtime-url URL]
  python -m laf demo
"""

import argparse
import os
import shutil
import sys
import tempfile
import time

from .chaine import Chaine, compter, lire_evenement, verifier_repertoires
from .runtime import ClientRuntime, creer_serveur, demarrer_en_fond
from .surveillance import Surveillant

FIXTURE_DEMO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "tests", "fixtures", "courrier-synthetique.txt")


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

    args = p.parse_args(argv)
    return args.fonction(args)


if __name__ == "__main__":
    sys.exit(main())
