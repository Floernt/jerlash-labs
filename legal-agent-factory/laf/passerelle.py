"""Passerelle de modèle : interface de forme « chat completions » compatible OpenAI.

Lot 1 : seule l'implémentation simulée (réponses déterministes) est utilisable.
Les adaptateurs Scaleway et Umans sont des squelettes : ils ne contiennent ni
adresse, ni nom de modèle, ni code réseau, et lèvent une erreur s'ils sont appelés.
Leur branchement relève d'un lot ultérieur, après décision de Florian, en suivant
la documentation officielle à jour du fournisseur (CLAUDE.md, règle 2).
"""

import hashlib
import json

MARQUEUR_QUALIFICATION = "TACHE=QUALIFICATION"


class Passerelle:
    """Interface commune. `messages` suit le format OpenAI : [{"role", "content"}]."""

    nom = "abstraite"

    def chat_completions(self, model: str, messages: list[dict], **options) -> dict:
        raise NotImplementedError


def _reponse(model: str, messages: list[dict], contenu: str | None, tool_calls=None) -> dict:
    """Construit une réponse au format OpenAI, identifiant déterministe."""
    graine = hashlib.sha256(json.dumps([model, messages], sort_keys=True).encode("utf-8")).hexdigest()
    message = {"role": "assistant", "content": contenu}
    if tool_calls:
        message["tool_calls"] = tool_calls
    return {
        "id": "simcmpl-" + graine[:24],
        "object": "chat.completion",
        "model": model,
        "choices": [{"index": 0, "message": message,
                     "finish_reason": "tool_calls" if tool_calls else "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


class PasserelleSimulee(Passerelle):
    """Modèle simulé : mêmes messages, même réponse. N'analyse rien.

    `repondre` permet aux tests de substituer une logique (modèle qui « obéit »
    à une injection, modèle qui demande des outils en boucle, etc.).
    """

    nom = "simulee"

    def __init__(self, repondre=None):
        self.repondre = repondre or self._par_defaut
        self.appels = 0

    def chat_completions(self, model: str, messages: list[dict], **options) -> dict:
        self.appels += 1
        resultat = self.repondre(model, messages)
        if isinstance(resultat, dict):
            return _reponse(model, messages, resultat.get("content"), resultat.get("tool_calls"))
        return _reponse(model, messages, resultat)

    @staticmethod
    def _par_defaut(model: str, messages: list[dict]) -> str:
        systeme = messages[0]["content"] if messages else ""
        if MARQUEUR_QUALIFICATION in systeme:
            return json.dumps({
                "schema_version": "laf-qualification/0.1",
                "categorie": "a_trier",
                "requires_human_triage": True,
                "confiance": 0.0,
                "motifs": ["simulation"],
            })
        return "Résultat simulé : aucune analyse réelle n'a été effectuée (Lot 1)."


class PasserelleEnregistree(PasserelleSimulee):
    """Modèle simulé à réponses enregistrées (Lot 2), pour les tests et la démonstration.

    Une réponse est choisie par une clé exacte, sans lire ni interpréter le texte :
    - routage : empreinte du message utilisateur encadré (voir `cle_routage`) ;
    - skill : nom du skill, repris du marqueur SKILL= des instructions.
    Hors de ces clés, comportement de PasserelleSimulee. Les réponses enregistrées
    sont des données de test du routage, pas des réponses de référence juridiques.
    """

    nom = "enregistree"

    def __init__(self, routages: dict | None = None, sorties_skills: dict | None = None):
        super().__init__(self._choisir)
        self.routages = routages or {}
        self.sorties_skills = sorties_skills or {}

    def _choisir(self, model, messages):
        systeme = messages[0]["content"] if messages else ""
        if systeme.startswith("TACHE=ROUTAGE"):
            cle = cle_routage(messages[1]["content"])
            if cle in self.routages:
                return json.dumps(self.routages[cle])
        if systeme.startswith("SKILL="):
            nom = systeme.split("\n", 1)[0][len("SKILL="):]
            if nom in self.sorties_skills:
                return json.dumps(self.sorties_skills[nom])
        return PasserelleSimulee._par_defaut(model, messages)


def cle_routage(message_utilisateur: str) -> str:
    return hashlib.sha256(message_utilisateur.encode("utf-8")).hexdigest()[:32]


class _Squelette(Passerelle):
    """Adaptateur non branché. Aucun appel n'est possible dans le Lot 1."""

    def __init__(self, *args, **kwargs):
        pass

    def chat_completions(self, model: str, messages: list[dict], **options) -> dict:
        raise NotImplementedError(
            f"Adaptateur {self.nom} non branché (Lot 1 : aucun appel réel). "
            "Adresse, modèle et en-têtes [À VÉRIFIER] dans la documentation officielle du fournisseur.")


class PasserelleScaleway(_Squelette):
    """Squelette. Variables prévues : voir env.example (SCALEWAY_*)."""

    nom = "scaleway"


class PasserelleUmans(_Squelette):
    """Squelette. Variables prévues : voir env.example (UMANS_*)."""

    nom = "umans"


def contenu(reponse: dict) -> str | None:
    return reponse["choices"][0]["message"].get("content")


def appels_outils(reponse: dict) -> list:
    return reponse["choices"][0]["message"].get("tool_calls") or []
