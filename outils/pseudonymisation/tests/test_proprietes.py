"""Propriétés générales, issues de la relecture indépendante du 2026-10-31 : aucune fuite partielle,
mots entiers, insensibilité à la forme Unicode, aller-retour, temps de calcul borné, fenêtre cohérente."""

import glob
import os
import time
import unicodedata
import unittest

import aide
from pseudonymisation.detection import dans_un_mot, detecter, preparer
from pseudonymisation.lecture import lire_fichier
from pseudonymisation.remplacement import pseudonymiser, retablir

PIECES_DEV = sorted(glob.glob(os.path.join(aide.PIECES, "*.txt")))
DIFFICILES = [
    "M. Lech Wałęsa, M. Pavel Dvořák, Mme Ayşe Yılmaz, M. Jean McDonald et Mme Anne DeBruyne signent.",
    "Łódź Trading SRL est créancière. M. Pieter D′Hondt et M. Jean-Luc OʼNeill interviennent.",
    "La SA Dupont est bailleresse. M. Jean Dupont, son administrateur, signe. M. Dupont déclare avoir reçu.",
    "Mme Rose Blanc a acheté du vin blanc. La porte est restée ouverte. M. Paul Porte en atteste.",
    "M. Hans Strauß loue le bien. Plus tard, Strauß a résilié le bail. M. Wei Li est gérant ; Li a signé.",
]


def textes():
    for chemin in PIECES_DEV:
        yield os.path.basename(chemin), lire_fichier(chemin)
    for i, t in enumerate(DIFFICILES):
        yield f"difficile {i}", t


class AucuneFuitePartielle(unittest.TestCase):
    def test_detections_sur_des_mots_entiers(self):
        for nom, texte in textes():
            for e in detecter(texte):
                self.assertFalse(dans_un_mot(texte, e.debut - 1, gauche=True) and texte[e.debut - 1].isalnum(),
                                 f"{nom} : « {e.texte} » commence au milieu d'un mot")
                self.assertFalse(dans_un_mot(texte, e.fin) and texte[e.fin].isalnum(),
                                 f"{nom} : « {e.texte} » finit au milieu d'un mot")

    def test_rien_de_detecte_ne_subsiste(self):
        for nom, texte in textes():
            entites = detecter(texte)
            sortie = pseudonymiser(texte, entites).texte
            for e in entites:
                if len(e.texte) >= 3:
                    self.assertNotIn(e.texte, sortie, f"{nom} : « {e.texte} » détecté mais encore présent")

    def test_meme_resultat_en_nfd(self):
        for nom, texte in textes():
            nfd = unicodedata.normalize("NFD", texte)
            self.assertEqual([(e.categorie, e.texte) for e in detecter(preparer(nfd))],
                             [(e.categorie, e.texte) for e in detecter(texte)], nom)

    def test_texte_non_normalise_refuse(self):
        with self.assertRaises(ValueError):
            detecter(unicodedata.normalize("NFD", "Mme Hélène Gérard"))

    def test_donnee_conservee_ne_masque_pas_sa_voisine(self):
        texte = DIFFICILES[2]
        cle_societe = next(e.cle for e in detecter(texte) if e.categorie == "ORGANISATION")
        sortie = pseudonymiser(texte, detecter(texte, desactives={cle_societe})).texte
        # La personne reste entièrement masquée ; « Dupont » l'est aussi dans le nom de la société,
        # comme nom de famille de la personne : en cas de conflit, l'outil masque.
        self.assertIn("M. [PERSONNE_1], son administrateur", sortie)
        self.assertNotIn("Jean", sortie)


class AllerRetour(unittest.TestCase):
    def test_retour_au_texte_d_origine(self):
        texte = "M. Thomas Wilmotte loue à Mme Nadia Bensalem, rue des Glacis 14, 4000 Liège (BE14 0631 2345 6783)."
        r = pseudonymiser(texte, detecter(texte))
        self.assertEqual(retablir(r.texte, r.table).texte, texte)

    def test_phrases_ordinaires_inchangees(self):
        texte = "M. Thomas Wilmotte loue."
        r = pseudonymiser(texte, detecter(texte))
        phrase = "Une personne 1 fois condamnée ; la personne 2 ; le terme 1 ; voir l'adresse 1."
        retour = retablir(phrase, r.table)
        self.assertEqual(retour.texte, phrase)
        self.assertEqual(retour.remplaces, {})

    def test_forme_approchee_signalee(self):
        texte = "M. Thomas Wilmotte loue."
        r = pseudonymiser(texte, detecter(texte))
        retour = retablir("Selon [Personne 1].", r.table)
        self.assertEqual(retour.texte, "Selon Thomas Wilmotte.")
        self.assertEqual(retour.approches, ["[Personne 1]"])

    def test_marqueurs_preexistants_jamais_reutilises(self):
        texte = "Le modèle cite [PERSONNE_1] et PERSONNE 2. M. Jean Dupont et Mme Anne Leroy signent."
        r = pseudonymiser(texte, detecter(texte))
        self.assertIn("M. [PERSONNE_3] et Mme [PERSONNE_4]", r.texte)
        self.assertEqual(retablir(r.texte, r.table).texte, texte)
        self.assertEqual(r.marqueurs_preexistants, ["PERSONNE 2", "[PERSONNE_1]"])


class TempsDeCalcul(unittest.TestCase):
    def mesurer(self, texte, limite):
        debut = time.perf_counter()
        detecter(texte)
        duree = time.perf_counter() - debut
        self.assertLess(duree, limite, f"{len(texte)} caractères : {duree:.1f} s")

    def test_un_mo_realiste(self):
        base = "".join(lire_fichier(c) + "\n" for c in PIECES_DEV)
        self.mesurer((base * (1_000_000 // len(base) + 1))[:1_000_000], 10)

    def test_entrees_hostiles(self):
        self.mesurer("ABC Def " * 50000, 5)
        self.mesurer("la SA et la SRL " * 12000, 5)
        self.mesurer("rue " + "A" * 20000, 2)
        self.mesurer(" ".join(f"M. Jean B{chr(97 + i % 26)}{chr(97 + i // 26 % 26)}{chr(97 + i // 676)} signe."
                              for i in range(5000)), 5)

    def test_texte_trop_long_refuse(self):
        with self.assertRaises(ValueError):
            detecter("a" * (5 * 1024 * 1024 + 1))


class Fenetre(unittest.TestCase):
    """Comportement de la fenêtre, sans l'afficher. Ignoré sur une machine sans affichage (CI)."""

    def setUp(self):
        try:
            import tkinter as tk
            from tkinter import messagebox
            self.racine = tk.Tk()
        except Exception as e:  # tkinter absent, ou pas d'affichage (TclError)
            self.skipTest(f"fenêtre indisponible : {e}")
        self.racine.withdraw()
        self.messages = []
        self._originaux = (messagebox.showinfo, messagebox.showerror)
        messagebox.showinfo = messagebox.showerror = lambda *a, **k: self.messages.append(a)
        from pseudonymisation.interface import Application
        self.app = Application(self.racine)
        self.p = self.app.pseudonymiser
        self.p.dossier = self.enterContext(__import__("tempfile").TemporaryDirectory())
        self.p.clipboard_append = lambda _t: None
        self.p.clipboard_clear = lambda: None

    def tearDown(self):
        from tkinter import messagebox
        messagebox.showinfo, messagebox.showerror = self._originaux
        self.racine.destroy()

    def test_modifier_le_texte_apres_detection_bloque_l_enregistrement(self):
        self.p.nouveau_document("M. Thomas Wilmotte loue à Mme Nadia Bensalem.", "a.txt")
        self.p.relu.set(True)
        self.p.actualiser_bouton()
        self.assertEqual(str(self.p.bouton.cget("state")), "normal")
        self.p.zone_source.insert("1.0", "Objet : ")
        self.racine.update()
        self.assertFalse(self.p.relu.get())
        self.assertEqual(str(self.p.bouton.cget("state")), "disabled")
        self.p.relu.set(True)
        self.p.enregistrer()
        self.assertEqual(os.listdir(self.p.dossier), [])

    def test_enregistre_exactement_le_texte_affiche(self):
        self.p.nouveau_document("M. Thomas Wilmotte loue.", "a.txt")
        self.p.relu.set(True)
        self.p.enregistrer()
        with open(os.path.join(self.p.dossier, "a - pseudonymise.txt"), encoding="utf-8") as f:
            self.assertEqual(f.read(), self.p.zone_resultat.get("1.0", "end-1c"))

    def test_choix_remis_a_zero_pour_un_nouveau_document(self):
        self.p.nouveau_document("Me Claire Hanquet plaide.", "a.txt")
        self.p.liste.selection_set(self.p.liste.get_children()[0])
        self.p.basculer()
        self.assertIn("Claire Hanquet", self.p.zone_resultat.get("1.0", "end-1c"))
        self.p.nouveau_document("Mme Claire Hanquet conteste.", "b.txt")
        self.assertNotIn("Hanquet", self.p.zone_resultat.get("1.0", "end-1c"))

    def test_ajout_avec_retour_a_la_ligne(self):
        self.p.nouveau_document("Le témoin\nKarim\nHaddad a signé.", "a.txt")
        self.p.nouveau.insert(0, "Karim Haddad")
        self.p.ajouter()
        self.assertNotIn("Haddad", self.p.zone_resultat.get("1.0", "end-1c"))


class Lecture(unittest.TestCase):
    def test_utf16_lu_correctement(self):
        import tempfile
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "a.txt")
            with open(chemin, "wb") as f:
                f.write("M. Thomas Wilmotte, BE14 0631 2345 6783".encode("utf-16"))
            self.assertEqual(lire_fichier(chemin), "M. Thomas Wilmotte, BE14 0631 2345 6783")


if __name__ == "__main__":
    unittest.main()
