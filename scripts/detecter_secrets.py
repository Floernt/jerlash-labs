"""Détection de secrets dans le dépôt (bibliothèque standard uniquement).

    python scripts/detecter_secrets.py              fichiers suivis et non ignorés du dépôt
    python scripts/detecter_secrets.py --indexe     contenu indexé pour le prochain commit (hook pre-commit)
    python scripts/detecter_secrets.py --auto-test  vérifie que la détection fonctionne sur une fausse clé

Code de sortie : 0 rien trouvé, 1 secret probable trouvé (ou auto-test en échec).
En cas de détection d'un secret déjà poussé : le révoquer chez le fournisseur d'abord,
puis nettoyer l'historique. Supprimer le fichier ne suffit pas.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOTIFS = [
    ("clé Anthropic", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("clé OpenAI", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{32,}")),
    ("clé Google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("clé AWS", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("jeton GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b")),
    ("clé privée", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY")),
    ("valeur secrète en clair", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|password|mot_de_passe)\b\s*[:=]\s*[\"'][^\"'\s]{16,}[\"']")),
]


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", DEPOT, *args], check=True, capture_output=True).stdout


def analyser_texte(nom: str, contenu: bytes) -> list[str]:
    if b"\x00" in contenu[:8000]:
        return []  # fichier binaire
    texte = contenu.decode("utf-8", errors="replace")
    trouves = []
    for numero, ligne in enumerate(texte.splitlines(), start=1):
        for libelle, motif in MOTIFS:
            if motif.search(ligne):
                trouves.append(f"{nom}:{numero} : {libelle} probable")
    return trouves


def fichiers_depot() -> list[tuple[str, bytes]]:
    noms = git("ls-files", "-co", "--exclude-standard", "-z").decode("utf-8").split("\0")
    resultat = []
    for nom in filter(None, noms):
        chemin = os.path.join(DEPOT, nom)
        if os.path.isfile(chemin):
            with open(chemin, "rb") as f:
                resultat.append((nom, f.read()))
    return resultat


def fichiers_indexes() -> list[tuple[str, bytes]]:
    noms = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").decode("utf-8").split("\0")
    return [(nom, git("show", f":{nom}")) for nom in filter(None, noms)]


def auto_test() -> bool:
    fausse_cle = "sk-" + "ant-" + "api03-" + "x" * 40  # construite à l'exécution : aucun motif littéral dans le dépôt
    with tempfile.TemporaryDirectory() as dossier:
        chemin = os.path.join(dossier, "config.py")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(f'CLE = "{fausse_cle}"\n')
        with open(chemin, "rb") as f:
            return bool(analyser_texte("config.py", f.read()))


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    groupe = parser.add_mutually_exclusive_group()
    groupe.add_argument("--indexe", action="store_true")
    groupe.add_argument("--auto-test", action="store_true")
    args = parser.parse_args(argv)
    if args.auto_test:
        ok = auto_test()
        print("Auto-test de détection : " + ("réussi" if ok else "ÉCHEC, la fausse clé n'a pas été détectée"))
        return 0 if ok else 1
    fichiers = fichiers_indexes() if args.indexe else fichiers_depot()
    trouves = [t for nom, contenu in fichiers for t in analyser_texte(nom, contenu)]
    for t in trouves:
        print(t)
    if trouves:
        print(f"\n{len(trouves)} secret(s) probable(s). Commit refusé. Retirez la valeur et, si elle a déjà circulé, révoquez-la.")
        return 1
    print(f"Aucun secret détecté ({len(fichiers)} fichier(s) examiné(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
