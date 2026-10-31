"""Fenêtre graphique (tkinter, inclus dans Python). Aucun accès réseau.

Le seul appel externe est l'ouverture du rapport HTML local dans le navigateur par défaut.
"""

from __future__ import annotations

import os
import pathlib
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .__main__ import ecrire
from .analyse import ErreurConfiguration, analyser, charger_configuration
from .rapport import en_html

RESULTATS = {"rien_detecte": "Rien détecté", "a_traiter": "Points à traiter",
             "incomplet": "Analyse incomplète", "erreur": "Analyse impossible"}


def dossier_par_defaut() -> str:
    documents = pathlib.Path.home() / "Documents"
    base = documents if documents.is_dir() else pathlib.Path.home()
    return str(base / "Controle avant envoi")


class Application(ttk.Frame):
    def __init__(self, racine: tk.Tk):
        super().__init__(racine, padding=16)
        self.racine = racine
        self.termes: str | None = None
        self.dossier = dossier_par_defaut()
        self.rapports: dict[str, tuple] = {}
        self.ecrits: set = set()
        racine.title(f"Contrôle avant envoi {__version__} — iavocat.be")
        racine.minsize(720, 460)
        self.grid(sticky="nsew")
        racine.columnconfigure(0, weight=1)
        racine.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Contrôle d'un document Word avant envoi", font=("Segoe UI", 13, "bold")).grid(sticky="w")
        ttk.Label(self, wraplength=680, justify="left", text=(
            "Le document est lu sur cet ordinateur, sans connexion réseau ni intelligence artificielle. "
            "Il n'est jamais modifié. Un rapport HTML est enregistré pour chaque document.")).grid(sticky="w", pady=(4, 12))

        options = ttk.Frame(self)
        options.grid(sticky="ew", pady=(0, 8))
        options.columnconfigure(1, weight=1)
        ttk.Button(options, text="Choisir des documents…", command=self.choisir).grid(row=0, column=0, sticky="w")
        ttk.Button(options, text="Liste de termes sensibles…", command=self.choisir_termes).grid(row=1, column=0, sticky="w", pady=4)
        self.etiquette_termes = ttk.Label(options, text="Aucune liste : le contrôle des noms d'autres dossiers ne sera pas réalisé.")
        self.etiquette_termes.grid(row=1, column=1, sticky="w", padx=8)
        ttk.Button(options, text="Dossier des rapports…", command=self.choisir_dossier).grid(row=2, column=0, sticky="w")
        self.etiquette_dossier = ttk.Label(options, text=self.dossier)
        self.etiquette_dossier.grid(row=2, column=1, sticky="w", padx=8)

        self.liste = ttk.Treeview(self, columns=("resultat",), height=8, selectmode="browse")
        self.liste.heading("#0", text="Document")
        self.liste.heading("resultat", text="Résultat")
        self.liste.column("resultat", width=170, stretch=False)
        self.liste.grid(sticky="nsew")
        self.liste.bind("<<TreeviewSelect>>", self.afficher)
        self.liste.bind("<Double-1>", lambda _e: self.ouvrir())

        self.verdict = tk.Text(self, height=4, wrap="word", relief="flat", background=racine.cget("background"))
        self.verdict.grid(sticky="ew", pady=8)
        self.verdict.configure(state="disabled")
        ttk.Button(self, text="Ouvrir le rapport", command=self.ouvrir).grid(sticky="e")

    def choisir_termes(self) -> None:
        chemin = filedialog.askopenfilename(title="Liste de termes (un par ligne)",
                                            filetypes=[("Texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if chemin:
            self.termes = chemin
            self.etiquette_termes.configure(text=os.path.basename(chemin))

    def choisir_dossier(self) -> None:
        chemin = filedialog.askdirectory(title="Dossier où enregistrer les rapports", initialdir=self.dossier)
        if chemin:
            self.dossier = chemin
            self.etiquette_dossier.configure(text=chemin)

    def choisir(self) -> None:
        chemins = filedialog.askopenfilenames(title="Documents à contrôler",
                                              filetypes=[("Documents Word", "*.docx *.docm"), ("Tous les fichiers", "*.*")])
        if not chemins:
            return
        try:
            cfg = charger_configuration(chemin_termes=self.termes)
        except ErreurConfiguration as e:
            messagebox.showerror("Configuration", str(e))
            return
        self.racine.configure(cursor="watch")
        self.racine.update_idletasks()
        try:
            for chemin in chemins:
                rapport = analyser(chemin, cfg)
                try:
                    fichier = ecrire(self.dossier, chemin, "html", en_html(rapport), self.ecrits)
                except (OSError, ErreurConfiguration) as e:
                    messagebox.showerror("Rapport", f"Le rapport n'a pas pu être enregistré : {e}")
                    fichier = None
                ident = self.liste.insert("", "end", text=rapport.nom, values=(RESULTATS[rapport.niveau],))
                self.rapports[ident] = (rapport, fichier)
                self.liste.selection_set(ident)
        finally:
            self.racine.configure(cursor="")

    def afficher(self, _evenement=None) -> None:
        selection = self.liste.selection()
        if not selection:
            return
        rapport, _ = self.rapports[selection[0]]
        self.verdict.configure(state="normal")
        self.verdict.delete("1.0", "end")
        self.verdict.insert("1.0", rapport.verdict)
        self.verdict.configure(state="disabled")

    def ouvrir(self) -> None:
        selection = self.liste.selection()
        if not selection:
            return
        _, fichier = self.rapports[selection[0]]
        if fichier:
            webbrowser.open(pathlib.Path(fichier).resolve().as_uri())


def main() -> int:
    racine = tk.Tk()
    Application(racine)
    racine.mainloop()
    return 0
