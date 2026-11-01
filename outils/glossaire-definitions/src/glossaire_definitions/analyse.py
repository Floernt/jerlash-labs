"""Définitions d'un contrat : repérage, emplois et défauts, par règles, sans IA.

Définitions reconnues :
- dans l'article ou l'annexe « Définitions » : « Terme » désigne / signifie / vise / s'entend de…,
  « Terme » : …, Terme : … (sans guillemets, chaque mot avec une majuscule), et les tableaux
  « Terme | Définition » ;
- partout : (ci-après « le Terme »), ci-après dénommée « la Société », (le « Prix »),
  (ensemble, les « Parties »), on entend par « Terme », le terme « Terme », « Terme » désigne….

Un emploi est une occurrence du terme avec ses majuscules, au singulier ou au pluriel, hors titres
d'articles et lignes en capitales. Défauts signalés : définition répétée (libellés identiques ou
divergents), terme défini jamais employé, terme écrit comme un terme défini sans définition, graphie
différente d'un terme défini, terme employé avant sa définition en cours de texte.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

from .lecture import Document

MAJ = "A-ZÀ-ÖØ-ÞŒ"
LETTRE = "A-Za-zÀ-ÖØ-öø-ÿŒœ"
MOT_MAJ = rf"[{MAJ}][{LETTRE}0-9-]*"
BORD_G = rf"(?<![{LETTRE}0-9-])"
BORD_D = rf"(?![{LETTRE}0-9-])"
ARTICLE = r"(?:(?:le|la|les)\s+|l')"
CONNECTEURS = {"de", "du", "des", "d", "l", "la", "le", "les", "en", "à", "au", "aux", "et", "sur", "pour", "par", "ou"}

# Guillemets : français, droits, courbes. Le terme ne contient ni guillemet ni retour à la ligne.
RE_CITATION = re.compile(r'«\s*([^«»\n]{1,120}?)\s*»|"\s*([^"\n]{1,120}?)\s*"|“\s*([^“”"\n]{1,120}?)\s*[”"]')
RE_VERBE = re.compile(r"\s*(?:\([^()]{0,80}\)\s*)?,?\s*(?:désign(?:e|ent)|signifi(?:e|ent)|vis(?:e|ent)|s'entend(?:ent)?"
                      r"|(?:a|ont) le sens|recouvr(?:e|ent)|correspond(?:ent)? à|(?:il faut|on doit|il y a lieu d')\s*entendre|on entend)"
                      + BORD_D, re.I)
RE_DEUX_POINTS = re.compile(r"\s*(?:\([^()]{0,80}\)\s*)?[:=–—]|\s+-\s")
RE_INTRODUCTION = re.compile(r"(?:(?:on|il faut|il y a lieu d'|on doit)\s*entendre par|on entend par|(?:^|[.;:]\s*)par|le terme|l'expression|les termes|les mots|le mot|la notion de)\s*" + ARTICLE + r"?$", re.I)
RE_CI_APRES = re.compile(r"ci-après\s*,?\s*(?:(?:dénommé|désigné|appelé|nommé)e?s?\s*,?\s*(?:par|sous le nom de)?\s*)?" + ARTICLE + r"?\s*$", re.I)
RE_PARENTHESE = re.compile(r"\(([^()]{0,240})\)")
RE_RENVOI = re.compile(r"(?:article|articles|art\.|annexe|point|section|chapitre|titre)\s+[\w.:-]+\s*$", re.I)
MOTS_DE_PARENTHESE = {"ci-après", "ci-dessous", "ci-dessus", "dénommé", "dénommée", "dénommés", "dénommées", "désigné",
                      "désignée", "désignés", "désignées", "appelé", "appelée", "appelés", "appelées", "nommé", "nommée",
                      "ensemble", "individuellement", "collectivement", "chacun", "chacune", "séparément", "conjointement",
                      "respectivement", "le", "la", "les", "l'", "un", "une", "et", "ou", "par", "ainsi", "que"}
RE_PREFIXE = re.compile(r"^\s*(?:\(?[a-zA-Z0-9]{1,3}[.)]\s+|\d+(?:\.\d+)*\.?\s+|[-–—•●▪*]\s*)?")
RE_SANS_GUILLEMETS = re.compile(rf"(?:{ARTICLE})?(?P<t>[{MAJ}][^:;,.()«»\"“”=]{{0,80}}?)\s*"
                                r"(?:[:=]|\s(?:désign(?:e|ent)|signifi(?:e|ent)|vis(?:e|ent)|s'entend(?:ent)?)\b)")
RE_TITRE_NUMEROTE = re.compile(rf"^\s*(\d+)\.?\s+[{MAJ}]")
RE_TITRE = re.compile(r"^\s*(?:article|art\.|annexe|chapitre|titre|section)\s+(?:\d+|[IVXLC]+|[A-Z]|premier|1er|unique)"
                      r"(?=[\s.:–—-]|$)", re.I)
RE_NUMERO = re.compile(r"^\s*(\d+(?:\.\d+)+)\.?\s")
RE_ARTICLE = re.compile(r"^\s*(article|art\.|annexe)\s+(\S+?)[.:]?(?=\s|$)", re.I)
RE_DEBUT_PHRASE = re.compile(r"(?:^|[.!?:;]\s+|^\s*(?:\(?[a-zA-Z0-9]{1,3}[.)]|\d+(?:\.\d+)*\.?|[-–—•●▪*])\s+)$")
TETES_TERME = {"terme", "termes", "terme défini", "termes définis", "expression", "notion"}
TETES_DEFINITION = {"définition", "définitions", "signification", "sens"}
RE_NUMERO_DE_LIGNE = re.compile(r"^\s*(?:n°|no|nr)?\s*[\d.]*\s*$", re.I)
TETES_DE_TABLEAU = TETES_TERME | TETES_DEFINITION | {"n°"}

# Termes écrits avec une majuscule sans être des termes définis : institutions, textes, lieux, structure.
INSTITUTIONS = {
    "Article", "Articles", "Annexe", "Annexes", "Chapitre", "Titre", "Section", "Préambule", "Code", "Codes",
    "Tribunal", "Tribunaux", "Cour", "Conseil", "Banque-Carrefour", "Moniteur", "Règlement", "Directive", "Loi",
    "Arrêté", "Décret", "Ordonnance", "Constitution", "Belgique", "France", "Luxembourg", "Grand-Duché", "Pays-Bas",
    "Allemagne", "Europe", "Union", "Région", "Communauté", "Province", "Ville", "Commune", "État", "Etat", "Roi",
    "Gouvernement", "Parlement", "Commission", "Autorité", "Ordre", "Barreau", "Chambre", "Office", "Institut",
    "Agence", "Bruxelles", "Wallonie", "Flandre", "Madame", "Monsieur", "Maître", "Docteur", "Internet", "Banque",
    "Ministre", "Ministère", "Service", "Administration", "Cabinet", "Greffe", "Juge", "Président", "Procureur",
    "Notaire", "Huissier", "Ordre", "Fédération", "Cellule", "Collège", "Conférence", "Convention européenne",
}
MOT_BORNE = rf"[{MAJ}][{LETTRE}0-9-]{{0,40}}"
RE_SOCIETE = re.compile(rf"{BORD_G}((?:{MOT_BORNE}[&.]?\s+(?:(?:de|du|des|la|le|et|&|d'|l')\s*)?){{1,6}})"
                        r"(?:SRL|SA|SC|SNC|SCS|SComm|ASBL|AISBL|BV|NV|BVBA|SPRL|SCRL|SAS|SARL|GmbH|Ltd|LLC|Inc|AG|SE)\b")
RE_PERSONNE = re.compile(rf"(?:Madame|Monsieur|Mme|M\.|Maître|Me|Docteur|Dr)\s+((?:{MOT_BORNE}\s*){{1,3}})")
DETERMINANTS = ("le|la|les|du|des|au|aux|un|une|ce|cet|cette|ces|chaque|tout|toute|tous|toutes|son|sa|ses|leur|leurs|"
                "notre|nos|votre|vos|aucun|aucune|ledit|ladite|lesdits|lesdites|dudit|desdits|desdites|audit|auxdits|"
                "deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|"
                "quarante|cinquante|soixante|cent|mille|plusieurs|quelques|autre|autres|nouveau|nouvelle|nouveaux|nouvelles")
LIAISON = r"(?:\s+(?:de\s+la|du|des|de|en|à|aux|au|sur|pour|par)\s+|\s+(?:de\s+l'|d'|l')|\s+)"
RE_CANDIDAT = re.compile(rf"(?:(?<![{LETTRE}'-])(?i:{DETERMINANTS})\s+|(?<![{LETTRE}-])(?i:l'))"
                         rf"(?P<c>{MOT_MAJ}(?:{LIAISON}{MOT_MAJ})*)")
RE_CHIFFRE = re.compile(r"\s*\d")
RE_VOIE = re.compile(r"\b(?:rue|avenue|av\.|place|quai|boulevard|bd|chaussée|chemin|square|allée|impasse|route|drève|"
                     r"clos|sentier|parc|résidence)\b[^,;()]{0,40}$", re.I)


def amorce(texte: str) -> str:
    mot = re.match(r"[A-Za-z0-9]*", plier(texte)).group().lower()
    return mot[:4]


def plier(texte: str) -> str:
    """Sans accents, caractère pour caractère (le texte est en NFC) : les positions sont conservées."""
    return "".join(unicodedata.normalize("NFD", c)[0] if ord(c) > 127 else c for c in texte)


def sans_article(terme: str) -> str:
    return re.sub(r"^(?:(?:le|la|les|un|une)\s+|l')", "", terme.strip(), flags=re.I).strip()


def cle(terme: str) -> str:
    """Identité d'un terme : sans article, casse, accents, ni marque du pluriel."""
    return " ".join(singulier(m) for m in re.split(r"[\s']+", plier(sans_article(terme)).lower()) if m)


def singulier(mot: str) -> str:
    if len(mot) > 4 and mot.endswith("eaux"):
        return mot[:-1]
    if len(mot) > 4 and mot.endswith("aux"):
        return mot[:-3] + "al"
    return mot[:-1] if len(mot) > 3 and mot[-1] in "sx" else mot


def est_terme(terme: str) -> bool:
    mots = terme.split()
    return (bool(terme) and terme[0].isupper() and 1 <= len(mots) <= 10 and not re.search(r"[.;!?]$", terme)
            and any(c.isalpha() for c in terme))


def motif(forme: str) -> str:
    morceaux = []
    for mot in forme.split():
        sous = []
        for partie in mot.split("'"):
            bas = partie.lower()
            if not partie or bas in CONNECTEURS or not partie[-1].isalpha():
                sous.append(re.escape(partie))
            elif len(bas) > 3 and (bas.endswith("al") or (bas.endswith("aux") and not bas.endswith("eaux"))):
                racine = partie[:-2] if bas.endswith("al") else partie[:-3]
                sous.append(re.escape(racine) + "(?:al|aux|AL|AUX)")
            elif bas.endswith("eau") or bas.endswith("eaux"):
                sous.append(re.escape(partie.rstrip("xX")) + "[xX]?")
            elif partie[-1] in "sS":
                sous.append(re.escape(partie[:-1]) + partie[-1] + "?")
            elif partie[-1] in "xX":
                sous.append(re.escape(partie))
            else:
                sous.append(re.escape(partie) + "s?")
        morceaux.append("'".join(sous))
    return BORD_G + r"\s+".join(morceaux) + BORD_D


def normaliser_libelle(texte: str) -> str:
    texte = plier(texte).lower()
    texte = re.sub(r"^[\s:=–—,-]*(?:designe(?:nt)?|signifie(?:nt)?|vise(?:nt)?|s'entend(?:ent)?(?: de)?|(?:a|ont) le sens de)?\s*", "", texte)
    return " ".join(re.sub(r"[^\w%]+", " ", texte).split())


def titre(p) -> bool:
    """Titre d'article ou d'annexe : style de titre Word, « Article 3 », « 3. Prix » ou ligne en capitales.
    Une simple ligne courte sans point (« Pour le Garant ») n'en est pas un : ses emplois comptent."""
    t = p.texte.strip()
    if not t or p.cellule is not None:
        return False
    court = len(t.split()) <= 12 and not re.search(r"[.;,]$", t) and not re.search(r"[«»\"“”]", t)
    if (p.titre and court) or (RE_TITRE.match(t) and len(t) <= 120):
        return True
    if RE_TITRE_NUMEROTE.match(t) and court and ":" not in t and len(t.split()) <= 8:
        return True
    # Numérotation automatique de Word sans style de titre : seulement un intitulé bref (« Prix », « Objet »).
    if p.numerote and len(t.split()) <= 4 and t[0].isupper() and not re.search(r"[.;:,!?«»\"“”]", t):
        return True
    lettres = [c for c in t if c.isalpha()]
    return len(lettres) >= 3 and all(c.isupper() for c in lettres)


@dataclass
class Definition:
    forme: str
    paragraphe: int
    lieu: str
    libelle: str
    glossaire: bool          # article ou annexe « Définitions », tableau de définitions
    debut: int
    fin: int


@dataclass
class Terme:
    forme: str
    cle: str
    definitions: list[Definition] = field(default_factory=list)
    emplois: list[int] = field(default_factory=list)              # un indice de paragraphe par emploi
    variantes: dict[str, list[int]] = field(default_factory=dict)


@dataclass
class Constat:
    categorie: str     # divergent, non_defini, variante, avant_definition, doublon, inutilise
    terme: str
    forme: str
    message: str


@dataclass
class Analyse:
    document: str
    paragraphes: list[str]
    lieux: list[str]
    termes: list[Terme]
    non_definis: dict[str, tuple[str, list[int]]]
    constats: list[Constat]

    def du_type(self, categorie: str) -> list[Constat]:
        return [c for c in self.constats if c.categorie == categorie]


ORDRE = ["divergent", "non_defini", "variante", "avant_definition", "doublon", "inutilise"]


def situer(paragraphes: list) -> tuple[list[str], list[bool], list[bool]]:
    """Pour chaque paragraphe : son lieu (« art. 7.2 », « article 7 », « annexe A »), s'il est un titre,
    et s'il appartient à une zone de définitions (article ou annexe « Définitions »)."""
    lieux, titres, zone = [], [], []
    courant, dans_zone = "début du contrat", False
    for p in paragraphes:
        t = p.texte
        est_titre = titre(p)
        if est_titre:
            m, n = RE_ARTICLE.match(t), RE_TITRE_NUMEROTE.match(t)
            if m:
                courant = f"{m.group(1).lower().rstrip('.')} {m.group(2).rstrip('.–—-')}".replace("art ", "article ")
            elif n:
                courant = f"article {n.group(1)}"
            elif p.titre or p.numerote:
                courant = f"« {abreger(t, 40)} »"
            dans_zone = "definition" in plier(t).lower()
        numero = RE_NUMERO.match(t) if p.cellule is None else None
        lieux.append(f"art. {numero.group(1)}" if numero else courant)
        titres.append(est_titre)
        zone.append(dans_zone)
    return lieux, titres, zone


def libelle_avant(texte: str, position: int) -> str:
    debut = max(texte.rfind(". ", 0, position), texte.rfind("; ", 0, position))
    return texte[debut + 1 if debut >= 0 else 0:position].strip()


def citations(texte: str):
    for m in RE_CITATION.finditer(texte):
        g = next(i for i in (1, 2, 3) if m.group(i) is not None)
        brut = m.group(g)
        forme = sans_article(brut)
        debut = m.start(g) + (len(brut) - len(brut.lstrip())) + (len(brut.strip()) - len(forme))
        yield m, forme, debut, debut + len(forme)


def definitions_du_paragraphe(texte: str, zone: bool) -> list[tuple[str, int, int, str]]:
    """(forme, début, fin, libellé) des définitions d'un paragraphe hors tableau."""
    trouvees = []
    prefixe = RE_PREFIXE.match(texte).end()
    parentheses = [(m.start(), m.end(), m.group(1)) for m in RE_PARENTHESE.finditer(texte)]
    for m, forme, debut, fin in citations(texte):
        if not est_terme(forme):
            continue
        avant = fenetre(texte, m.start(), 80)
        en_tete = m.start() - prefixe <= 40 and (not texte[prefixe:m.start()].strip(" ") or re.fullmatch(
            r"\s*(?:le terme|l'expression|les termes|le mot)?\s*" + ARTICLE + r"?\s*", texte[prefixe:m.start()], re.I))
        libelle = None
        verbe = RE_VERBE.match(texte, m.end())
        deux_points = RE_DEUX_POINTS.match(texte, m.end())
        ci_apres = RE_CI_APRES.search(avant)
        if verbe:
            libelle = texte[verbe.end():]
        elif en_tete and (zone or deux_points):
            libelle = texte[deux_points.end() if deux_points else m.end():]
        elif RE_INTRODUCTION.search(avant):
            libelle = texte[m.end():]
        elif ci_apres:
            libelle = libelle_avant(texte, m.start() - (len(avant) - ci_apres.start()))
        else:
            for p_debut, p_fin, contenu in parentheses:
                if p_debut < m.start() and m.end() <= p_fin:
                    if RE_RENVOI.search(fenetre(texte, p_debut, 40)):
                        break
                    reste = RE_CITATION.sub(" ", contenu).replace(",", " ").replace(";", " ")
                    reste = re.sub(r"\bl'", " l' ", reste)
                    if all(mot.lower() in MOTS_DE_PARENTHESE for mot in reste.split()):
                        libelle = libelle_avant(texte, p_debut)
                    break
        if libelle is not None:
            trouvees.append((forme, debut, fin, libelle.strip()))
    if not trouvees and zone:
        m = RE_SANS_GUILLEMETS.match(texte, prefixe)
        if m:
            forme = m.group("t").strip()
            mots = [x for x in re.split(r"[\s']+", forme) if x]
            if est_terme(forme) and len(mots) <= 8 and all(x[0].isupper() or x.lower() in CONNECTEURS for x in mots):
                trouvees.append((forme, m.start("t"), m.start("t") + len(forme), texte[m.end():].strip()))
    return trouvees


def definitions_des_tableaux(paragraphes: list, zone: list[bool]) -> list[tuple[int, str, int, int, str]]:
    cases: dict[tuple[int, int, int], list[int]] = {}
    for i, p in enumerate(paragraphes):
        if p.cellule is not None:
            cases.setdefault(p.cellule, []).append(i)
    tableaux: dict[int, list[tuple[int, int]]] = {}
    for (t, r, c) in cases:
        tableaux.setdefault(t, []).append((r, c))
    trouvees = []
    for t, positions in tableaux.items():
        def texte(r, c):
            return " ".join(paragraphes[i].texte for i in cases.get((t, r, c), [])).strip()
        rangees = sorted({r for r, _c in positions})
        colonnes = sorted({c for r, c in positions if r == rangees[0]})
        tetes = {c: texte(rangees[0], c).lower().rstrip(" :") for c in colonnes}
        entete = any(v in TETES_DE_TABLEAU for v in tetes.values())
        premier = cases[(t, rangees[0], colonnes[0])][0]
        if not (entete or zone[premier]):
            continue
        col_terme = next((c for c, v in tetes.items() if v in TETES_TERME), None)
        col_def = next((c for c, v in tetes.items() if v in TETES_DEFINITION), None)
        if col_terme is None:
            numeros = sum(bool(RE_NUMERO_DE_LIGNE.match(texte(r, 0))) for r in rangees)
            col_terme = 1 if numeros >= len(rangees) / 2 else 0
        if col_def is None or col_def == col_terme:
            col_def = col_terme + 1
        for r in rangees:
            if not cases.get((t, r, col_terme)) or not texte(r, col_def):
                continue
            i = cases[(t, r, col_terme)][0]
            brut = paragraphes[i].texte
            if brut.strip().lower().rstrip(" :") in TETES_DE_TABLEAU:
                continue
            nettoye = brut.strip().strip("«»\"“” :").strip()
            forme = sans_article(nettoye)
            if not est_terme(forme):
                continue
            debut = brut.find(forme)
            trouvees.append((i, forme, debut, debut + len(forme), texte(r, col_def)))
    return trouvees


def analyser(document: Document) -> Analyse:
    paragraphes = document.paragraphes
    textes = [p.texte for p in paragraphes]
    lieux, titres, zone = situer(paragraphes)

    # 1. Définitions.
    termes: dict[str, Terme] = {}
    occupees: dict[int, list[tuple[int, int]]] = {}

    def ajouter(i, forme, debut, fin, libelle, glossaire):
        terme = termes.setdefault(cle(forme), Terme(forme, cle(forme)))
        terme.definitions.append(Definition(forme, i, lieux[i], libelle, glossaire, debut, fin))
        occupees.setdefault(i, []).append((debut, fin))

    for i, p in enumerate(paragraphes):
        if p.cellule is None and not titres[i]:
            for forme, debut, fin, libelle in definitions_du_paragraphe(p.texte, zone[i]):
                ajouter(i, forme, debut, fin, libelle, zone[i])
    for i, forme, debut, fin, libelle in definitions_des_tableaux(paragraphes, zone):
        lieux[i] = f"{lieux[i]}, tableau des définitions" if "tableau" not in lieux[i] else lieux[i]
        ajouter(i, forme, debut, fin, libelle, True)

    # 2. Emplois et variantes : la plus longue occurrence l'emporte (« Prix de Cession » sur « Prix »).
    # Une seule expression pour tous les termes, la forme la plus longue en premier : un passage par paragraphe.
    formes = sorted({(d.forme, t.cle) for t in termes.values() for d in t.definitions}, key=lambda x: -len(x[0]))
    exacts: dict[str, list[re.Pattern]] = {}
    for f, k in formes:
        exacts.setdefault(k, []).append(re.compile(motif(f)))
    approches = {f: re.compile(motif(plier(f)), re.I) for f, _ in formes}
    simples = {f: re.compile(motif(f)) for f, _ in formes}
    # Un paragraphe n'est comparé qu'aux termes dont chaque mot significatif y figure (quatre premières
    # lettres, communes au singulier et au pluriel). Sans ce filtre, le coût croîtrait comme la longueur
    # du contrat multipliée par le nombre de termes.
    index: dict[str, list[tuple[str, str, frozenset]]] = {}
    for f, k in formes:
        mots = frozenset(amorce(x) for x in re.findall(r"[A-Za-z0-9]+", plier(f)) if len(x) > 2) or frozenset([amorce(f)])
        index.setdefault(amorce(f), []).append((f, k, mots))
    emplois: dict[int, bytearray] = {}
    for i, texte in enumerate(textes):
        if titres[i] or not texte.strip() or not formes:
            continue
        plie = plier(texte)
        presentes = {x[:4].lower() for x in re.findall(r"[A-Za-z0-9]+", plie)}
        trouves = []
        for f, k, _ in (x for a in presentes for x in index.get(a, []) if x[2] <= presentes):
            for m in simples[f].finditer(texte):
                trouves.append((m.start(), m.end(), termes[k], None))
            for m in approches[f].finditer(plie):
                forme = texte[m.start():m.end()]
                if any(e.fullmatch(forme) for e in exacts[k]) or not any(c.isupper() for c in forme):
                    continue
                if not any(c.isupper() for c in forme[1:]) and RE_DEBUT_PHRASE.search(fenetre(texte, m.start())):
                    continue   # majuscule de début de phrase sur un emploi en minuscules
                trouves.append((m.start(), m.end(), termes[k], forme))
        trouves.sort(key=lambda x: (-(x[1] - x[0]), x[3] is not None, x[0]))
        pris = bytearray(len(texte))   # masque des caractères déjà attribués à une définition ou un emploi
        for debut, fin in occupees.get(i, []):
            pris[debut:fin] = b"" * (fin - debut)
        for debut, fin, terme, variante in trouves:
            if pris.find(1, debut, fin) != -1:
                continue
            pris[debut:fin] = b"" * (fin - debut)
            if variante is None:
                terme.emplois.append(i)
            else:
                terme.variantes.setdefault(variante, []).append(i)
        emplois[i] = pris

    # 3. Termes écrits comme des termes définis, sans définition.
    noms_propres = set()
    for texte in textes:
        for m in list(RE_SOCIETE.finditer(texte)) + list(RE_PERSONNE.finditer(texte)):
            noms_propres.update(re.findall(MOT_MAJ, m.group(1)))
    non_definis: dict[str, tuple[Counter, list[int]]] = {}
    for i, texte in enumerate(textes):
        if titres[i] or not texte.strip():
            continue
        pris = emplois.get(i) or bytearray(len(texte))
        for m in RE_CANDIDAT.finditer(texte):
            candidat, debut = m.group("c"), m.start("c")
            # « Spécifications Techniques de l'Annexe 1 », « Activité Concurrente en Belgique » : le terme
            # s'arrête avant une institution, un lieu ou un sigle.
            for x in list(re.finditer(MOT_MAJ, candidat))[1:]:
                if x.group() in INSTITUTIONS or (len(x.group()) >= 2 and x.group().isupper()):
                    precedent = list(re.finditer(MOT_MAJ, candidat[:x.start()]))[-1]
                    candidat = candidat[:precedent.end()]
                    break
            fin = debut + len(candidat)
            mots = re.findall(MOT_MAJ, candidat)
            if (mots[0] in INSTITUTIONS or all(x in noms_propres for x in mots)
                    or (len(mots[0]) >= 2 and mots[0].isupper())
                    or RE_VOIE.search(fenetre(texte, debut)) or RE_CHIFFRE.match(texte, fin)
                    or cle(candidat) in termes):
                continue
            libres = [x for x in re.finditer(MOT_MAJ, candidat) if pris.find(1, debut + x.start(), debut + x.end()) == -1]
            if not libres:
                continue
            entree = non_definis.setdefault(cle(candidat), (Counter(), []))
            entree[0][candidat] += 1
            entree[1].append(i)

    # 4. Constats.
    constats = []
    for terme in termes.values():
        defs = terme.definitions
        groupes: dict[str, list[Definition]] = {}
        for d in defs:
            groupes.setdefault(plier(d.forme).lower(), []).append(d)
        repetees = max(groupes.values(), key=len)
        if len(repetees) > 1:
            defs = repetees
            libelles = {normaliser_libelle(d.libelle) for d in defs}
            ou = " ; ".join(f"{d.lieu} : « {abreger(d.libelle)} »" for d in defs)
            if len(libelles) > 1:
                constats.append(Constat("divergent", terme.forme, terme.forme,
                                        f"« {terme.forme} » est défini {len(defs)} fois, avec des libellés différents. "
                                        f"Comparez-les : {ou}"))
            else:
                constats.append(Constat("doublon", terme.forme, terme.forme,
                                        f"« {terme.forme} » est défini {len(defs)} fois dans les mêmes termes ({', '.join(d.lieu for d in defs)}) : une définition suffit."))
        defs = terme.definitions
        if not terme.emplois and not terme.variantes:
            constats.append(Constat("inutilise", terme.forme, terme.forme,
                                    f"« {terme.forme} » est défini ({defs[0].lieu}) mais n'est employé nulle part ailleurs."))
        for forme, ou in terme.variantes.items():
            constats.append(Constat("variante", terme.forme, forme,
                                    f"« {forme} » ({lister(ou, lieux)}) : graphie différente du terme défini « {terme.forme} »."))
        premiere = min(defs, key=lambda d: d.paragraphe)
        if not any(d.glossaire for d in defs):
            avant = [i for i in terme.emplois + [j for v in terme.variantes.values() for j in v] if i < premiere.paragraphe]
            if avant:
                constats.append(Constat("avant_definition", terme.forme, terme.forme,
                                        f"« {terme.forme} » est employé ({lister(avant, lieux)}) avant d'être défini ({premiere.lieu})."))
    resume = {}
    for k, (formes, ou) in non_definis.items():
        forme = formes.most_common(1)[0][0]
        resume[k] = (forme, ou)
        constats.append(Constat("non_defini", forme, forme,
                                f"« {forme} » est écrit avec des majuscules comme un terme défini ({lister(ou, lieux)}), "
                                "mais aucune définition n'a été trouvée."))
    constats.sort(key=lambda c: (ORDRE.index(c.categorie), cle(c.terme)))
    liste = sorted(termes.values(), key=lambda t: plier(t.forme).lower())
    return Analyse(document.nom, textes, lieux, liste, resume, constats)


def fenetre(texte: str, position: int, largeur: int = 60) -> str:
    """Les derniers caractères avant une position ; « x » marque une coupure, pour que « ^ » ne
    désigne que le vrai début du paragraphe. Chercher dans tout le début serait quadratique."""
    return texte[:position] if position <= largeur else "x" + texte[position - largeur:position]


def abreger(texte: str, longueur: int = 140) -> str:
    texte = " ".join(texte.split())
    return texte if len(texte) <= longueur else texte[:longueur - 1].rstrip() + "…"


def lister(indices: list[int], lieux: list[str]) -> str:
    vus = list(dict.fromkeys(lieux[i] for i in indices))
    return ", ".join(vus[:5]) + (f" et {len(vus) - 5} autres endroits" if len(vus) > 5 else "")
