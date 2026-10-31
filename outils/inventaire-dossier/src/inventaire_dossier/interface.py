"""Fenêtre graphique (tkinter, inclus dans Python). Aucun accès réseau.

Le seul appel externe est l'ouverture du registre Word enregistré sur le disque, par le programme
associé aux fichiers .docx (os.startfile, Windows).
"""

from __future__ import annotations

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .__main__ import dossier_par_defaut, ecrire_registre
from .analyse import inventorier
from .lecture import ErreurLecture, lire_dossier
from .rapport import AVERTISSEMENT, COLONNES, lignes


class Application(ttk.Frame):
    def __init__(self, racine: tk.Tk):
        super().__init__(racine, padding=12)
        self.racine = racine
        self.sortie = dossier_par_defaut()
        self.registre: str | None = None
        self.inventaire = None
        racine.title(f"Inventaire d'un dossier {__version__} — iavocat.be")
        racine.minsize(1000, 620)
        self.grid(sticky="nsew")
        racine.columnconfigure(0, weight=1)
        racine.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=3)
        self.rowconfigure(5, weight=1)

        ttk.Label(self, text="Inventaire d'un dossier contractuel", font=("Segoe UI", 13, "bold")).grid(sticky="w")
        ttk.Label(self, wraplength=960, justify="left", text=(
            "Les pièces sont lues sur cet ordinateur, sans IA ni connexion réseau, et ne sont jamais modifiées. "
            + AVERTISSEMENT)).grid(sticky="w", pady=(4, 10))

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

    def choisir(self) -> None:
        dossier = filedialog.askdirectory(title="Dossier à inventorier")
        if not dossier:
            return
        self.racine.configure(cursor="watch")
        self.racine.update_idletasks()
        try:
            pieces, ignores = lire_dossier(dossier)
            inventaire = inventorier(dossier, pieces, ignores)
            fichiers = ecrire_registre(inventaire, self.sortie)
        except Exception as e:  # lancée par pythonw, une erreur non affichée serait perdue
            # Rien de l'essai précédent ne reste affiché : pas de mélange entre deux dossiers.
            self.inventaire, self.registre = None, None
            self.liste.delete(*self.liste.get_children())
            self.ecrire_details("")
            self.etat.configure(text="")
            message = str(e) if isinstance(e, (ErreurLecture, OSError)) else f"Erreur inattendue ({type(e).__name__}) : {e}"
            messagebox.showerror("Inventaire", message)
            return
        finally:
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
                                 f"État : {self.inventaire.etat}. Registre : {self.registre}")
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
