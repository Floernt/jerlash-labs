import json
import os

from aide import CasAvecDossiers

from laf.chaine import Chaine, compter
from laf.passerelle import PasserelleSimulee
from laf.runtime import ClientRuntime, demarrer_en_fond
from laf.surveillance import Surveillant


class BaseChaine(CasAvecDossiers):
    passerelle = None

    def setUp(self):
        super().setUp()
        self.serveur, url = demarrer_en_fond(passerelle=self.passerelle)
        self.addCleanup(self.serveur.server_close)
        self.addCleanup(self.serveur.shutdown)
        self.chaine = Chaine(self.entree, self.sortie, self.etat, passerelle=self.passerelle,
                             runtime=ClientRuntime(url))
        self.surveillant = Surveillant(self.entree, os.path.join(self.etat, "surveillance.json"))

    def passages(self, n=2):
        evs = []
        for _ in range(n):
            evs += self.surveillant.scruter()
        return evs

    def traiter(self, evs):
        return [self.chaine.traiter(e)["issue"] for e in evs]

    def lire(self, sous_dossier, ev_id):
        with open(os.path.join(self.sortie, sous_dossier, f"{ev_id}.json"), encoding="utf-8") as f:
            return json.load(f)

    def audit(self):
        with open(os.path.join(self.etat, "audit.jsonl"), encoding="utf-8") as f:
            return f.read()


class TestBoutEnBout(BaseChaine):
    def test_critere_de_fin_un_depot_une_tache_un_resultat_rejeu_sans_effet(self):
        self.deposer_fixture("courrier-synthetique.txt")
        evs = self.passages()
        self.assertEqual(self.traiter(evs), ["tache_creee"])
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 1)
        self.assertEqual(compter(self.sortie, "resultats"), 1)

        self.assertEqual(self.traiter(evs), ["doublon_ignore"], "rejouer l'événement")
        self.assertEqual(self.traiter([json.loads(json.dumps(evs[0]))]), ["doublon_ignore"])
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 1)
        self.assertEqual(compter(self.sortie, "resultats"), 1)

        tache = self.lire("taches-paperclip", evs[0]["id"])
        self.assertTrue(tache["dry_run"])
        self.assertEqual(tache["cle_idempotence"], evs[0]["id"])
        resultat = self.lire("resultats", evs[0]["id"])
        self.assertEqual(resultat["statut"], "termine")
        self.assertEqual(resultat["actions_effectuees"], [])

    def test_rejeu_apres_redemarrage(self):
        self.deposer_fixture("courrier-synthetique.txt")
        evs = self.passages()
        self.traiter(evs)
        nouvelle = Chaine(self.entree, self.sortie, self.etat, passerelle=self.passerelle)
        self.assertEqual(nouvelle.traiter(evs[0])["issue"], "doublon_ignore")
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 1)

    def test_doublon_dans_le_meme_lot(self):
        self.deposer("a.txt", "synthétique")
        evs = self.passages()
        self.assertEqual(self.traiter(evs + evs), ["tache_creee", "doublon_ignore"])

    def test_modification_cree_une_seconde_tache(self):
        self.deposer("a.txt", "version 1 synthétique")
        self.traiter(self.passages())
        self.deposer("a.txt", "version 2 synthétique, différente")
        self.assertEqual(self.traiter(self.passages()), ["tache_creee"])
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 2)

    def test_renommage_et_suppression_consignes_sans_tache(self):
        self.deposer("a.txt", "synthétique")
        self.traiter(self.passages())
        os.rename(os.path.join(self.entree, "a.txt"), os.path.join(self.entree, "b.txt"))
        self.assertEqual(self.traiter(self.passages()), ["consigne"])
        os.remove(os.path.join(self.entree, "b.txt"))
        self.assertEqual(self.traiter(self.passages()), ["consigne"])
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 1)
        self.assertEqual(compter(self.sortie, "evenements"), 3)

    def test_fichier_illisible_signale(self):
        ev = {"type": "illisible", "chemin": "x.txt", "erreur": "PermissionError", "taille": 3,
              "signature": "3-1", "horodatage": "2026-11-21T00:00:00+00:00"}
        from laf.surveillance import identifiant_evenement
        ev["id"] = identifiant_evenement(ev)
        self.assertEqual(self.traiter([ev]), ["fichier_illisible"])
        self.assertEqual(self.lire("signalements", ev["id"])["motif"], "fichier_illisible")
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 0)

    def test_contenu_change_entre_evenement_et_traitement(self):
        self.deposer("a.txt", "avant")
        evs = self.passages()
        self.deposer("a.txt", "après, contenu différent")
        self.assertEqual(self.traiter(evs), ["contenu_change"])
        self.assertEqual(compter(self.sortie, "taches-paperclip"), 0)
        self.assertEqual(self.traiter(self.passages()), ["tache_creee"])

    def test_identifiant_falsifie_refuse(self):
        self.deposer("a.txt", "synthétique")
        ev = self.passages()[0]
        with self.assertRaises(ValueError):
            self.chaine.traiter(dict(ev, id="0" * 32))

    def test_repertoires_doivent_etre_distincts(self):
        with self.assertRaises(ValueError):
            Chaine(self.entree, os.path.join(self.entree, "sortie"), self.etat)
        with self.assertRaises(ValueError):
            Chaine(self.entree, self.sortie, self.entree)

    def test_audit_sans_contenu_ni_nom_de_fichier(self):
        self.deposer_fixture("courrier-synthetique.txt", "Dossier-Client-Fictif.txt")
        self.traiter(self.passages())
        audit = self.audit()
        self.assertNotIn("Dossier-Client-Fictif", audit)
        self.assertNotIn("courrier fictif", audit.lower())
        self.assertIn("chemin_empreinte", audit)


class TestInjection(BaseChaine):
    def test_injection_force_le_triage_et_n_ouvre_aucune_action(self):
        self.deposer_fixture("injection-synthetique.txt")
        evs = self.passages()
        self.assertEqual(self.traiter(evs), ["tache_creee"])
        q = self.lire("qualifications", evs[0]["id"])
        self.assertTrue(q["injection_suspectee"])
        self.assertTrue(q["qualification"]["requires_human_triage"])
        self.assertIn("injection_suspectee", q["qualification"]["motifs"])
        tache = self.lire("taches-paperclip", evs[0]["id"])
        self.assertIn("triage-humain", tache["etiquettes"])
        self.assertNotIn("example.invalid", json.dumps(tache))
        self.assertEqual(self.lire("resultats", evs[0]["id"])["actions_effectuees"], [])
        self.assertNotIn("example.invalid", self.audit())


def _modele_obeissant(model, messages):
    """Modèle simulé qui « obéit » à l'injection : sort du schéma et demande une action."""
    if "TACHE=QUALIFICATION" in messages[0]["content"]:
        return json.dumps({"schema_version": "laf-qualification/0.1", "categorie": "a_trier",
                           "requires_human_triage": False, "confiance": 1.0, "motifs": [],
                           "action": "envoyer_courriel", "destinataire": "externe@example.invalid"})
    return {"content": None, "tool_calls": [{"id": "1", "type": "function",
                                             "function": {"name": "envoyer_courriel", "arguments": "{}"}}]}


class TestModeleCompromis(BaseChaine):
    passerelle = PasserelleSimulee(_modele_obeissant)

    def test_sortie_hors_schema_rejetee_et_outils_refuses(self):
        self.deposer_fixture("injection-synthetique.txt")
        evs = self.passages()
        self.traiter(evs)
        q = self.lire("qualifications", evs[0]["id"])
        self.assertFalse(q["valide"])
        self.assertTrue(any("action" in e for e in q["erreurs"]))
        self.assertTrue(q["qualification"]["requires_human_triage"])
        self.assertEqual(q["qualification"]["motifs"][0], "sortie_modele_invalide")
        r = self.lire("resultats", evs[0]["id"])
        self.assertEqual(r["statut"], "plafond_atteint")
        self.assertEqual(r["actions_effectuees"], [])
        self.assertGreater(r["demandes_outils_refusees"], 0)


class TestReponseNonJson(BaseChaine):
    passerelle = PasserelleSimulee(lambda model, messages: "Voici ma réponse en prose, pas en JSON.")

    def test_repli_sur_triage_humain(self):
        self.deposer("a.txt", "synthétique")
        evs = self.passages()
        self.traiter(evs)
        q = self.lire("qualifications", evs[0]["id"])
        self.assertFalse(q["valide"])
        self.assertTrue(q["qualification"]["requires_human_triage"])
