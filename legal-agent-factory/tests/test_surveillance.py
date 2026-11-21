import os

from aide import CasAvecDossiers

from laf.outils_fichiers import empreinte_fichier
from laf.surveillance import Surveillant, identifiant_evenement


class TestSurveillance(CasAvecDossiers):
    def surveillant(self, **kw):
        return Surveillant(self.entree, os.path.join(self.etat, "surveillance.json"), **kw)

    def deux_passages(self, s):
        return s.scruter() + s.scruter()

    def test_creation_apres_stabilite(self):
        s = self.surveillant()
        chemin = self.deposer("a.txt", "contenu A")
        self.assertEqual(s.scruter(), [], "un fichier n'est pas annoncé au premier passage")
        evs = s.scruter()
        self.assertEqual([e["type"] for e in evs], ["creation"])
        self.assertEqual(evs[0]["sha256"], empreinte_fichier(chemin))
        self.assertEqual(evs[0]["version"], 1)
        self.assertIn("horodatage", evs[0])
        self.assertEqual(s.scruter(), [])

    def test_attend_la_fin_de_l_ecriture(self):
        s = self.surveillant()
        chemin = self.deposer("long.txt", "début")
        s.scruter()
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(" suite de l'écriture")
        self.assertEqual(s.scruter(), [], "la taille a changé : on attend")
        evs = s.scruter()
        self.assertEqual(len(evs), 1)
        self.assertEqual(evs[0]["sha256"], empreinte_fichier(chemin))

    def test_modification_meme_nom_nouvelle_version(self):
        s = self.surveillant()
        self.deposer("a.txt", "version 1")
        v1 = self.deux_passages(s)[0]
        self.deposer("a.txt", "version 2, plus longue")
        evs = self.deux_passages(s)
        self.assertEqual([e["type"] for e in evs], ["modification"])
        self.assertEqual(evs[0]["version"], 2)
        self.assertNotEqual(evs[0]["id"], v1["id"])

    def test_simple_changement_de_date_sans_evenement(self):
        s = self.surveillant()
        chemin = self.deposer("a.txt", "inchangé")
        self.deux_passages(s)
        st = os.stat(chemin)
        os.utime(chemin, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
        self.assertEqual(self.deux_passages(s), [])

    def test_renommage(self):
        s = self.surveillant()
        self.deposer("ancien.txt", "même contenu")
        self.deux_passages(s)
        os.rename(os.path.join(self.entree, "ancien.txt"), os.path.join(self.entree, "nouveau.txt"))
        evs = self.deux_passages(s)
        self.assertEqual([e["type"] for e in evs], ["renommage"])
        self.assertEqual(evs[0]["ancien_chemin"], "ancien.txt")
        self.assertEqual(evs[0]["chemin"], "nouveau.txt")
        self.assertEqual(self.deux_passages(s), [], "pas de suppression fantôme après un renommage")

    def test_suppression(self):
        s = self.surveillant()
        chemin = self.deposer("a.txt", "à supprimer")
        self.deux_passages(s)
        os.remove(chemin)
        self.assertEqual(s.scruter(), [], "la disparition est confirmée au passage suivant")
        evs = s.scruter()
        self.assertEqual([e["type"] for e in evs], ["suppression"])
        self.assertEqual(evs[0]["version"], 1)

    def test_recreation_meme_contenu_nouvelle_version(self):
        s = self.surveillant()
        chemin = self.deposer("a.txt", "identique")
        premier = self.deux_passages(s)[0]
        os.remove(chemin)
        self.deux_passages(s)
        self.deposer("a.txt", "identique")
        evs = self.deux_passages(s)
        self.assertEqual([e["type"] for e in evs], ["creation"])
        self.assertEqual(evs[0]["version"], 2)
        self.assertNotEqual(evs[0]["id"], premier["id"])

    def test_sous_dossier(self):
        s = self.surveillant()
        self.deposer("sous/dossier/b.txt", "imbriqué")
        evs = self.deux_passages(s)
        self.assertEqual(evs[0]["chemin"], "sous/dossier/b.txt")

    def test_fichier_illisible_signale_une_fois(self):
        bloque = {"actif": True}

        def lire(chemin):
            if bloque["actif"] and chemin.endswith("verrouille.txt"):
                raise PermissionError("simulé")
            return empreinte_fichier(chemin)

        s = self.surveillant(lire_empreinte=lire)
        self.deposer("verrouille.txt", "illisible")
        evs = self.deux_passages(s)
        self.assertEqual([e["type"] for e in evs], ["illisible"])
        self.assertEqual(evs[0]["erreur"], "PermissionError")
        self.assertEqual(self.deux_passages(s), [], "signalé une fois, pas à chaque passage")
        bloque["actif"] = False
        self.assertEqual([e["type"] for e in s.scruter()], ["creation"], "redevenu lisible : traité")

    def test_etat_persiste_entre_deux_lancements(self):
        s = self.surveillant()
        self.deposer("a.txt", "persisté")
        self.deux_passages(s)
        self.assertEqual(self.deux_passages(self.surveillant()), [])

    def test_identifiant_independant_de_l_heure(self):
        s = self.surveillant()
        self.deposer("a.txt", "x")
        ev = self.deux_passages(s)[0]
        autre = dict(ev, horodatage="2000-01-01T00:00:00+00:00")
        self.assertEqual(identifiant_evenement(autre), ev["id"])
