"""Mode IA (0.2.0) : ce qui part, lecture de la réponse, fusion avec les règles, parcours complet."""

import json
import os
import pathlib
import re
import tempfile
import unittest
from unittest import mock

import aide
from connecteur_ia import ErreurReponse
from inventaire_dossier import ia
from inventaire_dossier.analyse import classer, conclure
from inventaire_dossier.lecture import Piece, lire_dossier

CONTRAT = "CONTRAT DE LICENCE\nEntre Alphatech SRL et Betalog SA.\nFait à Liège, le 3 mars 2024.\nPour Alphatech SRL (signé)\nPour Betalog SA (signé)"
PROJET = "PROJET - NE PAS SIGNER\nCONTRAT DE LICENCE\nEntre Alphatech SRL et Betalog SA.\nVersion du 1er février 2024."
NOTE = "Note sur le dossier\nLe client Gammaprod SPRL demande une copie."


def piece(nom, texte, format_=".txt"):
    return Piece(nom, format_, len(texte), nom, "2026-11-01", texte=texte)


def blocs(texte):
    """Numéro de pièce -> texte de son bloc, dans un envoi."""
    morceaux = re.split(r"^=== (P\d+) ===$", texte, flags=re.M)
    return dict(zip(morceaux[1::2], morceaux[2::2]))


def repondre_comme_un_modele(texte):
    """Parties : les sociétés du bloc ; rattachement de chaque pièce non signée à la pièce signée."""
    b = blocs(texte)
    signee = next((n for n, t in b.items() if "statut signé" in t), None)
    return {"pieces": [{"piece": n, "parties": sorted(set(re.findall(r"\[ORGANISATION_\d+\] (?:SRL|SA|SPRL)", t))),
                        "rattache_a": signee if n != signee and "statut signé" not in t else None,
                        "justification": "même intitulé"} for n, t in b.items()]}


class Envoi(unittest.TestCase):
    def test_numeros_pas_de_nom_de_fichier_ni_de_nom_en_clair(self):
        pieces, ignores = lire_dossier(aide.PIECES)
        envoi = ia.preparer_envoi(classer(aide.PIECES, pieces, ignores))
        self.assertEqual(sorted(envoi.numeros.values()), sorted(p.chemin for p in pieces if p.texte is not None))
        for p in pieces:
            self.assertNotIn(p.chemin, envoi.texte)
        noms = [c["retablir_par"] for c in envoi.table["correspondances"]]
        self.assertTrue(noms)
        for nom in noms:
            self.assertNotIn(nom, envoi.texte)

    def test_plafond_par_piece_et_signalement(self):
        longue = "\n".join(f"Ligne {i} " + "x" * 300 for i in range(60))
        inv = classer(".", [piece("a.txt", longue), piece("b.txt", "court")], [])
        envoi = ia.preparer_envoi(inv)
        self.assertEqual(envoi.tronquees, ["a.txt"])
        self.assertLess(len(blocs(envoi.texte)["P1"]), ia.CARACTERES_PAR_PIECE + 300)

    def test_dossier_sans_piece_lisible(self):
        p = Piece("scan.pdf", ".pdf", 10, "scan.pdf", "2026-11-01", texte=None, non_lu="PDF")
        self.assertTrue(ia.preparer_envoi(classer(".", [p], [])).vide)


class Reponse(unittest.TestCase):
    def setUp(self):
        self.inv = classer(".", [piece("contrat.txt", CONTRAT), piece("projet.txt", PROJET)], [])
        self.envoi = ia.preparer_envoi(self.inv)

    def test_noms_retablis(self):
        props, rejets = ia.interpreter(json.dumps(repondre_comme_un_modele(self.envoi.texte)),
                                       self.envoi.table, self.envoi.numeros)
        self.assertEqual(rejets, [])
        self.assertEqual(sorted(props["projet.txt"].parties), ["Alphatech SRL", "Betalog SA"])
        self.assertEqual(props["projet.txt"].rattache_a, "contrat.txt")

    def test_propositions_douteuses_ecartees(self):
        reponse = {"pieces": [{"piece": "P1", "parties": ["[ORGANISATION_99] SRL"], "rattache_a": "P1"},
                              {"piece": "P2", "parties": [], "rattache_a": "P7"},
                              {"piece": "P9", "parties": []}]}
        props, rejets = ia.interpreter(json.dumps(reponse), self.envoi.table, self.envoi.numeros)
        self.assertEqual(props["contrat.txt"].parties, [])
        self.assertIsNone(props["contrat.txt"].rattache_a)
        self.assertIsNone(props["projet.txt"].rattache_a)
        self.assertEqual(len(rejets), 4)

    def test_reponse_illisible(self):
        with self.assertRaises(ErreurReponse):
            ia.interpreter("Je ne peux pas répondre.", self.envoi.table, self.envoi.numeros)
        with self.assertRaises(ErreurReponse):
            ia.interpreter('{"autre": 1}', self.envoi.table, self.envoi.numeros)


class Fusion(unittest.TestCase):
    def inventaire(self):
        return classer(".", [piece("contrat.txt", CONTRAT), piece("projet.txt", PROJET), piece("note.txt", NOTE)], [])

    def test_accord_proposition_et_divergence(self):
        inv = self.inventaire()
        regles = {f.piece.chemin: (list(f.parties), f.rattache_a) for f in inv.fiches}
        props = {
            "contrat.txt": ia.Proposition(list(regles["contrat.txt"][0]), None, ""),
            "projet.txt": ia.Proposition(["Alphatech SRL"], "contrat.txt", "projet du même contrat"),
            "note.txt": ia.Proposition([], None, ""),
        }
        ia.fusionner(inv, props)
        conclure(inv)
        f = {x.piece.chemin: x for x in inv.fiches}
        self.assertNotIn("parties", f["contrat.txt"].source)
        self.assertIn("parties : confirmées par le modèle", f["contrat.txt"].indices)
        self.assertEqual(f["projet.txt"].parties, ["Alphatech SRL"])
        self.assertEqual(f["projet.txt"].source["parties"], "divergence")
        self.assertTrue(any("les règles proposaient" in a for a in f["projet.txt"].alertes))
        self.assertEqual(f["projet.txt"].rattache_a, "contrat.txt")
        self.assertEqual(f["note.txt"].parties, regles["note.txt"][0])  # le modèle ne propose rien : règles

    def test_le_modele_complete_ce_que_les_regles_n_ont_pas_trouve(self):
        inv = classer(".", [piece("contrat.txt", CONTRAT), piece("lettre.txt", "Madame,\nVoici le texte.")], [])
        ia.fusionner(inv, {"lettre.txt": ia.Proposition(["Betalog SA"], "contrat.txt", "objet")})
        f = inv.fiches[1]
        self.assertEqual((f.parties, f.rattache_a), (["Betalog SA"], "contrat.txt"))
        self.assertEqual(f.source, {"parties": "modèle", "rattache_a": "modèle"})
        self.assertEqual(f.alertes, [])


class Parcours(unittest.TestCase):
    def setUp(self):
        self.tmp = self.enterContext(tempfile.TemporaryDirectory())
        self.dossier = os.path.join(self.tmp, "Dossier Alphatech")
        os.makedirs(self.dossier)
        for nom, texte in (("Licence Alphatech signée.txt", CONTRAT), ("Licence Alphatech v1.txt", PROJET)):
            pathlib.Path(self.dossier, nom).write_text(texte, encoding="utf-8")
        self.sortie = os.path.join(self.tmp, "registres")

    def registre(self):
        nom = next(n for n in os.listdir(self.sortie) if n.endswith(".json"))
        return json.loads(pathlib.Path(self.sortie, nom).read_text(encoding="utf-8"))

    def test_envoi_pseudonymise_et_registre_annote(self):
        with aide.Fournisseur(repondre_comme_un_modele) as fournisseur, aide.reseau_local_seulement():
            code = aide.cli_ia([self.dossier, "--sortie", self.sortie], fournisseur, self.tmp)
        self.assertIn(code, (0, 1))
        (corps,) = fournisseur.recus
        self.assertEqual(set(corps), {"model", "messages", "max_tokens"})
        envoye = corps["messages"][1]["content"]
        for interdit in ("Alphatech", "Betalog", "Licence Alphatech", "Dossier Alphatech"):
            self.assertNotIn(interdit, envoye)
        registre = self.registre()
        self.assertIn("faux-modele", registre["mode"])
        self.assertEqual(registre["ia"]["jetons_entree"], 1000)
        projet = next(p for p in registre["pieces"] if p["chemin"] == "Licence Alphatech v1.txt")
        self.assertEqual(projet["rattache_a"], "Licence Alphatech signée.txt")
        self.assertEqual(sorted(projet["parties"]), ["Alphatech SRL", "Betalog SA"])

    def test_envoi_refuse(self):
        with aide.Fournisseur() as fournisseur:
            code = aide.cli_ia([self.dossier, "--sortie", self.sortie], fournisseur, self.tmp, confirmer="non")
        self.assertEqual(code, 2)
        self.assertEqual(fournisseur.recus, [])
        self.assertFalse(os.path.exists(self.sortie))

    def test_erreur_du_fournisseur_aucun_registre(self):
        with aide.Fournisseur(statut=401) as fournisseur:
            code = aide.cli_ia([self.dossier, "--sortie", self.sortie], fournisseur, self.tmp)
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(self.sortie))

    def test_sans_cle_l_outil_ne_fonctionne_pas(self):
        from inventaire_dossier.__main__ import main as cli
        config = pathlib.Path(self.tmp, "config-ia.json")
        config.write_text(json.dumps({"prereglage": "openai"}), encoding="utf-8")
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch("sys.stderr") as erreur:
            code = cli([self.dossier, "--sortie", self.sortie, "--config", str(config)])
        self.assertEqual(code, 2)
        self.assertIn("OPENAI_API_KEY", "".join(str(c) for c in erreur.write.call_args_list))
        self.assertFalse(os.path.exists(self.sortie))


if __name__ == "__main__":
    unittest.main()
