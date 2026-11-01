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
from .analyse import ORDRE, analyser, lister
from .lecture import ErreurLecture, lire_contrat
from .rapport import AVERTISSEMENT, TITRES, synthese


class Application(ttk.Frame):
    def __init__(self, racine: tk.Tk):
        super().__init__(racine, padding=12)
        self.racine = racine
        self.sortie = dossier_par_defaut()
        self.rapport: str | None = None
        self.analyse = None
        racine.title(f"Glossaire des définitions {__version__} — iavocat.be")
        racine.minsize(1000, 640)
        self.grid(sticky="nsew")
        racine.columnconfigure(0, weight=1)
        racine.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        ttk.Label(self, text="Glossaire des définitions d'un contrat", font=("Segoe UI", 13, "bold")).grid(
            columnspan=2, sticky="w")
        ttk.Label(self, wraplength=960, justify="left", text=(
            "Le contrat est lu sur cet ordinateur, sans IA ni connexion réseau, et n'est jamais modifié. "
            + AVERTISSEMENT)).grid(columnspan=2, sticky="w", pady=(4, 10))

        options = ttk.Frame(self)
        options.grid(columnspan=2, sticky="ew", pady=(0, 8))
        options.columnconfigure(1, weight=1)
        ttk.Button(options, text="Choisir le contrat…", command=self.choisir).grid(row=0, column=0, sticky="w")
        self.etiquette_contrat = ttk.Label(options, text="")
        self.etiquette_contrat.grid(row=0, column=1, sticky="w", padx=8)
        ttk.Button(options, text="Dossier des rapports…", command=self.choisir_sortie).grid(row=1, column=0, sticky="w", pady=4)
        self.etiquette_sortie = ttk.Label(options, text=self.sortie)
        self.etiquette_sortie.grid(row=1, column=1, sticky="w", padx=8)

        ttk.Label(self, text="Points à examiner", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w")
        ttk.Label(self, text="Termes définis", font=("Segoe UI", 10, "bold")).grid(row=3, column=1, sticky="w", padx=(10, 0))
        self.points = tk.Text(self, wrap="word", relief="flat", background=racine.cget("background"))
        self.points.grid(row=4, column=0, sticky="nsew")
        self.points.configure(state="disabled")
        droite = ttk.Frame(self)
        droite.grid(row=4, column=1, sticky="nsew", padx=(10, 0))
        droite.columnconfigure(0, weight=1)
        droite.rowconfigure(0, weight=2)
        droite.rowconfigure(1, weight=1)
        self.liste = ttk.Treeview(droite, columns=("ou", "emplois"), height=10)
        self.liste.heading("#0", text="Terme")
        self.liste.heading("ou", text="Défini à")
        self.liste.heading("emplois", text="Emplois")
        self.liste.column("#0", width=220)
        self.liste.column("ou", width=180)
        self.liste.column("emplois", width=70, stretch=False)
        self.liste.grid(row=0, sticky="nsew")
        self.liste.bind("<<TreeviewSelect>>", self.afficher_terme)
        self.details = tk.Text(droite, height=8, wrap="word", relief="flat", background=racine.cget("background"))
        self.details.grid(row=1, sticky="nsew", pady=(8, 0))
        self.details.configure(state="disabled")

        bas = ttk.Frame(self)
        bas.grid(row=5, columnspan=2, sticky="ew", pady=(8, 0))
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
            self.ecrire(self.points, "")
            self.ecrire(self.details, "")
            self.etat.configure(text="")
            self.etiquette_contrat.configure(text="")
            message = str(e) if isinstance(e, (ErreurLecture, OSError)) else f"Erreur inattendue ({type(e).__name__}) : {e}"
            messagebox.showerror("Glossaire", message)
            return
        finally:
            self.racine.configure(cursor="")
        self.analyse, self.rapport = analyse, fichiers[0]
        self.etiquette_contrat.configure(text=chemin)
        texte = synthese(analyse)
        for c in ORDRE:
            if analyse.du_type(c):
                texte += ["", f"{TITRES[c]} :"] + [f"– {x.message}" for x in analyse.du_type(c)]
        self.ecrire(self.points, "\n".join(texte))
        self.liste.delete(*self.liste.get_children())
        signales = {x.terme for x in analyse.constats}
        for i, t in enumerate(analyse.termes):
            self.liste.insert("", "end", iid=str(i), text=t.forme, tags=("signale",) if t.forme in signales else (),
                              values=(", ".join(dict.fromkeys(d.lieu for d in t.definitions)), len(t.emplois)))
        self.liste.tag_configure("signale", foreground="#a23d24")
        self.ecrire(self.details, "")
        self.etat.configure(text=f"{len(analyse.termes)} termes définis ; {len(analyse.constats)} point(s) à examiner. "
                                 f"Rapport : {self.rapport}")

    @staticmethod
    def ecrire(zone: tk.Text, texte: str) -> None:
        zone.configure(state="normal")
        zone.delete("1.0", "end")
        zone.insert("1.0", texte)
        zone.configure(state="disabled")

    def afficher_terme(self, _evenement=None) -> None:
        selection = self.liste.selection()
        if not selection or not self.analyse:
            return
        terme = self.analyse.termes[int(selection[0])]
        texte = [f"{d.lieu} : {d.libelle}" for d in terme.definitions]
        if terme.emplois:
            texte.append(f"Employé à : {lister(terme.emplois, self.analyse.lieux)}")
        texte += [f"Graphie « {f} » : {lister(ou, self.analyse.lieux)}" for f, ou in terme.variantes.items()]
        self.ecrire(self.details, "\n".join(texte))

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
        "Glossaire", f"Erreur inattendue ({typ.__name__}) : {valeur}")
    Application(racine)
    racine.mainloop()
    return 0
