"""Construit les téléchargements de « Gouvernance de l'IA » à partir des pages du site.

    python outils/gouvernance-ia/telechargements/generer_telechargements.py [--copier-site] [--sortie DOSSIER]

Produit, pour chaque langue, le pack complet en zip, la charte modèle en .docx et le kit
« petit cabinet » (les six éléments du niveau 1), plus la copie du tableur versionné. Rien n'est
inventé ici : le contenu vient des pages de `site/content/outils/gouvernance-ia/` et du
référentiel `referentiel/gouvernance-ia.json`. Le script échoue si un intertitre attendu a
disparu d'une page, pour qu'une modification du site ne produise pas un téléchargement muet.

Bibliothèque standard seule (ADR-010). Les fichiers produits sont identiques octet par octet
d'une machine à l'autre (dates fixes, ordre trié, fins de ligne normalisées), comme les archives
de `scripts/empaqueter.py` : leur empreinte SHA-256 peut donc être publiée.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ICI = Path(__file__).resolve().parent
OUTIL = ICI.parent
DEPOT = ICI.parents[2]
PAGES = DEPOT / "site" / "content" / "outils" / "gouvernance-ia"
REFERENTIEL = OUTIL / "referentiel" / "gouvernance-ia.json"
TABLEURS = OUTIL / "tableur"
SORTIE_SITE = DEPOT / "site" / "static" / "telechargements"

DATE_ZIP = (2026, 1, 1, 0, 0, 0)  # même convention que scripts/empaqueter.py
SITE = "https://jerlash.eu"


# --------------------------------------------------------------------------------------
# Paramètres de langue : adresses des pages, noms des fichiers produits, intertitres repris
# et textes de liaison. Les textes de liaison sont les seules phrases écrites ici ; tout le
# reste est extrait des pages.
# --------------------------------------------------------------------------------------

LANGUES = {
    "fr": {
        "suffixe": "",
        "base": "/fr/outils/gouvernance-ia/",
        "pack": "gouvernance-ia-{v}.zip",
        "charte": "gouvernance-ia-charte-modele-{v}.docx",
        "kit": "gouvernance-ia-kit-petit-cabinet-{v}.zip",
        "dossier_kit": "kit-petit-cabinet",
        "lisez_moi": "LISEZ-MOI.md",
        "licence_fichier": "LICENCE.txt",
        "licence_nom": "Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International (CC BY-NC 4.0)",
        "licence_texte": "https://creativecommons.org/licenses/by-nc/4.0/legalcode.fr",
        "licence_resume": "https://creativecommons.org/licenses/by-nc/4.0/deed.fr",
        "titres": {
            "six": ("niveau-1", "Les six éléments"),
            "fiche": ("niveau-1", "La fiche de conformité d'un outil"),
            "verifier": ("supervision", "Vérifier un livrable juridique"),
            "refuser": ("supervision", "Quand refuser ou escalader"),
            "procedure": ("operations", "La procédure"),
            "fiche_incident": ("operations", "Fiche rapide d'incident"),
            "modules": ("operations", "Les modules"),
            "evaluation": ("operations", "L'évaluation"),
        },
        "textes": {
            "pack_titre": "Gouvernance de l'IA {v} : pack complet",
            "pack_intro": (
                "Ce pack rassemble la boîte à outils « Gouvernance de l'IA » telle qu'elle est publiée sur "
                "{url}, à la date de sa version {v}. Il ne contient aucune donnée : les formulaires et les "
                "registres sont vides, les exemples sont fictifs."
            ),
            "pack_contenu": "Ce que contient le pack",
            "pack_usage": "Comment s'en servir",
            "pack_usage_texte": (
                "Commencez par la page de présentation (`pages/00-...`), qui donne le diagnostic du niveau de "
                "gouvernance. Au niveau 1, le dossier `{kit}` suffit. Aux niveaux 2 et 3, ouvrez le tableur et "
                "suivez les modules dans l'ordre du parcours ; la charte vient en dernier."
            ),
            "avertissement": "Avertissement",
            "deux_points": " : ",
            "licence": "Licence",
            "attribution": "Attribution demandée",
            "source": "Version en ligne, toujours à jour",
            "pages": "Les pages de la boîte à outils, en Markdown",
            "kit_titre": "Kit « petit cabinet » {v} : les six éléments du niveau 1",
            "kit_intro": (
                "Ce kit regroupe les six éléments du minimum opérationnel décrits sur la page « Le niveau 1 » de "
                "la boîte à outils « Gouvernance de l'IA » ({url}). Il s'adresse à une organisation dont chaque "
                "outil d'IA est conforme, ou ne reçoit que des données publiques ou internes non sensibles "
                "(classes D0 et D1). Les textes repris ici viennent des pages de la boîte à outils ; les "
                "formulaires sont vides."
            ),
            "kit_fichiers": "Les fichiers du kit",
            "kit_rappel": (
                "Le niveau n'est pas acquis une fois pour toutes. Refaites le diagnostic à chaque nouvel outil, "
                "contrat, catégorie de données ou incident, et au moins une fois par an. Une charte courte suffit "
                "au niveau 1 : les articles 1, 2, 3, 5, 7, 8, 14 et 16 de la charte modèle en .docx couvrent "
                "l'essentiel."
            ),
            "kit_secret": (
                "Ne saisissez jamais de nom de client ni d'élément couvert par le secret professionnel dans ces "
                "formulaires : utilisez des références internes. Les pièces détaillées restent dans le dossier "
                "sécurisé de l'organisation."
            ),
            "autres": "Les autres éléments",
            "guillemets": ("« ", " »"),
            "kit_1_titre": "1. Le référent",
            "kit_1_forme": "Désignation",
            "kit_2_titre": "2. L'inventaire des outils",
            "kit_2_intro": (
                "Une ligne par outil, dans le fichier `{csv}` (séparateur : point-virgule). La conformité et le "
                "niveau de l'outil se lisent sur la fiche de conformité."
            ),
            "kit_3_titre": "3. La fiche de conformité d'un outil",
            "kit_4_titre": "4. La règle de vérification des productions",
            "kit_5_titre": "5. Le canal d'incident",
            "kit_5_forme": "Le point de contact de l'organisation",
            "kit_6_titre": "6. La formation courte",
            "kit_6_intro": (
                "Au niveau 1, la formation porte sur les modules F1 à F3 : les limites des outils, la "
                "confidentialité et la vérification des sources."
            ),
            "kit_6_suivi": "Suivi des formations",
            "kit_6_suivi_texte": (
                "Une ligne par personne et par module dans le fichier `{csv}` (séparateur : point-virgule). Le "
                "registre contient des données sur les membres du personnel : l'accès y est limité."
            ),
            "colonnes": "Colonnes",
            "registres_titre": "Registres vides",
            "registres_intro": (
                "Fichiers CSV séparés par des points-virgules, qui ne contiennent que leurs en-têtes. Ils sont "
                "conçus pour le registre de gouvernance : les références de dossier y sont internes et les "
                "preuves détaillées restent dans le dossier sécurisé."
            ),
            "tableur": "Le tableur des niveaux 2 et 3",
            "docx_source": "Texte de référence, toujours à jour : {url}",
            "docx_licence": "{nom} — Éditeur : {editeur} — Licence : {licence}",
        },
        "champs": {
            "nom_fonction": "Nom et fonction",
            "date": "Date",
            "remplir": "À compléter",
            "role": "Rôle",
            "mission": "Mission",
            "personne": "Personne (fonction)",
            "supplant": "Suppléant",
            "module": "Module",
            "public": "Public",
            "competence": "Compétence observable",
            "rubrique": "Rubrique",
        },
        "csv_inventaire": [
            "outil", "fournisseur", "formule_souscrite", "utilisateurs", "date_fiche_conformite",
            "conformite", "classe_la_plus_sensible_recue", "agit_seul", "niveau_de_l_outil",
            "validee_par", "reexamen",
        ],
        "csv_formations": ["personne_id_interne", "role", "module", "date_formation", "date_reexamen", "validateur"],
    },
    "en": {
        "suffixe": ".en",
        "base": "/en/tools/ai-governance/",
        "pack": "ai-governance-{v}.zip",
        "charte": "ai-governance-model-charter-{v}.docx",
        "kit": "ai-governance-small-firm-kit-{v}.zip",
        "dossier_kit": "small-firm-kit",
        "lisez_moi": "READ-ME.md",
        "licence_fichier": "LICENCE.txt",
        "licence_nom": "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
        "licence_texte": "https://creativecommons.org/licenses/by-nc/4.0/legalcode.en",
        "licence_resume": "https://creativecommons.org/licenses/by-nc/4.0/deed.en",
        "titres": {
            "six": ("niveau-1", "The six elements"),
            "fiche": ("niveau-1", "The compliance sheet for a tool"),
            "verifier": ("supervision", "Checking a legal deliverable"),
            "refuser": ("supervision", "When to refuse or escalate"),
            "procedure": ("operations", "The procedure"),
            "fiche_incident": ("operations", "Quick incident sheet"),
            "modules": ("operations", "The modules"),
            "evaluation": ("operations", "The assessment"),
        },
        "textes": {
            "pack_titre": "AI governance {v}: full pack",
            "pack_intro": (
                "This pack brings together the “AI governance” toolkit as published on {url}, at the date of its "
                "version {v}. It contains no data: the forms and registers are empty and the examples are "
                "fictitious."
            ),
            "pack_contenu": "What the pack contains",
            "pack_usage": "How to use it",
            "pack_usage_texte": (
                "Start with the presentation page (`pages/00-...`), which gives the governance level diagnosis. At "
                "level 1, the `{kit}` folder is enough. At levels 2 and 3, open the spreadsheet and follow the "
                "modules in the order of the path; the charter comes last."
            ),
            "avertissement": "Warning",
            "deux_points": ": ",
            # Traduction de « avertissement » du référentiel, qui n'existe qu'en français (ADR-023).
            "avertissement_texte": (
                "Working version. Neither an adopted charter, nor a compliance label, nor individual legal advice. "
                "The levels, thresholds, weightings and roles are proposals that each organisation sets for "
                "itself. No real client data, no material covered by professional secrecy."
            ),
            "licence": "Licence",
            "attribution": "Attribution requested",
            "source": "Online version, always up to date",
            "pages": "The toolkit pages, in Markdown",
            "kit_titre": "Small firm kit {v}: the six elements of level 1",
            "kit_intro": (
                "This kit brings together the six elements of the minimum set described on the “Level 1” page of "
                "the “AI governance” toolkit ({url}). It is intended for an organisation in which each AI tool is "
                "compliant, or receives only public or non-sensitive internal data (classes D0 and D1). The texts "
                "reproduced here come from the toolkit pages; the forms are empty."
            ),
            "kit_fichiers": "The files in the kit",
            "kit_rappel": (
                "The level is not acquired once and for all. Run the diagnosis again at each new tool, contract, "
                "data category or incident, and at least once a year. A short charter is enough at level 1: "
                "articles 1, 2, 3, 5, 7, 8, 14 and 16 of the model charter in .docx cover the essentials."
            ),
            "kit_secret": (
                "Never enter a client name or any material covered by professional secrecy in these forms: use "
                "internal references. Detailed documents stay in the organisation's secure file."
            ),
            "autres": "The other items",
            "guillemets": ("“", "”"),
            "kit_1_titre": "1. The AI lead",
            "kit_1_forme": "Appointment",
            "kit_2_titre": "2. The inventory of tools",
            "kit_2_intro": (
                "One row per tool, in the file `{csv}` (separator: semicolon). The compliance and the level of the "
                "tool are read from the compliance sheet."
            ),
            "kit_3_titre": "3. The compliance sheet for a tool",
            "kit_4_titre": "4. The rule for checking outputs",
            "kit_5_titre": "5. The incident channel",
            "kit_5_forme": "The organisation's point of contact",
            "kit_6_titre": "6. The short training",
            "kit_6_intro": (
                "At level 1, training covers modules F1 to F3: the limits of the tools, confidentiality and the "
                "checking of sources."
            ),
            "kit_6_suivi": "Training record",
            "kit_6_suivi_texte": (
                "One row per person and per module in the file `{csv}` (separator: semicolon). The record contains "
                "data about staff members: access to it is restricted."
            ),
            "colonnes": "Columns",
            "registres_titre": "Empty registers",
            "registres_intro": (
                "Semicolon-separated CSV files containing only their headers. They are designed for the governance "
                "register: case references are internal and detailed evidence stays in the secure file."
            ),
            "tableur": "The spreadsheet for levels 2 and 3 (in French)",
            "docx_source": "Reference text, always up to date: {url}",
            "docx_licence": "{nom} — Publisher: {editeur} — Licence: {licence}",
        },
        "champs": {
            "nom_fonction": "Name and position",
            "date": "Date",
            "remplir": "To be completed",
            "role": "Role",
            "mission": "Mission",
            "personne": "Person (position)",
            "supplant": "Deputy",
            "module": "Module",
            "public": "Audience",
            "competence": "Observable skill",
            "rubrique": "Item",
        },
        "csv_inventaire": [
            "tool", "provider", "subscribed_plan", "users", "compliance_sheet_date", "compliance",
            "most_sensitive_class_received", "acts_alone", "tool_level", "validated_by", "review",
        ],
        "csv_formations": ["person_internal_id", "role", "module", "training_date", "review_date", "validator"],
    },
}

NOMS_KIT = {
    "fr": {
        "lisez_moi": "0-LISEZ-MOI.md",
        1: "1-referent.md",
        2: "2-inventaire-des-outils.md",
        "inventaire": "2-inventaire-des-outils.csv",
        3: "3-fiche-de-conformite.md",
        4: "4-regle-de-verification-des-productions.md",
        5: "5-canal-d-incident.md",
        6: "6-formation-courte.md",
        "suivi": "6-suivi-des-formations.csv",
    },
    "en": {
        "lisez_moi": "0-READ-ME.md",
        1: "1-ai-lead.md",
        2: "2-inventory-of-tools.md",
        "inventaire": "2-inventory-of-tools.csv",
        3: "3-compliance-sheet.md",
        4: "4-rule-for-checking-outputs.md",
        5: "5-incident-channel.md",
        6: "6-short-training.md",
        "suivi": "6-training-record.csv",
    },
}


# --------------------------------------------------------------------------------------
# Lecture des pages
# --------------------------------------------------------------------------------------

class Page:
    def __init__(self, nom: str, chemin: Path):
        self.nom = nom
        texte = chemin.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", texte, re.DOTALL)
        if not m:
            raise SystemExit(f"{chemin} : front matter introuvable")
        self.entete, self.corps = m.group(1), m.group(2).strip("\n")
        self.titre = self.champ("title") or nom
        self.poids = int(self.champ("weight") or 0)
        self.url = self.champ("url")

    def champ(self, cle: str) -> str | None:
        m = re.search(rf'^{cle}:\s*"?([^"\n]*)"?\s*$', self.entete, re.MULTILINE)
        return m.group(1).strip() if m else None

    def section(self, titre: str) -> str:
        """Corps d'un intertitre, sans son titre et sans les sous-sections suivantes de même rang."""
        m = re.search(rf"^(#{{2,3}}) {re.escape(titre)}\s*$", self.corps, re.MULTILINE)
        if not m:
            raise SystemExit(f"{self.nom} : intertitre « {titre} » introuvable (page modifiée ?)")
        rang = len(m.group(1))
        suite = self.corps[m.end():]
        fin = re.search(rf"^#{{1,{rang}}} ", suite, re.MULTILINE)
        return (suite[:fin.start()] if fin else suite).strip("\n")


def lire_pages(langue: str) -> dict[str, Page]:
    suffixe = LANGUES[langue]["suffixe"]
    pages = {}
    for chemin in sorted(PAGES.glob("*.md")):
        nom = chemin.name[:-3]
        if suffixe:
            if not nom.endswith(suffixe):
                continue
            nom = nom[: -len(suffixe)]
        elif nom.endswith(".en"):
            continue
        pages[nom] = Page(nom, chemin)
    manquantes = {"_index", "niveau-1", "supervision", "operations", "charte"} - set(pages)
    if manquantes:
        raise SystemExit(f"pages manquantes en {langue} : {', '.join(sorted(manquantes))}")
    return pages


def adresses(langue: str, pages: dict[str, Page]) -> dict[str, str]:
    """Adresse publique de chaque page, pour réécrire les liens relatifs en liens absolus."""
    base = LANGUES[langue]["base"]
    url = {}
    for nom, page in pages.items():
        if nom == "_index":
            url[""] = SITE + base
        else:
            url[nom] = SITE + (page.url if page.url else base + nom + "/")
    return url


def reecrire_liens(texte: str, url: dict[str, str], propre: str) -> str:
    """Rend les liens utilisables hors du site : adresses absolues, téléchargements inclus."""

    def cible(destination: str) -> str:
        chemin, _, ancre = destination.partition("#")
        ancre = ("#" + ancre) if ancre else ""
        if chemin.startswith("/telechargements/"):
            return SITE + chemin + ancre
        if chemin.startswith("http") or chemin.startswith("mailto:"):
            return destination
        if not chemin:
            return propre + ancre
        nom = chemin.strip("/").split("/")[-1]
        if nom in ("outils", "gouvernance-ia", "tools", "ai-governance"):
            nom = ""
        if nom in url:
            return url[nom] + ancre
        if chemin.startswith("/"):
            return SITE + chemin + ancre
        raise SystemExit(f"lien non résolu : {destination}")

    return re.sub(r"\]\(([^)]+)\)", lambda m: "](" + cible(m.group(1)) + ")", texte)


# --------------------------------------------------------------------------------------
# Markdown : analyse en blocs (pour le .docx) et export autonome (pour le zip)
# --------------------------------------------------------------------------------------

def blocs(markdown: str) -> list[tuple]:
    """Découpe un sous-ensemble de Markdown : titres, paragraphes, listes, tableaux, blocs de code."""
    resultat: list[tuple] = []
    lignes = markdown.split("\n")
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        if not ligne.strip():
            i += 1
            continue
        if ligne.startswith("```"):
            j = i + 1
            while j < len(lignes) and not lignes[j].startswith("```"):
                j += 1
            resultat.append(("code", "\n".join(lignes[i + 1:j])))
            i = j + 1
            continue
        if ligne.startswith("#"):
            rang = len(ligne) - len(ligne.lstrip("#"))
            resultat.append(("titre", rang, ligne[rang:].strip()))
            i += 1
            continue
        if ligne.lstrip().startswith("|"):
            table = []
            while i < len(lignes) and lignes[i].lstrip().startswith("|"):
                cellules = [c.strip() for c in lignes[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cellules):
                    table.append(cellules)
                i += 1
            resultat.append(("table", table))
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", ligne):
            items = []
            while i < len(lignes) and re.match(r"^\s*([-*]|\d+\.)\s+", lignes[i]):
                m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", lignes[i])
                marque = "•" if m.group(1) in ("-", "*") else m.group(1)
                texte = m.group(2)
                i += 1
                while i < len(lignes) and lignes[i].strip() and not re.match(r"^\s*([-*]|\d+\.)\s+", lignes[i]) \
                        and not lignes[i].lstrip().startswith(("|", "#", "```")):
                    texte += " " + lignes[i].strip()
                    i += 1
                items.append((marque, texte))
            resultat.append(("liste", items))
            continue
        para = [ligne.strip()]
        i += 1
        while i < len(lignes) and lignes[i].strip() and not lignes[i].lstrip().startswith(("|", "#", "```")) \
                and not re.match(r"^\s*([-*]|\d+\.)\s+", lignes[i]):
            para.append(lignes[i].strip())
            i += 1
        resultat.append(("para", " ".join(para)))
    return resultat


def page_autonome(page: Page, url: dict[str, str], propre: str) -> str:
    corps = reecrire_liens(page.corps, url, propre)
    return f"# {page.titre}\n\n{corps}\n"


# --------------------------------------------------------------------------------------
# Production du .docx (WordprocessingML minimal, sans dépendance)
# --------------------------------------------------------------------------------------

STYLES_DOCX = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>\
<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="{langue}"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:spacing w:before="0" w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>\
<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="0"/><w:keepNext/>\
<w:spacing w:before="320" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>\
<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="1"/><w:keepNext/>\
<w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="25"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/>\
<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:ind w:left="567" w:hanging="283"/>\
<w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/>\
<w:rPr><w:i/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>\
<w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/>\
<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>\
<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>\
</w:tblBorders></w:tblPr></w:style>
</w:styles>
"""

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" \
ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" \
ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" \
Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

RELS_DOCUMENT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" \
Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


def runs(texte: str) -> str:
    """Convertit le gras, l'italique, le code et les liens d'une ligne en séries Word."""
    texte = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", texte)  # le lien devient son libellé
    morceaux = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", texte)
    sortie = []
    for morceau in morceaux:
        if not morceau:
            continue
        style = ""
        if morceau.startswith("**") and morceau.endswith("**"):
            morceau, style = morceau[2:-2], "<w:b/>"
        elif morceau.startswith("*") and morceau.endswith("*"):
            morceau, style = morceau[1:-1], "<w:i/>"
        elif morceau.startswith("`") and morceau.endswith("`"):
            morceau, style = morceau[1:-1], '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
        rpr = f"<w:rPr>{style}</w:rPr>" if style else ""
        sortie.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(morceau)}</w:t></w:r>')
    return "".join(sortie) or '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def paragraphe(texte: str, style: str = "") -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{runs(texte)}</w:p>"


def tableau(lignes: list[list[str]]) -> str:
    colonnes = max(len(l) for l in lignes)
    largeur = 9070 // colonnes
    grille = "".join(f'<w:gridCol w:w="{largeur}"/>' for _ in range(colonnes))
    corps = []
    for rang, ligne in enumerate(lignes):
        cellules = []
        for col in range(colonnes):
            texte = ligne[col] if col < len(ligne) else ""
            contenu = f"<w:p>{runs('**' + texte + '**' if rang == 0 and texte else texte)}</w:p>"
            cellules.append(f'<w:tc><w:tcPr><w:tcW w:w="{largeur}" w:type="dxa"/></w:tcPr>{contenu}</w:tc>')
        entete = '<w:trPr><w:tblHeader/></w:trPr>' if rang == 0 else ""
        corps.append(f"<w:tr>{entete}{''.join(cellules)}</w:tr>")
    return ('<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/></w:tblPr>'
            f"<w:tblGrid>{grille}</w:tblGrid>{''.join(corps)}</w:tbl><w:p/>")


def docx(titre: str, markdown: str, notes: list[str], langue: str) -> bytes:
    corps = [paragraphe(titre, "Title")]
    for bloc in blocs(markdown):
        if bloc[0] == "titre":
            corps.append(paragraphe(bloc[2], "Heading1" if bloc[1] <= 2 else "Heading2"))
        elif bloc[0] == "para":
            corps.append(paragraphe(bloc[1]))
        elif bloc[0] == "liste":
            corps += [paragraphe(f"{marque}\t{texte}", "ListParagraph") for marque, texte in bloc[1]]
        elif bloc[0] == "table":
            corps.append(tableau(bloc[1]))
        elif bloc[0] == "code":
            corps += [paragraphe(f"`{ligne}`") for ligne in bloc[1].split("\n")]
    corps += [paragraphe(note, "Note") for note in notes]
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
        + "".join(corps)
        + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
        'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr></w:body></w:document>'
    )
    parties = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": RELS,
        "word/document.xml": document,
        "word/_rels/document.xml.rels": RELS_DOCUMENT,
        "word/styles.xml": STYLES_DOCX.format(langue="fr-BE" if langue == "fr" else "en-GB"),
    }
    return archive(parties, prefixe="")


# --------------------------------------------------------------------------------------
# Archives reproductibles
# --------------------------------------------------------------------------------------

def archive(fichiers: dict[str, str | bytes], prefixe: str) -> bytes:
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for relatif in sorted(fichiers):
            donnees = fichiers[relatif]
            if isinstance(donnees, str):
                donnees = donnees.replace("\r\n", "\n").encode("utf-8")
            info = zipfile.ZipInfo(prefixe + relatif, DATE_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix partout : l'empreinte ne dépend pas du système
            info.external_attr = 0o644 << 16
            z.writestr(info, donnees)
    return sortie.getvalue()


def csv_entetes(colonnes: list[str]) -> str:
    return ";".join(colonnes) + "\n"


# --------------------------------------------------------------------------------------
# Contenus produits
# --------------------------------------------------------------------------------------

def avertissement(langue: str, ref: dict) -> str:
    """L'avertissement du référentiel, dans la langue de la publication."""
    return LANGUES[langue]["textes"].get("avertissement_texte") or ref["avertissement"]


def licence(langue: str, ref: dict, nom: str) -> str:
    cfg, t = LANGUES[langue], LANGUES[langue]["textes"]
    url = SITE + cfg["base"]
    ouvrant, fermant = t["guillemets"]
    return "\n".join([
        f"{nom} {ref['version']}",
        f"{t['licence']}{t['deux_points']}{cfg['licence_nom']}",
        f"  {cfg['licence_texte']}",
        f"  {cfg['licence_resume']}",
        "",
        f"{t['attribution']}{t['deux_points']}{ouvrant}{nom} {ref['version']}, {ref['editeur']}, {url}{fermant}",
        "",
        f"{t['avertissement']}{t['deux_points']}{avertissement(langue, ref)}",
        "",
        f"{t['source']}{t['deux_points']}{url}",
        "",
    ])


def kit(langue: str, pages: dict[str, Page], ref: dict, url: dict[str, str]) -> dict[str, str]:
    """Les six éléments du niveau 1, repris des pages de la boîte à outils."""
    cfg, t, ch = LANGUES[langue], LANGUES[langue]["textes"], LANGUES[langue]["champs"]
    noms, titres = NOMS_KIT[langue], cfg["titres"]

    def section(cle: str) -> str:
        page, titre = titres[cle]
        return reecrire_liens(pages[page].section(titre), url, url[page])

    def forme(lignes: list[str]) -> str:
        return "\n".join([f"| {ch['rubrique']} | {ch['remplir']} |", "| --- | --- |"]
                         + [f"| {l} | |" for l in lignes])

    six = section("six")
    element = {}
    for numero, ligne in enumerate(re.findall(r"^\d+\.\s+(.*(?:\n(?!\d+\.\s|\s*$).*)*)", six, re.MULTILINE), start=1):
        element[numero] = " ".join(l.strip() for l in ligne.split("\n"))

    roles = "\n".join([f"| {ch['role']} | {ch['mission']} |", "| --- | --- |"]
                      + [f"| {r['role']} | {r['mission']} |" for r in ref["roles_reduits"]])

    modules = [l for l in section("modules").split("\n") if l.startswith("|")]
    modules_f1_f3 = modules[:2] + [l for l in modules[2:] if re.match(r"\|\s*F[123],", l)]

    fichiers = {
        noms[1]: "\n".join([
            f"# {t['kit_1_titre']}", "", element[1], "",
            f"## {t['kit_1_forme']}", "",
            forme([ch["personne"], ch["supplant"], ch["date"]]), "",
            roles, "",
        ]),
        noms[2]: "\n".join([
            f"# {t['kit_2_titre']}", "", element[2], "",
            t["kit_2_intro"].format(csv=noms["inventaire"]), "",
            f"## {t['colonnes']}", "",
            "\n".join(f"- `{c}`" for c in cfg["csv_inventaire"]), "",
        ]),
        noms["inventaire"]: csv_entetes(cfg["csv_inventaire"]),
        noms[3]: "\n".join([f"# {t['kit_3_titre']}", "", element[3], "", section("fiche"), ""]),
        noms[4]: "\n".join([
            f"# {t['kit_4_titre']}", "", element[4], "",
            f"## {titres['verifier'][1]}", "", section("verifier"), "",
            f"## {titres['refuser'][1]}", "", section("refuser"), "",
        ]),
        noms[5]: "\n".join([
            f"# {t['kit_5_titre']}", "", element[5], "",
            f"## {t['kit_5_forme']}", "",
            forme([ch["nom_fonction"], ch["date"]]), "",
            f"## {titres['procedure'][1]}", "", section("procedure"), "",
            f"## {titres['fiche_incident'][1]}", "", section("fiche_incident"), "",
        ]),
        noms[6]: "\n".join([
            f"# {t['kit_6_titre']}", "", element[6], "", t["kit_6_intro"], "",
            f"## {titres['modules'][1]}", "", "\n".join(modules_f1_f3), "",
            f"## {titres['evaluation'][1]}", "", section("evaluation"), "",
            f"## {t['kit_6_suivi']}", "",
            t["kit_6_suivi_texte"].format(csv=noms["suivi"]), "",
        ]),
        noms["suivi"]: csv_entetes(cfg["csv_formations"]),
    }

    sommaire = "\n".join(
        f"- `{nom}` — {titre}" for nom, titre in [
            (noms[1], t["kit_1_titre"]), (noms[2], t["kit_2_titre"]), (noms[3], t["kit_3_titre"]),
            (noms[4], t["kit_4_titre"]), (noms[5], t["kit_5_titre"]), (noms[6], t["kit_6_titre"]),
        ])
    fichiers[noms["lisez_moi"]] = "\n".join([
        f"# {t['kit_titre'].format(v=ref['version'])}", "",
        t["kit_intro"].format(url=SITE + cfg["base"]), "",
        f"## {t['kit_fichiers']}", "", sommaire, "",
        t["kit_rappel"], "",
        t["kit_secret"], "",
        f"## {t['licence']}", "",
        f"{cfg['licence_nom']} — {ref['editeur']} — {cfg['licence_resume']}", "",
        f"{t['avertissement']}{t['deux_points']}{avertissement(langue, ref)}", "",
    ])
    return fichiers


def pack(langue: str, pages: dict[str, Page], ref: dict, url: dict[str, str],
         charte_docx: bytes, fichiers_kit: dict[str, str], tableur: Path) -> dict[str, str | bytes]:
    cfg, t = LANGUES[langue], LANGUES[langue]["textes"]
    fichiers: dict[str, str | bytes] = {}

    ordre = sorted(pages.values(), key=lambda p: (p.nom != "_index", p.poids, p.nom))
    sommaire = []
    for rang, page in enumerate(ordre):
        nom = f"pages/{rang:02d}-{'presentation' if page.nom == '_index' else page.nom}.md"
        propre = url[""] if page.nom == "_index" else url[page.nom]
        fichiers[nom] = page_autonome(page, url, propre)
        sommaire.append(f"- `{nom}` — {page.titre}")

    for nom, contenu in fichiers_kit.items():
        fichiers[f"{cfg['dossier_kit']}/{nom}"] = contenu

    charte_nom = cfg["charte"].format(v=ref["version"])
    fichiers[charte_nom] = charte_docx
    fichiers[f"referentiel/{REFERENTIEL.name}"] = REFERENTIEL.read_text(encoding="utf-8")
    fichiers[f"tableur/{tableur.name}"] = tableur.read_bytes()

    registres = {
        "REGISTRE_HOMOLOGATIONS.csv": ref["registres"]["homologations"],
        "REGISTRE_INCIDENTS.csv": ref["registres"]["incidents"],
        "REGISTRE_USAGES_SIGNIFICATIFS.csv": ref["registres"]["usages_significatifs"],
        "REGISTRE_FORMATIONS.csv": ref["registres"]["formations"],
    }
    for nom, colonnes in registres.items():
        fichiers[f"registres/{nom}"] = csv_entetes(colonnes)

    fichiers[cfg["licence_fichier"]] = licence(langue, ref, pages["_index"].titre)
    fichiers[cfg["lisez_moi"]] = "\n".join([
        f"# {t['pack_titre'].format(v=ref['version'])}", "",
        t["pack_intro"].format(url=SITE + cfg["base"], v=ref["version"]), "",
        f"## {t['pack_contenu']}", "",
        f"### {t['pages']}", "", "\n".join(sommaire), "",
        f"### {t['autres']}", "",
        f"- `{cfg['dossier_kit']}/` — {t['kit_titre'].format(v=ref['version'])}",
        f"- `{charte_nom}` — {pages['charte'].titre}",
        f"- `tableur/{tableur.name}` — {t['tableur']}",
        f"- `referentiel/{REFERENTIEL.name}`",
        "",
        f"### {t['registres_titre']}", "", t["registres_intro"], "",
        "\n".join(f"- `registres/{nom}`" for nom in sorted(registres)), "",
        f"## {t['pack_usage']}", "", t["pack_usage_texte"].format(kit=cfg["dossier_kit"]), "",
        f"## {t['licence']}", "",
        f"{cfg['licence_nom']} — {ref['editeur']} — {cfg['licence_resume']}", "",
        f"{t['avertissement']}{t['deux_points']}{avertissement(langue, ref)}", "",
        f"{t['source']}{t['deux_points']}{SITE + cfg['base']}", "",
    ])
    return fichiers


def generer() -> dict[str, bytes]:
    ref = json.loads(REFERENTIEL.read_text(encoding="utf-8"))
    version = ref["version"]
    tableurs = sorted(TABLEURS.glob(f"gouvernance-ia-matrices-{version}.xlsx"))
    if not tableurs:
        raise SystemExit(f"tableur de la version {version} introuvable dans {TABLEURS}")
    tableur = tableurs[0]

    produits: dict[str, bytes] = {tableur.name: tableur.read_bytes()}
    for langue, cfg in LANGUES.items():
        pages = lire_pages(langue)
        url = adresses(langue, pages)
        charte = pages["charte"]
        notes = [
            cfg["textes"]["docx_source"].format(url=url["charte"]),
            cfg["textes"]["docx_licence"].format(nom=f"{pages['_index'].titre} {version}", editeur=ref["editeur"],
                                                 licence=cfg["licence_nom"]),
            avertissement(langue, ref),
        ]
        charte_docx = docx(charte.titre, reecrire_liens(charte.corps, url, url["charte"]), notes, langue)
        fichiers_kit = kit(langue, pages, ref, url)
        produits[cfg["charte"].format(v=version)] = charte_docx
        produits[cfg["kit"].format(v=version)] = archive(
            fichiers_kit, prefixe=cfg["kit"].format(v=version)[:-4] + "/")
        produits[cfg["pack"].format(v=version)] = archive(
            pack(langue, pages, ref, url, charte_docx, fichiers_kit, tableur),
            prefixe=cfg["pack"].format(v=version)[:-4] + "/")
    return produits


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sortie", default=str(ICI), help="dossier où écrire les fichiers produits")
    parser.add_argument("--copier-site", action="store_true",
                        help="écrire dans site/static/telechargements/ (utilisé par la publication)")
    args = parser.parse_args(argv)
    dossier = SORTIE_SITE if args.copier_site else Path(args.sortie)
    dossier.mkdir(parents=True, exist_ok=True)
    for nom, donnees in sorted(generer().items()):
        (dossier / nom).write_bytes(donnees)
        print(f"{nom} : {len(donnees)} octets, SHA-256 {hashlib.sha256(donnees).hexdigest()}")
    print(f"écrit dans {dossier}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
