"""Runtime d'exécution : execute(task, case_context, skill_bundle, policy) -> result.

Indépendant de Paperclip : il reçoit des dictionnaires et renvoie un dictionnaire.
Il est exposé par un petit serveur HTTP (bibliothèque standard) qui n'écoute que
sur l'interface locale.

Lot 1, niveau A3 de la fiche §12 : aucune action n'est disponible. Le runtime ne
connaît aucun outil ; une demande d'outil du modèle est refusée et comptée comme
un tour. Le nombre de tours est plafonné.
"""

import http.client
import ipaddress
import json
import socketserver
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import securite
from .passerelle import PasserelleSimulee, appels_outils, contenu

PLAFOND_TOURS = 4
TAILLE_MAX_REQUETE = 1_000_000
POLITIQUE_LOT1 = {"niveau": "A3", "actions_autorisees": [], "max_tours": PLAFOND_TOURS}


def _refus(task, motif):
    return {"task_id": task.get("id"), "statut": "refuse", "motif": motif, "tours": 0,
            "sortie": None, "actions_effectuees": []}


def execute(task: dict, case_context: dict, skill_bundle: dict, policy: dict,
            passerelle=None, modele: str = "simule-deterministe") -> dict:
    passerelle = passerelle or PasserelleSimulee()
    if policy.get("actions_autorisees"):
        return _refus(task, "le Lot 1 n'autorise aucune action (niveau A3)")
    max_tours = min(int(policy.get("max_tours", PLAFOND_TOURS)), PLAFOND_TOURS)
    if max_tours < 1:
        return _refus(task, "plafond de tours invalide")

    donnees = json.dumps({"tache": task, "contexte": case_context}, ensure_ascii=False, sort_keys=True)
    messages = [
        {"role": "system", "content": f"{skill_bundle.get('instructions', '')}\n"
                                      "Aucun outil n'est disponible. " + securite.AVERTISSEMENT},
        {"role": "user", "content": securite.encadrer(donnees, 50_000)},
    ]
    tours, refusees = 0, 0
    while tours < max_tours:
        tours += 1
        reponse = passerelle.chat_completions(modele, messages, temperature=0)
        demandes = appels_outils(reponse)
        if not demandes:
            return {"task_id": task.get("id"), "statut": "termine", "tours": tours,
                    "sortie": contenu(reponse), "actions_effectuees": [],
                    "demandes_outils_refusees": refusees, "skill": skill_bundle.get("nom"),
                    "modele": modele}
        refusees += len(demandes)
        messages.append(reponse["choices"][0]["message"])
        for d in demandes:
            messages.append({"role": "tool", "tool_call_id": d.get("id", ""),
                             "content": "Refusé : aucun outil n'est disponible (niveau A3)."})
    return {"task_id": task.get("id"), "statut": "plafond_atteint", "tours": tours, "sortie": None,
            "actions_effectuees": [], "demandes_outils_refusees": refusees,
            "skill": skill_bundle.get("nom"), "modele": modele}


def _boucle_locale(hote: str) -> bool:
    if hote == "localhost":
        return True
    try:
        return ipaddress.ip_address(hote).is_loopback
    except ValueError:
        return False


class _Gestionnaire(BaseHTTPRequestHandler):
    passerelle = None

    def log_message(self, *args):  # pas de journal HTTP : il pourrait contenir des données
        pass

    def _repondre(self, code, corps):
        donnees = json.dumps(corps, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)

    def do_GET(self):
        if self.path == "/sante":
            self._repondre(200, {"statut": "ok", "politique": POLITIQUE_LOT1})
        else:
            self._repondre(404, {"erreur": "inconnu"})

    def do_POST(self):
        if self.path != "/execute":
            return self._repondre(404, {"erreur": "inconnu"})
        longueur = int(self.headers.get("Content-Length") or 0)
        if longueur <= 0 or longueur > TAILLE_MAX_REQUETE:
            return self._repondre(413, {"erreur": "taille de requête refusée"})
        try:
            corps = json.loads(self.rfile.read(longueur).decode("utf-8"))
            arguments = [corps[k] for k in ("task", "case_context", "skill_bundle", "policy")]
            if not all(isinstance(a, dict) for a in arguments):
                raise TypeError
        except (ValueError, KeyError, TypeError):
            return self._repondre(400, {"erreur": "requête invalide"})
        self._repondre(200, execute(*arguments, passerelle=self.passerelle))


class _ServeurLocal(ThreadingHTTPServer):
    daemon_threads = True

    def server_bind(self):
        # HTTPServer.server_bind résout le nom complet de la machine (lent sous Windows) : inutile ici
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


def creer_serveur(port: int = 0, hote: str = "127.0.0.1", passerelle=None) -> ThreadingHTTPServer:
    """Serveur prêt à démarrer. Refuse toute interface autre que locale."""
    if not _boucle_locale(hote):
        raise ValueError("le runtime n'écoute que sur l'interface locale")
    gestionnaire = type("Gestionnaire", (_Gestionnaire,), {"passerelle": passerelle or PasserelleSimulee()})
    return _ServeurLocal((hote, port), gestionnaire)


def demarrer_en_fond(port: int = 0, passerelle=None) -> tuple[ThreadingHTTPServer, str]:
    serveur = creer_serveur(port, passerelle=passerelle)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur, f"http://127.0.0.1:{serveur.server_address[1]}"


class ClientRuntime:
    """Appelle le runtime HTTP local. Refuse une adresse qui n'est pas locale."""

    def __init__(self, url: str, delai: float = 30):
        morceaux = urllib.parse.urlsplit(url)
        if morceaux.scheme != "http" or not _boucle_locale(morceaux.hostname or ""):
            raise ValueError("le runtime doit être joint sur l'interface locale (http://127.0.0.1:port)")
        self.hote, self.port, self.delai = morceaux.hostname, morceaux.port or 80, delai

    def execute(self, task, case_context, skill_bundle, policy) -> dict:
        corps = json.dumps({"task": task, "case_context": case_context,
                            "skill_bundle": skill_bundle, "policy": policy}).encode("utf-8")
        # connexion directe : le serveur est local, aucun mandataire (proxy) ne doit s'interposer
        connexion = http.client.HTTPConnection(self.hote, self.port, timeout=self.delai)
        try:
            connexion.request("POST", "/execute", body=corps, headers={"Content-Type": "application/json"})
            reponse = connexion.getresponse()
            donnees = reponse.read().decode("utf-8")
            if reponse.status != 200:
                raise RuntimeError(f"runtime : réponse HTTP {reponse.status}")
            return json.loads(donnees)
        finally:
            connexion.close()


class RuntimeLocal:
    """Même interface que ClientRuntime, sans HTTP (utile hors service)."""

    def __init__(self, passerelle=None, modele: str = "simule-deterministe"):
        self.passerelle = passerelle
        self.modele = modele

    def execute(self, task, case_context, skill_bundle, policy) -> dict:
        return execute(task, case_context, skill_bundle, policy, passerelle=self.passerelle, modele=self.modele)
