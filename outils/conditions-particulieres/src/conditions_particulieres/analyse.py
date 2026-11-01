"""Préparation de la séparation d'un contrat en conditions particulières et conditions générales.

Par règles, sans IA. Le contrat est découpé en blocs (comparution, chaque article, signatures). Dans chaque
bloc, intitulé compris, l'outil repère les données propres à l'opération : parties et personnes, adresses,
identifiants (numéro d'entreprise, IBAN, courriel, téléphone, référence), montants, dates, quantités.
Il propose ensuite un classement :
- conditions particulières : bloc dont l'objet est propre à l'opération (comparution, objet, prix, durée,
  coordonnées…), ou dont la plupart des paragraphes contiennent de telles données ;
- conditions générales : bloc de nature générale sans aucune donnée propre à l'opération ;
- clause mixte : clause de nature générale qui contient une donnée propre à l'opération, à extraire avant
  de réutiliser la clause.
Les délais génériques, taux légaux, dates des textes de loi et numéros d'articles ne sont pas des données
propres. L'erreur à éviter en priorité est de présenter comme réutilisable une clause qui contient encore
une donnée de l'opération : dans le doute, les règles signalent.
"""

from __future__ import annotations

import functools
import re
from dataclasses import dataclass, field

from .lecture import Document

MAJ = "A-ZÀ-ÖØ-ÞŒ"
LETTRE = "A-Za-zÀ-ÖØ-öø-ÿŒœ"
BORD_G = rf"(?<![{LETTRE}0-9-])"
BORD_D = rf"(?![{LETTRE}0-9-])"
MOT_MAJ = rf"[{MAJ}][{LETTRE}0-9'-]{{0,40}}"
CATEGORIES = ["PARTIE", "ADRESSE", "IDENTIFIANT", "MONTANT", "DATE", "QUANTITE"]
LIBELLES = {"PARTIE": "partie ou personne", "ADRESSE": "adresse", "IDENTIFIANT": "identifiant", "MONTANT": "montant",
            "DATE": "date", "QUANTITE": "quantité"}
# Longueur analysée par paragraphe : un article réel en compte bien moins ; au-delà, le temps de calcul
# d'un texte hostile n'est plus borné.
LONGUEUR_MAX = 20000

# --- Données -------------------------------------------------------------------------------------

FORMES = (r"(?:SRL|SA|SC|SNC|SCS|SComm|ASBL|AISBL|BV|NV|BVBA|SPRL|SPRLU|SCRL|SAS|SARL|GmbH|Ltd|LLC|Inc|AG|SE|"
          r"S\.R\.L\.?|S\.A\.|S\.C\.|S\.P\.R\.L\.?|(?i:srl|sprl|scrl|asbl|bvba|s\.r\.l\.?|s\.a\.|s\.p\.r\.l\.?))")
RE_SOCIETE = re.compile(rf"{BORD_G}(?:{MOT_MAJ}[&.]?\s+(?:(?:de|du|des|la|le|et|&)\s+|d'|l')?){{1,6}}{FORMES}{BORD_D}")
# Mots qui précèdent souvent le nom dans la comparution et n'en font pas partie (« Entre Alpha SRL »).
RE_AVANT_NOM = re.compile(r"^(?:(?:Entre|Et|Avec|Par|Pour|Ladite|Laquelle|La société|Société|D'une part|D'autre part)[\s,:]+)+")
RE_SOCIETE_NOMMEE = re.compile(rf"(?i:la société|société)\s+(?P<nom>{MOT_MAJ}(?:\s+(?:(?:de|du|des|la|le)\s+|d'|l')?{MOT_MAJ}){{0,5}})")
CIVILITES = r"(?:Madame|Monsieur|Mme|M\.|Maître|Me|Docteur|Dr)"
RE_PERSONNE = re.compile(rf"{BORD_G}{CIVILITES}\s+(?P<nom>{MOT_MAJ}(?:[\s-]+{MOT_MAJ}){{0,3}})")
VOIES = (r"(?i:rue|avenue|av\.|place|quai|boulevard|bd|chaussée|chemin|square|allée|impasse|route|drève|clos|sentier|"
         r"parc|rempart|galerie|cour|venelle|voie|esplanade|digue|mont|steenweg|grand-place|grand'place)")
NOM_DE_VOIE = rf"(?:(?:de\s+la|de\s+l'|du|des|de|d'|la|le|l'|op)\s*)?[{MAJ}0-9][^,;()\n]{{0,58}}?"
NUMERO = r"\d{1,4}[A-Za-z]?(?:\s*(?:bte|boîte|bus|/)\s*\w{1,5})?"
LOCALITE = rf"{MOT_MAJ}(?:[\s-]+(?:{MOT_MAJ}|en|sur|lez|les)){{0,4}}"
RE_ADRESSE = re.compile(
    rf"{BORD_G}(?:{VOIES}\s+{NOM_DE_VOIE},?\s+{NUMERO}"
    rf"|[{MAJ}][{LETTRE}-]{{2,30}}(?:straat|laan|steenweg|plein|weg|lei|dreef|baan)\s+{NUMERO})"
    rf"(?:(?:\s*,\s*|\s+à\s+|\s+)(?:B-)?[1-9]\d{{3}}\s+{LOCALITE}|\s+à\s+{LOCALITE})?")
RE_CODE_POSTAL = re.compile(rf"(?:(?<=à )|(?<=, )|^)(?:B-)?[1-9]\d{{3}}\s+{LOCALITE}")
RE_COURRIEL = re.compile(r"(?<![\w.+-])[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63}){1,5}")
RE_TELEPHONE = re.compile(r"(?<![\w+])(?:\+32|0032)\s?(?:\(0\)\s?)?\d{1,3}(?:[\s./-]?\d{2,3}){2,4}(?!\d)"
                          r"|(?<![\w,.])0\d{1,3}(?:[\s./]\d{2,3}){2,4}(?![\d,])|(?<![\d.,])0[1-9]\d{7,8}(?!\d|[.,]\d)")
RE_BCE = re.compile(r"(?<![\d.])(?:BE\s?)?(\d{3,4})([.\s]?)(\d{3})\2(\d{3})(?!\d|[.,]\d)", re.I)
RE_IBAN = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]{2}\d{2}(?:[\s-]?[A-Za-z0-9]{4}){2,7}(?:[\s-]?[A-Za-z0-9]{1,3})?)(?![A-Za-z0-9])")
RE_REFERENCE = re.compile(r"\b[A-Z]{2,6}[-/]\d{2,6}(?:[-/][A-Z0-9]{1,8}){0,3}\b"
                          r"|(?i:n°|no\.|numéro|référence|réf\.?|dossier|commande|bon de commande)\s*(?:n°\s*)?:?\s*"
                          r"(?P<ref>[A-Z0-9][A-Za-z0-9/.-]{2,20}[A-Za-z0-9])")
NOMBRES = ("zéro|un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|"
           "vingts?|trente|quarante|cinquante|soixante|cents?|mille|mil|millions?|milliards?")
# Bornés : un montant en lettres ne compte pas plus de douze mots, ni un nombre plus de six groupes de chiffres.
# Une suite sans fin relue depuis chaque position rendrait le temps de calcul quadratique.
EN_LETTRES = rf"(?i:(?:{NOMBRES})(?:[\s-]+(?:{NOMBRES}|et)){{0,12}})"
CHIFFRES = r"\d{1,3}(?:[.  ]\d{3}){1,5}(?:,(?:\d{1,2}|-))?|\d{1,12}(?:,(?:\d{1,2}|-))?"
DEVISE = r"(?:euros?|EUR|€|USD|GBP|CHF|dollars?|livres? sterling|francs? suisses?)"
RE_MONTANT = re.compile(
    rf"{BORD_G}(?:{EN_LETTRES}\s+{DEVISE}(?:\s*\(\s*(?:{CHIFFRES})\s*{DEVISE}\s*\))?"
    rf"|(?:{CHIFFRES}|{EN_LETTRES})\s+(?:millions?|milliards?)\s+(?:d'|de\s+)(?:euros|EUR|dollars)"
    rf"|(?:{CHIFFRES})\s*{DEVISE}|(?:EUR|USD|GBP|CHF|€)\s?(?:{CHIFFRES})|\d{{1,6}}(?:,\d{{1,2}})?\s?[kKM]€)"
    rf"(?![{LETTRE}0-9])")
MOIS = "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre"
RE_DATE = re.compile(
    rf"{BORD_G}(?:(?:1er|premier|[1-9]|[12]\d|3[01]|{EN_LETTRES})\s+(?:{MOIS})\s+(?:(?:19|20)\d{{2}}|{EN_LETTRES})"
    r"|(?:0?[1-9]|[12]\d|3[01])[/.-](?:0?[1-9]|1[0-2])[/.-](?:(?:19|20)\d{2}|\d{2})"
    r"|(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"
    rf"|(?P<mois>(?:{MOIS})\s+(?:19|20)\d{{2}}))(?![\d])", re.I)
RE_JOUR_AVANT = re.compile(r"(?:\d|1er|premier)\s+$", re.I)
# Seule la date d'un texte de loi est écartée : celle d'une convention ou d'un jugement entre les parties
# est une donnée de l'opération.
RE_TEXTE_NORMATIF = re.compile(r"(?:loi|lois|arrêté|arrêté royal|décret|ordonnance|directive|règlement|code|A\.R\.|AR)"
                               r"\s+(?:\S+\s+){0,3}(?:du|des)\s+$", re.I)
UNITES = (r"bouteilles?|unités?|pièces?|licences?|utilisateurs?|postes?(?: de travail)?|jours?[- ]hommes?|"
          r"jours?[- ]homme|heures? de (?:prestation|travail|formation|consultance)|m2|m²|m³|mètres? carrés?|mètres? cubes?|"
          r"tonnes?|kg|kilos?|kilogrammes?|litres?|hectolitres?|hl|palettes?|caisses?|cartons?|véhicules?|machines?|"
          r"appareils?|équipements?|emplacements?|places? de parking|bureaux|abonnements?|sièges?|lots?|colis|sacs?|fûts?")
RE_QUANTITE = re.compile(rf"{BORD_G}(?:{CHIFFRES}|{EN_LETTRES})\s+(?:{UNITES}){BORD_D}")
# Rôles définis dans la comparution : ce ne sont pas des noms à rechercher.
ROLES = {"client", "fournisseur", "prestataire", "partie", "parties", "société", "bailleur", "preneur", "cédant",
         "cessionnaire", "vendeur", "acheteur", "licencié", "concédant", "distributeur", "mandant", "mandataire",
         "exploitant", "occupant", "prêteur", "emprunteur", "donneur", "entrepreneur", "maître", "garant", "agent",
         "commettant", "franchiseur", "franchisé", "sous-traitant", "acquéreur", "locataire", "propriétaire"}


def bce_valide(chiffres: str) -> bool:
    return len(chiffres) == 10 and 97 - int(chiffres[:8]) % 97 == int(chiffres[8:])


def iban_valide(iban: str) -> bool:
    compact = re.sub(r"[\s-]", "", iban).upper()
    if not 15 <= len(compact) <= 34 or not compact[:2].isalpha() or not compact[2:4].isdigit():
        return False
    chiffre = "".join(str(int(c, 36)) for c in compact[4:] + compact[:4])
    return int(chiffre) % 97 == 1


def fenetre(texte: str, position: int, largeur: int = 40) -> str:
    return texte[:position] if position <= largeur else "x" + texte[position - largeur:position]


@functools.lru_cache(maxsize=8)
def motif_noms(noms: tuple[str, ...]) -> re.Pattern | None:
    """Une seule expression pour tous les noms connus, sans tenir compte de la casse (« BRASSERIE DU CONDROZ »)."""
    if not noms:
        return None
    return re.compile(BORD_G + "(?:" + "|".join(re.escape(n) for n in sorted(noms, key=len, reverse=True)) + ")" + BORD_D, re.I)


@dataclass
class Donnee:
    categorie: str
    texte: str
    paragraphe: int
    debut: int
    fin: int


def detecter(texte: str, i: int, noms) -> list[Donnee]:
    """Données propres à l'opération dans un paragraphe ; la plus longue l'emporte en cas de chevauchement."""
    texte = texte[:LONGUEUR_MAX]
    trouvees: list[tuple[int, int, str]] = []
    for m in RE_SOCIETE.finditer(texte):
        debut = m.start() + RE_AVANT_NOM.match(m.group()).end() if RE_AVANT_NOM.match(m.group()) else m.start()
        trouvees.append((debut, m.end(), "PARTIE"))
    for m in RE_SOCIETE_NOMMEE.finditer(texte):
        trouvees.append((m.start("nom"), m.end("nom"), "PARTIE"))
    for m in RE_PERSONNE.finditer(texte):
        trouvees.append((m.start(), m.end(), "PARTIE"))
    motif = motif_noms(tuple(noms)) if not isinstance(noms, re.Pattern) else noms
    if motif is not None:
        for m in motif.finditer(texte):
            if m.group()[0].isupper():
                trouvees.append((m.start(), m.end(), "PARTIE"))
    for m in RE_ADRESSE.finditer(texte):
        trouvees.append((m.start(), m.end(), "ADRESSE"))
    for m in RE_CODE_POSTAL.finditer(texte):
        trouvees.append((m.start(), m.end(), "ADRESSE"))
    for m in RE_COURRIEL.finditer(texte):
        trouvees.append((m.start(), m.end(), "IDENTIFIANT"))
    for m in RE_TELEPHONE.finditer(texte):
        if 9 <= sum(c.isdigit() for c in m.group()) <= 12:
            trouvees.append((m.start(), m.end(), "IDENTIFIANT"))
    for m in RE_BCE.finditer(texte):
        chiffres = "".join(m.group(1, 3, 4)).rjust(10, "0")
        # Écrit « 0712.345.630 », c'est un numéro d'entreprise même mal recopié : il faut l'extraire.
        # Sans points, seule la somme de contrôle le distingue d'un autre nombre.
        if chiffres[0] in "01" and ("." in m.group() or bce_valide(chiffres)):
            trouvees.append((m.start(), m.end(), "IDENTIFIANT"))
    for m in RE_IBAN.finditer(texte):
        # La casse étant libre, le mot suivant (« … 6769 du Fournisseur ») peut être pris pour un groupe :
        # on retire les groupes de fin jusqu'à obtenir un IBAN valide.
        candidat = m.group(1)
        while len(re.sub(r"[\s-]", "", candidat)) >= 15 and not iban_valide(candidat):
            candidat = re.sub(r"[\s-]?[A-Za-z0-9]{1,4}$", "", candidat)
        if iban_valide(candidat):
            trouvees.append((m.start(), m.start() + len(candidat), "IDENTIFIANT"))
    for m in RE_REFERENCE.finditer(texte):
        debut, fin = (m.start("ref"), m.end("ref")) if m.group("ref") else (m.start(), m.end())
        if any(c.isdigit() for c in texte[debut:fin]):
            trouvees.append((debut, fin, "IDENTIFIANT"))
    for m in RE_MONTANT.finditer(texte):
        trouvees.append((m.start(), m.end(), "MONTANT"))
    for m in RE_DATE.finditer(texte):
        if RE_TEXTE_NORMATIF.search(fenetre(texte, m.start())):
            continue
        if m.group("mois") and RE_JOUR_AVANT.search(fenetre(texte, m.start())):
            continue   # fin d'une date complète déjà examinée (« 2 août 2002 » d'une loi)
        trouvees.append((m.start(), m.end(), "DATE"))
    for m in RE_QUANTITE.finditer(texte):
        trouvees.append((m.start(), m.end(), "QUANTITE"))
    trouvees.sort(key=lambda x: (-(x[1] - x[0]), x[0]))
    pris = bytearray(len(texte))
    retenues = []
    for debut, fin, categorie in trouvees:
        if pris.find(1, debut, fin) != -1:
            continue
        pris[debut:fin] = b"\x01" * (fin - debut)
        retenues.append(Donnee(categorie, texte[debut:fin].strip(), i, debut, fin))
    return sorted(retenues, key=lambda d: d.debut)


RE_SURNOM = re.compile(r"ci-après\s*(?:dénommée?s?\s*)?,?\s*(?:(?:le|la|les)\s+|l')?[«\"“]\s*(?:(?:le|la|les)\s+|l')?(?P<nom>[^»\"”]{2,40}?)\s*[»\"”]",
                       re.I)


def noms_des_personnes(textes: list[str]) -> list[str]:
    """Noms connus par leur civilité (« Madame Claire Dumont ») ou leur forme sociale, cherchés ensuite
    partout : un signataire est souvent nommé sans civilité (« Pour le Client, Claire Dumont »), une société
    sans sa forme (« Alpha ne divulgue »). S'y ajoutent les noms abrégés (« ci-après « BDC » ») qui reprennent
    un mot du nom ou forment un sigle ; un rôle (« le Client ») n'est pas un nom."""
    noms = set()
    for texte in textes:
        texte = texte[:LONGUEUR_MAX]
        trouves = []
        for m in RE_PERSONNE.finditer(texte):
            noms.add(m.group("nom"))
            if len(m.group("nom").split()) >= 2:
                noms.add(m.group("nom").split()[-1])   # « Monsieur Jean Dupont », puis « M. Dupont » ou « Dupont »
            trouves.append(m.group("nom"))
        for m in RE_SOCIETE.finditer(texte):
            base = re.sub(rf"\s+{FORMES}$", "", m.group()[RE_AVANT_NOM.match(m.group()).end() if RE_AVANT_NOM.match(m.group()) else 0:])
            noms.add(base)
            trouves.append(base)
        for m in RE_SOCIETE_NOMMEE.finditer(texte):
            noms.add(m.group("nom"))
            trouves.append(m.group("nom"))
        for m in RE_SURNOM.finditer(texte):
            surnom = m.group("nom").strip()
            mots = {x.lower() for t in trouves for x in t.split()}
            if surnom.lower() in ROLES:
                continue
            if (surnom.isupper() and len(surnom) >= 2) or surnom.lower() in mots:
                noms.add(surnom)
    return sorted((n for n in noms if len(n) >= 3 and n.lower() not in ROLES), key=len, reverse=True)


# --- Blocs ---------------------------------------------------------------------------------------

RE_TITRE = re.compile(r"^\s*(?:article|art\.|annexe|chapitre|titre|section)\s+"
                      r"(?:\d+(?:bis|ter|quater)?|[IVXLC]+|[A-Z]|premier|1er|unique)(?=[\s.:–—-]|$)", re.I)
RE_TITRE_NUMEROTE = re.compile(rf"^\s*(?:\d+(?:bis|ter)?[.)]?|§\s*\d+\.?)\s+[{MAJ}]")
RE_PREAMBULE = re.compile(r"^\s*(?:préambule|exposé(?: préalable| des motifs)?|considérants?|rappel préalable"
                          r"|il (?:a été|est préalablement) exposé ce qui suit)\s*:?\s*$", re.I)
RE_SIGNATURES = re.compile(r"^\s*(?:fait à|fait en|fait et signé|ainsi fait|signé à|signé en|établi à|établi en|"
                           r"convenu à|pour accord)\b", re.I)
MOTS_PARTICULIERES = re.compile(
    r"objet|prix|honoraires|rémunération|tarif|redevance|loyer|durée|entrée en vigueur|mission|prestations?\b|"
    r"quantit|parties\b|coordonnées|notification|interlocuteur|contact|calendrier|planning|désignation|description|"
    r"biens?\b|locaux|préambule|exposé|considérant|budget|commande initiale|lieu d'exécution|conditions particulières",
    re.I)
MOTS_GENERALES = re.compile(
    r"confidentialit|responsabilit|résiliation|paiement|facturation|garantie|force majeure|droit applicable|juridiction|"
    r"litige|propriété intellectuelle|sous-traitance|cession|assurance|non-concurrence|non-sollicitation|données|"
    r"divers|dispositions|intégralité|obligations|exécution|réception|livraison|révision|indexation|audit|"
    r"conformité|élection de domicile|renonciation|nullité|modification|conditions générales", re.I)


def titre(p) -> bool:
    t = p.texte.strip()
    if not t or p.cellule is not None:
        return False
    court = len(t.split()) <= 12 and not re.search(r"[.;,]$", t) and not re.search(r"[«»\"“”]", t)
    if (p.titre and court) or (RE_TITRE.match(t) and len(t) <= 120) or RE_PREAMBULE.match(t):
        return True
    if RE_TITRE_NUMEROTE.match(t) and court and ":" not in t and len(t.split()) <= 8:
        return True
    if p.numerote and len(t.split()) <= 4 and t[0].isupper() and not re.search(r"[.;:,!?«»\"“”]", t):
        return True
    # Une ligne en capitales est un titre si elle est brève ; une clause entière en capitales (limitation de
    # responsabilité, mise en évidence) n'en est pas un.
    lettres = [c for c in t if c.isalpha()]
    return court and len(lettres) >= 3 and all(c.isupper() for c in lettres)


@dataclass
class Bloc:
    titre: str                       # « comparution », « signatures » ou le titre de l'article
    paragraphes: list[int] = field(default_factory=list)   # intitulé compris, le cas échéant en premier
    donnees: list[Donnee] = field(default_factory=list)
    classement: str = ""             # particulieres, generales, mixte
    raison: str = ""
    renvois: list[str] = field(default_factory=list)
    intitule: int | None = None      # indice du paragraphe d'intitulé


@dataclass
class Analyse:
    document: str
    paragraphes: list[str]
    blocs: list[Bloc]

    def du_type(self, classement: str) -> list[Bloc]:
        return [b for b in self.blocs if b.classement == classement]

    @property
    def donnees(self) -> list[Donnee]:
        return [d for b in self.blocs for d in b.donnees]


RE_RENVOI = re.compile(r"\b(?:articles?|art\.)\s+\d+(?:\.\d+)*(?:\s*(?:,|et|à)\s*\d+(?:\.\d+)*){0,10}", re.I)


def decouper(document: Document) -> list[Bloc]:
    blocs = [Bloc("comparution")]
    article_vu = False
    for i, p in enumerate(document.paragraphes):
        texte = p.texte.strip()
        signatures = blocs[-1].titre == "signatures"
        # Après « Fait à … », tout appartient aux signatures (« POUR LE FOURNISSEUR », noms, qualités)
        # jusqu'à une annexe ou un article.
        if titre(p) and (not signatures or RE_TITRE.match(texte)):
            debut = blocs[-1].titre == "comparution" and not any(document.paragraphes[j].texte.strip()
                                                                 for j in blocs[-1].paragraphes)
            if debut and not (RE_TITRE.match(texte) or RE_PREAMBULE.match(texte) or RE_TITRE_NUMEROTE.match(texte)):
                blocs[-1].paragraphes.append(i)   # intitulé du contrat (« CONTRAT DE FOURNITURE ») : comparution
                continue
            blocs.append(Bloc(texte, [i], intitule=i))
            article_vu = article_vu or not RE_PREAMBULE.match(texte)
            continue
        if article_vu and RE_SIGNATURES.match(texte) and not signatures:
            blocs.append(Bloc("signatures"))
        blocs[-1].paragraphes.append(i)
    return [b for b in blocs if b.paragraphes or b.titre not in ("comparution", "signatures")]


def classer(bloc: Bloc, textes: list[str]) -> None:
    if bloc.titre in ("comparution", "signatures"):
        bloc.classement = "particulieres"
        bloc.raison = "identité des parties" if bloc.titre == "comparution" else "lieu, date et signataires"
        return
    sujet = re.sub(r"^\s*(?:article|art\.|annexe|chapitre|titre|section|§)?\s*[\dIVXLC.)]*(?:bis|ter)?\s*[–—:.-]?\s*",
                   "", bloc.titre, flags=re.I)
    corps = [i for i in bloc.paragraphes if i != bloc.intitule and textes[i].strip()]
    avec = {d.paragraphe for d in bloc.donnees if d.paragraphe != bloc.intitule}
    part = len(avec) / max(1, len(corps))
    # Une clause de nature générale le reste même si son intitulé contient aussi un mot de l'opération
    # (« Obligations des parties », « Durée et résiliation ») : ses données sont alors à extraire.
    if MOTS_GENERALES.search(sujet):
        if bloc.donnees:
            bloc.classement, bloc.raison = "mixte", f"clause de nature générale (« {sujet} ») qui contient des données propres"
        else:
            bloc.classement, bloc.raison = "generales", "clause de nature générale, aucune donnée propre à l'opération repérée"
    elif MOTS_PARTICULIERES.search(sujet):
        # Même sans donnée repérée : un « Prix » ou un « Objet » est propre à l'opération par nature.
        bloc.classement, bloc.raison = "particulieres", f"intitulé « {sujet} »" + (
            " et données propres à l'opération" if bloc.donnees else ", propre à l'opération par nature")
    elif not bloc.donnees:
        bloc.classement, bloc.raison = "generales", "aucune donnée propre à l'opération repérée"
    elif part >= 0.5 or not corps:
        bloc.classement, bloc.raison = "particulieres", "la plupart des paragraphes contiennent des données propres"
    else:
        bloc.classement, bloc.raison = "mixte", "données propres dans une partie seulement de la clause"


def analyser(document: Document) -> Analyse:
    textes = [p.texte for p in document.paragraphes]
    motif = motif_noms(tuple(noms_des_personnes(textes)))
    blocs = decouper(document)
    for bloc in blocs:
        for i in bloc.paragraphes:
            bloc.donnees += detecter(textes[i], i, motif if motif is not None else [])
            bloc.renvois += [m.group() for m in RE_RENVOI.finditer(textes[i][:LONGUEUR_MAX])]
        classer(bloc, textes)
    return Analyse(document.nom, textes, blocs)
