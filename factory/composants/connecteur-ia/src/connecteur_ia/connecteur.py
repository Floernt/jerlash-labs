"""Appel d'un modèle de langue au format Chat Completions, avec la clé de l'utilisateur.

Un seul format pour tous les fournisseurs (ADR-020) : POST {adresse}/chat/completions,
clé en "Authorization: Bearer", réponse lue dans choices[0].message.content et usage.
La requête se limite à model, messages et max_tokens, ce que tous les préréglages acceptent.

Le connecteur ne pseudonymise pas : l'outil appelle P09 avant, puis l'écran d'envoi
(interface.confirmer_envoi) laisse l'avocat relire et corriger le texte (ADR-019, point 4).
"""

from __future__ import annotations

import json
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

CHEMIN_APPEL = "/chat/completions"
HOTES_LOCAUX = {"localhost", "127.0.0.1", "::1"}
CARACTERES_PAR_JETON = 4  # estimation grossière, présentée comme telle à l'utilisateur
PREREGLAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prereglages.json")
NOM_VARIABLE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
CHAMPS_INTERDITS = {"cle", "clé", "api_key", "apikey", "key", "token", "secret"}


class ErreurConnecteur(Exception):
    """Erreur présentable à l'utilisateur. Le message ne contient jamais la clé."""


class ErreurConfiguration(ErreurConnecteur):
    pass


class ErreurFournisseur(ErreurConnecteur):
    def __init__(self, message: str, statut: int | None = None):
        super().__init__(message)
        self.statut = statut


class ErreurReponse(ErreurConnecteur):
    pass


@dataclass(frozen=True)
class Informations:
    """Ce que le fournisseur déclare, tel que relevé dans docs/fournisseurs-ia.md. Rien n'est vérifié par l'outil."""

    lieu_traitement: str = "non renseigné"
    conservation: str = "non renseignée"
    zdr: str = "non renseigné"
    entrainement: str = "non renseigné"
    nationalite: str = "non renseignée"
    remarque: str = ""
    source: str = ""
    releve_le: str = ""


@dataclass(frozen=True)
class Configuration:
    fournisseur: str
    adresse: str
    modele: str
    variable_cle: str = ""
    cle_requise: bool = True
    entetes: dict = field(default_factory=dict)
    tarif_entree: float | None = None  # USD par million de jetons
    tarif_sortie: float | None = None
    tarifs_releves_le: str = ""
    max_jetons_sortie: int = 4000
    delai: float = 120.0
    informations: Informations = field(default_factory=Informations)

    @property
    def url(self) -> str:
        return self.adresse.rstrip("/") + CHEMIN_APPEL

    @property
    def locale(self) -> bool:
        return (urllib.parse.urlsplit(self.adresse).hostname or "") in HOTES_LOCAUX


@dataclass(frozen=True)
class Estimation:
    caracteres: int
    jetons_entree: int
    jetons_sortie_max: int
    cout_max_usd: float | None


@dataclass(frozen=True)
class Reponse:
    texte: str
    modele: str
    jetons_entree: int | None
    jetons_sortie: int | None
    cout_usd: float | None


def _prereglages() -> dict:
    with open(PREREGLAGES, encoding="utf-8") as f:
        return json.load(f)


def charger_configuration(source: str | dict) -> Configuration:
    """Lit une configuration (chemin d'un fichier JSON ou dictionnaire), complétée par un préréglage éventuel."""
    if isinstance(source, dict):
        brut = dict(source)
    else:
        try:
            with open(source, encoding="utf-8") as f:
                brut = json.load(f)
        except FileNotFoundError:
            raise ErreurConfiguration(f"Fichier de configuration introuvable : {source}") from None
        except json.JSONDecodeError as e:
            raise ErreurConfiguration(f"Fichier de configuration illisible (ligne {e.lineno}) : {source}") from None
    if not isinstance(brut, dict):
        raise ErreurConfiguration("La configuration doit être un objet JSON.")

    interdits = sorted(k for k in brut if k.lower() in CHAMPS_INTERDITS)
    if interdits:
        raise ErreurConfiguration(
            "La clé API ne se met pas dans la configuration (champ " + ", ".join(interdits) + "). "
            "Indiquez seulement le nom de la variable qui la contient (variable_cle).")

    nom = brut.pop("prereglage", None)
    if nom is not None:
        tous = _prereglages()
        if nom not in tous:
            raise ErreurConfiguration(f"Préréglage inconnu : {nom}. Disponibles : {', '.join(sorted(tous))}.")
        base = dict(tous[nom])
        base.pop("description", None)
        infos = {**base.pop("informations", {}), **brut.pop("informations", {})}
        brut = {**base, **brut, "informations": infos}

    infos = brut.pop("informations", {}) or {}
    connus = set(Configuration.__dataclass_fields__)
    inconnus = sorted(set(brut) - connus)
    if inconnus:
        raise ErreurConfiguration("Champ(s) de configuration inconnu(s) : " + ", ".join(inconnus))
    try:
        config = Configuration(**brut, informations=Informations(**infos))
    except TypeError as e:
        raise ErreurConfiguration(f"Configuration incomplète ou invalide : {e}") from None
    _valider(config)
    return config


def _valider(config: Configuration) -> None:
    if not config.fournisseur or not config.modele:
        raise ErreurConfiguration("La configuration doit indiquer le fournisseur et le modèle.")
    parties = urllib.parse.urlsplit(config.adresse)
    if parties.scheme not in ("https", "http") or not parties.hostname:
        raise ErreurConfiguration(f"Adresse invalide : {config.adresse}")
    if parties.scheme == "http" and not config.locale:
        raise ErreurConfiguration("Une adresse distante doit être en https : la clé et le texte partiraient en clair.")
    if config.cle_requise and not NOM_VARIABLE.match(config.variable_cle or ""):
        raise ErreurConfiguration("variable_cle doit être un nom de variable en majuscules, par exemple MISTRAL_API_KEY.")
    if config.max_jetons_sortie <= 0 or config.delai <= 0:
        raise ErreurConfiguration("max_jetons_sortie et delai doivent être positifs.")
    for nom, valeur in config.entetes.items():
        if nom.lower() == "authorization" or not isinstance(valeur, str):
            raise ErreurConfiguration(f"En-tête refusé dans la configuration : {nom}")


def _lire_env(chemin: str) -> dict:
    valeurs = {}
    try:
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne or ligne.startswith("#") or "=" not in ligne:
                    continue
                nom, _, valeur = ligne.partition("=")
                valeurs[nom.strip()] = valeur.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return valeurs


def lire_cle(config: Configuration, dossier_env: str | None = None) -> str:
    """Lit la clé dans l'environnement, sinon dans le fichier .env du dossier de l'outil."""
    if not config.cle_requise:
        return "local"  # un serveur local exige une valeur mais l'ignore
    cle = os.environ.get(config.variable_cle, "").strip()
    if not cle and dossier_env:
        cle = _lire_env(os.path.join(dossier_env, ".env")).get(config.variable_cle, "")
    if not cle:
        raise ErreurConfiguration(
            f"Aucune clé API trouvée. Cet outil ne fonctionne pas sans clé : définissez la variable "
            f"{config.variable_cle} ou ajoutez-la au fichier .env de l'outil (voir le guide « Obtenir une clé API »).")
    return cle


def estimer(config: Configuration, systeme: str, texte: str) -> Estimation:
    caracteres = len(systeme) + len(texte)
    jetons = -(-caracteres // CARACTERES_PAR_JETON)
    cout = None
    if config.tarif_entree is not None and config.tarif_sortie is not None:
        cout = (jetons * config.tarif_entree + config.max_jetons_sortie * config.tarif_sortie) / 1_000_000
    return Estimation(caracteres, jetons, config.max_jetons_sortie, cout)


def resume_envoi(config: Configuration, estimation: Estimation) -> list[str]:
    """Lignes de l'écran d'envoi (ADR-019, point 4)."""
    i = config.informations
    if config.locale:
        lieu = "sur cet ordinateur (modèle local)"
    else:
        lieu = i.lieu_traitement
    if estimation.cout_max_usd is None:
        cout = "non estimé (tarifs absents de la configuration)"
    else:
        cout = f"au plus {estimation.cout_max_usd:.4f} USD (tarifs relevés le {config.tarifs_releves_le or 'date inconnue'})"
    lignes = [
        f"Fournisseur : {config.fournisseur}",
        f"Adresse : {config.url}",
        f"Modèle : {config.modele}",
        f"Lieu de traitement déclaré : {lieu}",
        f"Conservation déclarée : {i.conservation}",
        f"Absence de conservation (ZDR) : {i.zdr}",
        f"Entraînement sur les données : {i.entrainement}",
        f"Nationalité du prestataire : {i.nationalite}",
        f"Taille : {estimation.caracteres} caractères, environ {estimation.jetons_entree} jetons "
        f"(estimation grossière), réponse limitée à {estimation.jetons_sortie_max} jetons",
        f"Coût estimé : {cout}",
    ]
    if i.remarque:
        lignes.append(f"Remarque : {i.remarque}")
    if i.source:
        lignes.append(f"Source des déclarations : {i.source}" + (f" (relevé du {i.releve_le})" if i.releve_le else ""))
    lignes.append("L'outil ne vérifie pas ces déclarations. Vous restez seul juge de ce que vous envoyez "
                  "et des garanties du fournisseur (lignes directrices AVOCATS.BE et OVB).")
    return lignes


def _masquer(message: str, cle: str) -> str:
    return message.replace(cle, "[clé masquée]") if cle and len(cle) > 3 else message


def _message_erreur(corps: bytes) -> str:
    try:
        donnees = json.loads(corps.decode("utf-8", "replace"))
        erreur = donnees.get("error") if isinstance(donnees, dict) else None
        message = erreur.get("message") if isinstance(erreur, dict) else (erreur or donnees.get("message"))
        return str(message)[:300] if message else ""
    except (ValueError, AttributeError):
        return ""


def appeler(config: Configuration, cle: str, systeme: str, texte: str) -> Reponse:
    """Envoie la consigne et le texte au modèle configuré et renvoie sa réponse."""
    corps = json.dumps({
        "model": config.modele,
        "messages": [{"role": "system", "content": systeme}, {"role": "user", "content": texte}],
        "max_tokens": config.max_jetons_sortie,
    }).encode("utf-8")
    entetes = {"Content-Type": "application/json", "Authorization": f"Bearer {cle}", **config.entetes}
    requete = urllib.request.Request(config.url, data=corps, headers=entetes, method="POST")
    # Un modèle local ne doit pas passer par un proxy ; un fournisseur distant suit les réglages du poste.
    ouvreur = urllib.request.build_opener(urllib.request.ProxyHandler({})) if config.locale \
        else urllib.request.build_opener()
    try:
        with ouvreur.open(requete, timeout=config.delai) as r:
            brut = r.read()
    except urllib.error.HTTPError as e:
        detail = _masquer(_message_erreur(e.read()), cle)
        if e.code in (401, 403):
            message = "Clé API refusée par le fournisseur (clé invalide, expirée ou sans accès à ce modèle)."
        elif e.code == 429:
            message = "Limite atteinte chez le fournisseur (débit ou plafond de dépense). Réessayez plus tard."
        elif e.code >= 500:
            message = f"Le fournisseur ne répond pas correctement (erreur {e.code}). Réessayez plus tard."
        else:
            message = f"Requête refusée par le fournisseur (erreur {e.code})."
        raise ErreurFournisseur(message + (f" Détail : {detail}" if detail else ""), e.code) from None
    except (socket.timeout, TimeoutError):
        raise ErreurFournisseur(f"Pas de réponse du fournisseur après {config.delai:.0f} secondes.") from None
    except urllib.error.URLError as e:
        raise ErreurFournisseur(f"Connexion impossible à {config.url} ({_masquer(str(e.reason), cle)}).") from None

    try:
        donnees = json.loads(brut.decode("utf-8"))
        contenu = donnees["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise ErreurReponse("Réponse du fournisseur illisible (format inattendu).") from None
    if not isinstance(contenu, str):
        raise ErreurReponse("Réponse du fournisseur sans texte.")
    usage = donnees.get("usage") or {}
    entree, sortie = usage.get("prompt_tokens"), usage.get("completion_tokens")
    cout = None
    if isinstance(entree, int) and isinstance(sortie, int) \
            and config.tarif_entree is not None and config.tarif_sortie is not None:
        cout = (entree * config.tarif_entree + sortie * config.tarif_sortie) / 1_000_000
    return Reponse(contenu, str(donnees.get("model") or config.modele), entree, sortie, cout)


def extraire_json(texte: str):
    """Extrait l'objet ou le tableau JSON d'une réponse, même entouré de texte ou d'un bloc de code."""
    decodeur = json.JSONDecoder()
    for i, c in enumerate(texte):
        if c in "{[":
            try:
                valeur, _ = decodeur.raw_decode(texte, i)
                return valeur
            except ValueError:
                continue
    raise ErreurReponse("La réponse du modèle ne contient pas de JSON lisible ; relancez ou changez de modèle.")
