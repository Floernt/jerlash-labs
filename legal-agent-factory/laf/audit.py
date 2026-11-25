"""Journal d'audit sans contenu sensible.

Une ligne JSON par fait. Seuls des champs de la liste blanche sont écrits : jamais
le contenu d'un fichier, jamais son nom (seulement une empreinte du chemin),
jamais le texte d'une qualification ou d'un résultat.
"""

import json
import os
import threading

from .outils_fichiers import empreinte_texte, horodatage

CHAMPS = {"evenement_id", "type", "sha256", "version", "taille", "issue", "categorie",
          "triage_humain", "injection_suspectee", "sortie_modele_valide", "statut_runtime",
          "tours", "erreur",
          # Lot 2 : aucun de ces champs ne porte d'adresse, d'objet ni de texte
          "statut_routage", "skill", "rattache", "lien_rattachement", "motifs", "demandes_ignorees",
          "revue_conforme", "decision", "statut_decision"}


class Journal:
    def __init__(self, chemin: str):
        self.chemin = chemin
        self._verrou = threading.Lock()
        os.makedirs(os.path.dirname(chemin), exist_ok=True)

    def ecrire(self, chemin_document: str | None = None, **champs) -> None:
        inconnus = set(champs) - CHAMPS
        if inconnus:
            raise ValueError(f"champs d'audit non autorisés : {sorted(inconnus)}")
        ligne = {"horodatage": horodatage(), **champs}
        if chemin_document:
            ligne["chemin_empreinte"] = empreinte_texte(chemin_document, 16)
        with self._verrou, open(self.chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False, sort_keys=True) + "\n")
