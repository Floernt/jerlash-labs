"""Fenêtre graphique (tkinter, inclus dans Python). Aucun accès réseau.

Le seul appel externe est l'ouverture du rapport Word enregistré sur le disque, par le programme
associé aux fichiers .docx (os.startfile, Windows).
"""

from __future__ import annotations

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .__main__ import dossier_par_defaut, ecrire_rapport
from .analyse import LIBELLES, analyser
from .lecture import ErreurLecture, lire_contrat
from .rapport import AVERTISSEMENT, CLASSEMENTS, nom_du_bloc, synthese

COULEURS = {"mixte": "#a23d24", "particulieres": "#1f4e79", "generales": "#333333"}


class Application(ttk.Frame):
    def __init__(self, racine: tk.Tk):
        super().__init__(racine, padding=12)
        self.racine = racine
        self.sortie = dossier_par_defaut()
        self.rapport: str | None = None
        self.analyse = None
        racine.title(f"Conditions particulières et générales {__version__} — jerlash.labs")
        racine.minsize(1000, 640)
        self.grid(sticky="nsew")
        racine.columnconfigure(0, weight=1)
        racine.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=3)
        self.rowconfigure(6, weight=1)

        ttk.Label(self, text="Conditions particulières et générales d'un contrat", font=("Segoe UI", 13, "bold")).grid(sticky="w")
        ttk.Label(self, wraplength=960, justify="left", text=(
            "Le contrat est lu sur cet ordinateur, sans IA ni connexion réseau, et n'est jamais modifié. "
            + AVERTISSEMENT)).grid(sticky="w", pady=(4, 10))

        options = ttk.Frame(self)
        options.grid(sticky="ew", pady=(0, 8))
        options.columnconfigure(1, weight=1)
        ttk.Button(options, text="Choisir le contrat…", command=self.choisir).grid(row=0, column=0, sticky="w")
        self.etiquette_contrat = ttk.Label(options, text="")
        self.etiquette_contrat.grid(row=0, column=1, sticky="w", padx=8)
        ttk.Button(options, text="Dossier des rapports…", command=self.choisir_sortie).grid(row=1, column=0, sticky="w", pady=4)
        self.etiquette_sortie = ttk.Label(options, text=self.sortie)
        self.etiquette_sortie.grid(row=1, column=1, sticky="w", padx=8)

        self.resume = ttk.Label(self, text="", wraplength=960, justify="left")
        self.resume.grid(row=3, sticky="w", pady=(0, 6))
        self.liste = ttk.Treeview(self, columns=("proposition", "donnees"), height=12)
        self.liste.heading("#0", text="Bloc")
        self.liste.heading("proposition", text="Proposition")
        self.liste.heading("donnees", text="Données propres")
        self.liste.column("#0", width=420)
        self.liste.column("proposition", width=220)
        self.liste.column("donnees", width=120, stretch=False)
        self.liste.grid(row=4, sticky="nsew")
        self.liste.bind("<<TreeviewSelect>>", self.afficher_bloc)
        ttk.Label(self, text="Bloc sélectionné", font=("Segoe UI", 10, "bold")).grid(row=5, sticky="w", pady=(8, 2))
        self.details = tk.Text(self, height=8, wrap="word", relief="flat", background=racine.cget("background"))
        self.details.grid(row=6, sticky="nsew")
        self.details.configure(state="disabled")

        bas = ttk.Frame(self)
        bas.grid(row=7, sticky="ew", pady=(8, 0))
        bas.columnconfigure(0, weight=1)
        self.etat = ttk.Label(bas, text="")
        self.etat.grid(row=0, column=0, sticky="w")
        ttk.Button(bas, text="Ouvrir le rapport Word", command=self.ouvrir).grid(row=0, column=1, sticky="e")

    def choisir_sortie(self) -> None:
        chemin = filedialog.askdirectory(title="Dossier où enregistrer les rapports", initialdir=self.sortie)
        if chemin:
            self.sortie = chemin
            self.etiquette_sortie.configure(text=chemin)

    def choisir(self) -> None:
        chemin = filedialog.askopenfilename(title="Contrat à analyser", filetypes=[
            ("Contrats", "*.docx *.txt *.md"), ("Tous les fichiers", "*.*")])
        if not chemin:
            return
        self.racine.configure(cursor="watch")
        self.racine.update_idletasks()
        try:
            analyse = analyser(lire_contrat(chemin))
            fichiers = ecrire_rapport(analyse, self.sortie)
        except Exception as e:  # lancée par pythonw, une erreur non affichée serait perdue
            # Rien de l'essai précédent ne reste affiché : pas de mélange entre deux contrats.
            self.analyse, self.rapport = None, None
            self.liste.delete(*self.liste.get_children())
            self.ecrire("")
            self.resume.configure(text="")
            self.etat.configure(text="")
            self.etiquette_contrat.configure(text="")
            message = str(e) if isinstance(e, (ErreurLecture, OSError)) else f"Erreur inattendue ({type(e).__name__}) : {e}"
            messagebox.showerror("Conditions", message)
            return
        finally:
            self.racine.configure(cursor="")
        self.analyse, self.rapport = analyse, fichiers[0]
        self.etiquette_contrat.configure(text=chemin)
        self.resume.configure(text="\n".join(synthese(analyse)))
        self.liste.delete(*self.liste.get_children())
        for i, b in enumerate(analyse.blocs):
            self.liste.insert("", "end", iid=str(i), text=nom_du_bloc(b), tags=(b.classement,),
                              values=(CLASSEMENTS[b.classement], len(b.donnees)))
        for classement, couleur in COULEURS.items():
            self.liste.tag_configure(classement, foreground=couleur)
        self.ecrire("")
        self.etat.configure(text=f"{len(analyse.du_type('mixte'))} clause(s) mixte(s) à épurer. Rapport : {self.rapport}")

    def ecrire(self, texte: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", texte)
        self.details.configure(state="disabled")

    def afficher_bloc(self, _evenement=None) -> None:
        selection = self.liste.selection()
        if not selection or not self.analyse:
            return
        b = self.analyse.blocs[int(selection[0])]
        texte = [f"{CLASSEMENTS[b.classement]} : {b.raison}."]
        texte += [f"– {LIBELLES[d.categorie]} : {d.texte}" for d in b.donnees]
        if b.renvois:
            texte.append("Renvois : " + ", ".join(b.renvois))
        self.ecrire("\n".join(texte))

    def ouvrir(self) -> None:
        if not self.rapport:
            return
        if sys.platform == "win32":
            try:
                os.startfile(self.rapport)  # programme associé aux .docx, sur ce poste
            except OSError as e:
                messagebox.showerror("Rapport", f"Le rapport n'a pas pu être ouvert ({e}).\nIl est enregistré ici :\n{self.rapport}")
        else:
            messagebox.showinfo("Rapport", f"Rapport enregistré ici :\n{self.rapport}")


def main() -> int:
    racine = tk.Tk()
    # Lancée par pythonw, une erreur non affichée serait perdue : toute erreur d'un bouton est montrée.
    racine.report_callback_exception = lambda typ, valeur, _trace: messagebox.showerror(
        "Conditions", f"Erreur inattendue ({typ.__name__}) : {valeur}")
    Application(racine)
    racine.mainloop()
    return 0
