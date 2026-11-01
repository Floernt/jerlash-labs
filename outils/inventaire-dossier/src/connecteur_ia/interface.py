"""Écran d'envoi commun (ADR-019, point 4) : informations sur le fournisseur, texte modifiable, case à cocher."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .connecteur import Configuration, estimer, resume_envoi


def confirmer_envoi(parent: tk.Misc, config: Configuration, systeme: str, texte: str) -> str | None:
    """Affiche le texte qui va partir. Renvoie le texte relu (éventuellement corrigé), ou None si l'avocat annule."""
    fenetre = tk.Toplevel(parent)
    fenetre.title(f"Envoi à {config.fournisseur}")
    fenetre.transient(parent)
    fenetre.grab_set()
    resultat: dict[str, str | None] = {"texte": None}

    cadre = ttk.Frame(fenetre, padding=12)
    cadre.pack(fill="both", expand=True)
    infos = tk.StringVar()
    ttk.Label(cadre, textvariable=infos, justify="left", wraplength=720).pack(anchor="w")

    ttk.Label(cadre, text="Texte qui va partir (après pseudonymisation). Corrigez ce qui a échappé à la pseudonymisation :"
              ).pack(anchor="w", pady=(10, 2))
    zone = tk.Text(cadre, width=100, height=20, wrap="word")
    zone.insert("1.0", texte)
    zone.pack(fill="both", expand=True)

    def actualiser(_evenement=None):
        infos.set("\n".join(resume_envoi(config, estimer(config, systeme, zone.get("1.0", "end-1c")))))

    zone.bind("<KeyRelease>", actualiser)
    actualiser()

    accord = tk.BooleanVar(value=False)
    boutons = ttk.Frame(cadre)
    envoyer = ttk.Button(boutons, text="Envoyer", state="disabled")

    def basculer():
        envoyer.configure(state="normal" if accord.get() else "disabled")

    ttk.Checkbutton(cadre, variable=accord, command=basculer,
                    text=f"J'ai relu ce texte et j'accepte qu'il soit envoyé à {config.fournisseur}."
                    ).pack(anchor="w", pady=8)

    def valider():
        if accord.get():
            resultat["texte"] = zone.get("1.0", "end-1c")
            fenetre.destroy()

    envoyer.configure(command=valider)
    boutons.pack(anchor="e")
    ttk.Button(boutons, text="Annuler", command=fenetre.destroy).pack(side="right")
    envoyer.pack(side="right", padx=6)

    parent.wait_window(fenetre)
    return resultat["texte"]
