"""Construit l'archive téléchargeable d'un outil, de façon reproductible.

    python scripts/empaqueter.py                 construit l'archive dans site/static/telechargements/
    python scripts/empaqueter.py --fiche         construit et reporte version, taille, empreinte dans la fiche du site
    python scripts/empaqueter.py --verifier      échoue si la fiche du site ne correspond pas à l'archive

L'archive est identique octet par octet d'une machine à l'autre (dates fixes, ordre trié,
fins de ligne normalisées), ce qui permet de publier son empreinte SHA-256 dans la fiche.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import re
import sys
import zipfile

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_ZIP = (2026, 1, 1, 0, 0, 0)
TEXTE = (".py", ".pyw", ".md", ".json", ".txt")
EXCLUS = {"tests", "verifications", "__pycache__"}

OUTILS = {
    "controle-avant-envoi": {
        "dossier": os.path.join(DEPOT, "outils", "controle-avant-envoi"),
        "version": os.path.join(DEPOT, "outils", "controle-avant-envoi", "src", "controle_avant_envoi", "__init__.py"),
        "fiche": os.path.join(DEPOT, "site", "content", "outils", "controle-avant-envoi.md"),
    },
    "glossaire-definitions": {
        "dossier": os.path.join(DEPOT, "outils", "glossaire-definitions"),
        "version": os.path.join(DEPOT, "outils", "glossaire-definitions", "src", "glossaire_definitions", "__init__.py"),
        "fiche": os.path.join(DEPOT, "site", "content", "outils", "glossaire-definitions.md"),
    },
    "inventaire-dossier": {
        "dossier": os.path.join(DEPOT, "outils", "inventaire-dossier"),
        "version": os.path.join(DEPOT, "outils", "inventaire-dossier", "src", "inventaire_dossier", "__init__.py"),
        "fiche": os.path.join(DEPOT, "site", "content", "outils", "inventaire-dossier.md"),
    },
    "pseudonymisation": {
        "dossier": os.path.join(DEPOT, "outils", "pseudonymisation"),
        "version": os.path.join(DEPOT, "outils", "pseudonymisation", "src", "pseudonymisation", "__init__.py"),
        "fiche": os.path.join(DEPOT, "site", "content", "outils", "pseudonymisation.md"),
    },
}


def version(chemin: str) -> str:
    with open(chemin, encoding="utf-8") as f:
        return re.search(r'__version__ = "([^"]+)"', f.read()).group(1)


def construire(slug: str) -> tuple[str, bytes]:
    outil = OUTILS[slug]
    v = version(outil["version"])
    prefixe = f"{slug}-{v}/"
    fichiers = []
    for racine, dossiers, noms in os.walk(outil["dossier"]):
        dossiers[:] = sorted(d for d in dossiers if d not in EXCLUS)
        for nom in noms:
            if nom.endswith(".pyc"):
                continue
            chemin = os.path.join(racine, nom)
            fichiers.append((os.path.relpath(chemin, outil["dossier"]).replace(os.sep, "/"), chemin))
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for relatif, chemin in sorted(fichiers):
            with open(chemin, "rb") as f:
                donnees = f.read()
            if relatif.endswith(TEXTE) or relatif == "LICENSE":
                donnees = donnees.replace(b"\r\n", b"\n")
            info = zipfile.ZipInfo(prefixe + relatif, DATE_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, donnees)
    return f"{slug}-{v}.zip", sortie.getvalue()


def taille_lisible(n: int) -> str:
    return f"{max(1, round(n / 1024))} Ko"


def valeurs_fiche(nom: str, donnees: bytes, v: str) -> dict[str, str]:
    return {"version": f'"{v}"', "telechargement": f'"/telechargements/{nom}"',
            "taille": f'"{taille_lisible(len(donnees))}"', "sha256": f'"{hashlib.sha256(donnees).hexdigest()}"'}


def lire_fiche(chemin: str) -> str:
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def ecarts_fiche(texte: str, valeurs: dict[str, str]) -> list[str]:
    ecarts = []
    for cle, valeur in valeurs.items():
        m = re.search(rf"^{cle}:\s*(.*)$", texte, re.MULTILINE)
        if not m or m.group(1).strip() != valeur:
            ecarts.append(f"{cle} : fiche {m.group(1).strip() if m else '(absent)'} / archive {valeur}")
    return ecarts


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sortie", default=os.path.join(DEPOT, "site", "static", "telechargements"))
    parser.add_argument("--fiche", action="store_true", help="met à jour la fiche du site")
    parser.add_argument("--verifier", action="store_true", help="contrôle la fiche sans rien écrire dans le dépôt")
    args = parser.parse_args(argv)
    code = 0
    for slug, outil in OUTILS.items():
        nom, donnees = construire(slug)
        valeurs = valeurs_fiche(nom, donnees, version(outil["version"]))
        if not args.verifier:
            os.makedirs(args.sortie, exist_ok=True)
            with open(os.path.join(args.sortie, nom), "wb") as f:
                f.write(donnees)
            print(f"{nom} : {len(donnees)} octets, SHA-256 {valeurs['sha256'].strip(chr(34))}")
        texte = lire_fiche(outil["fiche"])
        if args.fiche:
            for cle, valeur in valeurs.items():
                if re.search(rf"^{cle}:", texte, re.MULTILINE):
                    texte = re.sub(rf"^{cle}:.*$", f"{cle}: {valeur}", texte, count=1, flags=re.MULTILINE)
                else:
                    texte = texte.replace("\n---", f"\n{cle}: {valeur}\n---", 1)
            with open(outil["fiche"], "w", encoding="utf-8", newline="\n") as f:
                f.write(texte)
            print(f"Fiche mise à jour : {os.path.relpath(outil['fiche'], DEPOT)}")
        ecarts = ecarts_fiche(lire_fiche(outil["fiche"]), valeurs)
        if ecarts:
            code = 1
            print(f"{slug} : la fiche du site ne correspond pas à l'archive (lancer scripts/empaqueter.py --fiche)")
            for e in ecarts:
                print(f"  {e}")
    return code


if __name__ == "__main__":
    sys.exit(main())
