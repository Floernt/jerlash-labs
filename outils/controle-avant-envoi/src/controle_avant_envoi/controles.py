"""Contrôles réalisés sur un paquet .docx.

Chaque contrôle renvoie un statut parmi :
- "detecte" : au moins un élément a été trouvé ;
- "non_detecte" : rien trouvé, dans les limites du contrôle décrit ;
- "non_verifie" : contrôle non réalisé (donnée manquante, cas non pris en charge) ;
- "erreur" : le contrôle a échoué ; il ne doit jamais être lu comme un feu vert.
"""

from __future__ import annotations

import posixpath
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable

from .ooxml import NS, ErreurLecture, PaquetDocx, extrait, libelle_partie, q, texte_element

DETECTE, NON_DETECTE, NON_VERIFIE, ERREUR = "detecte", "non_detecte", "non_verifie", "erreur"
IMPORTANT, A_EXAMINER, INFORMATION = "important", "a_examiner", "information"
MAX_CONSTATS = 200


@dataclass
class Constat:
    localisation: str
    detail: str


@dataclass
class Controle:
    ident: str
    titre: str
    gravite: str
    pourquoi: str
    conseil: str
    statut: str = NON_DETECTE
    constats: list[Constat] = field(default_factory=list)
    note: str = ""
    omis: int = 0

    def ajouter(self, localisation: str, detail: str) -> None:
        self.statut = DETECTE
        if len(self.constats) < MAX_CONSTATS:
            self.constats.append(Constat(localisation, detail))
        else:
            self.omis += 1


# --- Contrôles ---------------------------------------------------------------


def controle_commentaires(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    for partie in p.parties_commentaires():
        for el in p.xml(partie).findall(q("w", "comment")):
            auteur = el.get(q("w", "author"), "") or "auteur non renseigné"
            date = el.get(q("w", "date"), "")
            texte = extrait(texte_element(el)) or "(commentaire vide)"
            c.ajouter(f"Commentaire n° {el.get(q('w', 'id'), '?')}",
                      f"{auteur}{' — ' + date[:10] if date else ''} : « {texte} »")


TYPES_REVISION = {
    "ins": "Insertion",
    "del": "Suppression",
    "moveFrom": "Déplacement (origine)",
    "moveTo": "Déplacement (destination)",
    "rPrChange": "Mise en forme modifiée",
    "pPrChange": "Paragraphe modifié",
    "sectPrChange": "Section modifiée",
    "tblPrChange": "Tableau modifié",
    "trPrChange": "Ligne de tableau modifiée",
    "tcPrChange": "Cellule modifiée",
    "numberingChange": "Numérotation modifiée",
    "cellIns": "Cellule insérée",
    "cellDel": "Cellule supprimée",
    "tblGridChange": "Grille de tableau modifiée",
    "tblPrExChange": "Tableau modifié",
}


def _parties_revisions(p: PaquetDocx) -> list[str]:
    parties = list(p.parties_texte())
    numerotation = p.partie_liee("numbering")
    if numerotation and numerotation not in parties:
        parties.append(numerotation)
    return parties


def controle_modifications(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    for partie in _parties_revisions(p):
        racine = p.xml(partie)
        for nom, libelle in TYPES_REVISION.items():
            for el in racine.iter(q("w", nom)):
                # Une marque w:ins / w:del dans les propriétés d'un paragraphe signale la marque de paragraphe.
                auteur = el.get(q("w", "author"), "") or "auteur non renseigné"
                date = el.get(q("w", "date"), "")
                texte = extrait(texte_element(el), 100)
                detail = f"{libelle} par {auteur}{' le ' + date[:10] if date else ''}"
                if texte:
                    detail += f" : « {texte} »"
                c.ajouter(libelle_partie(partie), detail)


CHAMPS_CORE = [
    ("dc", "creator", "Auteur"),
    ("cp", "lastModifiedBy", "Dernière modification par"),
    ("dc", "title", "Titre"),
    ("dc", "subject", "Sujet"),
    ("dc", "description", "Commentaires (propriétés)"),
    ("cp", "keywords", "Mots-clés"),
    ("cp", "category", "Catégorie"),
    ("cp", "contentStatus", "État du contenu"),
    ("cp", "revision", "Numéro de révision"),
    ("dcterms", "created", "Créé le"),
    ("dcterms", "modified", "Modifié le"),
    ("cp", "lastPrinted", "Dernière impression"),
]
CHAMPS_APP = [("Company", "Société"), ("Manager", "Responsable"), ("Template", "Modèle"),
              ("HyperlinkBase", "Base des liens hypertexte"), ("TotalTime", "Temps d'édition (minutes)")]
# Champs qui n'identifient personne : listés pour information, sans déclencher le contrôle.
CHAMPS_NEUTRES = {"Créé le", "Modifié le", "Dernière impression", "Numéro de révision", "Temps d'édition (minutes)", "Modèle"}
MODELES_NEUTRES = {"normal.dotm", "normal", "normal.dot"}


def _proprietes(p: PaquetDocx, genre: str):
    """Partie de propriétés trouvée par sa relation (son chemin varie selon le logiciel qui a créé le fichier)."""
    defaut = {"core-properties": "docProps/core.xml", "extended-properties": "docProps/app.xml",
              "custom-properties": "docProps/custom.xml"}[genre]
    return p.xml(p.partie_paquet(genre) or defaut)


def controle_proprietes(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    neutres = []
    core = _proprietes(p, "core-properties")
    if core is not None:
        for prefixe, nom, libelle in CHAMPS_CORE:
            el = core.find(q(prefixe, nom))
            valeur = (el.text or "").strip() if el is not None else ""
            if not valeur:
                continue
            if libelle in CHAMPS_NEUTRES:
                neutres.append((libelle, valeur))
            else:
                c.ajouter("Propriétés du document", f"{libelle} : {extrait(valeur)}")
    app = _proprietes(p, "extended-properties")
    if app is not None:
        for nom, libelle in CHAMPS_APP:
            el = app.find("{%s}%s" % (NS["ep"], nom))
            valeur = (el.text or "").strip() if el is not None else ""
            if not valeur:
                continue
            if libelle == "Modèle" and valeur.lower() not in MODELES_NEUTRES:
                c.ajouter("Propriétés étendues", f"{libelle} : {extrait(valeur)}")
            elif libelle in CHAMPS_NEUTRES:
                neutres.append((libelle, valeur))
            else:
                c.ajouter("Propriétés étendues", f"{libelle} : {extrait(valeur)}")
    custom = _proprietes(p, "custom-properties")
    if custom is not None:
        for el in custom.findall("{%s}property" % NS["cust"]):
            valeur = " ".join((s.text or "").strip() for s in el)
            c.ajouter("Propriétés personnalisées", f"{el.get('name', '?')} : {extrait(valeur) or '(vide)'}")
    if neutres:
        c.note = "Également présents, sans identifier personne : " + "; ".join(f"{l} : {v}" for l, v in neutres) + "."


def controle_personnes(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    auteurs: dict[str, set[str]] = {}

    def noter(nom: str, source: str) -> None:
        if nom:
            auteurs.setdefault(nom, set()).add(source)

    for partie in p.parties_commentaires():
        for el in p.xml(partie).findall(q("w", "comment")):
            noter(el.get(q("w", "author"), ""), "commentaires")
    for partie in _parties_revisions(p):
        for nom in TYPES_REVISION:
            for el in p.xml(partie).iter(q("w", nom)):
                noter(el.get(q("w", "author"), ""), "modifications suivies")
    for nom in p.noms:
        if posixpath.basename(nom) == "people.xml":
            for el in p.xml(nom).iter(q("w15", "person")):
                noter(el.get(q("w15", "author"), ""), "liste des relecteurs (people.xml)")
    core = _proprietes(p, "core-properties")
    if core is not None:
        for prefixe, nom, libelle in CHAMPS_CORE[:2]:
            el = core.find(q(prefixe, nom))
            if el is not None:
                noter((el.text or "").strip(), "propriétés")
    for nom in sorted(auteurs, key=str.casefold):
        c.ajouter("Ensemble du fichier", f"{nom} (dans : {', '.join(sorted(auteurs[nom]))})")


def _actif(el, nom: str) -> bool:
    sous = el.find(q("w", nom)) if el is not None else None
    if sous is None:
        return False
    return sous.get(q("w", "val"), "true").lower() not in ("0", "false", "off")


class Styles:
    """Propriétés de caractère effectives : mise en forme directe, puis style de caractère,
    puis style de paragraphe (chacun en suivant sa chaîne basedOn), puis valeurs par défaut du document."""

    def __init__(self, p: PaquetDocx):
        self.styles: dict = {}
        self.defauts = None
        partie = p.partie_liee("styles")
        if partie is None:
            return
        racine = p.xml(partie)
        defauts = racine.find(q("w", "docDefaults"))
        if defauts is not None:
            self.defauts = defauts.find(f"{q('w', 'rPrDefault')}/{q('w', 'rPr')}")
        for style in racine.findall(q("w", "style")):
            base = style.find(q("w", "basedOn"))
            self.styles[style.get(q("w", "styleId"), "")] = (
                base.get(q("w", "val")) if base is not None else None, style.find(q("w", "rPr")))
            if style.get(q("w", "type")) == "paragraph" and _vrai_attr(style.get(q("w", "default"))):
                self.paragraphe_defaut = style.get(q("w", "styleId"), "")

    paragraphe_defaut: str | None = None

    def _chaine(self, ident):
        vus = set()
        while ident and ident in self.styles and ident not in vus:
            vus.add(ident)
            base, rpr = self.styles[ident]
            yield ident, rpr
            ident = base

    def propriete(self, rpr, style_car, style_para, nom: str):
        """Renvoie (élément, origine) pour la première définition trouvée de la propriété."""
        if rpr is not None and rpr.find(q("w", nom)) is not None:
            return rpr.find(q("w", nom)), "mise en forme directe"
        for chaine in (style_car, style_para or self.paragraphe_defaut):
            for ident, srpr in self._chaine(chaine):
                if srpr is not None and srpr.find(q("w", nom)) is not None:
                    return srpr.find(q("w", nom)), f"style « {ident} »"
        if self.defauts is not None and self.defauts.find(q("w", nom)) is not None:
            return self.defauts.find(q("w", nom)), "valeurs par défaut du document"
        return None, ""


def _vrai_attr(valeur) -> bool:
    return valeur is not None and valeur.lower() in ("1", "true", "on")


def _vrai(el) -> bool:
    return el is not None and el.get(q("w", "val"), "true").lower() not in ("0", "false", "off")


def _precision(origine: str) -> str:
    return "" if origine == "mise en forme directe" else f" (par {origine})"


def controle_texte_masque(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    styles = Styles(p)
    for partie in p.parties_texte():
        for i, para in enumerate(p.xml(partie).iter(q("w", "p")), start=1):
            ppr = para.find(q("w", "pPr"))
            pstyle = ppr.find(q("w", "pStyle")) if ppr is not None else None
            style_para = pstyle.get(q("w", "val")) if pstyle is not None else None
            lieu = f"{libelle_partie(partie)}, paragraphe {i}"
            for run in para.iter(q("w", "r")):
                texte = "".join(t.text or "" for t in run.iter(q("w", "t")))
                if not texte.strip():
                    continue
                rpr = run.find(q("w", "rPr"))
                rstyle = rpr.find(q("w", "rStyle")) if rpr is not None else None
                style_car = rstyle.get(q("w", "val")) if rstyle is not None else None
                masque, origine = styles.propriete(rpr, style_car, style_para, "vanish")
                if _vrai(masque):
                    c.ajouter(lieu, f"Texte masqué{_precision(origine)} : « {extrait(texte)} »")
                    continue
                couleur, origine = styles.propriete(rpr, style_car, style_para, "color")
                if couleur is not None and (couleur.get(q("w", "val"), "") or "").upper() in ("FFFFFF", "FFFFFE"):
                    c.ajouter(lieu, f"Texte écrit en blanc{_precision(origine)} : « {extrait(texte)} »")
                taille, origine = styles.propriete(rpr, style_car, style_para, "sz")
                valeur = (taille.get(q("w", "val"), "") or "") if taille is not None else ""
                if valeur.isdigit() and int(valeur) <= 4:
                    c.ajouter(lieu, f"Texte de taille minuscule ({int(valeur) / 2:g} pt){_precision(origine)} : "
                                    f"« {extrait(texte)} »")


def _codes_de_champ(racine) -> list[str]:
    """Codes de champ, simples (w:fldSimple) et complexes (w:fldChar + w:instrText)."""
    codes = [el.get(q("w", "instr"), "") for el in racine.iter(q("w", "fldSimple"))]
    pile: list[dict] = []
    for el in racine.iter():
        if el.tag == q("w", "fldChar"):
            genre = el.get(q("w", "fldCharType"))
            if genre == "begin":
                pile.append({"morceaux": [], "releve": False})
            elif genre == "separate" and pile and not pile[-1]["releve"]:
                codes.append("".join(pile[-1]["morceaux"]))
                pile[-1]["releve"] = True
            elif genre == "end" and pile:
                champ = pile.pop()
                if not champ["releve"]:
                    codes.append("".join(champ["morceaux"]))
        elif el.tag == q("w", "instrText") and pile and not pile[-1]["releve"]:
            pile[-1]["morceaux"].append(el.text or "")
    return [" ".join(code.split()) for code in codes if code.strip()]


def controle_champs(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    revelateurs = [m.upper() for m in cfg["champs_revelateurs"]]
    for partie in p.parties_texte():
        for code in _codes_de_champ(p.xml(partie)):
            mot = code.split()[0].upper() if code.split() else ""
            if mot in revelateurs:
                c.ajouter(libelle_partie(partie), f"Champ {code}")
            elif mot == "HYPERLINK":
                cible = re.search(r'"([^"]*)"', code)
                if cible and lien_sensible(cible.group(1), cfg):
                    c.ajouter(libelle_partie(partie), f"Champ {code} (lien vers un fichier ou un serveur interne)")


RE_HOTE = re.compile(r"^https?://(?:[^@/]*@)?([^/:?#]+)", re.IGNORECASE)
RE_IP_PRIVEE = re.compile(r"^(?:10\.|127\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.|169\.254\.)")
SUFFIXES_INTERNES = (".local", ".lan", ".internal", ".intra", ".corp", ".home", ".localdomain")


def lien_sensible(cible: str, cfg: dict) -> str:
    """Motif de sensibilité d'une cible de lien, ou chaîne vide pour un lien web public.

    Toute cible qui n'est ni une adresse web (http, https) ni une adresse de courriel est sensible :
    chemin local, partage réseau, chemin relatif vers un autre fichier, schéma inconnu.
    """
    bas = cible.strip().lower()
    if bas.startswith(("mailto:", "#")):
        return ""
    hote = RE_HOTE.match(bas)
    if not hote:
        return "chemin local, réseau ou relatif"
    nom = hote.group(1).strip("[]")
    if "." not in nom or RE_IP_PRIVEE.match(nom) or nom.endswith(SUFFIXES_INTERNES):
        return "serveur interne"
    if any(d.lower() in bas for d in cfg.get("domaines_internes", [])):
        return "adresse interne ou de stockage en ligne"
    return ""


def _sources_relations(p: PaquetDocx):
    for fichier in p.fichiers_relations():
        dossier = posixpath.dirname(posixpath.dirname(fichier))
        yield posixpath.join(dossier, posixpath.basename(fichier)[: -len(".rels")])


def controle_liens(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    sensible = False
    for source in _sources_relations(p):
        lieu = libelle_partie(source) if source else "Paquet"
        for rel in p.relations(source):
            if not rel.externe:
                continue
            genre = {"hyperlink": "Lien hypertexte", "attachedTemplate": "Modèle attaché",
                     "oleObject": "Objet lié", "image": "Image liée", "subDocument": "Sous-document",
                     "frame": "Cadre lié"}.get(rel.type_court, f"Lien externe ({rel.type_court})")
            motif = lien_sensible(rel.cible, cfg)
            if motif or rel.type_court != "hyperlink":
                sensible = True
                c.ajouter(lieu, f"{genre}{' — ' + motif if motif else ''} : {extrait(rel.cible, 200)}")
            else:
                c.ajouter(lieu, f"{genre} : {extrait(rel.cible, 200)}")
    if c.statut == DETECTE and not sensible:
        c.gravite = INFORMATION
        c.note = "Seulement des liens web publics : vérifiez qu'ils sont voulus."


TYPES_OBJETS = {"oleObject": "Objet OLE incorporé", "package": "Fichier incorporé",
                "aFChunk": "Contenu importé (altChunk)", "control": "Contrôle ActiveX",
                "glossaryDocument": "Blocs de construction (glossaire)"}


def controle_objets(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    vus = set()
    for source in _sources_relations(p):
        for rel in p.relations(source):
            cible = None if rel.externe else p.resoudre(rel.cible)
            if rel.type_court in TYPES_OBJETS and cible and cible not in vus:
                vus.add(cible)
                taille = p._zip.getinfo(cible).file_size
                c.ajouter(TYPES_OBJETS[rel.type_court], f"{cible} ({taille} octets), contenu non analysé")
    for nom in p.noms:
        if nom.lower().startswith("word/embeddings/") and nom not in vus:
            vus.add(nom)
            c.ajouter("Objets incorporés", f"{nom} ({p._zip.getinfo(nom).file_size} octets), contenu non analysé")


def controle_macros(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    trouves = set()
    for nom in p.noms:
        if posixpath.basename(nom).lower() in ("vbaproject.bin", "vbadata.xml"):
            trouves.add(nom)
    for fichier in p.fichiers_relations():
        for el in p.xml(fichier):
            if el.get("Type", "").endswith(("/vbaProject", "/wordVbaData")):
                trouves.add(el.get("Target", ""))
    types = p.xml("[Content_Types].xml")
    if types is not None and any("macroenabled" in (el.get("ContentType", "") or "").lower() for el in types):
        trouves.add("type de document avec macros")
    for t in sorted(trouves):
        c.ajouter("Macros", f"Code de macro présent ({t})")


def controle_notes(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    for genre, libelle in (("footnotes", "footnote"), ("endnotes", "endnote")):
        partie = p.partie_liee(genre)
        if partie is None:
            continue
        for note in p.xml(partie).findall(q("w", libelle)):
            if note.get(q("w", "type")) in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            c.ajouter(libelle_partie(partie), f"Note {note.get(q('w', 'id'))} : « {extrait(texte_element(note))} »")


def controle_marqueurs(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    motifs = [(re.compile(m["motif"]), m["libelle"]) for m in cfg["marqueurs"]]
    for partie in p.parties_texte():
        if partie == p.partie_liee("comments"):
            continue  # les commentaires sont traités à part
        for i, para in enumerate(p.xml(partie).iter(q("w", "p")), start=1):
            texte = texte_element(para)
            for motif, libelle in motifs:
                for m in motif.finditer(texte):
                    debut = max(0, m.start() - 50)
                    c.ajouter(f"{libelle_partie(partie)}, paragraphe {i}",
                              f"{libelle} : « {extrait(texte[debut:m.end() + 50])} »")
            for run in para.iter(q("w", "r")):
                rpr = run.find(q("w", "rPr"))
                surligne = rpr.find(q("w", "highlight")) if rpr is not None else None
                ombre = rpr.find(q("w", "shd")) if rpr is not None else None
                marque = (surligne is not None and surligne.get(q("w", "val")) not in (None, "none")) or \
                    (ombre is not None and (ombre.get(q("w", "fill")) or "auto").lower() not in ("auto", "ffffff"))
                texte_run = "".join(t.text or "" for t in run.iter(q("w", "t")))
                if marque and texte_run.strip():
                    c.ajouter(f"{libelle_partie(partie)}, paragraphe {i}", f"Texte surligné : « {extrait(texte_run)} »")


EQUIVALENTS = str.maketrans({"\u2019": "'", "\u2018": "'", "\u02bc": "'", "\u00b4": "'", "`": "'",
                             "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
                             "\u00a0": " ", "\u202f": " ", "\u2007": " ", "\u00ad": None})


def normaliser(texte: str) -> str:
    """Forme de comparaison : sans majuscules ni accents ; apostrophes, tirets et espaces unifiés."""
    decompose = unicodedata.normalize("NFKD", texte.casefold().translate(EQUIVALENTS))
    return " ".join("".join(ch for ch in decompose if not unicodedata.combining(ch)).split())


def _textes_du_paquet(p: PaquetDocx):
    """Tout le texte du paquet : paragraphes rédigés (avec leur numéro), puis chaque texte et chaque
    attribut de toutes les parties XML (codes de champ, textes alternatifs, customXml, SmartArt,
    graphiques, propriétés, variables, relations), puis les noms des éléments internes."""
    for partie in p.parties_texte():
        for i, para in enumerate(p.xml(partie).iter(q("w", "p")), start=1):
            yield partie, f"{libelle_partie(partie)}, paragraphe {i}", texte_element(para)
    for partie in p.parties_xml():
        for el in p.xml(partie).iter():
            if el.text and el.text.strip():
                yield partie, libelle_partie(partie), el.text
            for valeur in el.attrib.values():
                if len(valeur) > 2:
                    yield partie, libelle_partie(partie), valeur
    for nom in p.noms:
        yield "", "Noms des éléments internes", nom


def controle_termes(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    termes = [t for t in cfg.get("termes_sensibles", []) if t.strip()]
    if not termes:
        c.statut = NON_VERIFIE
        c.note = ("Aucune liste de termes fournie. Ajoutez les noms d'autres clients, d'autres dossiers "
                  "ou de parties adverses pour vérifier qu'ils n'apparaissent pas dans le document.")
        return
    cherches = [(t.strip(), normaliser(t.strip())) for t in termes]
    deja: set = set()  # (terme, partie) déjà signalés : une seule mention par partie hors paragraphes
    for partie, lieu, texte in _textes_du_paquet(p):
        norm = normaliser(texte)
        for terme, cle in cherches:
            if not cle or cle not in norm:
                continue
            if "paragraphe" not in lieu and (terme, partie) in deja:
                continue
            deja.add((terme, partie))
            c.ajouter(lieu, f"« {terme} » trouvé dans : « {extrait(texte)} »")
    c.note = (f"{len(cherches)} terme(s) recherché(s) dans le texte et dans toutes les données du fichier, "
              "sans tenir compte des majuscules, des accents ni des variantes d'apostrophe et de tiret.")
    non_analyses = [n for n in p.noms if not n.lower().endswith((".xml", ".rels", ".psmdcp"))
                    and not n.lower().startswith("word/media/")]
    if non_analyses:
        c.note += (" Contenus non analysés : " + ", ".join(non_analyses[:5]) + ("…" if len(non_analyses) > 5 else "")
                   + " (objets incorporés ou contenus binaires).")


def controle_reglages(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    partie = p.partie_liee("settings")
    if partie is None:
        return
    racine = p.xml(partie)
    if _actif(racine, "trackRevisions"):
        c.ajouter("Réglages", "Le suivi des modifications est activé : les changements que fera le destinataire "
                  "seront enregistrés, et ceux que vous ferez avant l'envoi aussi.")
    for var in racine.iter(q("w", "docVar")):
        c.ajouter("Variables du document",
                  f"{var.get(q('w', 'name'), '?')} = {extrait(var.get(q('w', 'val'), ''))}")
    protection = racine.find(q("w", "documentProtection"))
    if protection is not None and protection.get(q("w", "enforcement"), "0").lower() in ("1", "true", "on"):
        c.ajouter("Réglages", f"Protection du document : {protection.get(q('w', 'edit'), 'non précisée')} "
                  "(une protection sans mot de passe fort se retire facilement).")


def _exif_jpeg(donnees: bytes) -> bool:
    if not donnees.startswith(b"\xff\xd8"):
        return False
    i = 2
    while i + 4 <= len(donnees) and donnees[i] == 0xFF:
        marqueur, longueur = donnees[i + 1], int.from_bytes(donnees[i + 2:i + 4], "big")
        if marqueur == 0xE1 and (donnees[i + 4:i + 10] == b"Exif\x00\x00"
                                 or donnees[i + 4:i + 33] == b"http://ns.adobe.com/xap/1.0/\x00"):
            return True
        if marqueur == 0xDA or longueur < 2:
            break
        i += 2 + longueur
    return False


def _meta_png(donnees: bytes) -> list[str]:
    if not donnees.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    trouves, i = [], 8
    while i + 8 <= len(donnees):
        longueur = int.from_bytes(donnees[i:i + 4], "big")
        genre = donnees[i + 4:i + 8].decode("latin-1")
        if genre in ("tEXt", "iTXt", "zTXt", "eXIf"):
            trouves.append(genre)
        if genre == "IEND":
            break
        i += 12 + longueur
    return trouves


def controle_images(p: PaquetDocx, c: Controle, cfg: dict) -> None:
    images = [n for n in p.noms if n.lower().startswith("word/media/")]
    autres = 0
    for nom in images:
        donnees = p.octets(nom) or b""
        if _exif_jpeg(donnees):
            c.ajouter("Images", f"{posixpath.basename(nom)} : métadonnées EXIF ou XMP (appareil, logiciel, date, parfois position GPS)")
        elif _meta_png(donnees):
            c.ajouter("Images", f"{posixpath.basename(nom)} : métadonnées texte PNG ({', '.join(_meta_png(donnees))})")
        elif not nom.lower().endswith((".jpg", ".jpeg", ".png")):
            autres += 1
    if autres:
        c.note = f"{autres} image(s) dans un autre format (EMF, GIF, SVG…) : métadonnées non vérifiées."


# --- Catalogue ----------------------------------------------------------------

CATALOGUE: list[tuple[str, str, str, str, str, Callable]] = [
    ("commentaires", "Commentaires", IMPORTANT,
     "Les commentaires restent dans le fichier envoyé et révèlent souvent des positions internes.",
     "Supprimez les commentaires (Révision > Supprimer > Supprimer tous les commentaires) sur la copie à envoyer.",
     controle_commentaires),
    ("modifications", "Modifications suivies non acceptées", IMPORTANT,
     "Le destinataire peut afficher les textes supprimés et les auteurs de chaque modification.",
     "Acceptez ou refusez toutes les modifications, sauf si l'envoi d'une version en mode révision est voulu.",
     controle_modifications),
    ("texte_masque", "Texte masqué ou invisible", IMPORTANT,
     "Un texte masqué, écrit en blanc ou en taille minuscule reste lisible pour qui le cherche.",
     "Affichez les marques de mise en forme (Ctrl+Maj+8) et supprimez ces passages.",
     controle_texte_masque),
    ("marqueurs", "Marqueurs à compléter et texte surligné", IMPORTANT,
     "Un blanc à compléter ou une note surlignée signale un document inachevé.",
     "Complétez ou retirez chaque marqueur, et retirez les surlignages de travail.",
     controle_marqueurs),
    ("termes", "Noms d'autres dossiers", IMPORTANT,
     "Un nom d'un autre client ou d'un autre dossier dans le fichier peut violer le secret professionnel.",
     "Retirez chaque occurrence, y compris dans les propriétés et les noms d'éléments internes.",
     controle_termes),
    ("macros", "Macros", IMPORTANT,
     "Un document à macros peut être bloqué par le destinataire et contenir du code inattendu.",
     "Enregistrez une copie au format .docx sans macros.",
     controle_macros),
    ("proprietes", "Propriétés du document", A_EXAMINER,
     "Auteur, société, titre et propriétés personnalisées voyagent avec le fichier.",
     "Utilisez Fichier > Informations > Inspecter le document, ou corrigez les propriétés à la main.",
     controle_proprietes),
    ("personnes", "Personnes mentionnées dans le fichier", A_EXAMINER,
     "Synthèse des noms qui apparaissent comme auteurs de commentaires, de modifications ou du document.",
     "Vérifiez que chaque nom peut être communiqué au destinataire.",
     controle_personnes),
    ("champs", "Champs révélateurs", A_EXAMINER,
     "Certains champs affichent ou recalculent le nom du fichier, son chemin ou l'auteur.",
     "Sélectionnez le champ et convertissez-le en texte (Ctrl+Maj+F9), ou supprimez-le.",
     controle_champs),
    ("liens", "Liens et chemins externes", A_EXAMINER,
     "Un lien vers un serveur, un modèle ou un site interne révèle l'organisation de vos fichiers.",
     "Supprimez les liens non voulus ; détachez le modèle (Développeur > Modèle de document).",
     controle_liens),
    ("objets", "Objets incorporés", A_EXAMINER,
     "Un tableau Excel ou un autre fichier incorporé peut contenir bien plus que ce qui est affiché.",
     "Ouvrez chaque objet, ou remplacez-le par une image ou un tableau Word.",
     controle_objets),
    ("reglages", "Réglages et variables du document", A_EXAMINER,
     "Les variables de document sont invisibles à l'écran mais lisibles dans le fichier.",
     "Supprimez les variables par une macro dédiée ou repartez d'une copie propre ; désactivez le suivi si nécessaire.",
     controle_reglages),
    ("images", "Métadonnées des images", A_EXAMINER,
     "Une photo peut contenir l'appareil, la date et parfois la position GPS de la prise de vue.",
     "Remplacez l'image par une version sans métadonnées (capture d'écran ou export).",
     controle_images),
    ("notes", "Notes de bas de page et de fin", INFORMATION,
     "Les notes sont souvent oubliées lors de la relecture finale.",
     "Relisez chaque note listée.",
     controle_notes),
]


def executer(p: PaquetDocx, cfg: dict) -> list[Controle]:
    resultats = []
    for ident, titre, gravite, pourquoi, conseil, fonction in CATALOGUE:
        c = Controle(ident, titre, gravite, pourquoi, conseil)
        try:
            fonction(p, c, cfg)
        except ErreurLecture as e:
            c.statut, c.constats, c.note = ERREUR, [], e.message
        except Exception as e:  # un contrôle en échec ne doit jamais passer pour un contrôle réussi
            c.statut, c.constats, c.note = ERREUR, [], f"Erreur inattendue pendant ce contrôle ({type(e).__name__})."
        resultats.append(c)
    return resultats
