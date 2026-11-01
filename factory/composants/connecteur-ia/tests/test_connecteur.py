"""Tests du connecteur IA, sans réseau : un faux fournisseur écoute sur 127.0.0.1."""

import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest import mock

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from connecteur_ia import (  # noqa: E402
    ErreurConfiguration,
    ErreurFournisseur,
    ErreurReponse,
    appeler,
    charger_configuration,
    estimer,
    extraire_json,
    lire_cle,
    resume_envoi,
)
from connecteur_ia.connecteur import PREREGLAGES  # noqa: E402

CLE = "sk-test-0123456789abcdef"


class FauxFournisseur(BaseHTTPRequestHandler):
    reponse = (200, {})
    recu = {}

    def do_POST(self):
        longueur = int(self.headers.get("Content-Length", 0))
        FauxFournisseur.recu = {"chemin": self.path, "entetes": self.headers,  # noms insensibles à la casse
                                "corps": json.loads(self.rfile.read(longueur))}
        statut, corps = FauxFournisseur.reponse
        donnees = corps if isinstance(corps, bytes) else json.dumps(corps).encode("utf-8")
        self.send_response(statut)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)

    def log_message(self, *_args):
        pass


def succes(contenu="Bonjour", entree=100, sortie=20):
    return (200, {"model": "faux-modele", "choices": [{"message": {"role": "assistant", "content": contenu}}],
                  "usage": {"prompt_tokens": entree, "completion_tokens": sortie}})


class AvecServeur(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serveur = HTTPServer(("127.0.0.1", 0), FauxFournisseur)
        threading.Thread(target=cls.serveur.serve_forever, daemon=True).start()
        cls.adresse = f"http://127.0.0.1:{cls.serveur.server_address[1]}/v1"

    @classmethod
    def tearDownClass(cls):
        cls.serveur.shutdown()
        cls.serveur.server_close()

    def config(self, **autres):
        base = {"fournisseur": "Faux", "adresse": self.adresse, "modele": "faux-modele",
                "variable_cle": "FAUSSE_CLE", "tarif_entree": 2.0, "tarif_sortie": 10.0,
                "tarifs_releves_le": "2026-10-31", "delai": 5}
        base.update(autres)
        return charger_configuration(base)


class Appel(AvecServeur):
    def test_requete_minimale_et_reponse(self):
        FauxFournisseur.reponse = succes("Réponse")
        r = appeler(self.config(entetes={"anthropic-workspace-id": "ws1"}), CLE, "Consigne", "Texte")
        recu = FauxFournisseur.recu
        self.assertEqual(recu["chemin"], "/v1/chat/completions")
        self.assertEqual(recu["entetes"]["Authorization"], f"Bearer {CLE}")
        self.assertEqual(recu["entetes"]["anthropic-workspace-id"], "ws1")
        self.assertEqual(set(recu["corps"]), {"model", "messages", "max_tokens"})
        self.assertEqual(recu["corps"]["messages"],
                         [{"role": "system", "content": "Consigne"}, {"role": "user", "content": "Texte"}])
        self.assertEqual(r.texte, "Réponse")
        self.assertEqual((r.jetons_entree, r.jetons_sortie), (100, 20))
        self.assertAlmostEqual(r.cout_usd, (100 * 2 + 20 * 10) / 1_000_000)

    def test_erreurs_traduites_sans_la_cle(self):
        cas = {401: "Clé API refusée", 403: "Clé API refusée", 429: "Limite atteinte",
               500: "ne répond pas correctement", 400: "Requête refusée"}
        for statut, attendu in cas.items():
            with self.subTest(statut=statut):
                FauxFournisseur.reponse = (statut, {"error": {"message": f"mauvaise clé {CLE}"}})
                with self.assertRaises(ErreurFournisseur) as ctx:
                    appeler(self.config(), CLE, "s", "t")
                self.assertIn(attendu, str(ctx.exception))
                self.assertNotIn(CLE, str(ctx.exception))
                self.assertEqual(ctx.exception.statut, statut)

    def test_reponse_illisible(self):
        for corps in (b"<html>pas du json</html>", {"choices": []}, {"choices": [{"message": {"content": None}}]}):
            with self.subTest(corps=corps):
                FauxFournisseur.reponse = (200, corps)
                with self.assertRaises(ErreurReponse):
                    appeler(self.config(), CLE, "s", "t")

    def test_cout_inconnu_sans_tarifs(self):
        FauxFournisseur.reponse = succes()
        r = appeler(self.config(tarif_entree=None, tarif_sortie=None), CLE, "s", "t")
        self.assertIsNone(r.cout_usd)

    def test_connexion_impossible(self):
        config = charger_configuration({"fournisseur": "Faux", "adresse": "http://127.0.0.1:9/v1",
                                        "modele": "m", "variable_cle": "X", "delai": 2})
        with self.assertRaises(ErreurFournisseur) as ctx:
            appeler(config, CLE, "s", "t")
        self.assertNotIn(CLE, str(ctx.exception))


class Configuration_(unittest.TestCase):
    def test_tous_les_prereglages_se_chargent(self):
        with open(PREREGLAGES, encoding="utf-8") as f:
            noms = json.load(f)
        for nom in noms:
            with self.subTest(prereglage=nom):
                config = charger_configuration({"prereglage": nom, "modele": "modele-choisi"})
                self.assertTrue(config.fournisseur)

    def test_prereglage_complete_et_surcharge(self):
        config = charger_configuration({"prereglage": "anthropic", "modele": "autre",
                                        "informations": {"zdr": "actif (déclaré)"}})
        self.assertEqual(config.url, "https://api.anthropic.com/v1/chat/completions")
        self.assertEqual(config.modele, "autre")
        self.assertEqual(config.informations.zdr, "actif (déclaré)")
        self.assertEqual(config.informations.nationalite, "société américaine")

    def test_modele_obligatoire(self):
        with self.assertRaises(ErreurConfiguration):
            charger_configuration({"prereglage": "mistral"})

    def test_cle_refusee_dans_la_configuration(self):
        with self.assertRaises(ErreurConfiguration) as ctx:
            charger_configuration({"prereglage": "openai", "api_key": CLE})
        self.assertNotIn(CLE, str(ctx.exception))

    def test_http_distant_refuse_http_local_admis(self):
        with self.assertRaises(ErreurConfiguration):
            charger_configuration({"fournisseur": "F", "adresse": "http://exemple.be/v1", "modele": "m",
                                   "variable_cle": "X"})
        self.assertTrue(charger_configuration({"prereglage": "local", "modele": "m"}).locale)

    def test_entete_authorization_refuse(self):
        with self.assertRaises(ErreurConfiguration):
            charger_configuration({"prereglage": "openai", "entetes": {"Authorization": "Bearer x"}})

    def test_champ_inconnu_et_fichier(self):
        with self.assertRaises(ErreurConfiguration):
            charger_configuration({"prereglage": "openai", "temperature": 0.2})
        with tempfile.TemporaryDirectory() as tmp:
            chemin = os.path.join(tmp, "config.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump({"prereglage": "openai"}, f)
            self.assertEqual(charger_configuration(chemin).fournisseur, "OpenAI")
            with self.assertRaises(ErreurConfiguration):
                charger_configuration(os.path.join(tmp, "absent.json"))


class Cle(unittest.TestCase):
    def setUp(self):
        self.config = charger_configuration({"prereglage": "openai"})

    def test_environnement_puis_fichier_env(self):
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": CLE}):
            self.assertEqual(lire_cle(self.config), CLE)
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=True):
            with open(os.path.join(tmp, ".env"), "w", encoding="utf-8") as f:
                f.write(f'# commentaire\nOPENAI_API_KEY="{CLE}"\n')
            self.assertEqual(lire_cle(self.config, tmp), CLE)

    def test_sans_cle_l_outil_ne_fonctionne_pas(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ErreurConfiguration) as ctx:
                lire_cle(self.config, tmp)
        self.assertIn("OPENAI_API_KEY", str(ctx.exception))

    def test_modele_local_sans_cle(self):
        self.assertEqual(lire_cle(charger_configuration({"prereglage": "local", "modele": "m"})), "local")


class EcranEtJson(unittest.TestCase):
    def test_estimation_et_resume(self):
        config = charger_configuration({"prereglage": "anthropic"})
        e = estimer(config, "a" * 400, "b" * 400)
        self.assertEqual(e.jetons_entree, 200)
        self.assertAlmostEqual(e.cout_max_usd, (200 * 2 + 4000 * 10) / 1_000_000)
        lignes = "\n".join(resume_envoi(config, e))
        for attendu in ("Anthropic", "aucune option UE", "société américaine", "ne vérifie pas", "2026-10-31"):
            self.assertIn(attendu, lignes)

    def test_resume_sans_tarifs(self):
        config = charger_configuration({"prereglage": "mistral", "modele": "m"})
        self.assertIn("non estimé", "\n".join(resume_envoi(config, estimer(config, "s", "t"))))

    def test_extraire_json(self):
        self.assertEqual(extraire_json('Voici :\n```json\n{"a": [1, 2]}\n```'), {"a": [1, 2]})
        self.assertEqual(extraire_json('[{"x": 1}] fin'), [{"x": 1}])
        self.assertEqual(extraire_json('{incomplet puis {"b": 2}'), {"b": 2})
        with self.assertRaises(ErreurReponse):
            extraire_json("aucun json ici")


if __name__ == "__main__":
    unittest.main()
