"""Fenêtre graphique (tkinter, inclus dans Python).

Le seul accès réseau est l'appel au fournisseur d'IA configuré, par le connecteur embarqué, après
l'écran d'envoi. L'autre appel externe est l'ouverture du registre Word enregistré sur le disque, par le
programme associé aux fichiers .docx (os.startfile, Windows).
"""

from __future__ import annotations

import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from connecteur_ia import ErreurConnecteur
from connecteur_ia.interface import confirmer_envoi

from . import __version__, ia
from .__main__ import dossier_par_defaut, ecrire_registre, refuser_si_dans_le_dossier
from .analyse import classer
from .lecture import ErreurLecture, lire_dossier
from .rapport import AVERTISSEMENT_IA, COLONNES, lignes, mode


class Application(ttk.Frame):
    def __init__(self, racine: tk.Tk):
        super().__init__(racine, padding=12)
        self.racine = racine
        self.sortie = dossier_par_defaut()
        self.registre: str | None = None
        self.inventaire = None
        self.config_ia: str | None = None   # None : config-ia.json à la racine de l'outil
        self.synchrone = False               # True dans les tests : l'appel se fait sans fil d'exécution
        racine.title(f"Inventaire d'un dossier {__version__} — jerlash.labs")
        racine.minsize(1000, 620)
        self.grid(sticky="nsew")
        racine.columnconfigure(0, weight=1)
        racine.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=3)
        self.rowconfigure(5, weight=1)

        ttk.Label(self, text="Inventaire d'un dossier contractuel", font=("Segoe UI", 13, "bold")).grid(sticky="w")
        ttk.Label(self, wraplength=960, justify="left", text=(
            "Les pièces sont lues sur cet ordinateur et ne sont jamais modifiées. Des extraits pseudonymisés sont "
            "envoyés au fournisseur d'IA de votre configuration, avec votre clé, après votre relecture. "
            + AVERTISSEMENT_IA)).grid(sticky="w", pady=(4, 10))

        options = ttk.Frame(self)
        options.grid(sticky="ew", pady=(0, 8))
        options.columnconfigure(1, weight=1)
        ttk.Button(options, text="Choisir le dossier à inventorier…", command=self.choisir).grid(row=0, column=0, sticky="w")
        self.etiquette_dossier = ttk.Label(options, text="")
        self.etiquette_dossier.grid(row=0, column=1, sticky="w", padx=8)
        ttk.Button(options, text="Dossier des registres…", command=self.choisir_sortie).grid(row=1, column=0, sticky="w", pady=4)
        self.etiquette_sortie = ttk.Label(options, text=self.sortie)
        self.etiquette_sortie.grid(row=1, column=1, sticky="w", padx=8)

        self.liste = ttk.Treeview(self, columns=COLONNES[2:], height=12)
        self.liste.heading("#0", text="Pièce")
        self.liste.column("#0", width=300)
        for colonne, largeur in zip(COLONNES[2:], (120, 90, 90, 260, 90, 70)):
            self.liste.heading(colonne, text=colonne)
            self.liste.column(colonne, width=largeur, stretch=colonne == "Parties")
        self.liste.grid(row=3, sticky="nsew")
        self.liste.bind("<<TreeviewSelect>>", self.afficher_indices)

        ttk.Label(self, text="Alertes et indices de la pièce sélectionnée", font=("Segoe UI", 10, "bold")).grid(
            row=4, sticky="w", pady=(8, 2))
        self.details = tk.Text(self, height=8, wrap="word", relief="flat", background=racine.cget("background"))
        self.details.grid(row=5, sticky="nsew")
        self.details.configure(state="disabled")
        bas = ttk.Frame(self)
        bas.grid(row=6, sticky="ew", pady=(8, 0))
        bas.columnconfigure(0, weight=1)
        self.etat = ttk.Label(bas, text="")
        self.etat.grid(row=0, column=0, sticky="w")
        ttk.Button(bas, text="Ouvrir le registre Word", command=self.ouvrir).grid(row=0, column=1, sticky="e")

    def choisir_sortie(self) -> None:
        chemin = filedialog.askdirectory(title="Dossier où enregistrer les registres", initialdir=self.sortie)
        if chemin:
            self.sortie = chemin
            self.etiquette_sortie.configure(text=chemin)

    def vider(self, etat: str = "") -> None:
        """Rien de l'essai précédent ne reste affiché : pas de mélange entre deux dossiers."""
        self.inventaire, self.registre = None, None
        self.liste.delete(*self.liste.get_children())
        self.ecrire_details("")
        self.etat.configure(text=etat)

    def echec(self, e: Exception) -> None:
        # lancée par pythonw, une erreur non affichée serait perdue
        self.racine.configure(cursor="")
        self.vider()
        connue = isinstance(e, (ErreurLecture, ErreurConnecteur, OSError))
        messagebox.showerror("Inventaire", str(e) if connue else f"Erreur inattendue ({type(e).__name__}) : {e}")

    def lancer(self, travail, suite) -> None:
        """Exécute l'appel au fournisseur hors de la boucle de la fenêtre, qui reste réactive."""
        if self.synchrone:
            try:
                resultat = travail()
            except Exception as e:
                self.echec(e)
                return
            suite(resultat)
            return
        file: queue.Queue = queue.Queue()
        threading.Thread(target=lambda: file.put(self._essayer(travail)), daemon=True).start()

        def attendre():
            try:
                ok, resultat = file.get_nowait()
            except queue.Empty:
                self.racine.after(150, attendre)
                return
            if ok:
                suite(resultat)
            else:
                self.echec(resultat)

        self.racine.after(150, attendre)

    @staticmethod
    def _essayer(travail):
        try:
            return True, travail()
        except Exception as e:
            return False, e

    def choisir(self) -> None:
        try:
            config, cle = ia.charger_acces(ia.dossier_outil(), self.config_ia)
        except Exception as e:  # sans configuration ni clé, l'outil ne fonctionne pas (ADR-019)
            self.echec(e)
            return
        dossier = filedialog.askdirectory(title="Dossier à inventorier")
        if not dossier:
            return
        self.racine.configure(cursor="watch")
        self.racine.update_idletasks()
        try:
            refuser_si_dans_le_dossier(self.sortie, os.path.abspath(dossier))
            pieces, ignores = lire_dossier(dossier)
            inventaire = classer(dossier, pieces, ignores)
            envoi = ia.preparer_envoi(inventaire)
        except Exception as e:
            self.echec(e)
            return
        self.racine.configure(cursor="")
        texte = envoi.texte
        if not envoi.vide:
            texte = confirmer_envoi(self.racine, config, ia.CONSIGNE, envoi.texte)
            if texte is None:
                self.vider("Envoi annulé : rien n'a été envoyé, aucun registre n'a été écrit.")
                return
        self.vider(f"Envoi à {config.fournisseur} en cours…")
        self.racine.configure(cursor="watch")

        def travail():
            ia.completer(inventaire, envoi, texte, config, cle)
            return inventaire, ecrire_registre(inventaire, self.sortie)

        self.lancer(travail, lambda r: self.afficher(dossier, *r))

    def afficher(self, dossier: str, inventaire, fichiers: list[str]) -> None:
        self.racine.configure(cursor="")
        self.inventaire = inventaire
        self.registre = fichiers[0]
        self.etiquette_dossier.configure(text=dossier)
        self.liste.delete(*self.liste.get_children())
        for ligne, fiche in zip(lignes(self.inventaire), self.inventaire.fiches):
            self.liste.insert("", "end", iid=fiche.piece.chemin, text=f"{ligne[0]}. {ligne[1]}", values=ligne[2:],
                              tags=("alerte",) if fiche.alertes else ())
        self.liste.tag_configure("alerte", foreground="#a23d24")
        self.etat.configure(text=f"{len(self.inventaire.fiches)} pièces ; {len(self.inventaire.alertes)} alerte(s). "
                                 f"État : {self.inventaire.etat}. Mode : {mode(self.inventaire)}. "
                                 f"Registre : {self.registre}")
        self.ecrire_details("\n".join(f"– {a}" for a in self.inventaire.alertes) or "Aucune alerte.")

    def ecrire_details(self, texte: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", texte)
        self.details.configure(state="disabled")

    def afficher_indices(self, _evenement=None) -> None:
        selection = self.liste.selection()
        if not selection or not self.inventaire:
            return
        fiche = next((f for f in self.inventaire.fiches if f.piece.chemin == selection[0]), None)
        if fiche is None:
            return
        texte = [f"Alerte : {a}" for a in fiche.alertes] + [f"Indice : {i}" for i in fiche.indices]
        if fiche.piece.auteur:
            texte.append(f"Auteur : {fiche.piece.auteur}")
        texte.append(f"SHA-256 : {fiche.piece.sha256 or '(non calculée)'}")
        self.ecrire_details("\n".join(texte))

    def ouvrir(self) -> None:
        if not self.registre:
            return
        if sys.platform == "win32":
            os.startfile(self.registre)  # programme associé aux .docx, sur ce poste
        else:
            messagebox.showinfo("Registre", f"Registre enregistré ici :\n{self.registre}")


def main() -> int:
    racine = tk.Tk()
    Application(racine)
    racine.mainloop()
    return 0
