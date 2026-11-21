"""Charge utile de création de tâche Paperclip, en simulation (« dry run »).

Rien n'est envoyé : la charge utile est seulement écrite dans le répertoire de
sortie. Les noms de champs de l'API Paperclip ne sont pas repris ici faute de
documentation consultée ; le format ci-dessous est interne et provisoire.
"""

FORMAT = "laf-tache-paperclip/0.1"
NOTE_FORMAT = "[À VÉRIFIER] correspondance avec les champs de l'API Paperclip de création de tâche"


def charge_utile(evenement: dict, qualification: dict) -> dict:
    q = qualification["qualification"]
    nom = evenement["chemin"].rsplit("/", 1)[-1]
    return {
        "format": FORMAT,
        "note_format": NOTE_FORMAT,
        "dry_run": True,
        "cle_idempotence": evenement["id"],
        "titre": f"[laf] {evenement['type']} : {nom} (version {evenement['version']})",
        "description": "Document déposé dans le dossier surveillé. Qualification simulée (Lot 1) : "
                       "aucune analyse réelle, aucune action autorisée.",
        "etiquettes": ["laf:lot-1", f"categorie:{q['categorie']}"]
                      + (["triage-humain"] if q["requires_human_triage"] else []),
        "triage_humain_requis": q["requires_human_triage"],
        "source": {"evenement_id": evenement["id"], "type": evenement["type"],
                   "chemin": evenement["chemin"], "sha256": evenement["sha256"],
                   "version": evenement["version"], "horodatage": evenement["horodatage"]},
    }
