"""Détection des données à pseudonymiser, par règles déterministes.

Deux familles de règles :
- les identifiants à somme de contrôle (numéro national, numéro d'entreprise, IBAN, carte) ne sont
  retenus que si la somme est juste, ou si le texte annonce explicitement un numéro national ;
- les noms, sociétés et adresses sont repérés par leur contexte (civilité, forme sociale, type de voie),
  puis chaque nom trouvé est recherché dans tout le texte.

Une détection couvre toujours des mots entiers : un nom que les règles ne savent lire qu'en partie
n'est pas retenu, plutôt que d'être présenté comme remplacé alors qu'un morceau resterait visible.
Le texte doit être en forme Unicode NFC (voir preparer()).

Aucune règle ne garantit de tout trouver. La relecture humaine reste obligatoire.
"""

from __future__ import annotations

import bisect
import re
import unicodedata
from dataclasses import dataclass

CATEGORIES = {
    "TERME": "terme de votre liste",
    "EMAIL": "adresse électronique",
    "IBAN": "numéro de compte (IBAN)",
    "NUMERO_NATIONAL": "numéro de registre national",
    "NUMERO_ENTREPRISE": "numéro d'entreprise ou de TVA",
    "CARTE_BANCAIRE": "numéro de carte",
    "REFERENCE": "référence de dossier",
    "PLAQUE": "plaque d'immatriculation",
    "DATE_NAISSANCE": "date de naissance",
    "ADRESSE": "adresse postale",
    "ORGANISATION": "société ou association",
    "PERSONNE": "personne",
    "TELEPHONE": "numéro de téléphone",
}
# Départage de deux détections de même longueur qui se chevauchent : la première catégorie l'emporte.
PRIORITE = {c: i for i, c in enumerate(CATEGORIES)}
TAILLE_MAX_TEXTE = 5 * 1024 * 1024

ESPACE = "[   ]"
SEP = "[.   ]?"
# Latin étendu (U+0100 à U+024F : ł, ř, ş, ı…) admis comme majuscule et comme minuscule.
ETENDU = "Ā-ɏ"
MAJ = f"A-ZÀ-ÖØ-Þ{ETENDU}"
MIN = f"a-zß-öø-ÿ{ETENDU}"
APOS = "['’ʼ]"
NOM_TITRE = rf"[{MAJ}](?:{APOS}[{MAJ}])?[{MIN}]+(?:[{MAJ}][{MIN}]+)?(?:-[{MAJ}][{MIN}]+)*"
NOM_MAJ = rf"[{MAJ}](?:{APOS}[{MAJ}])?[{MAJ}]+(?:-[{MAJ}]+)*"
BORDS = ",.;:!?)]}»\"“”…/"            # caractères qui peuvent suivre un mot
BORDS_GAUCHE = "([{«\"“'’ʼ/"       # caractères qui peuvent précéder un mot


def dans_un_mot(texte: str, i: int, gauche: bool = False) -> bool:
    """Vrai si la position i prolonge le mot voisin : ni fin de texte, ni espace, ni ponctuation connue.

    Liste blanche plutôt que noire : un caractère inattendu (prime ′, lettre d'un autre alphabet…)
    est traité comme faisant partie du mot, ce qui fait abandonner la détection au lieu de la tronquer."""
    if i < 0 or i >= len(texte):
        return False
    ch = texte[i]
    return not (ch.isspace() or ch in (BORDS_GAUCHE if gauche else BORDS))
PARTICULES = {"de", "du", "des", "van", "von", "der", "den", "ter", "ten", "da", "di", "del", "della", "le", "la", "dos"}
PARTICULES_INITIALES = PARTICULES - {"le", "la"}
MOIS = "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre"
DATE = rf"\d{{1,2}}(?:er)?{ESPACE}+(?:{MOIS}){ESPACE}+\d{{4}}|\d{{1,2}}[/.-]\d{{1,2}}[/.-](?:\d{{4}}|\d{{2}})"

# Mots qui commencent par une majuscule sans être un nom de personne ou de société.
MOTS_COURANTS = {
    "le", "la", "les", "l", "un", "une", "des", "du", "de", "et", "ou", "pour", "par", "contre", "entre", "avec",
    "chez", "en", "au", "aux", "dans", "sur", "sous", "ce", "cette", "ces", "son", "sa", "ses", "leur", "il", "elle",
    "nous", "vous", "ils", "elles", "je", "si", "mais", "donc", "ainsi", "attendu", "vu", "fait", "concerne",
    "article", "articles", "chapitre", "titre", "section", "annexe", "code", "loi", "arrêté", "décret", "ordonnance",
    "tribunal", "cour", "cass", "justice", "président", "présidente", "juge", "procureur", "greffier", "greffière",
    "bâtonnier", "ministre", "directeur", "directrice", "service", "public", "fédéral", "société", "sociétés",
    "siège", "monsieur", "madame", "mademoiselle", "maître", "messieurs", "mesdames", "client", "prestataire",
    "m", "mm", "mme", "mmes", "mlle", "me", "dr", "pr",
    "parties", "partie", "premier", "première", "total", "objet", "prix", "droit", "confidentialité", "pièce",
    "pièces", "demandeur", "demanderesse", "défendeur", "défenderesse", "conseil", "notaire", "assemblée",
    "rpm", "tva", "bce", "srl", "sa", "sc", "asbl", "nv", "bv", "eur", "rg", "cde", "iban", "bic", "niss", "rgpd",
    "onss", "spf", "ue", "mb", "pv", "ii", "iii", "iv", "vi", "vii", "viii", "ix", "xi", "xx", "ok", "cv", "nb",
}
FORMES = ["SRL", "SPRL", "SA", "SC", "SCRL", "SCS", "SNC", "SComm", "ASBL", "AISBL", "BV", "BVBA", "NV", "CV",
          "CVBA", "VZW", "SAS", "SARL", "GmbH", "Ltd", "LLC", "SE"]
FORMES_LONGUES = ["société anonyme", "société à responsabilité limitée", "société coopérative",
                  "association sans but lucratif", "société en nom collectif", "société en commandite"]
TYPES_VOIE = ["rue", "avenue", "av.", "boulevard", "bd", "chaussée", "place", "quai", "chemin", "allée", "impasse",
              "square", "route", "clos", "drève", "sentier", "venelle", "rempart", "thier", "cour", "voie",
              "passage", "parvis", "esplanade", "galerie", "faubourg", "rond-point", "cité", "résidence", "ruelle",
              "montagne", "quartier", "hameau"]
VOIES_SANS_NOM = ["Grand-Route", "Grand-Place", "Grand'Place", "Grand-Rue", "Grand'Rue"]
SUFFIXES_NL = "straat|laan|steenweg|plein|weg|lei|dreef|kaai|markt|baan|singel|dijk|hof"
NUMERO_VOIE = rf"\d{{1,4}}(?:{ESPACE}?[A-Za-z](?![\w]))?(?:{ESPACE}*(?:/|bte|boîte|bus|b\.){ESPACE}*\d{{1,4}}[A-Za-z]?)?"
LOCALITE = rf"(?:B-)?[1-9]\d{{3}}{ESPACE}+[{MAJ}][\w'’-]*(?:{ESPACE}(?:sur|sous|lez|en|[{MAJ}][\w'’-]*)){{0,3}}"


@dataclass
class Entite:
    categorie: str
    debut: int
    fin: int
    texte: str
    raison: str
    certitude: str = "probable"          # "vérifié" quand une somme de contrôle confirme
    cle: str = ""                        # deux entités de même clé reçoivent le même remplacement
    actif: bool = True

    def __post_init__(self):
        if not self.cle:
            self.cle = cle_par_defaut(self.categorie, self.texte)


def preparer(texte: str) -> str:
    """Forme attendue par detecter() : Unicode NFC, fins de ligne \\n.

    Un texte copié depuis un PDF ou un Mac est souvent en NFD (« é » = « e » + accent combinant) :
    sans cette étape, un nom accentué ne serait remplacé qu'en partie."""
    return unicodedata.normalize("NFC", texte.replace("\r\n", "\n"))


def cle_par_defaut(categorie: str, texte: str) -> str:
    if categorie == "TELEPHONE":
        # +32 4 222 33 44, 0032 4 222 33 44, +32 (0)4 222 33 44 et 04 222 33 44 : un seul numéro.
        sans_zero = texte.replace("(0)", "")
        c = chiffres(sans_zero)
        if sans_zero.lstrip().startswith("+32"):
            c = "0" + c[2:]
        elif c.startswith("0032"):
            c = "0" + c[4:]
        return "TELEPHONE:" + c
    if categorie in ("IBAN", "NUMERO_NATIONAL", "NUMERO_ENTREPRISE", "CARTE_BANCAIRE", "PLAQUE"):
        valeur = re.sub(r"[^0-9A-Z]", "", texte.upper())
        return categorie + ":" + (valeur.removeprefix("BE") if categorie == "NUMERO_ENTREPRISE" else valeur)
    return categorie + ":" + " ".join(normaliser(texte).split())


def normaliser(texte: str) -> str:
    """Forme de comparaison (clés, exclusions) ; ne sert jamais à chercher dans le texte."""
    texte = unicodedata.normalize("NFC", texte).replace("’", "'").replace("ʼ", "'")
    return texte.replace(" ", " ").replace(" ", " ").casefold()


# --- Sommes de contrôle -------------------------------------------------------------------------

def chiffres(texte: str) -> str:
    return re.sub(r"\D", "", texte)


def nn_valide(texte: str) -> bool:
    c = chiffres(texte)
    if len(c) != 11:
        return False
    mois, jour = int(c[2:4]), int(c[4:6])
    if not (mois <= 12 or 20 <= mois <= 32 or 40 <= mois <= 52) or jour > 31:
        return False
    return int(c[9:]) in (97 - int(c[:9]) % 97, 97 - int("2" + c[:9]) % 97)


def bce_valide(texte: str) -> bool:
    c = chiffres(texte)
    return len(c) == 10 and c[0] in "01" and int(c[8:]) == 97 - int(c[:8]) % 97


def iban_valide(texte: str) -> bool:
    s = re.sub(r"\s", "", texte).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", s) or (s.startswith("BE") and len(s) != 16):
        return False
    s = s[4:] + s[:4]
    return int("".join(str(int(ch, 36)) for ch in s)) % 97 == 1


def luhn_valide(texte: str) -> bool:
    c = chiffres(texte)
    if not 13 <= len(c) <= 19:
        return False
    total = 0
    for i, ch in enumerate(reversed(c)):
        n = int(ch) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


# --- Détecteurs d'identifiants ------------------------------------------------------------------

RE_EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_NN = re.compile(rf"(?<![\d.])\d{{2}}{SEP}\d{{2}}{SEP}\d{{2}}[-.   ]?\d{{3}}[-.   ]?\d{{2}}(?![\d])")
RE_CONTEXTE_NN = re.compile(r"(?:registre national|numéro national|n° national|niss|numéro d'identification)", re.I)
RE_BCE = re.compile(rf"(?<![\w.])(?:BE{ESPACE}?|be{ESPACE}?)?[01]\d{{3}}{SEP}\d{{3}}{SEP}\d{{3}}(?!\d)")
RE_IBAN_DEBUT = re.compile(r"(?<![\w])[A-Za-z]{2}\d{2}(?=[  ]?[A-Za-z0-9])")
RE_IBAN_GROUPE = re.compile(r"[  ]?[A-Za-z0-9]{1,4}")
RE_CARTE = re.compile(r"(?<![\d])\d(?:[  -]?\d){12,18}(?![\d])")
RE_PLAQUE = re.compile(r"(?<![\w-])[1-9]-[A-Z]{3}-\d{3}(?![\w-])")
RE_REFERENCE = re.compile(
    rf"(?:\bR\.?{ESPACE}?G\.?|\bN/{ESPACE}?[Rr]éf\.?|\bNotre{ESPACE}référence)(?:{ESPACE}*n°)?{ESPACE}*:?{ESPACE}*"
    r"(?P<ref>[\w][\w./-]*\d[\w./-]*)")
RE_TEL_INTER = re.compile(rf"(?<![\w+])(?:\+|00)[1-9]\d{{0,2}}{ESPACE}?(?:\(0\){ESPACE}?)?\d(?:[  ./-]?\d){{6,11}}(?!\d)")
RE_TEL_NATIONAL = re.compile(r"(?<![\w/.,])0[1-9](?:[  ./-]?\d){7,8}(?!\d)")
RE_NAISSANCE = re.compile(
    rf"(?:\bné(?:e|\(e\))?|\bnaissance){ESPACE}+(?:à{ESPACE}+[{MAJ}][\w'’-]*(?:[ -][{MAJ}][\w'’-]*)*{ESPACE}+)?"
    rf"(?:le{ESPACE}+|:{ESPACE}*)?(?P<date>{DATE})", re.I)


def detecter_identifiants(texte: str) -> list[Entite]:
    trouves: list[Entite] = []

    def ajouter(categorie, debut, fin, raison, certitude="vérifié"):
        trouves.append(Entite(categorie, debut, fin, texte[debut:fin], raison, certitude))

    for m in RE_EMAIL.finditer(texte):
        ajouter("EMAIL", m.start(), m.end(), "forme d'une adresse électronique", "probable")
    for m in RE_NN.finditer(texte):
        if nn_valide(m.group()):
            ajouter("NUMERO_NATIONAL", m.start(), m.end(), "numéro national à somme de contrôle juste")
        elif RE_CONTEXTE_NN.search(texte, max(0, m.start() - 60), m.start()):
            ajouter("NUMERO_NATIONAL", m.start(), m.end(), "annoncé comme numéro national (somme de contrôle fausse)", "probable")
    for m in RE_BCE.finditer(texte):
        if bce_valide(m.group()):
            ajouter("NUMERO_ENTREPRISE", m.start(), m.end(), "numéro d'entreprise à somme de contrôle juste")
    for m in RE_IBAN_DEBUT.finditer(texte):
        # Prend le plus long candidat valide, groupe par groupe, sans avaler le mot suivant.
        morceaux, i = [], m.end()
        while len(morceaux) < 8:
            g = RE_IBAN_GROUPE.match(texte, i)
            if not g:
                break
            morceaux.append(g.group())
            i = g.end()
        for n in range(len(morceaux), 2, -1):
            fin = m.end() + sum(len(x) for x in morceaux[:n])
            if iban_valide(texte[m.start():fin]):
                ajouter("IBAN", m.start(), fin, "IBAN à somme de contrôle juste")
                break
    for m in RE_CARTE.finditer(texte):
        if luhn_valide(m.group()):
            ajouter("CARTE_BANCAIRE", m.start(), m.end(), "numéro de carte à somme de contrôle juste (Luhn)")
    for m in RE_PLAQUE.finditer(texte):
        ajouter("PLAQUE", m.start(), m.end(), "forme d'une plaque belge", "probable")
    for m in RE_REFERENCE.finditer(texte):
        ajouter("REFERENCE", m.start("ref"), m.end("ref") - (1 if m.group("ref").endswith(".") else 0),
                "référence de dossier annoncée", "probable")
    for m in RE_TEL_INTER.finditer(texte):
        ajouter("TELEPHONE", m.start(), m.end(), "numéro international", "probable")
    for m in RE_TEL_NATIONAL.finditer(texte):
        c = chiffres(m.group())
        if len(c) == 9 or (len(c) == 10 and re.match(r"04[5-9]", c)):
            ajouter("TELEPHONE", m.start(), m.end(), "numéro belge (fixe ou mobile)", "probable")
    for m in RE_NAISSANCE.finditer(texte):
        ajouter("DATE_NAISSANCE", m.start("date"), m.end("date"), "date annoncée comme date de naissance", "probable")
    return trouves


# --- Noms de personnes --------------------------------------------------------------------------

RE_JETON = re.compile(rf"{NOM_TITRE}|{NOM_MAJ}|d{APOS}(?={NOM_TITRE})|[a-z]+")
RE_ESPACE = re.compile(ESPACE)
RE_DAPOS = re.compile(rf"d{APOS}")
RE_CIVILITE = re.compile(
    rf"\b(?:M\.|MM\.|Mme|Mmes|Mlle|Monsieur|Madame|Mademoiselle|Maître|Me|Dr|Docteur|Pr|Professeur){ESPACE}+")
RE_INDICE = re.compile(
    rf"\b(?:épou(?:se|x)|veu(?:ve|f)|représentée?s?{ESPACE}+par|assistée?s?{ESPACE}+par|fils{ESPACE}+de|"
    rf"fille{ESPACE}+de|soussignée?s?){ESPACE}+(?:de{ESPACE}+)?")
RE_PRENOM_NOM = re.compile(rf"(?<![\w'’ʼ-])({NOM_TITRE})((?:{ESPACE}{NOM_MAJ})+)(?![\w'’ʼ-])")
RE_NOM_PRENOM = re.compile(rf"(?<![\w'’ʼ-])({NOM_MAJ}){ESPACE}({NOM_TITRE})(?![\w'’ʼ-])")


def courant(mot: str) -> bool:
    return normaliser(mot).strip("'.") in MOTS_COURANTS


def lire_nom(texte: str, pos: int, max_jetons: int = 5) -> tuple[int, int] | None:
    """Lit un nom propre à partir de pos : jetons à majuscule et particules, sur une seule ligne.

    Si un jeton s'arrête au milieu d'un mot (lettre que les règles ne connaissent pas), rien n'est
    retenu : mieux vaut un oubli visible à la relecture qu'un remplacement partiel."""
    jetons: list[tuple[int, int, str]] = []
    i = pos
    while len(jetons) < max_jetons:
        m = RE_JETON.match(texte, i)
        if not m:
            if jetons and i < len(texte) and texte[i].isupper():
                return None    # mot à majuscule que les règles ne savent pas lire : ne rien tronquer
            break
        mot = m.group()
        colle = bool(RE_DAPOS.fullmatch(mot))
        if not colle and dans_un_mot(texte, m.end()) and not RE_ESPACE.match(texte, m.end()):
            if mot[0].islower():
                break
            return None
        if mot[0].islower() and mot not in PARTICULES and not colle:
            break
        if not mot[0].islower() and courant(mot):
            break
        jetons.append((m.start(), m.end(), mot))
        i = m.end()
        if colle:
            continue
        if not RE_ESPACE.match(texte, i):
            break
        i += 1
    while jetons and (jetons[-1][2] in PARTICULES or RE_DAPOS.fullmatch(jetons[-1][2])):
        jetons.pop()
    if not jetons or (jetons[0][2] in PARTICULES and jetons[0][2] not in PARTICULES_INITIALES):
        return None
    if not any(not j[2][0].islower() for j in jetons):
        return None
    return jetons[0][0], jetons[-1][1]


def detecter_personnes(texte: str) -> list[Entite]:
    trouves = []
    for motif, raison in ((RE_CIVILITE, "précédé d'une civilité"), (RE_INDICE, "précédé d'une mention de lien")):
        for m in motif.finditer(texte):
            nom = lire_nom(texte, m.end())
            if nom:
                trouves.append(Entite("PERSONNE", nom[0], nom[1], texte[nom[0]:nom[1]], raison))
    for motif in (RE_PRENOM_NOM, RE_NOM_PRENOM):
        for m in motif.finditer(texte):
            if any(courant(mot) for mot in RE_ESPACE.split(m.group())):
                continue
            trouves.append(Entite("PERSONNE", m.start(), m.end(), m.group(), "prénom et nom en capitales"))
    return trouves


def nom_de_famille(nom: str) -> str:
    """« Jean Dupont » -> « Dupont » ; « Jean Pierre van Damme » -> « van Damme » ; « DUPONT Jean » -> « DUPONT »."""
    mots = RE_ESPACE.split(nom)
    if len(mots) < 2 or normaliser(mots[0]) in PARTICULES:
        return nom
    if RE_NOM_PRENOM.fullmatch(nom):
        return mots[0]
    debut = len(mots) - 1
    while debut > 1 and normaliser(mots[debut - 1]) in PARTICULES:
        debut -= 1
    return " ".join(mots[debut:])


# --- Sociétés -----------------------------------------------------------------------------------

RE_FORME = re.compile(r"(?<![\w-])(?:" + "|".join(FORMES) + r")(?![\w-])")
RE_FORME_LONGUE = re.compile(rf"(?:{'|'.join(FORMES_LONGUES)}){ESPACE}+", re.I)
RE_MOT_SOCIETE = re.compile(rf"[{MAJ}0-9][\w&'’.-]*|&|de|du|des|d'|l'|la|le|les|en|et|sur")
RE_MOT_SOCIETE_FIN = re.compile(rf"([{MAJ}0-9][\w&'’.-]*|&|de|du|des|la|le|les|en|et|sur)$")
ARTICLES = {"Les", "La", "Le", "L'"}
PROPAGATION = "même nom trouvé ailleurs dans le texte"
FUSION = " (étendu à une détection voisine)"
FENETRE = 200  # caractères examinés à gauche d'une forme sociale


def nom_vers_la_gauche(texte: str, fin: int) -> tuple[int, int] | None:
    debut_fenetre = max(0, fin - FENETRE)
    mots = []
    i = fin
    while len(mots) < 6:
        avant = texte[debut_fenetre:i].rstrip("   ,")
        if "\n" in texte[debut_fenetre + len(avant):i] and mots:
            break
        m = RE_MOT_SOCIETE_FIN.search(avant)
        if not m or RE_FORME.fullmatch(m.group()) or (m.group()[0].isupper() and courant(m.group())):
            break
        debut = debut_fenetre + m.start()
        if dans_un_mot(texte, debut - 1, gauche=True):
            if not mots or m.group()[0].isupper():
                return None    # nom commencé dans un mot que les règles ne savent pas lire
            break
        mots.insert(0, (debut, debut_fenetre + m.end(), m.group()))
        i = debut
    while mots and not mots[0][2][0].isupper() and not mots[0][2][0].isdigit():
        mots.pop(0)
    return (mots[0][0], mots[-1][1]) if mots else None


def nom_vers_la_droite(texte: str, debut: int) -> tuple[int, int] | None:
    mots = []
    i = debut
    guillemet = re.compile(rf"«{ESPACE}*").match(texte, i)
    if guillemet:
        i = guillemet.end()
    while len(mots) < 6:
        m = RE_MOT_SOCIETE.match(texte, i)
        if not m:
            break
        mot = m.group()
        if dans_un_mot(texte, m.end()) and not mot.endswith("'"):
            if mots and mot[0].islower():
                break
            return None
        if mot[0].isupper() and courant(mot) and not (not mots and mot in ARTICLES):
            break
        mots.append((m.start(), m.end(), mot))
        i = m.end()
        if not RE_ESPACE.match(texte, i):
            break
        i += 1
    while mots and not mots[-1][2][0].isupper() and not mots[-1][2][0].isdigit():
        mots.pop()
    if not mots:
        return None
    fin = mots[-1][1] - (1 if mots[-1][2].endswith(".") and len(mots[-1][2]) > 2 else 0)
    return mots[0][0], fin


def detecter_organisations(texte: str) -> list[Entite]:
    trouves = []
    for m in RE_FORME.finditer(texte):
        span = nom_vers_la_gauche(texte, m.start()) or nom_vers_la_droite(texte, m.end() + 1)
        if span and texte[m.end():m.end() + 1] in (" ", " ", " ", ",", ".", ":", ";", ")", "\n", ""):
            trouves.append(Entite("ORGANISATION", span[0], span[1], texte[span[0]:span[1]],
                                  f"nom accolé à la forme sociale {m.group()}"))
    for m in RE_FORME_LONGUE.finditer(texte):
        span = nom_vers_la_droite(texte, m.end())
        if span:
            trouves.append(Entite("ORGANISATION", span[0], span[1], texte[span[0]:span[1]],
                                  "nom qui suit la forme sociale en toutes lettres"))
    return trouves


# --- Adresses -----------------------------------------------------------------------------------

RE_VOIE = re.compile(
    rf"(?<![\w-])(?:(?i:{'|'.join(re.escape(t) for t in TYPES_VOIE)}){ESPACE}+"
    rf"(?P<nom>(?:[\w'’.-]+{ESPACE}){{0,5}}?(?=[\w'’.-]*[{MAJ}])[\w'’.-]+),?{ESPACE}+"
    rf"|(?:{'|'.join(re.escape(t) for t in VOIES_SANS_NOM)}){ESPACE}+"
    rf"|[{MAJ}][{MIN}]+(?:{SUFFIXES_NL}){ESPACE}+)"
    rf"{NUMERO_VOIE}(?:,?{ESPACE}+{LOCALITE})?(?![\w])")


def detecter_adresses(texte: str) -> list[Entite]:
    return [Entite("ADRESSE", m.start(), m.end(), m.group(), "type de voie suivi d'un numéro")
            for m in RE_VOIE.finditer(texte)]


# --- Assemblage ---------------------------------------------------------------------------------

def motif_recherche(forme: str, casse_stricte: bool) -> re.Pattern:
    """Motif qui retrouve une forme quel que soit le type d'espace ou d'apostrophe.

    casse_stricte : chaque mot doit garder sa casse d'origine ou être tout en capitales
    (« Porte » ne trouve pas « porte ») ; sinon la casse est ignorée (termes fournis par la personne)."""
    mots = []
    for mot in re.split(r"[\s  ]+", forme.strip()):
        variantes = [mot] if not casse_stricte or mot.upper() == mot else [mot, mot.upper()]
        alternatives = []
        for v in variantes:
            alternatives.append("".join(APOS if ch in "'’ʼ" else re.escape(ch) for ch in v))
        mots.append("(?:" + "|".join(alternatives) + ")")
    return re.compile(r"(?<![\w'’ʼ-])" + r"[\s  ]+".join(mots) + r"(?![\w'’ʼ-])",
                      0 if casse_stricte else re.I)


def propager(texte: str, entites: list[Entite]) -> list[Entite]:
    """Recherche dans tout le texte chaque nom de personne ou de société déjà trouvé, et son nom de famille."""
    noms_de_famille: dict[str, tuple[str, set[str]]] = {}
    for e in entites:
        if e.categorie == "PERSONNE":
            famille = nom_de_famille(e.texte)
            if famille != e.texte:
                noms_de_famille.setdefault(normaliser(famille), (famille, set()))[1].add(e.cle)
    # Une civilité suivie du seul nom de famille désigne la personne connue, si elle est unique.
    for e in entites:
        if e.categorie == "PERSONNE" and normaliser(e.texte) in noms_de_famille:
            cles = noms_de_famille[normaliser(e.texte)][1]
            if len(cles) == 1:
                e.cle = next(iter(cles))
    a_chercher: dict[tuple[str, str], tuple[str, str, bool]] = {}
    for e in entites:
        # Un nom tient en quelques mots : une fusion de détections voisines n'est pas un nom à rechercher.
        if e.categorie in ("PERSONNE", "ORGANISATION", "TERME") and len(e.texte) <= 80 and not e.raison.endswith(FUSION):
            casse_stricte = e.raison != "terme de votre liste"
            a_chercher.setdefault((e.categorie, normaliser(e.texte)), (e.texte, e.cle, casse_stricte))
    for normalise, (famille, cles) in noms_de_famille.items():
        if len(famille) >= 2 and not courant(famille):
            cle = next(iter(cles)) if len(cles) == 1 else "PERSONNE:" + normalise
            a_chercher.setdefault(("PERSONNE", normalise), (famille, cle, True))
    formes = [(forme, categorie, cle, casse_stricte) for (categorie, _n), (forme, cle, casse_stricte) in a_chercher.items()]
    return entites + rechercher_formes(texte, formes)


RE_MOT = re.compile(r"[\w'’ʼ-]+")


def mot_compare(mot: str) -> str:
    return mot.replace("’", "'").replace("ʼ", "'")


def rechercher_formes(texte: str, formes: list[tuple[str, str, str, bool]]) -> list[Entite]:
    """Toutes les occurrences de formes connues, en un seul passage sur le texte.

    Le texte est découpé en mots ; chaque suite de mots séparés par des espaces est cherchée dans un
    index des formes. Le coût ne dépend donc pas du nombre de noms connus (contrairement à une
    expression régulière par nom). Une forme qui contient autre chose que des mots et des espaces
    (« A&B », « S.A. ») est cherchée par expression régulière."""
    index: dict[tuple[str, ...], list[tuple[list[str], str, str, bool]]] = {}
    longueur_max = 0
    trouves = []
    for forme, categorie, cle, casse_stricte in formes:
        mots = RE_MOT.findall(forme)
        if " ".join(mots) != " ".join(forme.split()):
            for m in motif_recherche(forme, casse_stricte).finditer(texte):
                trouves.append(Entite(categorie, m.start(), m.end(), m.group(), PROPAGATION, cle=cle))
            continue
        index.setdefault(tuple(normaliser(m) for m in mots), []).append(([mot_compare(m) for m in mots], categorie, cle, casse_stricte))
        longueur_max = max(longueur_max, len(mots))
    if not index:
        return trouves
    jetons = [(m.start(), m.end(), m.group()) for m in RE_MOT.finditer(texte)]
    for i in range(len(jetons)):
        for n in range(1, longueur_max + 1):
            if i + n > len(jetons):
                break
            if n > 1 and not texte[jetons[i + n - 2][1]:jetons[i + n - 1][0]].isspace():
                break
            suite = jetons[i:i + n]
            for originaux, categorie, cle, casse_stricte in index.get(tuple(normaliser(j[2]) for j in suite), ()):
                if casse_stricte and not all(mot_compare(j[2]) in (o, o.upper()) for j, o in zip(suite, originaux)):
                    continue
                debut, fin = suite[0][0], suite[-1][1]
                trouves.append(Entite(categorie, debut, fin, texte[debut:fin], PROPAGATION, cle=cle))
    return trouves


def detecter_termes(texte: str, termes: list[tuple[str, str]]) -> list[Entite]:
    trouves = []
    for categorie, terme in termes:
        if not terme.strip():
            continue
        for m in motif_recherche(terme, casse_stricte=False).finditer(texte):
            trouves.append(Entite(categorie, m.start(), m.end(), m.group(), "terme de votre liste", "vérifié",
                                  cle=cle_par_defaut(categorie, terme.strip())))
    return trouves


def resoudre_chevauchements(entites: list[Entite], texte: str) -> list[Entite]:
    """Une seule détection par portion de texte, sans jamais laisser en clair une partie détectée.

    La plus longue l'emporte ; à longueur égale : terme de la personne, puis détection directe plutôt
    que propagée, puis ordre de CATEGORIES.
    Une détection entièrement contenue dans une autre disparaît ; une détection qui en déborde
    à moitié est fusionnée avec elle, pour que la réunion des deux soit remplacée."""
    retenues: list[Entite] = []      # triées par début, sans chevauchement
    debuts: list[int] = []
    for e in sorted(entites, key=lambda e: (-(e.fin - e.debut), e.raison != "terme de votre liste",
                                            e.raison == PROPAGATION, PRIORITE[e.categorie], e.debut)):
        i = bisect.bisect_left(debuts, e.fin)
        voisines = []
        j = i - 1
        while j >= 0 and retenues[j].fin > e.debut:
            voisines.append(j)
            j -= 1
        if not voisines:
            retenues.insert(i, e)
            debuts.insert(i, e.debut)
            continue
        if len(voisines) == 1 and retenues[voisines[0]].debut <= e.debut and e.fin <= retenues[voisines[0]].fin:
            continue
        gardee = max((retenues[k] for k in voisines), key=lambda r: r.fin - r.debut)
        debut = min([e.debut] + [retenues[k].debut for k in voisines])
        fin = max([e.fin] + [retenues[k].fin for k in voisines])
        for k in sorted(voisines, reverse=True):
            del retenues[k]
            del debuts[k]
        raison = gardee.raison if gardee.raison.endswith(FUSION) else gardee.raison + FUSION
        # Texte et clé calculés une seule fois à la fin : une chaîne de fusions resterait sinon quadratique.
        fusion = Entite(gardee.categorie, debut, fin, "", raison, gardee.certitude, cle=FUSION)
        k = bisect.bisect_left(debuts, debut)
        retenues.insert(k, fusion)
        debuts.insert(k, debut)
    for e in retenues:
        if e.cle == FUSION:
            e.texte = texte[e.debut:e.fin]
            e.cle = cle_par_defaut(e.categorie, e.texte)
    return retenues


def detecter(texte: str, termes: list[tuple[str, str]] | None = None, exclus: list[str] | None = None,
             desactives: set[str] | None = None) -> list[Entite]:
    """Toutes les détections, triées par position, sans chevauchement entre détections actives.

    termes : couples (catégorie, texte) à pseudonymiser en tout cas ;
    exclus : textes à ne jamais pseudonymiser (comparaison sans casse) ;
    desactives : clés que la personne a choisi de ne pas remplacer. Elles sont retirées avant le
    départage, pour qu'une donnée conservée n'en masque pas une autre qui la chevauche ; elles restent
    dans la liste, inactives, quand elles ne chevauchent aucune détection active.
    """
    if len(texte) > TAILLE_MAX_TEXTE:
        raise ValueError(f"Texte trop long ({len(texte) // 1024} Ko ; maximum {TAILLE_MAX_TEXTE // 1024} Ko). "
                         "Découpez-le en plusieurs parties.")
    if texte != unicodedata.normalize("NFC", texte):
        raise ValueError("Texte non normalisé : appeler preparer() avant detecter().")
    exclus_normalises = {" ".join(normaliser(x).split()) for x in (exclus or []) if x.strip()}
    desactives = desactives or set()

    def sans_exclus(liste):
        return [e for e in liste if " ".join(normaliser(e.texte).split()) not in exclus_normalises]

    regles = (detecter_identifiants(texte) + detecter_personnes(texte) + detecter_organisations(texte)
              + detecter_adresses(texte))
    # Les termes de la personne et ses noms de personnes sont, comme les autres, recherchés partout,
    # nom de famille seul compris. Exclure avant la propagation : un nom exclu n'est pas recherché ailleurs.
    candidats = sans_exclus(detecter_termes(texte, termes or []) + regles)
    candidats = sans_exclus(propager(texte, resoudre_chevauchements(candidats, texte)))
    actives = resoudre_chevauchements([e for e in candidats if e.cle not in desactives], texte)
    debuts = [a.debut for a in actives]

    def chevauche_une_active(e):
        i = bisect.bisect_left(debuts, e.fin)
        return i > 0 and actives[i - 1].fin > e.debut

    inactives = [e for e in resoudre_chevauchements([e for e in candidats if e.cle in desactives], texte)
                 if not chevauche_une_active(e)]
    for e in inactives:
        e.actif = False
    return sorted(actives + inactives, key=lambda e: e.debut)


def lire_termes(contenu: str) -> list[tuple[str, str]]:
    """Une ligne par terme ; « CATÉGORIE | texte » pour choisir la catégorie, sinon TERME. # = commentaire."""
    termes = []
    for ligne in contenu.splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        if "|" in ligne:
            categorie, terme = (x.strip() for x in ligne.split("|", 1))
            categorie = categorie.upper()
            if categorie not in CATEGORIES:
                raise ValueError(f"Catégorie inconnue : {categorie}. Catégories admises : {', '.join(CATEGORIES)}")
        else:
            categorie, terme = "TERME", ligne
        termes.append((categorie, terme))
    return termes
