"""Chemins et utilitaires communs aux tests (bibliothèque standard uniquement)."""

import ast
import importlib.util
import os
import sys

OUTIL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(OUTIL, "src")
DEPOT = os.path.dirname(os.path.dirname(OUTIL))
JEU = os.path.join(DEPOT, "factory", "jeux-de-test", "F-IDENT-01")
PIECES = os.path.join(JEU, "pieces")

if SRC not in sys.path:
    sys.path.insert(0, SRC)


def module_du_jeu(nom: str):
    spec = importlib.util.spec_from_file_location(f"f_ident_01_{nom}", os.path.join(JEU, f"{nom}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Modules qui permettent une communication réseau. L'outil n'en importe aucun, pas même webbrowser.
MODULES_RESEAU = {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "poplib", "imaplib", "telnetlib",
                  "xmlrpc", "requests", "httpx", "aiohttp", "asyncio", "subprocess", "multiprocessing", "webbrowser"}


def auditer_imports(dossier: str, recursif: bool = True) -> list[str]:
    """Liste des importations interdites dans les fichiers Python d'un dossier."""
    violations = []
    for racine, dossiers, fichiers in os.walk(dossier):
        if not recursif:
            dossiers.clear()
        for nom in fichiers:
            if not nom.endswith((".py", ".pyw")):
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
                violations += [f"{nom}: import {m}" for m in modules if m.split(".")[0] in MODULES_RESEAU]
    return violations
