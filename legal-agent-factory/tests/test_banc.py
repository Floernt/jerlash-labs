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
        self.assertIn("| inj-depot | 1 | 0/1 | 1/1 | 0 | 0 |", texte)
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


# --- Banc branché sur la chaîne du Lot 2 -------------------------------------------------------

from laf.banc import lot2 as mod_lot2
from laf import courriel as mod_courriel
from aide_lot2 import INTAKE, reponses

SERIE_LOT2 = os.path.join(RACINE, "config", "banc", "serie-simulee-lot2-design.json")
COURRIEL = ("DOCUMENT SYNTHÉTIQUE DE TEST.\n\nDe : creancier@exemple.invalid\n"
            "À : cabinet@exemple.invalid, associe@exemple.invalid\nDate : 2026-11-04 10:12\n"
            "Objet : Société fictive - faillite\nPièces jointes : facture.txt\n\nMaître,\n\nCorps du message.\n")


def routage_valide(**champs) -> str:
    return json.dumps(dict(reponses()["defaut"], intention="nouvelle_affaire_faillite",
                           skill_propose=INTAKE, **champs))


class Routante(PasserelleSimulee):
    """Modèle simulé qui renvoie un routage conforme et la sortie de skill enregistrée.
    Données de test du routage, pas une réponse juridique."""

    def __init__(self, tokens=0):
        super().__init__(self._repondre)
        self.tokens = tokens

    def _repondre(self, model, messages):
        systeme = messages[0]["content"]
        if systeme.startswith("TACHE=ROUTAGE"):
            return routage_valide()
        if systeme.startswith("SKILL="):
            return json.dumps(dict(reponses()["sortie_skill_simulee"], skill=INTAKE, dossier="ATTENTE"))
        return PasserelleSimulee._par_defaut(model, messages)

    def chat_completions(self, model, messages, **options):
        r = super().chat_completions(model, messages, **options)
        r["usage"] = {"prompt_tokens": self.tokens, "completion_tokens": 0}
        return r


class BaseLot2Banc(Base):
    def setUp(self):
        super().setUp()
        shutil.rmtree(self.pieces)
        self.deposer("T-01", "01-jugement.txt", "Jugement synthétique.")
        self.deposer("T-01", "02-note.txt", "Note synthétique du curateur fictif.")
        self.deposer("T-02", "00-contexte-dossiers-cabinet.txt", "PIÈCE DE CONTEXTE synthétique.")
        self.deposer("T-02", "01-courriel.txt", COURRIEL)
        self.deposer("T-02", "02-facture.txt", "Facture synthétique n° 1, montant 100 EUR.")
        self.serie = charger_serie(SERIE_LOT2)


class TestCourrielDuBanc(BaseLot2Banc):
    def test_conversion_au_format_intermediaire(self):
        from laf.banc.execution import lire_pieces
        recues, contexte = mod_lot2.separer_contexte(lire_pieces(self.pieces, "T-02"))
        self.assertEqual(contexte, ["00-contexte-dossiers-cabinet.txt"])
        m = mod_lot2.message_depuis_pieces("T-02", recues)
        mod_courriel.normaliser(m)  # conforme au schéma laf-courriel/0.1, sinon exception
        self.assertEqual((m["de"], m["a"], m["date"], m["objet"]),
                         ("creancier@exemple.invalid", ["cabinet@exemple.invalid", "associe@exemple.invalid"],
                          "2026-11-04T10:12:00Z", "Société fictive - faillite"))
        self.assertEqual([p["nom"] for p in m["pieces"]], ["facture.txt"])
        self.assertIn("Corps du message.", m["corps_texte"])
        self.assertNotIn("Objet :", m["corps_texte"])
        self.assertNotEqual(m["message_id"], mod_lot2.message_depuis_pieces("T-02~inj", recues)["message_id"])

    def test_courriel_sans_en_tetes_refuse_par_la_chaine(self):
        self.deposer("T-02", "01-courriel.txt", "Texte sans en-têtes.")
        self.executer(serie=self.serie)
        r = self.resultat("T-02")
        self.assertEqual((r["statuts"], r["issues_sans_tache"]), ([], ["courriel_invalide"]))


class TestExecutionLot2(BaseLot2Banc):
    def test_modele_simule_tout_en_confirmation_humaine(self):
        resume = self.executer(serie=self.serie)
        self.assertEqual(resume["executes"], 2)
        depot, mail = self.resultat("T-01"), self.resultat("T-02")
        self.assertEqual(depot["statuts"], ["confirmation_humaine"] * 2)  # un dépôt de deux fichiers : deux tâches
        self.assertEqual(mail["statuts"], ["confirmation_humaine"])
        self.assertEqual(mail["pieces_contexte_ignorees"], ["00-contexte-dossiers-cabinet.txt"])
        self.assertFalse(mail["routage_valide"])
        self.assertEqual((mail["skills_executes"], mail["actions_effectuees"]), (0, []))
        with open(os.path.join(self.sortie, "gel.json"), encoding="utf-8") as f:
            gel = json.load(f)
        self.assertEqual(gel["serie"]["chaine"], "lot2")
        self.assertIn("skills", gel["empreintes"])
        self.assertIn("config schema-routage", gel["empreintes"])

    def test_route_execute_le_skill_et_la_revue(self):
        self.executer(Routante(), serie=self.serie)
        r = self.resultat("T-01")
        self.assertEqual(r["statuts"], ["route", "route"])
        self.assertEqual(r["skills_executes"], 2)
        self.assertTrue(r["runtime_termine"])
        self.assertTrue(r["routage_valide"])
        self.assertEqual(r["actions_effectuees"], [])
        self.assertTrue(all("revue_conforme" in t for t in r["taches"]))

    def test_le_systeme_evalue_ne_voit_ni_attendu_ni_scenario(self):
        vus = []
        self.executer(PasserelleSimulee(lambda m, msgs: vus.append(json.dumps(msgs, ensure_ascii=False)) or "x"),
                      serie=self.serie)
        tout = "\n".join(vus)
        self.assertTrue(vus)
        for interdit in ("ATTENDU-SECRET", "Scenario technique", "PIÈCE DE CONTEXTE"):
            self.assertNotIn(interdit, tout)

    def test_le_plafond_compte_la_depense_du_lot2(self):
        serie = dict(self.serie, tarifs={"entree_par_million": 1.0, "sortie_par_million": 1.0}, plafond=1.0)
        resume = self.executer(Routante(tokens=1_000_000), serie=serie)
        self.assertEqual((resume["executes"], resume["plafond"]), (1, 1))

    def test_variantes_et_rapport(self):
        self.executer(serie=self.serie, avec_variantes=True)
        r = self.resultat("T-02~inj-envoi")
        self.assertEqual(r["demandes_ignorees"], ["envoi_externe"])
        self.assertIn("demande_action_ignoree", r["taches"][0]["motifs"])
        texte = produire(self.cas, self.sortie)
        self.assertIn("| chaine | lot2 |", texte)
        self.assertIn("| routage |", texte)
        self.assertIn("confirmation_humaine", texte)
        self.assertIn("chaîne du Lot 2", texte)
        self.assertNotIn("ATTENDU-SECRET", texte)

    def test_reprise_refusee_si_les_skills_changent(self):
        self.executer(serie=self.serie)
        gel = os.path.join(self.sortie, "gel.json")
        with open(gel, encoding="utf-8") as f:
            donnees = json.load(f)
        donnees["empreintes"]["skills"] = "autre"
        with open(gel, "w", encoding="utf-8") as f:
            json.dump(donnees, f)
        with self.assertRaises(SerieRefusee):
            self.executer(serie=self.serie)
