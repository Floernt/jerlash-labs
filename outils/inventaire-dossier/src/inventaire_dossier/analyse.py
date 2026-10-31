"""Classement des pièces par règles (mode local, sans IA).

Pour chaque pièce : type, statut, date, parties, rattachement, document qui fait foi. Chaque conclusion
garde l'indice qui l'a produite, pour que l'avocat puisse la vérifier. Quand aucun indice ne suffit,
la valeur est « à vérifier » : l'outil ne comble pas les vides.
"""

from __future__ import annotations

import datetime
import os
import re
from collections import Counter
from dataclasses import dataclass, field

from .lecture import Piece

MOIS = {"janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
        "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12}
ESP = "[   ]"
DATE_LONGUE = rf"(\d{{1,2}})(?:er)?{ESP}+({'|'.join(MOIS)}){ESP}+(\d{{4}})"
DATE_COURTE = r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})"
RE_DATE = re.compile(f"{DATE_LONGUE}|{DATE_COURTE}", re.I)
RE_DATE_NOM = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
FORMES = "SRL|SPRL|SA|SC|SCRL|SNC|SCS|ASBL|BV|NV|CV|VZW|SAS|SARL|GmbH"
MOT_NOM = r"[A-ZÀ-Ý][\w'’-]*"
LIAISON = r"(?:de la|de l'|du|des|de|d'|et|&)"
RE_SOCIETE = re.compile(rf"(?<![\w-])({MOT_NOM}(?:{ESP}+(?:{LIAISON}{ESP}*)?{MOT_NOM}){{0,4}}){ESP}+({FORMES})(?![\w-])")
MOTS_EXCLUS_DEBUT = {"la", "le", "les", "pour", "par", "entre", "et", "ou", "société", "concerne", "avec", "chez"}

TYPES = ["contrat", "avenant", "conditions générales", "courrier", "courriel", "note interne", "modèle",
         "précédent", "autre", "non lu"]
ACTES = ("contrat", "avenant", "précédent")


@dataclass
class Fiche:
    piece: Piece
    type: str = "autre"
    statut: str = "à vérifier"
    date: str | None = None
    parties: list[str] = field(default_factory=list)
    rattache_a: str | None = None
    fait_foi: bool | None = False
    indices: list[str] = field(default_factory=list)
    alertes: list[str] = field(default_factory=list)
    signe_par_le_texte: bool = False


@dataclass
class Inventaire:
    dossier: str
    fiches: list[Fiche]
    ignores: list[str]
    contrat_principal: str | None = None
    etat: str = ""
    alertes: list[str] = field(default_factory=list)


def iso(jour: int, mois: int, annee: int) -> str | None:
    """Date AAAA-MM-JJ, ou None si elle n'existe pas (31 février, mois 13…)."""
    try:
        return datetime.date(annee, mois, jour).isoformat()
    except ValueError:
        return None


def date_depuis(m: re.Match) -> str | None:
    if m.group(1):
        return iso(int(m.group(1)), MOIS[m.group(2).lower()], int(m.group(3)))
    return iso(int(m.group(4)), int(m.group(5)), int(m.group(6)))


def debut(texte: str, lignes: int = 4) -> str:
    return "\n".join([l for l in texte.splitlines() if l.strip()][:lignes])


RE_HORS_INTITULE = re.compile(
    r"[ \t]*(?:[-•*][ \t]|(?:Concerne|Objet|N/R[ée]f|V/R[ée]f|R[ée]f)[ \t.]*:|[^\n,]{1,60},[ \t]+le[ \t]+\d)", re.I)


def intitule(texte: str) -> str:
    """Les deux premières lignes qui ne sont ni des puces, ni une ligne « Concerne », ni « lieu, le date » :
    là où figure l'intitulé d'un acte (« PROJET » puis « AVENANT N° 2… », par exemple)."""
    lignes = [l for l in texte.splitlines() if l.strip() and not RE_HORS_INTITULE.match(l)]
    return "\n".join(lignes[:2])


def fin(texte: str, lignes: int = 15) -> str:
    return "\n".join([l for l in texte.splitlines() if l.strip()][-lignes:])


# « signé » comme participe, sauf précédé d'une négation ou de « à » (« NON signé », « à signer », « pas signé »).
RE_SIGNE_NOM = re.compile(r"(?<!non[ _-])(?<!non)(?<!pas[ _-])\bsign(?:é|ée|és|ées|ed)\b", re.I)


# --- Règles par pièce ---------------------------------------------------------------------------

def classer_type(f: Fiche) -> None:
    p, nom = f.piece, f.piece.nom.lower()
    if p.texte is None:
        f.type, f.statut, f.fait_foi = "non lu", "inconnu", None
        f.indices.append(f"non lu : {p.non_lu}")
        return
    tete = intitule(p.texte).upper()
    regles = [
        (p.format == ".eml", "courriel", "fichier de courriel"),
        (bool(re.search(r"\bmod[eè]le\b", nom)) or "MODÈLE" in tete or "MODELE" in tete
         or len(re.findall(r"\[(?:●|NOM|ADRESSE|DATE)", p.texte)) >= 2, "modèle",
         "nom ou en-tête « modèle », ou champs à compléter [●]"),
        (bool(re.search(r"\bpr[ée]c[ée]dent\b", nom)), "précédent", "nom du fichier « précédent »"),
        ("CONDITIONS GÉNÉRALES" in tete or "CONDITIONS GENERALES" in tete or nom.startswith("cg "),
         "conditions générales", "intitulé « conditions générales »"),
        # Le courrier passe avant les actes : sa ligne « Concerne » cite souvent un contrat.
        (bool(re.search(r"^[ \t]*(Concerne|Objet)[ \t]*:", p.texte, re.M | re.I))
         and bool(re.search(r"^(Madame|Monsieur|Maître|Cher|Chère)", p.texte, re.M)), "courrier",
         "« Concerne » et formule d'appel"),
        ("AVENANT" in tete, "avenant", "intitulé « avenant »"),
        (bool(re.search(r"\b(CONTRAT|CONVENTION|ACCORD|PACTE)\b", tete)), "contrat", "intitulé de contrat"),
        (bool(re.search(r"\bnotes?\b|\bcompte[- ]rendu\b|\bpv\b", nom)), "note interne", "nom du fichier « notes »"),
    ]
    for condition, type_, indice in regles:
        if condition:
            f.type = type_
            f.indices.append(f"type : {indice}")
            return
    f.indices.append("type : aucun indice suffisant")


def classer_statut(f: Fiche) -> None:
    p, nom = f.piece, f.piece.nom.lower()
    if f.type not in ACTES + ("courrier",):
        if f.type != "non lu":
            f.statut = "sans objet"
        return
    texte = p.texte or ""
    projet = [indice for condition, indice in (
        (bool(re.search(r"\b(projet|draft|brouillon)\b", nom)), "nom du fichier « projet »"),
        (bool(re.search(r"\bPROJET\b", debut(texte, 3))), "mention « PROJET » en tête"),
        ("NE PAS SIGNER" in texte.upper(), "mention « ne pas signer »"),
        (bool(re.search(r"soumis\w*\s+à\s+(?:la\s+)?signature", texte, re.I)), "mention « soumis à la signature »"),
        (bool(re.search(r"\.{8,}", texte)), "blancs de signature non remplis"),
        (bool(re.search(r"\[Commentaire", texte)), "commentaires de négociation dans le texte"),
    ) if condition]
    # « (signé) » dans les dernières lignes, là où figurent les signatures. Une citation (« l'avenant 1 (signé)
    # reste applicable ») dans un acte court y tombe aussi : l'indice de projet « soumis à la signature » l'emporte.
    par_le_texte = bool(re.search(r"\(sign[ée]e?\)", fin(texte)))
    signe = [indice for condition, indice in (
        (bool(RE_SIGNE_NOM.search(nom)), "nom du fichier « signé »"),
        (par_le_texte, "mention « (signé) » dans les dernières lignes"),
    ) if condition]
    if projet:
        f.statut = "projet"
        f.indices.append("statut : " + ", ".join(projet))
    elif signe:
        f.statut = "signé"
        f.signe_par_le_texte = par_le_texte
        f.indices.append("statut : " + ", ".join(signe)
                         + ("" if par_le_texte else " (seul indice : le nom du fichier ; fait foi à vérifier)"))
    else:
        f.indices.append("statut : ni mention de signature, ni marque de projet")


def classer_date(f: Fiche) -> None:
    p = f.piece
    if p.texte is None:
        return
    texte = p.texte
    if p.courriel.get("date"):
        # L'en-tête du courriel prime : son texte cite souvent la date d'autres documents.
        f.date = p.courriel["date"]
        f.indices.append("date : en-tête du courriel")
        return
    candidats = [
        (RE_DATE_NOM.search(p.nom), "date dans le nom du fichier", lambda m: iso(int(m.group(3)), int(m.group(2)), int(m.group(1)))),
        (re.search(rf"Fait[ \t]+à[ \t]+[^,\n]{{1,80}},[ \t]+le[ \t]+(?:{DATE_LONGUE}|{DATE_COURTE})", texte, re.I), "« Fait à …, le … »", date_depuis),
        (re.search(rf"^[A-ZÀ-Ý][\w' -]{{0,60}},[ \t]+le[ \t]+(?:{DATE_LONGUE}|{DATE_COURTE})", texte, re.M | re.I), "lieu et date du courrier", date_depuis),
        (re.search(rf"[Vv]ersion[ \t]+du[ \t]+(?:{DATE_LONGUE}|{DATE_COURTE})", texte, re.I), "« version du … »", date_depuis),
    ]
    for m, indice, conversion in candidats:
        if m and conversion(m):
            f.date = conversion(m)
            f.indices.append(f"date : {indice}")
            return
        if m:
            f.indices.append(f"date : {indice} impossible ({m.group(0)[-20:]}), ignorée")
    premiere = RE_DATE.search(debut(texte, 1))
    if premiere:
        f.date = date_depuis(premiere)
        f.indices.append("date : première ligne")


def classer_parties(f: Fiche) -> None:
    if f.piece.texte is None or f.type == "modèle":
        return
    vues = []
    for m in RE_SOCIETE.finditer(f.piece.texte):
        mots = m.group(1).split()
        while mots and mots[0].lower() in MOTS_EXCLUS_DEBUT:
            mots.pop(0)
        if not mots:
            continue
        nom = f"{' '.join(mots)} {m.group(2)}"
        if nom not in vues:
            vues.append(nom)
    f.parties = vues


def mots_significatifs(nom: str) -> set[str]:
    formes = {x.lower() for x in FORMES.split("|")}
    return {m for m in re.findall(r"\w+", nom.lower()) if len(m) >= 4 and m not in formes}


def parties_des_courriels(fiches: list[Fiche]) -> None:
    """Complète les parties d'un courriel par le domaine des adresses : « marc@brasserie-condroz.example »
    désigne « Brasserie du Condroz SRL » si cette société figure ailleurs dans le dossier."""
    connues = {p for f in fiches for p in f.parties}
    for f in fiches:
        if f.type != "courriel":
            continue
        adresses = f"{f.piece.courriel.get('de', '')} {f.piece.courriel.get('a', '')}".lower()
        domaines = [set(re.findall(r"[a-z0-9]+", d)) for d in re.findall(r"@([\w.-]+)", adresses)]
        for partie in sorted(connues - set(f.parties)):
            mots = mots_significatifs(partie)
            if len(mots) >= 2 and any(mots <= d for d in domaines):
                f.parties.append(partie)
                f.indices.append(f"parties : {partie} reconnue par le domaine d'une adresse")


# --- Règles sur le dossier ----------------------------------------------------------------------

RE_REF_CONTRAT = re.compile(rf"contrat[\w\s'’-]{{0,60}}?\bdu\s+(?:{DATE_LONGUE}|{DATE_COURTE})", re.I)
RE_REF_AVENANT = re.compile(r"avenant\s+(?:n[°o]\s*)?(\d+)", re.I)


def numero_avenant(f: Fiche) -> str | None:
    m = RE_REF_AVENANT.search(debut(f.piece.texte or "", 3)) or RE_REF_AVENANT.search(f.piece.nom)
    return m.group(1) if m else None


def rattacher(fiches: list[Fiche]) -> None:
    dates = Counter(f.date for f in fiches if f.type == "contrat" and f.statut == "signé" and f.date)
    # Deux contrats signés le même jour : une référence à cette date est ambiguë, aucun rattachement par date.
    contrats_signes = {f.date: f for f in fiches if f.type == "contrat" and f.statut == "signé" and f.date
                       and dates[f.date] == 1}
    avenants = {numero_avenant(f): f for f in fiches if f.type == "avenant" and numero_avenant(f)}
    for f in fiches:
        texte = f.piece.texte or ""
        if f.type in ("modèle", "précédent", "note interne", "non lu") or (f.type == "contrat" and f.statut == "signé"):
            continue
        ref = RE_REF_CONTRAT.search(texte)
        cible = contrats_signes.get(date_depuis(_groupes_date(ref))) if ref else None
        if cible is not None and cible is not f:
            f.rattache_a = cible.piece.chemin
            f.indices.append(f"rattachement : référence au contrat du {cible.date}")
            continue
        m = RE_REF_AVENANT.search(texte)
        if m and m.group(1) in avenants and avenants[m.group(1)] is not f and f.type in ("courriel", "courrier"):
            f.rattache_a = avenants[m.group(1)].piece.chemin
            f.indices.append(f"rattachement : mention de l'avenant n° {m.group(1)}")
            continue
        if f.type in ("contrat", "conditions générales"):
            proche = [c for c in contrats_signes.values() if set(f.parties) & set(c.parties) and c is not f]
            if f.type == "conditions générales":
                proche = [c for c in proche if re.search(r"conditions générales", c.piece.texte or "", re.I)]
            if len(proche) == 1:
                f.rattache_a = proche[0].piece.chemin
                f.indices.append("rattachement : mêmes parties que le contrat signé" +
                                 (" qui mentionne les conditions générales" if f.type == "conditions générales" else ""))


def _groupes_date(m: re.Match) -> re.Match:
    """Rend un match de RE_REF_CONTRAT utilisable par date_depuis (mêmes groupes 1 à 6)."""
    return RE_DATE.search(m.group(0)[m.group(0).lower().rfind("du ") + 3:])


def fait_foi(f: Fiche) -> None:
    if f.type == "non lu":
        f.fait_foi = None
    elif f.type in ("contrat", "avenant", "courrier") and f.statut == "signé":
        # Signé d'après le seul nom du fichier : indice trop faible pour affirmer que la pièce fait foi.
        f.fait_foi = True if f.signe_par_le_texte else None
    else:
        f.fait_foi = False


def alerter(inventaire: Inventaire) -> None:
    fiches = inventaire.fiches
    frequence = Counter(p for f in fiches for p in set(f.parties))
    communes = {p for p, n in frequence.items() if n >= 2}
    for f in fiches:
        if f.type == "non lu":
            f.alertes.append(f"non lu ({f.piece.non_lu}) : à examiner à la main")
        if f.type in ("contrat", "avenant") and f.statut == "projet":
            f.alertes.append(f"{f.type} non signé")
        if f.parties and not set(f.parties) & communes and f.type != "modèle":
            f.alertes.append("aucune partie commune avec le reste du dossier : pièce d'un autre dossier ou d'un autre client ?")
        if f.type == "précédent":
            f.alertes.append("précédent d'un autre dossier : vérifier qu'il peut figurer dans ce dossier")
        if f.statut == "à vérifier":
            f.alertes.append("statut à vérifier : aucune mention de signature ni marque de projet")
        if f.statut == "signé" and f.fait_foi is None and f.type != "non lu":
            f.alertes.append("signé selon le nom du fichier seulement : vérifier la signature")
        if f.piece.tronque:
            f.alertes.append("texte très long : seuls les 2 premiers millions de caractères ont été examinés")
        jointes = f.piece.courriel.get("pieces_jointes") or []
        if jointes:
            f.alertes.append(f"{len(jointes)} pièce(s) jointe(s) non inventoriée(s) : {', '.join(jointes)}")
    preuves = [f for f in fiches if re.search(r"accusé de réception|preuve de dépôt|récépissé|bpost",
                                               f"{f.piece.nom} {debut(f.piece.texte or '', 3)}", re.I)]
    for f in fiches:
        if f.type == "courrier" and re.search(r"recommand", f.piece.texte or "", re.I) and not preuves:
            f.alertes.append("envoi recommandé annoncé : preuve de dépôt ou accusé de réception absente du dossier")
    empreintes = Counter(f.piece.sha256 for f in fiches if f.piece.sha256)
    for f in fiches:
        if empreintes[f.piece.sha256] > 1:
            f.alertes.append("fichier identique à une autre pièce (même empreinte)")
    for f in fiches:
        inventaire.alertes += [f"{f.piece.chemin} : {a}" for a in f.alertes]
    if inventaire.ignores:
        inventaire.alertes.append(f"{len(inventaire.ignores)} élément(s) non inventorié(s) : {', '.join(inventaire.ignores)}")
    if not fiches:
        inventaire.alertes.append("aucune pièce dans ce dossier : vérifiez le dossier choisi")


# Formules par lesquelles l'auteur du courrier résilie lui-même ; une négation dans la phrase les écarte.
RE_RESILIATION = re.compile(r"\b(?:nous\s+)?(?:vous\s+)?(?:notifions|notifie)\b[^.;]{0,120}\b(?:résiliation|mettre fin|résilier)"
                            r"|\b(?:nous\s+résilions|je\s+résilie|mettons\s+fin|met\s+fin\s+au|résilie\s+par\s+la\s+présente)", re.I)
RE_NEGATION = re.compile(r"\bn['’]\w+\s+pas\b|\bne\s+\w+\s+pas\b|\bconteste|\brefus|\bn['’]entend", re.I)


def synthese(inventaire: Inventaire) -> None:
    signes = [f for f in inventaire.fiches if f.type == "contrat" and f.statut == "signé"]
    if not signes:
        inventaire.etat = "aucun contrat signé identifié"
        return
    principal = max(signes, key=lambda c: sum(f.rattache_a == c.piece.chemin for f in inventaire.fiches))
    inventaire.contrat_principal = principal.piece.chemin
    inventaire.etat = f"contrat signé le {principal.date}" if principal.date else "contrat signé (date à vérifier)"
    for f in inventaire.fiches:
        texte = f.piece.texte or ""
        if f.rattache_a != principal.piece.chemin or f.type != "courrier" or not re.search(r"résili|mettre fin|met fin", texte, re.I):
            continue
        phrases = re.split(r"(?<=[.;!?])\s+", texte)
        positives = [p for p in phrases if RE_RESILIATION.search(p) and not RE_NEGATION.search(p)]
        if positives and f.statut == "signé":
            echeance = re.search(rf"(?:expirera|prendra fin|expire)[\w ]{{0,20}}?[ \t]+le[ \t]+(?:{DATE_LONGUE}|{DATE_COURTE})", texte, re.I)
            date_fin = date_depuis(RE_DATE.search(echeance.group(0))) if echeance else None
            inventaire.etat = (f"résiliation notifiée par courrier du {f.date or '(date à vérifier)'}"
                               + (f", fin le {date_fin}" if date_fin else ", date de fin à vérifier")
                               + " (d'après le texte du courrier : à vérifier)")
        else:
            inventaire.etat += f" ; un courrier ({f.piece.chemin}) mentionne une résiliation : à vérifier"


def inventorier(dossier: str, pieces: list[Piece], ignores: list[str]) -> Inventaire:
    fiches = [Fiche(p) for p in pieces]
    for f in fiches:
        classer_type(f)
        classer_statut(f)
        classer_date(f)
        classer_parties(f)
    parties_des_courriels(fiches)
    rattacher(fiches)
    for f in fiches:
        fait_foi(f)
    inventaire = Inventaire(os.path.abspath(dossier), fiches, ignores)
    alerter(inventaire)
    synthese(inventaire)
    return inventaire
