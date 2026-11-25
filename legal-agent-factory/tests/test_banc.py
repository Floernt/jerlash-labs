"""Tests du banc d'évaluation (Lot 3, MVP) : modèle simulé, aucun appel réseau.

Les cas de test sont techniques : ils ne reprennent pas le benchmark (hors dépôt)
et ne contiennent aucune réponse juridique.
"""

import json
import os
import shutil
import tempfile
import unittest

from aide import RACINE

from laf.banc import cas as mod_cas
from laf.banc.execution import SerieRefusee, executer_serie
from laf.banc.rapport import produire
from laf.banc.sonde import sonder
from laf.passerelle import PasserelleSimulee, _reponse
from laf.__main__ import charger_serie, main

ENTETE = "id,axe,scenario,canal,acteur,attendu,sources_a_verifier,erreur_critique,jeu,statut_gold\n"
CSV = ENTETE + (
    "T-01,ingestion,Scenario technique A,folder,curateur,ATTENDU-SECRET-A,F1,non,design,a_valider_humainement\n"
    "T-02,cautions,Scenario technique B,email,creancier,ATTENDU-SECRET-B,F7;F8,oui,design,a_valider_humainement\n"
    "T-03,curatelle,Scenario technique C,email,curateur,ATTENDU-SECRET-C,F3,oui,holdout,a_valider_humainement\n")
SERIE_EXEMPLE = os.path.join(RACINE, "config", "banc", "serie-simulee-design.json")


class Base(unittest.TestCase):
    def setUp(self):
        self.racine = tempfile.mkdtemp(prefix="laf-banc-")
        self.csv = os.path.join(self.racine, "cas.csv")
        with open(self.csv, "w", encoding="utf-8-sig", newline="") as f:
            f.write(CSV)
        self.pieces = os.path.join(self.racine, "pieces")
        self.sortie = os.path.join(self.racine, "serie")
        self.deposer("T-02", "facture.txt", "Facture synthétique n° 1, montant 100 EUR.")
        self.deposer("T-02", "courriel.txt", "Courriel synthétique d'un créancier fictif.")
        self.deposer("T-03", "note.txt", "Note synthétique du curateur fictif.")
        self.serie = charger_serie(SERIE_EXEMPLE)
        self.cas = mod_cas.charger_cas(self.csv)

    def tearDown(self):
        shutil.rmtree(self.racine, ignore_errors=True)

    def deposer(self, id_, nom, texte):
        os.makedirs(os.path.join(self.pieces, id_), exist_ok=True)
        with open(os.path.join(self.pieces, id_, nom), "w", encoding="utf-8") as f:
            f.write(texte)

    def executer(self, passerelle=None, **kw):
        return executer_serie(kw.pop("serie", self.serie), self.cas, self.csv, self.pieces, self.sortie,
                              passerelle or PasserelleSimulee(), **kw)

    def resultat(self, id_):
        with open(os.path.join(self.sortie, "resultats", f"{id_}.json"), encoding="utf-8") as f:
            return json.load(f)


class TestCas(Base):
    def test_chargement_et_jeux_repris_du_fichier(self):
        self.assertEqual([c["jeu"] for c in self.cas], ["design", "design", "holdout"])
        self.assertTrue(self.cas[1]["erreur_critique"])
        self.assertEqual(self.cas[1]["sources_a_verifier"], ["F7", "F8"])

    def test_colonnes_inattendues_refusees(self):
        with open(self.csv, "w", encoding="utf-8") as f:
            f.write("id,axe\nX,ingestion\n")
        with self.assertRaises(mod_cas.CasInvalides):
            mod_cas.charger_cas(self.csv)

    def test_reference_non_signee_ecartee_et_note_sans_reference_ignoree(self):
        refs = os.path.join(self.racine, "refs")
        notes = os.path.join(self.racine, "notes")
        os.makedirs(refs)
        os.makedirs(notes)
        for id_, ref in (("T-01", {"signe_par": "", "date_signature": "2026-12-01"}),
                         ("T-02", {"signe_par": "FE", "date_signature": "2026-12-01"})):
            with open(os.path.join(refs, f"{id_}.json"), "w", encoding="utf-8") as f:
                json.dump(ref, f)
        for id_ in ("T-01", "T-02"):
            with open(os.path.join(notes, f"{id_}.json"), "w", encoding="utf-8") as f:
                json.dump({"note_par": "FE", "dimensions": {"faits_critiques": "echec", "inconnue": "reussi"}}, f)
        retenues, ecartees = mod_cas.charger_references(refs, ["T-01", "T-02"])
        self.assertEqual((list(retenues), ecartees), (["T-02"], ["T-01"]))
        n, ignorees = mod_cas.charger_notes(notes, ["T-01", "T-02"], retenues)
        self.assertEqual(n, {"T-02": {"faits_critiques": "echec"}})
        self.assertEqual(ignorees, ["T-01"])


class TestExecution(Base):
    def test_design_seulement_et_pieces_manquantes(self):
        resume = self.executer()
        self.assertEqual((resume["executes"], resume["pieces_manquantes"]), (1, 1))
        self.assertEqual(self.resultat("T-01")["motif"], "pieces_manquantes")
        r = self.resultat("T-02")
        self.assertEqual((r["statut_execution"], r["runtime_statut"], r["pieces"]), ("execute", "termine", 2))
        self.assertEqual(r["actions_effectuees"], [])
        self.assertFalse(os.path.exists(os.path.join(self.sortie, "resultats", "T-03.json")))

    def test_holdout_exige_une_confirmation(self):
        serie = dict(self.serie, jeu="holdout")
        with self.assertRaises(SerieRefusee):
            self.executer(serie=serie)
        self.assertEqual(self.executer(serie=serie, confirmer_holdout=True)["executes"], 1)

    def test_le_systeme_evalue_ne_voit_ni_attendu_ni_scenario(self):
        vus = []

        def repondre(model, messages):
            vus.append(json.dumps(messages, ensure_ascii=False))
            return PasserelleSimulee._par_defaut(model, messages)
        self.executer(PasserelleSimulee(repondre))
        self.assertTrue(vus)
        self.assertFalse(any("ATTENDU-SECRET" in m or "Scenario technique" in m for m in vus))

    def test_gel_refuse_une_configuration_modifiee_et_reprend_a_l_identique(self):
        self.executer()
        self.assertEqual(self.executer()["repris"], 2)
        with self.assertRaises(SerieRefusee):
            self.executer(serie=dict(self.serie, modele="autre"))
        self.deposer("T-02", "nouvelle.txt", "Pièce ajoutée après le gel.")
        with self.assertRaises(SerieRefusee):
            self.executer()

    def test_fournisseur_reel_sans_plafond_ni_tarifs_refuse(self):
        class Reelle(PasserelleSimulee):
            nom = "scaleway"
        with self.assertRaises(SerieRefusee):
            self.executer(Reelle())
        with self.assertRaises(SerieRefusee):
            self.executer(Reelle(), serie=dict(self.serie, plafond=1.0))

    def test_plafond_arrete_la_serie(self):
        class Couteuse(PasserelleSimulee):
            def chat_completions(self, model, messages, **options):
                r = super().chat_completions(model, messages, **options)
                r["usage"] = {"prompt_tokens": 1_000_000, "completion_tokens": 0}
                return r
        self.deposer("T-01", "a.txt", "Pièce synthétique.")
        serie = dict(self.serie, tarifs={"entree_par_million": 1.0, "sortie_par_million": 1.0}, plafond=1.0)
        resume = self.executer(Couteuse(), serie=serie)
        self.assertEqual((resume["executes"], resume["plafond"]), (1, 1))
        self.assertEqual(self.resultat("T-01")["cout"], 2.0)
        # Plafond relevé : même série, reprise du cas restant.
        resume = self.executer(Couteuse(), serie=dict(serie, plafond=10.0))
        self.assertEqual((resume["executes"], resume["repris"]), (1, 1))

    def test_variantes_et_tentative_d_action_comptee(self):
        def obeit(model, messages):
            if "TACHE=QUALIFICATION" in messages[0]["content"]:
                return PasserelleSimulee._par_defaut(model, messages)
            texte = messages[-1].get("content") or ""
            if "dépôt sur la plateforme" in texte and messages[-1]["role"] == "user":
                return {"content": None, "tool_calls": [
                    {"id": "c1", "type": "function", "function": {"name": "deposer", "arguments": "{}"}}]}
            return "ok"
        self.executer(PasserelleSimulee(obeit), avec_variantes=True)
        inj = self.resultat("T-02~inj-depot")
        self.assertGreater(inj["demandes_outils_refusees"], 0)
        self.assertEqual(inj["actions_effectuees"], [])
        self.assertTrue(self.resultat("T-02~inj-consigne")["injection_suspectee"])
        self.assertEqual(self.resultat("T-02~ordre-inverse")["pieces"], 2)


class TestRapport(Base):
    def test_rapport_non_evalue_et_critiques_separes(self):
        self.executer(avec_variantes=True)
        texte = produire(self.cas, self.sortie, sentinelles={"$comment": "x", "essai": ["T-02", "T-03"]})
        self.assertTrue(texte.splitlines()[2].startswith("> [À VÉRIFIER]"))
        self.assertIn("Cas à erreur critique", texte)
        self.assertIn("| T-02 | cautions | exécuté | aucune | non évalué (pas de référence signée) |", texte)
        self.assertIn("Cas critiques de l'autre jeu, non couverts par cette série : T-03.", texte)
        self.assertIn("non évalué : 2 cas sans référence signée", texte)
        self.assertIn("T-03 : hors jeu", texte)
        self.assertIn("T-02~inj-depot", texte)
        self.assertNotIn("ATTENDU-SECRET", texte)
        self.assertNotIn("moyenne", texte.lower())


class Capable:
    nom = "capable"

    def chat_completions(self, model, messages, **options):
        if "response_format" in options:
            return _reponse(model, messages, '{"statut": "ok", "nombre": 3}')
        return _reponse(model, messages, None, [{"id": "x", "type": "function", "function": {
            "name": "enregistrer_sonde", "arguments": '{"valeur": 7}'}}])


class Defaillante:
    nom = "defaillante"

    def chat_completions(self, model, messages, **options):
        raise ConnectionError("endpoint indisponible")


class TestSonde(unittest.TestCase):
    def test_capacites_observees_ou_non(self):
        r = sonder(Capable(), "m", repetitions=2)
        self.assertEqual((r["json_contraint"]["conclusion"], r["appels_outils"]["conclusion"]),
                         ("observe", "observe"))
        r = sonder(PasserelleSimulee(), "m", repetitions=1)
        self.assertEqual((r["json_contraint"]["conclusion"], r["appels_outils"]["conclusion"]),
                         ("non_observe", "non_observe"))
        r = sonder(Defaillante(), "m", repetitions=1)
        self.assertEqual(r["json_contraint"]["essais"][0], {"issue": "erreur", "detail": "ConnectionError"})

    def test_adaptateurs_non_branches_donnent_une_erreur_observee(self):
        self.assertEqual(main(["evaluer", "sonde", "--fournisseur", "scaleway", "--modele", "x",
                               "--repetitions", "1"]), 0)


class TestLigneDeCommande(Base):
    def test_executer_puis_rapport(self):
        self.assertEqual(main(["evaluer", "executer", "--cas", self.csv, "--serie", SERIE_EXEMPLE,
                               "--pieces", self.pieces, "--sortie", self.sortie]), 0)
        self.assertEqual(main(["evaluer", "rapport", "--cas", self.csv, "--sortie", self.sortie]), 0)
        self.assertTrue(os.path.isfile(os.path.join(self.sortie, "rapport.md")))
        self.assertEqual(main(["evaluer", "executer", "--cas", self.csv, "--serie", SERIE_EXEMPLE,
                               "--sortie", self.sortie, "--confirmer-holdout"]), 2)


if __name__ == "__main__":
    unittest.main()
