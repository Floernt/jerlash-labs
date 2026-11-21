"""Lot 2 : courriel, rapprochement, routeur, skills, revue qualité et décision humaine.

Les démonstrateurs couvrent les cas de routage du ticket FLO-65. Leur
correspondance exacte avec UC01, UC03 et UC04 de la fiche §15 n'a pas pu être
vérifiée (fiche hors dépôt) [À VÉRIFIER].
"""

import os
import re
import tempfile
import unittest

from aide import RACINE
from aide_lot2 import CLAIM, INTAKE, BaseLot2, message, sortie_skill

from laf import approbation, courriel, routeur, skills
from laf.approbation import DecisionInvalide
from laf.revue import charger_niveaux, reviser

FLORIAN = "Florian Ernotte"


class TestCritereDeFin(BaseLot2):
    """Fiche §17, partie hors modèle réel."""

    def test_courriel_ouvre_une_tache_et_active_le_skill_attendu(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        self.assertEqual((r["statut"], r["skill"], r["dossier"]), ("route", CLAIM, "SYN-2026-001"))
        self.assertEqual(self.fichiers("taches-paperclip"), [f"{r['evenement_id']}.json"])
        tache = self.chaine.lire("taches-paperclip", r["evenement_id"])
        self.assertTrue(tache["dry_run"])
        self.assertEqual((tache["skill_attendu"], tache["role_assigne"]), (CLAIM, "Insolvency Legal Worker"))
        self.assertTrue(r["revue"]["conforme"], r["revue"])
        self.assertIn("source_unverified:cde-livre-xx", r["revue"]["avertissements"])
        self.assertIn("skill_non_verifie_juridiquement", r["revue"]["avertissements"])

    def test_depot_ouvre_une_tache_et_active_le_skill_attendu(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        resultats = self.deposer_depot("jugement-et-facture.txt", "SYN-2026-001")
        self.assertEqual(len(resultats), 1)
        r = resultats[0]
        self.assertEqual((r["statut"], r["skill"], r["dossier"]), ("route", CLAIM, "SYN-2026-001"))
        self.assertEqual(len(self.fichiers("taches-paperclip")), 1)
        self.assertTrue(r["revue"]["conforme"])

    def test_lacune_bloque_needs_clarification(self):
        r = self.deposer_depot("aveu-incomplet.txt", "SYN-2026-002")[0]
        self.assertEqual((r["statut"], r["skill"]), ("needs_clarification", INTAKE))
        tache = self.chaine.lire("taches-paperclip", r["evenement_id"])
        self.assertEqual(tache["elements_manquants"], ["liste_creanciers", "comptes_annuels"])
        self.assertEqual(tache["role_assigne"], "Intake & Triage")
        self.assertNotIn("revue", r)
        self.assertEqual(self.fichiers("revues"), [])

    def test_aucun_envoi_externe_possible(self):
        # aucun module d'envoi n'est importé ; le seul client HTTP est celui du runtime local
        interdits = re.compile(r"^\s*(import|from)\s+(smtplib|urllib\.request|ftplib|requests|httpx|socket)\b", re.M)
        dossier = os.path.join(RACINE, "laf")
        for nom in os.listdir(dossier):
            if nom.endswith(".py"):
                with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                    self.assertIsNone(interdits.search(f.read()), nom)
        # même approuvée, une action A3 reste bloquée
        self.skill_repond(CLAIM, "SYN-2026-001", actions_proposees=[
            {"action": "deposer_regsol", "niveau": "A3"}, {"action": "envoyer_courriel", "niveau": "A3"}])
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        d = self.chaine.decider(r["evenement_id"], {"decision": "approuve", "relecteur": FLORIAN})
        self.assertEqual({a["effet"] for a in d["actions"]}, {"bloquee"})
        self.assertEqual(d["actions_executees"], [])

    def test_le_reviseur_peut_refuser(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        d = self.chaine.decider(r["evenement_id"], {"decision": "refuse", "relecteur": FLORIAN, "motif": "test"})
        self.assertEqual((d["statut"], d["actions"]), ("refuse", []))
        with self.assertRaises(DecisionInvalide):
            self.chaine.decider(r["evenement_id"], {"decision": "approuve", "relecteur": FLORIAN})

    def test_le_reviseur_peut_corriger(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        corrigee = sortie_skill(CLAIM, "SYN-2026-001", actions_proposees=[
            {"action": "rediger_projet_declaration_creance", "niveau": "A1"},
            {"action": "classer_piece", "niveau": "A2"}, {"action": "deposer_regsol", "niveau": "A3"}])
        d = self.chaine.decider(r["evenement_id"], {"decision": "corrige", "relecteur": FLORIAN,
                                                    "sortie_corrigee": corrigee})
        self.assertEqual(d["statut"], "corrige_approuve")
        effets = {a["action"]: a["effet"] for a in d["actions"]}
        self.assertEqual(effets, {"rediger_projet_declaration_creance": "interne",
                                  "classer_piece": "autorisee_execution_simulee", "deposer_regsol": "bloquee"})


class TestCourriel(BaseLot2):
    def test_fil_conserve_sans_texte(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        ev = self.chaine.lire("evenements", r["evenement_id"])
        self.assertEqual(ev["type"], "courriel")
        self.assertEqual(set(ev["fil"]), {"message_id", "in_reply_to", "references", "de", "a", "cc", "date"})
        self.assertEqual([p["nom"] for p in ev["pieces"]],
                         ["jugement-synthetique.txt", "facture-F-001.txt", "facture-F-002.txt"])
        self.assertTrue(all(set(p) == {"nom", "type_mime", "sha256", "taille"} for p in ev["pieces"]))
        self.assertNotIn("corps_texte", ev)

    def test_reponse_suit_le_fil_et_piece_sans_instruction_est_classee(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        r = self.chaine.recevoir_courriel(message("c02-reponse-piece-nouvelle.json"))
        self.assertEqual((r["statut"], r["skill"], r["dossier"]), ("classement", None, "SYN-2026-001"))
        routage = self.chaine.lire("routages", r["evenement_id"])
        self.assertEqual(routage["rattachement"]["lien"], "fil")
        self.assertEqual(self.chaine.lire("taches-paperclip", r["evenement_id"])["role_assigne"], "Case Analyst")

    def test_reponse_a_un_message_inconnu_reste_en_attente(self):
        r = self.chaine.recevoir_courriel(message("c02-reponse-piece-nouvelle.json"))
        self.assertEqual((r["statut"], r["dossier"]), ("confirmation_humaine", "ATTENTE"))

    def test_hors_perimetre(self):
        r = self.chaine.recevoir_courriel(message("c03-hors-perimetre.json"))
        self.assertEqual((r["statut"], r["skill"], r["dossier"]), ("hors_perimetre", None, "ATTENTE"))
        self.assertEqual(self.fichiers("revues"), [])

    def test_expediteur_non_inscrit_pas_d_attribution(self):
        r = self.chaine.recevoir_courriel(message("c05-expediteur-non-inscrit.json"))
        self.assertEqual((r["statut"], r["dossier"]), ("confirmation_humaine", "ATTENTE"))
        routage = self.chaine.lire("routages", r["evenement_id"])
        self.assertEqual(routage["rattachement"]["motif"], "expediteur_non_inscrit")
        self.assertIn("rattachement_expediteur_non_inscrit", routage["routage"]["motifs"])
        with self.assertRaises(DecisionInvalide):  # pas d'analyse de créance sans dossier
            self.chaine.confirmer(r["evenement_id"], FLORIAN)
        self.skill_repond(CLAIM, "SYN-2026-001")
        revue = self.chaine.confirmer(r["evenement_id"], FLORIAN, dossier="SYN-2026-001")
        self.assertTrue(revue["conforme"])
        self.assertEqual(self.chaine.lire("routages", r["evenement_id"])["routage"]["confirme_par"], FLORIAN)

    def test_injection_et_demandes_d_action_ignorees(self):
        r = self.chaine.recevoir_courriel(message("c04-injection.json"))
        routage = self.chaine.lire("routages", r["evenement_id"])
        self.assertEqual(routage["regles"]["demandes_ignorees"], ["administration", "depot_regsol", "envoi_externe"])
        self.assertTrue(routage["regles"]["injection_suspectee"])
        self.assertFalse(routage["regles"]["autorisation_accordee_par_le_message"])
        self.assertEqual(r["statut"], "confirmation_humaine")
        self.assertEqual(self.passerelle.appels, 1)  # routage seulement : aucun skill exécuté
        self.assertEqual(self.fichiers("revues"), [])

    def test_rejeu_sans_effet(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        m = message("c01-jugement-factures.json")
        self.chaine.recevoir_courriel(m)
        self.assertEqual(self.chaine.recevoir_courriel(m)["issue"], "doublon_ignore")
        self.assertEqual(len(self.fichiers("taches-paperclip")), 1)

    def test_courriel_hors_format_signale(self):
        m = message("c01-jugement-factures.json")
        del m["in_reply_to"]
        r = self.chaine.recevoir_courriel(m)
        self.assertEqual(r["issue"], "courriel_invalide")
        self.assertEqual(self.fichiers("taches-paperclip"), [])
        m["champ_en_plus"] = "x"
        with self.assertRaises(courriel.CourrielInvalide):
            courriel.normaliser(m)

    def test_audit_sans_adresse_ni_objet(self):
        self.skill_repond(CLAIM, "SYN-2026-001")
        self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        audit = self.audit()
        self.assertNotIn("@", audit)
        self.assertNotIn("jugement de faillite", audit)
        self.assertNotIn("Débiteur", audit)


class TestDepots(BaseLot2):
    def test_personne_physique_sans_date(self):
        r = self.deposer_depot("personne-physique-sans-date.txt", "SYN-2026-003")[0]
        self.assertEqual(r["statut"], "needs_clarification")
        tache = self.chaine.lire("taches-paperclip", r["evenement_id"])
        self.assertEqual(tache["elements_manquants"], ["date_jugement", "jugement_faillite"])

    def test_personne_physique_avec_date_exige_confirmation(self):
        r = self.deposer_depot("personne-physique-avec-date.txt", "SYN-2026-003")[0]
        self.assertEqual((r["statut"], r["skill"]), ("confirmation_humaine", CLAIM))
        motifs = self.chaine.lire("routages", r["evenement_id"])["routage"]["motifs"]
        self.assertEqual(motifs, ["personne_physique_version_de_la_loi"])
        with self.assertRaises(DecisionInvalide):
            self.chaine.confirmer(r["evenement_id"], "Quelqu'un d'autre")
        self.skill_repond(CLAIM, "SYN-2026-003")
        self.assertTrue(self.chaine.confirmer(r["evenement_id"], FLORIAN)["conforme"])
        with self.assertRaises(DecisionInvalide):  # déjà confirmée
            self.chaine.confirmer(r["evenement_id"], FLORIAN)

    def test_piece_nouvelle_sans_instruction(self):
        r = self.deposer_depot("piece-nouvelle.txt", "SYN-2026-001")[0]
        self.assertEqual((r["statut"], r["skill"], r["dossier"]), ("classement", None, "SYN-2026-001"))

    def test_depot_hors_sous_dossier_non_attribue(self):
        r = self.deposer_depot("jugement-et-facture.txt")[0]
        self.assertEqual((r["statut"], r["dossier"]), ("confirmation_humaine", "ATTENTE"))
        self.assertIn("rattachement_fichier_hors_sous_dossier",
                      self.chaine.lire("routages", r["evenement_id"])["routage"]["motifs"])

    def test_sous_dossier_inconnu_non_attribue(self):
        r = self.deposer_depot("piece-nouvelle.txt", "SYN-2099-999")[0]
        self.assertEqual((r["statut"], r["dossier"]), ("confirmation_humaine", "ATTENTE"))


class TestRevueEtDecision(BaseLot2):
    def _route(self, dossier="SYN-2026-001", **champs):
        self.skill_repond(CLAIM, dossier, **champs)
        return self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))

    def test_sortie_non_conforme_ne_peut_pas_etre_approuvee(self):
        self.passerelle.sorties_skills.clear()  # modèle simulé par défaut : texte libre, hors schéma
        r = self.chaine.recevoir_courriel(message("c01-jugement-factures.json"))
        self.assertFalse(r["revue"]["conforme"])
        d = self.chaine.decider(r["evenement_id"], {"decision": "approuve", "relecteur": FLORIAN})
        self.assertEqual(d["statut"], "approbation_impossible_revue_non_conforme")

    def test_correction_non_conforme_refusee(self):
        r = self._route()
        mauvaise = sortie_skill(CLAIM, "SYN-2026-001", constats=[
            {"texte": "Voir aussi SYN-2026-002 ; IBAN BE71 0961 2345 6769.", "sources": ["inventee"]}])
        d = self.chaine.decider(r["evenement_id"], {"decision": "corrige", "relecteur": FLORIAN,
                                                    "sortie_corrigee": mauvaise})
        self.assertEqual(d["statut"], "correction_non_conforme")
        self.assertIn("reference_autre_dossier", d["revue"]["erreurs"])
        self.assertIn("confidentialite:iban", d["revue"]["erreurs"])
        self.assertIn("source_inconnue:inventee", d["revue"]["erreurs"])

    def test_niveau_vient_de_la_configuration(self):
        r = self._route(actions_proposees=[{"action": "deposer_regsol", "niveau": "A1"},
                                           {"action": "action_inventee", "niveau": "A0"}])
        self.assertFalse(r["revue"]["conforme"])
        self.assertIn("niveau_declare_incorrect:deposer_regsol", r["revue"]["erreurs"])
        self.assertIn("action_inconnue:action_inventee", r["revue"]["erreurs"])
        self.assertEqual(r["revue"]["actions"][0]["etat"], "bloquee")

    def test_dossier_ou_skill_incoherent(self):
        r = self._route(dossier="SYN-2026-003")
        self.assertIn("dossier_incoherent", r["revue"]["erreurs"])

    def test_relecteur_non_inscrit(self):
        r = self._route()
        with self.assertRaises(DecisionInvalide):
            self.chaine.decider(r["evenement_id"], {"decision": "approuve", "relecteur": "agent"})
        with self.assertRaises(DecisionInvalide):
            self.chaine.decider(r["evenement_id"], {"decision": "valider", "relecteur": FLORIAN})

    def test_approbation_simple(self):
        r = self._route()
        d = self.chaine.decider(r["evenement_id"], {"decision": "approuve", "relecteur": FLORIAN})
        self.assertEqual(d["statut"], "approuve")
        self.assertEqual(d["actions"], [{"action": "rediger_note_interne", "niveau": "A1", "etat": "interne",
                                         "effet": "interne"}])


class TestSkills(unittest.TestCase):
    def test_deux_skills_en_brouillon_non_verifies(self):
        self.assertEqual(skills.lister(), [CLAIM, INTAKE])
        registre = skills.charger_registre()
        for nom in (INTAKE, CLAIM):
            s = skills.charger(nom, registre)
            self.assertEqual((s["status"], s["last_legal_review"]), ("draft", None))
            self.assertFalse(s["verifie_juridiquement"])
            self.assertEqual(s["mention"], skills.MENTION_NON_VERIFIE)
            self.assertEqual({x["statut"] for x in s["sources"]}, {"source_unverified"})

    def test_skill_dit_relu_sans_date_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "x"))
            with open(os.path.join(d, "x", "SKILL.md"), "w", encoding="utf-8") as f:
                f.write("---\nname: x\nversion: 1\nstatus: reviewed\nlast_legal_review: null\njurisdiction: BE\n"
                        "output_schema: s.json\nmax_action_level: A1\nsources: [cde-livre-xx]\n---\ncorps\n")
            with self.assertRaises(skills.SkillInvalide):
                skills.charger("x", skills.charger_registre(), d)

    def test_source_absente_du_registre_refusee(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "x"))
            with open(os.path.join(d, "x", "SKILL.md"), "w", encoding="utf-8") as f:
                f.write("---\nname: x\nversion: 1\nstatus: draft\nlast_legal_review: null\njurisdiction: BE\n"
                        "output_schema: s.json\nmax_action_level: A1\nsources: [inventee]\n---\ncorps\n")
            with self.assertRaises(skills.SkillInvalide):
                skills.charger("x", skills.charger_registre(), d)


class TestRouteur(unittest.TestCase):
    ATTENTE = {"dossier": "ATTENTE", "rattache": False, "lien": None, "motif": "aucune_reference"}

    def test_simple_mention_d_envoi_n_est_pas_une_demande(self):
        self.assertEqual(routeur.regles_autorisations("Je vous envoie le jugement en pièce jointe.")["demandes_ignorees"], [])
        self.assertEqual(routeur.regles_autorisations("Merci de transmettre ceci au curateur.")["demandes_ignorees"],
                         ["envoi_externe"])
        self.assertEqual(routeur.regles_autorisations("Pouvez-vous payer la facture ?")["demandes_ignorees"],
                         ["paiement"])

    def test_sortie_modele_hors_schema(self):
        from laf.passerelle import PasserelleSimulee
        p = PasserelleSimulee(lambda m, msgs: '{"intention": "declaration_creance", "action": "deposer"}')
        classe = routeur.classifier("x", p, "m", routeur.charger_schema(), 1000)
        self.assertFalse(classe["valide"])
        d = routeur.decider(routeur.regles_autorisations("x"), classe, self.ATTENTE)
        self.assertEqual((d["statut"], d["skill_attendu"]), ("confirmation_humaine", None))

    def test_intention_et_skill_incoherents(self):
        c = {"schema_version": "laf-routage/0.1", "intention": "nouvelle_affaire_faillite", "skill_propose": CLAIM,
             "pieces": [], "personne": "morale", "date_jugement": "inconnue", "elements_manquants": [],
             "risque": "faible", "ambiguite": False, "confiance": 0.95, "motifs": []}
        d = routeur.decider(routeur.regles_autorisations(""), {"classification": c, "valide": True}, self.ATTENTE)
        self.assertEqual((d["statut"], d["skill_attendu"]), ("confirmation_humaine", INTAKE))

    def test_confiance_faible_ou_risque_eleve(self):
        base = {"schema_version": "laf-routage/0.1", "intention": "nouvelle_affaire_faillite", "skill_propose": INTAKE,
                "pieces": ["aveu_faillite"], "personne": "morale", "date_jugement": "inconnue",
                "elements_manquants": [], "risque": "faible", "ambiguite": False, "confiance": 0.95, "motifs": []}
        regles = routeur.regles_autorisations("")
        self.assertEqual(routeur.decider(regles, {"classification": base, "valide": True}, self.ATTENTE)["statut"],
                         "route")
        for modif in ({"confiance": 0.5}, {"risque": "eleve"}, {"ambiguite": True}):
            c = dict(base, **modif)
            self.assertEqual(routeur.decider(regles, {"classification": c, "valide": True}, self.ATTENTE)["statut"],
                             "confirmation_humaine", modif)


class TestNiveaux(unittest.TestCase):
    def test_a3_bloque_dans_la_configuration(self):
        n = charger_niveaux()
        self.assertEqual(n["niveaux_bloques"], ["A3"])
        for action in ("envoyer_courriel", "deposer_regsol", "contacter_curateur"):
            self.assertEqual(n["actions"][action], "A3")

    def test_decision_venue_d_un_message_impossible(self):
        # appliquer exige un relecteur inscrit ; un courriel n'a aucun chemin vers decider()
        n = charger_niveaux()
        with self.assertRaises(approbation.DecisionInvalide):
            approbation.appliquer({"conforme": True, "actions": []}, {"decision": "approuve",
                                  "relecteur": "comptabilite@alpha-fournitures.example"}, {}, {}, "", {}, n)


if __name__ == "__main__":
    unittest.main()
