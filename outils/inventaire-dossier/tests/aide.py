"""Chemins et utilitaires communs aux tests (bibliothèque standard uniquement)."""

import ast
import importlib.util
import json
import os
import re
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest import mock

OUTIL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(OUTIL, "src")
DEPOT = os.path.dirname(os.path.dirname(OUTIL))
JEU = os.path.join(DEPOT, "factory", "jeux-de-test", "F-DOSSIER-01")
PIECES = os.path.join(JEU, "pieces")

if SRC not in sys.path:
    sys.path.insert(0, SRC)


def module_du_jeu(nom: str):
    spec = importlib.util.spec_from_file_location(f"f_dossier_01_{nom}", os.path.join(JEU, f"{nom}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def neutre(texte: str) -> dict:
    """Réponse qui ne propose rien : le résultat reste celui des règles."""
    return {"pieces": [{"piece": n, "parties": [], "rattache_a": None, "justification": ""}
                       for n in re.findall(r"^=== (P\d+) ===$", texte, re.M)]}


class Fournisseur:
    """Faux fournisseur d'IA sur 127.0.0.1. repondre(texte envoyé) -> objet JSON de la réponse du modèle."""

    def __init__(self, repondre=neutre, statut=200):
        self.repondre, self.statut, self.recus = repondre, statut, []
        fournisseur = self

        class Gestion(BaseHTTPRequestHandler):
            def do_POST(self):
                corps = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                fournisseur.recus.append(corps)
                contenu = json.dumps(fournisseur.repondre(corps["messages"][1]["content"]), ensure_ascii=False)
                donnees = json.dumps({"model": "faux-modele", "usage": {"prompt_tokens": 1000, "completion_tokens": 200},
                                      "choices": [{"message": {"role": "assistant", "content": contenu}}]}).encode()
                self.send_response(fournisseur.statut)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(donnees)))
                self.end_headers()
                self.wfile.write(donnees)

            def log_message(self, *_a):
                pass

        self.serveur = HTTPServer(("127.0.0.1", 0), Gestion)
        self.adresse = f"http://127.0.0.1:{self.serveur.server_address[1]}/v1"

    def __enter__(self):
        threading.Thread(target=self.serveur.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *_a):
        self.serveur.shutdown()
        self.serveur.server_close()

    def config(self, dossier: str) -> str:
        """Écrit une configuration qui pointe vers ce faux fournisseur (préréglage local : pas de clé)."""
        chemin = os.path.join(dossier, "config-ia.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump({"prereglage": "local", "adresse": self.adresse, "modele": "faux-modele",
                       "tarif_entree": 2.0, "tarif_sortie": 10.0, "tarifs_releves_le": "2026-10-31", "delai": 5}, f)
        return chemin


def cli_ia(arguments, fournisseur: Fournisseur, dossier_config: str, confirmer: str = "oui") -> int:
    """Ligne de commande avec le faux fournisseur et la confirmation tapée par l'avocat."""
    from inventaire_dossier.__main__ import main as cli
    with mock.patch("builtins.input", return_value=confirmer), mock.patch("sys.stdout"):
        return cli(list(arguments) + ["--config", fournisseur.config(dossier_config)])


def reseau_local_seulement():
    """Neutralise tout accès réseau, sauf vers 127.0.0.1 (le faux fournisseur)."""
    origine_connexion, origine_adresses = socket.create_connection, socket.getaddrinfo

    def connexion(adresse, *a, **k):
        if adresse[0] != "127.0.0.1":
            raise AssertionError(f"tentative d'accès réseau vers {adresse[0]}")
        return origine_connexion(adresse, *a, **k)

    def adresses(hote, *a, **k):
        if hote != "127.0.0.1":
            raise AssertionError(f"résolution de nom interdite : {hote}")
        return origine_adresses(hote, *a, **k)

    return mock.patch.multiple(socket, create_connection=connexion, getaddrinfo=adresses)


# Modules qui permettent une communication réseau. Seule la copie du connecteur IA en importe.
MODULES_RESEAU = {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "poplib", "imaplib", "telnetlib",
                  "xmlrpc", "requests", "httpx", "aiohttp", "asyncio", "subprocess", "multiprocessing", "webbrowser"}


def auditer_imports(dossier: str, recursif: bool = True, exclus: tuple[str, ...] = ()) -> list[str]:
    """Liste des importations interdites dans les fichiers Python d'un dossier (sous-dossiers exclus à part)."""
    violations = []
    for racine, dossiers, fichiers in os.walk(dossier):
        if not recursif:
            dossiers.clear()
        dossiers[:] = [d for d in dossiers if d not in exclus]
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
