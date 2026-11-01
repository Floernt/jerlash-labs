"""Mode IA (0.2.0) : parties et rattachement proposés par un modèle de langue, avec la clé de l'avocat.

Déroulement (projets/P01-mode-ia-spec.md) :
1. les règles classent le dossier, sans rien envoyer (analyse.classer) ;
2. preparer_envoi : un seul texte pour tout le dossier, un numéro (P1, P2…) à la place de chaque nom de
   fichier, des extraits plafonnés, puis pseudonymisation par la copie embarquée de P09 ;
3. l'avocat relit et valide ce texte (écran d'envoi du connecteur, ou confirmation en ligne de commande) ;
4. completer : appel, lecture du JSON, rétablissement des noms à partir de la table (qui ne quitte
   jamais le poste), fusion avec les règles, puis alertes et synthèse (analyse.conclure).

Seuls les parties et le rattachement viennent du modèle ; le type, statut, date et document qui fait foi
restent calculés par les règles.
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field

from connecteur_ia import (Configuration, ErreurConfiguration, ErreurReponse, appeler, charger_configuration,
                           extraire_json, lire_cle)
from pseudonymisation.detection import detecter, preparer
from pseudonymisation.remplacement import pseudonymiser, retablir

from .analyse import Inventaire, conclure, debut, fin

CARACTERES_PAR_PIECE = 2000
CARACTERES_TOTAL = 80_000
LIGNES_EXTRAIT = 15
FICHIER_CONFIG = "config-ia.json"

CONSIGNE = """Tu aides un avocat à inventorier un dossier contractuel. Tu reçois des extraits des pièces du dossier, chacune identifiée par un numéro (P1, P2…). Les noms de personnes, de sociétés, les adresses et les identifiants ont été remplacés par des marqueurs comme [ORGANISATION_1] ou [PERSONNE_2] : recopie-les tels quels, sans les modifier ni chercher à les deviner.

Pour chaque pièce, indique :
1. "parties" : les parties à la pièce, écrites exactement comme dans le texte, forme sociale comprise (par exemple "[ORGANISATION_1] SRL"). Pour un contrat, un avenant ou des conditions générales : les sociétés ou personnes qui s'engagent. Pour un courrier ou un courriel : les sociétés de l'expéditeur et du destinataire. Ne compte pas les personnes qui signent au nom d'une société, ni les avocats, ni les sociétés seulement citées. Liste vide si aucune partie n'apparaît.
2. "rattache_a" : le numéro de la pièce à laquelle celle-ci se rapporte, ou null. Un projet se rapporte à la version signée du même acte ; des conditions générales, au contrat qui les vise ; un courrier ou un courriel, à l'acte dont il traite (contrat ou avenant). Le contrat signé principal ne se rapporte à rien. Une pièce ne se rapporte jamais à elle-même. Un modèle ou le précédent d'un autre dossier ne se rapporte à rien.
3. "justification" : une phrase courte qui cite l'indice retenu.

N'invente rien : en cas de doute, liste vide ou null.

Réponds uniquement par un objet JSON de cette forme, sans autre texte :
{"pieces": [{"piece": "P1", "parties": ["[ORGANISATION_1] SRL"], "rattache_a": null, "justification": "..."}]}"""


@dataclass
class Envoi:
    texte_clair: str            # avant pseudonymisation : ne quitte jamais le poste
    texte: str                  # pseudonymisé : proposé à l'avocat sur l'écran d'envoi
    table: dict                 # correspondances marqueur -> donnée d'origine : reste sur le poste
    numeros: dict[str, str]     # "P1" -> chemin de la pièce
    tronquees: list[str] = field(default_factory=list)

    @property
    def vide(self) -> bool:
        return not self.numeros


def charger_acces(dossier_outil: str, config: str | None = None) -> tuple[Configuration, str]:
    """Configuration du fournisseur et clé de l'avocat. Sans elles, l'outil ne fonctionne pas (ADR-019)."""
    chemin = config or os.path.join(dossier_outil, FICHIER_CONFIG)
    if not os.path.isfile(chemin):
        raise ErreurConfiguration(
            f"Aucune configuration IA ({chemin}). Copiez config-ia.example.json sous le nom {FICHIER_CONFIG}, "
            "choisissez votre fournisseur et votre modèle, puis placez votre clé API dans le fichier .env "
            "(voir le README).")
    configuration = charger_configuration(chemin)
    return configuration, lire_cle(configuration, os.path.dirname(os.path.abspath(chemin)))


def _extrait(texte: str) -> str:
    lignes = [l for l in texte.splitlines() if l.strip()]
    if len(lignes) <= 2 * LIGNES_EXTRAIT:
        return "\n".join(lignes)
    return f"{debut(texte, LIGNES_EXTRAIT)}\n[…]\n{fin(texte, LIGNES_EXTRAIT)}"


def preparer_envoi(inventaire: Inventaire) -> Envoi:
    """Texte unique pour tout le dossier, puis pseudonymisation locale (P09, une seule table)."""
    fiches = [f for f in inventaire.fiches if f.piece.texte is not None]
    plafond = min(CARACTERES_PAR_PIECE, CARACTERES_TOTAL // max(1, len(fiches)))
    blocs, numeros, tronquees = [], {}, []
    for rang, f in enumerate(fiches, start=1):
        numero = f"P{rang}"
        numeros[numero] = f.piece.chemin
        entete = [f"=== {numero} ===", f"Format : {f.piece.format}",
                  f"Selon les règles : type {f.type}, statut {f.statut}, date {f.date or 'inconnue'}"]
        if f.piece.courriel:
            c = f.piece.courriel
            entete += [f"De : {c.get('de', '')}", f"À : {c.get('a', '')}", f"Date : {c.get('date', '')}"]
        extrait = _extrait(f.piece.texte)
        if len(extrait) > plafond:
            extrait = extrait[:plafond] + "\n[… extrait tronqué]"
            tronquees.append(f.piece.chemin)
        blocs.append("\n".join(entete) + "\nExtrait :\n" + extrait)
    clair = preparer("\n\n".join(blocs))
    if not clair:
        return Envoi("", "", {"correspondances": []}, {}, [])
    resultat = pseudonymiser(clair, detecter(clair), source="inventaire-dossier")
    return Envoi(clair, resultat.texte, resultat.table, numeros, tronquees)


@dataclass
class Proposition:
    parties: list[str]
    rattache_a: str | None
    justification: str


def _retablir(valeur: str, table: dict) -> tuple[str, list[str]]:
    r = retablir(valeur, table)
    return " ".join(r.texte.split()), r.inconnus


def interpreter(reponse: str, table: dict, numeros: dict[str, str]) -> tuple[dict[str, Proposition], list[str]]:
    """Propositions du modèle par chemin de pièce, et liste de ce qui a été écarté (jamais deviné)."""
    donnees = extraire_json(reponse)
    elements = donnees.get("pieces") if isinstance(donnees, dict) else donnees
    if not isinstance(elements, list):
        raise ErreurReponse("Réponse du modèle sans liste de pièces.")
    propositions, rejets = {}, []
    for e in elements:
        numero = str(e.get("piece", "")).strip().upper() if isinstance(e, dict) else ""
        if numero not in numeros:
            rejets.append(f"pièce inconnue dans la réponse du modèle ({numero or 'sans numéro'}) : écartée")
            continue
        chemin = numeros[numero]
        parties = []
        for brute in e.get("parties") or []:
            if not isinstance(brute, str) or not brute.strip():
                continue
            nom, inconnus = _retablir(brute, table)
            if inconnus:
                rejets.append(f"{chemin} : partie « {brute} » écartée (marqueur inconnu {', '.join(inconnus)})")
            elif nom not in parties:
                parties.append(nom)
        cible = e.get("rattache_a")
        cible = str(cible).strip().upper() if cible not in (None, "", "null") else None
        if cible is not None and (cible not in numeros or cible == numero):
            rejets.append(f"{chemin} : rattachement proposé à « {cible} » écarté (pièce inconnue ou elle-même)")
            cible = None
        justification, _ = _retablir(str(e.get("justification") or ""), table)
        propositions[chemin] = Proposition(parties, numeros[cible] if cible else None, justification[:300])
    return propositions, rejets


def _norme(nom: str) -> str:
    return " ".join(nom.casefold().split())


def fusionner(inventaire: Inventaire, propositions: dict[str, Proposition]) -> None:
    """Règles et modèle d'accord : valeur confirmée. Seul le modèle propose : sa valeur, marquée.
    Désaccord : la valeur du modèle, marquée, et une alerte qui donne celle des règles.
    Le modèle ne propose rien là où les règles ont trouvé : la valeur des règles reste."""
    for f in inventaire.fiches:
        p = propositions.get(f.piece.chemin)
        if p is None or f.type == "non lu":
            continue
        motif = f" ({p.justification})" if p.justification else ""
        regles, modele = {_norme(x) for x in f.parties}, {_norme(x) for x in p.parties}
        if not modele:
            pass
        elif regles == modele:
            f.indices.append("parties : confirmées par le modèle")
        elif not regles:
            f.parties = list(p.parties)
            f.source["parties"] = "modèle"
            f.indices.append(f"parties : proposées par le modèle{motif}")
        else:
            ancien = ", ".join(f.parties)
            f.parties = list(p.parties)
            f.source["parties"] = "divergence"
            f.indices.append(f"parties : proposées par le modèle{motif}")
            f.alertes.append(f"parties à vérifier : le modèle propose {', '.join(p.parties)} ; les règles proposaient {ancien}")
        if p.rattache_a is None or p.rattache_a == f.rattache_a:
            if p.rattache_a:
                f.indices.append("rattachement : confirmé par le modèle")
            continue
        if f.rattache_a is None:
            f.source["rattache_a"] = "modèle"
        else:
            f.source["rattache_a"] = "divergence"
            f.alertes.append(f"rattachement à vérifier : le modèle propose {p.rattache_a} ; les règles proposaient {f.rattache_a}")
        f.rattache_a = p.rattache_a
        f.indices.append(f"rattachement : proposé par le modèle{motif}")


def completer(inventaire: Inventaire, envoi: Envoi, texte_valide: str, config: Configuration, cle: str) -> Inventaire:
    """Envoie le texte validé par l'avocat, fusionne la réponse, puis calcule alertes et synthèse."""
    rejets: list[str] = []
    infos = {"fournisseur": config.fournisseur, "modele": config.modele, "adresse": config.url,
             "envoye_le": datetime.datetime.now().isoformat(timespec="seconds"),
             "caracteres_envoyes": len(texte_valide), "pieces_tronquees": envoi.tronquees}
    if envoi.vide:
        infos["note"] = "aucune pièce lisible : rien n'a été envoyé"
    else:
        reponse = appeler(config, cle, CONSIGNE, texte_valide)
        propositions, rejets = interpreter(reponse.texte, envoi.table, envoi.numeros)
        fusionner(inventaire, propositions)
        infos.update({"modele_repondant": reponse.modele, "jetons_entree": reponse.jetons_entree,
                      "jetons_sortie": reponse.jetons_sortie, "cout_usd": reponse.cout_usd,
                      "pieces_sans_proposition": len(envoi.numeros) - len(propositions)})
    inventaire.ia = infos
    conclure(inventaire)
    inventaire.alertes += [f"réponse du modèle : {r}" for r in rejets]
    inventaire.alertes += [f"{c} : extrait tronqué avant l'envoi au modèle" for c in envoi.tronquees]
    return inventaire


def dossier_outil() -> str:
    """Racine de l'outil (là où se trouvent config-ia.json et .env), que l'outil soit lancé du dépôt ou de l'archive."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

