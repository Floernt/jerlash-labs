"""Connecteur IA commun aux outils iavocat.be : un seul format d'appel, la clé de l'utilisateur (ADR-019, ADR-020)."""

__version__ = "0.1.0"

from .connecteur import (  # noqa: E402,F401
    Configuration,
    ErreurConfiguration,
    ErreurConnecteur,
    ErreurFournisseur,
    ErreurReponse,
    Estimation,
    Informations,
    Reponse,
    appeler,
    charger_configuration,
    estimer,
    extraire_json,
    lire_cle,
    resume_envoi,
)
