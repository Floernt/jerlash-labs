"""Fenêtre graphique (tkinter, inclus dans Python). Aucun accès réseau.

Deux onglets : « Pseudonymiser » (détecter, relire, corriger, enregistrer) et « Rétablir »
(remettre les données d'origine dans la réponse de l'IA à l'aide de la table de correspondance).

Règle centrale : ce qui est enregistré est exactement le texte pseudonymisé affiché et relu. Toute
modification du texte d'origine ou des choix de remplacement décoche la case de relecture.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .__main__ import AVERTISSEMENT, dossier_par_defaut, enregistrer
from .detection import CATEGORIES, detecter, lire_termes, motif_recherche, preparer
from .lecture import ErreurLecture, lire_fichier
from .remplacement import RE_MARQUEUR_EXACT, attribuer_marqueurs, lire_table, pseudonymiser, retablir


def zone_texte(parent, titre: str, lecture_seule: bool = False) -> tk.Text:
    cadre = ttk.LabelFrame(parent, text=titre, padding=4)
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)
    zone = tk.Text(cadre, wrap="word", height=12, undo=not lecture_seule, font=("Segoe UI", 10))
    defilement = ttk.Scrollbar(cadre, command=zone.yview)
    zone.configure(yscrollcommand=defilement.set)
    zone.grid(row=0, column=0, sticky="nsew")
    defilement.grid(row=0, column=1, sticky="ns")
    if lecture_seule:
        zone.configure(state="disabled", background="#f6f4f0")
    zone.cadre = cadre
    return zone


def remplir(zone: tk.Text, texte: str) -> None:
    etat = zone.cget("state")
    zone.configure(state="normal")
    zone.delete("1.0", "end")
    zone.insert("1.0", texte)
    zone.configure(state=etat)


class Pseudonymiser(ttk.Frame):
    def __init__(self, parent, application):
        super().__init__(parent, padding=8)
        self.application = application
        self.entites = []
        self.termes_fichier: list[tuple[str, str]] = []   # liste choisie par la personne, gardée d'un document à l'autre
        self.termes_ajoutes: list[tuple[str, str]] = []   # ajouts propres au document en cours
        self.desactives: set[str] = set()                 # clés que la personne a choisi de ne pas remplacer
        self.source = ""
        self.texte_detecte: str | None = None             # texte sur lequel la détection affichée a été faite
        self.resultat = None                              # résultat affiché, seul enregistrable
        self.dossier = dossier_par_defaut()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=2)

        barre = ttk.Frame(self)
        barre.grid(row=0, sticky="ew", pady=(0, 6))
        ttk.Button(barre, text="Ouvrir un fichier…", command=self.ouvrir).pack(side="left")
        ttk.Button(barre, text="Coller", command=self.coller).pack(side="left", padx=4)
        ttk.Button(barre, text="Liste de termes…", command=self.choisir_termes).pack(side="left", padx=(12, 4))
        self.etiquette_termes = ttk.Label(barre, text="")
        self.etiquette_termes.pack(side="left")
        ttk.Button(barre, text="Détecter", command=self.detecter).pack(side="right")

        textes = ttk.Panedwindow(self, orient="horizontal")
        textes.grid(row=1, sticky="nsew")
        self.zone_source = zone_texte(textes, "Texte d'origine (collez ou ouvrez un fichier, puis « Détecter »)")
        self.zone_resultat = zone_texte(textes, "Texte pseudonymisé : c'est ce texte qui sera enregistré", lecture_seule=True)
        self.zone_resultat.tag_configure("marqueur", foreground="#a23d24", font=("Segoe UI", 10, "bold"))
        textes.add(self.zone_source.cadre, weight=1)
        textes.add(self.zone_resultat.cadre, weight=1)
        self.zone_source.bind("<<Modified>>", self.source_modifiee)

        cadre_liste = ttk.LabelFrame(self, text="Données détectées : double-clic pour remplacer ou non", padding=4)
        cadre_liste.grid(row=2, sticky="nsew", pady=6)
        cadre_liste.columnconfigure(0, weight=1)
        cadre_liste.rowconfigure(0, weight=1)
        self.liste = ttk.Treeview(cadre_liste, columns=("remplacer", "donnees", "nombre", "motif"), height=7)
        for colonne, titre, largeur in (("#0", "Marqueur", 150), ("remplacer", "Remplacer", 80),
                                        ("donnees", "Données d'origine", 280), ("nombre", "Occurrences", 90),
                                        ("motif", "Motif de détection", 260)):
            self.liste.heading(colonne, text=titre)
            self.liste.column(colonne, width=largeur, stretch=colonne in ("donnees", "motif"))
        self.liste.tag_configure("non", foreground="#8a8a8a")
        defilement = ttk.Scrollbar(cadre_liste, command=self.liste.yview)
        self.liste.configure(yscrollcommand=defilement.set)
        self.liste.grid(row=0, column=0, sticky="nsew")
        defilement.grid(row=0, column=1, sticky="ns")
        self.liste.bind("<Double-1>", self.basculer)
        self.liste.bind("<space>", self.basculer)

        ajout = ttk.Frame(cadre_liste)
        ajout.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        ttk.Label(ajout, text="Ajouter une donnée oubliée :").pack(side="left")
        self.categorie = ttk.Combobox(ajout, values=list(CATEGORIES), width=18, state="readonly")
        self.categorie.set("PERSONNE")
        self.categorie.pack(side="left", padx=4)
        self.nouveau = ttk.Entry(ajout, width=34)
        self.nouveau.pack(side="left", padx=4)
        self.nouveau.bind("<Return>", lambda _e: self.ajouter())
        ttk.Button(ajout, text="Ajouter", command=self.ajouter).pack(side="left")

        bas = ttk.Frame(self)
        bas.grid(row=3, sticky="ew")
        bas.columnconfigure(0, weight=1)
        ttk.Label(bas, text=AVERTISSEMENT, wraplength=900, justify="left", foreground="#7a2e1b").grid(
            row=0, column=0, columnspan=2, sticky="w")
        self.relu = tk.BooleanVar(value=False)
        self.case = ttk.Checkbutton(bas, text="J'ai relu le texte pseudonymisé et ajouté ce que l'outil avait manqué.",
                                    variable=self.relu, command=self.actualiser_bouton, state="disabled")
        self.case.grid(row=1, column=0, sticky="w", pady=6)
        self.bouton = ttk.Button(bas, text="Enregistrer et copier le texte", command=self.enregistrer, state="disabled")
        self.bouton.grid(row=1, column=1, sticky="e")
        self.etat = ttk.Label(bas, text=f"Dossier d'enregistrement : {self.dossier}", wraplength=900, justify="left")
        self.etat.grid(row=2, column=0, columnspan=2, sticky="w")

    # Chargement ------------------------------------------------------------------------------------

    def nouveau_document(self, texte: str, source: str) -> None:
        """Un autre document : les choix faits sur le précédent ne s'appliquent pas à celui-ci."""
        self.termes_ajoutes = []
        self.desactives = set()
        self.source = source
        remplir(self.zone_source, preparer(texte))
        self.detecter()

    def ouvrir(self) -> None:
        chemin = filedialog.askopenfilename(title="Texte à pseudonymiser", filetypes=[
            ("Textes et documents Word", "*.txt *.md *.docx"), ("Tous les fichiers", "*.*")])
        if not chemin:
            return
        try:
            texte = lire_fichier(chemin)
        except ErreurLecture as e:
            messagebox.showerror("Lecture", str(e))
            return
        self.nouveau_document(texte, os.path.basename(chemin))
        if chemin.lower().endswith(".docx"):
            self.signaler("Document Word : seul le corps du texte est repris (ni en-têtes, ni pieds de page, "
                          "ni notes, ni commentaires).")

    def coller(self) -> None:
        try:
            texte = self.clipboard_get()
        except tk.TclError:
            messagebox.showinfo("Coller", "Le presse-papiers ne contient pas de texte.")
            return
        self.nouveau_document(texte, "texte collé")

    def choisir_termes(self) -> None:
        chemin = filedialog.askopenfilename(title="Liste de termes (un par ligne ; « PERSONNE | Jean Dupont »)",
                                            filetypes=[("Texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if not chemin:
            return
        try:
            with open(chemin, encoding="utf-8-sig") as f:
                self.termes_fichier = lire_termes(f.read())
        except (OSError, ValueError) as e:
            messagebox.showerror("Liste de termes", str(e))
            return
        self.etiquette_termes.configure(text=f"{os.path.basename(chemin)} ({len(self.termes_fichier)} termes)")
        if self.texte_source().strip():
            self.detecter()

    # Détection et relecture ------------------------------------------------------------------------

    def texte_source(self) -> str:
        return self.zone_source.get("1.0", "end-1c")

    def source_modifiee(self, _evenement=None) -> None:
        if not self.zone_source.edit_modified():
            return
        self.zone_source.edit_modified(False)
        if self.texte_detecte is not None and self.texte_source() != self.texte_detecte:
            self.resultat = None
            self.relu.set(False)
            self.case.configure(state="disabled")
            self.actualiser_bouton()
            self.signaler("Texte d'origine modifié : cliquez sur « Détecter » pour mettre à jour le texte pseudonymisé.")

    def detecter(self) -> None:
        texte = self.texte_source()
        if texte != preparer(texte):
            remplir(self.zone_source, preparer(texte))
            texte = self.texte_source()
        try:
            self.entites = detecter(texte, self.termes_fichier + self.termes_ajoutes, desactives=self.desactives)
        except ValueError as e:
            messagebox.showerror("Détection", str(e))
            return
        self.texte_detecte = texte
        self.zone_source.edit_modified(False)
        self.actualiser()

    def actualiser(self) -> None:
        texte = self.texte_detecte or ""
        self.relu.set(False)
        marqueurs = attribuer_marqueurs(self.entites, texte)
        groupes: dict[str, list] = {}
        for e in self.entites:
            groupes.setdefault(e.cle, []).append(e)
        self.liste.delete(*self.liste.get_children())
        for cle, liste in groupes.items():
            actif = liste[0].actif
            formes = " / ".join(sorted({e.texte for e in liste}, key=len, reverse=True))
            self.liste.insert("", "end", iid=cle, text=marqueurs.get(cle, f"[{liste[0].categorie}]"),
                              values=("oui" if actif else "non", formes, len(liste), liste[0].raison),
                              tags=() if actif else ("non",))
        self.resultat = pseudonymiser(texte, self.entites, self.source)
        remplir(self.zone_resultat, self.resultat.texte)
        self.zone_resultat.configure(state="normal")
        for m in RE_MARQUEUR_EXACT.finditer(self.resultat.texte):
            self.zone_resultat.tag_add("marqueur", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        self.zone_resultat.configure(state="disabled")
        self.case.configure(state="normal" if texte.strip() else "disabled")
        self.actualiser_bouton()
        if self.resultat.marqueurs_preexistants:
            self.signaler("Attention : le texte d'origine contient déjà des marqueurs "
                          f"({', '.join(self.resultat.marqueurs_preexistants)}). Ils resteront tels quels au "
                          "rétablissement ; vérifiez qu'ils ne désignent pas des données réelles.")
        elif not self.entites and texte.strip():
            self.signaler("Aucune donnée détectée : cela ne prouve pas que le texte n'en contient pas. Relisez-le.")
        else:
            self.signaler(f"Dossier d'enregistrement : {self.dossier}")

    def basculer(self, _evenement=None) -> None:
        selection = self.liste.selection()
        if not selection or self.texte_detecte is None:
            return
        self.desactives ^= set(selection)
        if self.texte_source() != self.texte_detecte:
            self.source_modifiee()
            return
        self.entites = detecter(self.texte_detecte, self.termes_fichier + self.termes_ajoutes,
                                desactives=self.desactives)
        self.actualiser()
        self.liste.selection_set([c for c in selection if self.liste.exists(c)])

    def ajouter(self) -> None:
        terme = self.nouveau.get().strip()
        if not terme:
            return
        if not motif_recherche(terme, casse_stricte=False).search(self.texte_source()):
            messagebox.showinfo("Ajouter", f"« {terme} » ne figure pas tel quel dans le texte "
                                           "(vérifiez l'orthographe ; un retour à la ligne compte comme une espace).")
            return
        self.termes_ajoutes.append((self.categorie.get(), terme))
        self.nouveau.delete(0, "end")
        self.detecter()

    def actualiser_bouton(self) -> None:
        pret = self.relu.get() and self.resultat is not None and self.texte_source() == self.texte_detecte
        self.bouton.configure(state="normal" if pret else "disabled")

    def signaler(self, message: str) -> None:
        self.etat.configure(text=message)

    # Enregistrement --------------------------------------------------------------------------------

    def enregistrer(self) -> None:
        if not self.relu.get() or self.resultat is None or self.texte_source() != self.texte_detecte:
            self.actualiser_bouton()
            return
        resultat = self.resultat   # exactement ce qui est affiché et a été relu
        base = os.path.splitext(self.source)[0] if self.source and self.source != "texte collé" else "texte"
        try:
            chemin_texte, chemin_table = enregistrer(self.dossier, base, resultat.texte, resultat.table)
        except OSError as e:
            messagebox.showerror("Enregistrement", f"Enregistrement impossible : {e}")
            return
        self.clipboard_clear()
        self.clipboard_append(resultat.texte)
        self.application.retablir.charger_table(chemin_table)
        self.signaler(f"Texte copié et enregistré : {chemin_texte}\nTable de correspondance : {chemin_table}")
        messagebox.showinfo("Enregistré", "Le texte pseudonymisé est copié dans le presse-papiers.\n\n"
                            f"La table de correspondance est enregistrée ici :\n{chemin_table}\n\n"
                            "Elle contient les données d'origine : ne l'envoyez pas. Elle sert à rétablir "
                            "les noms dans la réponse de l'IA (onglet « Rétablir »).")


class Retablir(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.table = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        barre = ttk.Frame(self)
        barre.grid(row=0, sticky="ew", pady=(0, 6))
        ttk.Button(barre, text="Choisir la table…", command=self.choisir_table).pack(side="left")
        self.etiquette = ttk.Label(barre, text="Aucune table choisie.")
        self.etiquette.pack(side="left", padx=8)
        ttk.Button(barre, text="Rétablir", command=self.retablir).pack(side="right")
        textes = ttk.Panedwindow(self, orient="horizontal")
        textes.grid(row=1, sticky="nsew")
        self.zone_reponse = zone_texte(textes, "Réponse de l'IA (collez-la ici)")
        self.zone_retablie = zone_texte(textes, "Réponse avec les données d'origine", lecture_seule=True)
        textes.add(self.zone_reponse.cadre, weight=1)
        textes.add(self.zone_retablie.cadre, weight=1)
        bas = ttk.Frame(self)
        bas.grid(row=2, sticky="ew", pady=(6, 0))
        bas.columnconfigure(0, weight=1)
        self.etat = ttk.Label(bas, text="", wraplength=900, justify="left")
        self.etat.grid(row=0, column=0, sticky="w")
        ttk.Button(bas, text="Copier", command=self.copier).grid(row=0, column=1, sticky="e")

    def choisir_table(self) -> None:
        chemin = filedialog.askopenfilename(title="Table de correspondance", initialdir=dossier_par_defaut(),
                                            filetypes=[("Table", "*.json"), ("Tous les fichiers", "*.*")])
        if chemin:
            self.charger_table(chemin)

    def charger_table(self, chemin: str) -> None:
        try:
            self.table = lire_table(chemin)
        except (OSError, ValueError) as e:
            messagebox.showerror("Table", str(e))
            return
        self.etiquette.configure(text=os.path.basename(chemin))

    def retablir(self) -> None:
        if not self.table:
            messagebox.showinfo("Rétablir", "Choisissez d'abord la table de correspondance du texte envoyé.")
            return
        r = retablir(self.zone_reponse.get("1.0", "end-1c"), self.table)
        remplir(self.zone_retablie, r.texte)
        message = f"{sum(r.remplaces.values())} marqueur(s) remplacé(s)."
        if r.approches:
            message += f" Formes approchées remplacées, à vérifier : {', '.join(r.approches)}."
        if r.inconnus:
            message += f" Absents de la table, laissés tels quels : {', '.join(r.inconnus)}."
        self.etat.configure(text=message)

    def copier(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.zone_retablie.get("1.0", "end-1c"))


class Application:
    def __init__(self, racine: tk.Tk):
        racine.title(f"Pseudonymisation {__version__} — iavocat.be")
        racine.minsize(980, 680)
        onglets = ttk.Notebook(racine)
        onglets.pack(fill="both", expand=True)
        self.retablir = Retablir(onglets)
        self.pseudonymiser = Pseudonymiser(onglets, self)
        onglets.add(self.pseudonymiser, text="Pseudonymiser")
        onglets.add(self.retablir, text="Rétablir")


def main() -> int:
    racine = tk.Tk()
    Application(racine)
    racine.mainloop()
    return 0
