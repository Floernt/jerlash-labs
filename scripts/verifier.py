"""Vérification complète du dépôt, en local comme en intégration continue.

    python scripts/verifier.py                 contrôles techniques
    python scripts/verifier.py --publication   en plus : aucun marqueur [À COMPLÉTER] / [À VÉRIFIER] / [À DÉCIDER]
                                               dans ce qui sera publié
    python scripts/verifier.py --exiger-hugo   échoue si Hugo est absent (utilisé en CI)

Chaque étape affiche sa preuve (commande, compte, fichier fautif). Code de sortie 0 seulement si tout passe.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(DEPOT, "site")
HUGO_VERSION = "0.148.2"
MARQUEURS = re.compile(r"\[À (?:COMPLÉTER|VÉRIFIER|DÉCIDER|VALIDER)[^\]]*\]")
CSP = "default-src 'none'; script-src 'self';"
# Seuls scripts admis : ceux du design system, servis par le site (ADR-022).
SCRIPTS_ADMIS = ("js/bundle.js", "js/init.js")

resultats: list[tuple[bool, str]] = []


def etape(ok: bool, message: str) -> bool:
    resultats.append((ok, message))
    print(("  ok    " if ok else "  ÉCHEC ") + message)
    return ok


def lancer(commande: list[str], cwd: str = DEPOT) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(commande)}")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(commande, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)


def verifier_secrets() -> None:
    print("\n[1] Secrets")
    r = lancer([sys.executable, "scripts/detecter_secrets.py", "--auto-test"])
    etape(r.returncode == 0, "la détection repère une fausse clé plantée")
    r = lancer([sys.executable, "scripts/detecter_secrets.py"])
    etape(r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())


def verifier_outils() -> None:
    print("\n[2] Outils : tests automatiques")
    dossiers = [os.path.join(DEPOT, base, nom)
                for base in ("outils", os.path.join("factory", "composants"))
                for nom in sorted(os.listdir(os.path.join(DEPOT, base)))]
    for dossier in dossiers:
        if not os.path.isdir(os.path.join(dossier, "tests")):
            continue
        outil = os.path.basename(dossier)
        r = lancer([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=dossier)
        bilan = [l for l in r.stderr.splitlines() if l.startswith(("Ran ", "OK", "FAILED"))]
        if r.returncode:
            print(r.stderr[-4000:])
        etape(r.returncode == 0, f"{outil} : " + " / ".join(bilan))


def verifier_composants() -> None:
    print("\n[2b] Composants copiés dans les outils (ADR-021)")
    r = lancer([sys.executable, "scripts/synchroniser_composants.py", "--verifier"])
    sortie = r.stdout.strip().splitlines()
    if r.returncode:
        print(r.stdout)
    etape(r.returncode == 0, sortie[-1] if sortie else r.stderr.strip())


def verifier_archive() -> None:
    print("\n[3] Archive téléchargeable et fiche du site")
    r = lancer([sys.executable, "scripts/empaqueter.py"])
    print(r.stdout.strip())
    etape(r.returncode == 0, "archive reproductible conforme à la fiche du site (version, taille, SHA-256)")


class Collecteur(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts, self.styles_inline, self.csp, self.liens, self.ressources = [], 0, False, [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type") != "application/ld+json":
            src = a.get("src", "")
            if not (src.startswith("/") and src.lstrip("/").endswith(SCRIPTS_ADMIS)):
                self.scripts.append(src or "inline")
        if tag == "style" or "style" in a:
            self.styles_inline += 1
        if tag == "meta" and a.get("http-equiv", "").lower() == "content-security-policy" and CSP in a.get("content", ""):
            self.csp = True
        if tag == "a" and a.get("href"):
            self.liens.append(a["href"])
        for attribut in ("src", "srcset"):
            if a.get(attribut):
                self.ressources.append(a[attribut])
        if tag == "link" and a.get("href") and a.get("rel") not in ("canonical", "alternate"):
            self.ressources.append(a["href"])


def verifier_site(exiger_hugo: bool) -> None:
    print("\n[4] Site")
    hugo = shutil.which("hugo")
    if not hugo:
        etape(not exiger_hugo, "Hugo absent : construction du site non vérifiée")
        return
    r = lancer(["hugo", "version"])
    etape(f"v{HUGO_VERSION}" in r.stdout and "extended" in r.stdout, f"Hugo extended {HUGO_VERSION} (ADR-002) : {r.stdout.strip()[:60]}")
    sortie = tempfile.mkdtemp(prefix="iavocat-site-")
    try:
        r = lancer(["hugo", "--source", SITE, "--destination", sortie, "--cleanDestinationDir",
                    "--panicOnWarning", "--printPathWarnings", "--quiet"])
        if not etape(r.returncode == 0, "construction Hugo sans erreur ni avertissement"):
            print(r.stdout[-3000:], r.stderr[-3000:])
            return
        pages = []
        for racine, _d, noms in os.walk(sortie):
            pages += [os.path.join(racine, n) for n in noms if n.endswith(".html")]
        defauts, liens_morts, externes = [], [], []
        for page in pages:
            c = Collecteur()
            with open(page, encoding="utf-8") as f:
                c.feed(f.read())
            rel = os.path.relpath(page, sortie)
            if not c.csp:
                defauts.append(f"{rel} : balise CSP absente")
            if c.scripts:
                defauts.append(f"{rel} : script {c.scripts}")
            if c.styles_inline:
                defauts.append(f"{rel} : {c.styles_inline} style(s) en ligne")
            externes += [f"{rel} : {x}" for x in c.ressources if re.match(r"(https?:)?//", x)]
            for lien in c.liens:
                if not lien.startswith("/") or lien.startswith("//"):
                    continue
                cible = os.path.join(sortie, lien.split("#")[0].split("?")[0].lstrip("/"))
                if not (os.path.isfile(cible) or os.path.isfile(os.path.join(cible, "index.html"))):
                    liens_morts.append(f"{rel} -> {lien}")
        etape(not defauts, f"{len(pages)} pages : CSP présente, aucun script hors design system, aucun style en ligne"
              + ("" if not defauts else " — " + "; ".join(defauts[:5])))
        etape(not externes, "aucune ressource chargée depuis un domaine tiers" + ("" if not externes else " — " + "; ".join(externes[:5])))
        etape(not liens_morts, "liens internes valides" + ("" if not liens_morts else " — " + "; ".join(liens_morts[:10])))
        for attendu in ("blog/index.xml", "sitemap.xml", ".nojekyll", ".well-known/security.txt", "js/bundle.js"):
            etape(os.path.isfile(os.path.join(sortie, attendu)), f"fichier produit : {attendu}")
    finally:
        shutil.rmtree(sortie, ignore_errors=True)


def verifier_blog() -> None:
    print("\n[4 ter] Blog : articles conformes à leur source (ADR-022)")
    r = lancer([sys.executable, "scripts/importer_articles.py", "--verifier"])
    sortie = r.stdout.strip().splitlines()
    if r.returncode:
        print(r.stdout)
    etape(r.returncode == 0, sortie[-1] if sortie else r.stderr.strip())


def verifier_typographie() -> None:
    print("\n[4 bis] Typographie française du site")
    r = lancer([sys.executable, "scripts/typographie.py", "--verifier"])
    etape(r.returncode == 0, "espaces insécables en place" if r.returncode == 0 else r.stdout.strip())


def verifier_marqueurs(publication: bool) -> None:
    print("\n[5] Marqueurs de travail dans ce qui sera publié")
    trouves = []
    # Les fiches des outils (outils/*/FICHE.md) ne sont plus publiées tant que les outils sont en brouillon (ADR-022).
    racines = [os.path.join(SITE, "content"), os.path.join(SITE, "static")]
    for racine in racines:
        chemins = [racine] if os.path.isfile(racine) else \
            [os.path.join(r, n) for r, _d, ns in os.walk(racine) for n in ns if n.endswith((".md", ".txt"))]
        for chemin in chemins:
            with open(chemin, encoding="utf-8") as f:
                lignes = f.readlines()
            if re.search(r"^draft:\s*true", "".join(lignes[:15]), re.MULTILINE):
                continue  # brouillon : non publié par Hugo
            for i, ligne in enumerate(lignes, start=1):
                for m in MARQUEURS.finditer(ligne):
                    trouves.append(f"{os.path.relpath(chemin, DEPOT)}:{i} {m.group(0)}")
    for t in trouves:
        print(f"    {t}")
    message = f"{len(trouves)} marqueur(s) à lever avant publication"
    etape(not trouves or not publication, message if trouves else "aucun marqueur")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--publication", action="store_true")
    parser.add_argument("--exiger-hugo", action="store_true")
    args = parser.parse_args(argv)
    verifier_secrets()
    verifier_outils()
    verifier_composants()
    verifier_archive()
    verifier_site(args.exiger_hugo)
    verifier_typographie()
    verifier_blog()
    verifier_marqueurs(args.publication)
    echecs = [m for ok, m in resultats if not ok]
    print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} vérifications réussies.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
