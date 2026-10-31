"""Chemins et utilitaires communs aux tests (bibliothèque standard uniquement)."""

import ast
import importlib.util
import os
import sys

OUTIL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(OUTIL, "src")
DEPOT = os.path.dirname(os.path.dirname(OUTIL))
JEU = os.path.join(DEPOT, "factory", "jeux-de-test", "F-DOCX-01")
PIECES = os.path.join(JEU, "pieces")

if SRC not in sys.path:
    sys.path.insert(0, SRC)


def generateur():
    spec = importlib.util.spec_from_file_location("generer_f_docx_01", os.path.join(JEU, "generer.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Modules qui permettent une communication réseau. webbrowser n'est admis que dans
# l'interface, pour ouvrir le rapport local (fichier sur le disque) dans le navigateur.
MODULES_RESEAU = {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "poplib", "imaplib", "telnetlib",
                  "xmlrpc", "requests", "httpx", "aiohttp", "asyncio", "subprocess", "multiprocessing"}
EXCEPTIONS = {("interface.py", "webbrowser")}


def auditer_imports(dossier: str) -> list[str]:
    """Liste des importations interdites dans les fichiers Python d'un dossier."""
    violations = []
    for racine, _dossiers, fichiers in os.walk(dossier):
        for nom in fichiers:
            if not nom.endswith(".py"):
                continue
            chemin = os.path.join(racine, nom)
            with open(chemin, encoding="utf-8") as f:
                arbre = ast.parse(f.read(), chemin)
            for noeud in ast.walk(arbre):
                if isinstance(noeud, ast.Import):
                    modules = [a.name for a in noeud.names]
                elif isinstance(noeud, ast.ImportFrom) and noeud.level == 0 and noeud.module:
                    modules = [noeud.module]
                elif isinstance(noeud, ast.Call) and getattr(noeud.func, "id", "") in ("__import__", "exec", "eval"):
                    violations.append(f"{nom}: appel dynamique {noeud.func.id}()")
                    continue
                else:
                    continue
                for module in modules:
                    racine_module = module.split(".")[0]
                    if racine_module == "webbrowser" and (nom, "webbrowser") in EXCEPTIONS:
                        continue
                    if racine_module in MODULES_RESEAU or racine_module == "webbrowser":
                        violations.append(f"{nom}: import {module}")
    return violations
