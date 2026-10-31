"""Génère le jeu F-IDENT-01 à partir des textes annotés de sources/ et sources-controle/.

    python -I factory/jeux-de-test/F-IDENT-01/generer.py            régénère pieces/ et attendu/annotations.json
    python -I factory/jeux-de-test/F-IDENT-01/generer.py --verifier échoue si les fichiers sur disque diffèrent

Une annotation s'écrit [[CATEGORIE:texte]]. Le générateur retire les balises, calcule la position de
chaque entité dans le texte nu et contrôle la somme de contrôle des numéros nationaux, numéros
d'entreprise, IBAN et cartes : une erreur de saisie dans le jeu ferait mesurer un faux résultat.
Toutes les personnes, sociétés, adresses et numéros sont fictifs.
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(ICI, "sources")                    # jeu de développement : sert à écrire les règles
SOURCES_CONTROLE = os.path.join(ICI, "sources-controle")  # jeu de contrôle : rédigé à part, jamais pour régler
PIECES = os.path.join(ICI, "pieces")
ATTENDU = os.path.join(ICI, "attendu", "annotations.json")
ATTENDU_CONTROLE = os.path.join(ICI, "attendu", "annotations-controle.json")
VERSION = "1.0"
DOCX = ["contrat-prestation"]
DATE_ZIP = (2026, 1, 1, 0, 0, 0)

CATEGORIES = {"PERSONNE", "ORGANISATION", "ADRESSE", "NUMERO_NATIONAL", "NUMERO_ENTREPRISE", "IBAN",
              "CARTE_BANCAIRE", "EMAIL", "TELEPHONE", "DATE_NAISSANCE", "PLAQUE", "REFERENCE"}
BALISE = re.compile(r"\[\[([A-Z_]+):(.+?)\]\]")


def chiffres(texte: str) -> str:
    return re.sub(r"\D", "", texte)


def nn_valide(texte: str) -> bool:
    c = chiffres(texte)
    return len(c) == 11 and int(c[9:]) in (97 - int(c[:9]) % 97, 97 - int("2" + c[:9]) % 97)


def bce_valide(texte: str) -> bool:
    c = chiffres(texte)
    return len(c) == 10 and c[0] in "01" and int(c[8:]) == 97 - int(c[:8]) % 97


def iban_valide(texte: str) -> bool:
    s = re.sub(r"\s", "", texte).upper()
    s = s[4:] + s[:4]
    return int("".join(str(int(ch, 36)) for ch in s)) % 97 == 1


def luhn_valide(texte: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(chiffres(texte))):
        n = int(ch) * (2 if i % 2 else 1)
        total += n - 9 if n > 9 else n
    return total % 10 == 0


CONTROLES = {"NUMERO_NATIONAL": nn_valide, "NUMERO_ENTREPRISE": bce_valide, "IBAN": iban_valide,
             "CARTE_BANCAIRE": luhn_valide}


def lire_source(chemin: str) -> tuple[str, list[dict]]:
    nom = os.path.basename(chemin)
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().replace("\r\n", "\n")
    texte, entites, curseur = [], [], 0
    longueur = 0
    for m in BALISE.finditer(brut):
        avant = brut[curseur:m.start()]
        texte.append(avant)
        longueur += len(avant)
        categorie, valeur = m.group(1), m.group(2)
        if categorie not in CATEGORIES:
            raise ValueError(f"{nom} : catégorie inconnue {categorie}")
        controle = CONTROLES.get(categorie)
        if controle and not controle(valeur):
            raise ValueError(f"{nom} : {categorie} « {valeur} » a une somme de contrôle invalide")
        entites.append({"categorie": categorie, "debut": longueur, "fin": longueur + len(valeur), "texte": valeur})
        texte.append(valeur)
        longueur += len(valeur)
        curseur = m.end()
    texte.append(brut[curseur:])
    resultat = "".join(texte)
    if "[[" in resultat or "]]" in resultat:
        raise ValueError(f"{nom} : balise mal fermée")
    for e in entites:
        assert resultat[e["debut"]:e["fin"]] == e["texte"]
    return resultat, entites


def docx_depuis_texte(texte: str) -> bytes:
    """Document Word minimal : un paragraphe par ligne."""
    paragraphes = "".join(
        f'<w:p><w:r><w:t xml:space="preserve">{escape(ligne)}</w:t></w:r></w:p>' if ligne else "<w:p/>"
        for ligne in texte.split("\n"))
    parties = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/></Relationships>'),
        "word/document.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{paragraphes}<w:sectPr/></w:body></w:document>'),
    }
    sortie = io.BytesIO()
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, contenu in parties.items():
            info = zipfile.ZipInfo(nom, DATE_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, contenu.encode("utf-8"))
    return sortie.getvalue()


def produire() -> dict[str, bytes]:
    fichiers = {}
    for prefixe, dossier, chemin_attendu in (("", SOURCES, ATTENDU), ("controle/", SOURCES_CONTROLE, ATTENDU_CONTROLE)):
        annotations = {"jeu": "F-IDENT-01", "version": VERSION, "pieces": {}}
        for nom in sorted(os.listdir(dossier)):
            if not nom.endswith(".txt"):
                continue
            texte, entites = lire_source(os.path.join(dossier, nom))
            fichiers[os.path.join(PIECES, prefixe, nom)] = texte.encode("utf-8")
            annotations["pieces"][prefixe + nom] = entites
            base = nom[:-4]
            if not prefixe and base in DOCX:
                fichiers[os.path.join(PIECES, base + ".docx")] = docx_depuis_texte(texte)
                annotations["pieces"][base + ".docx"] = entites
        fichiers[chemin_attendu] = (json.dumps(annotations, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return fichiers


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    verifier = "--verifier" in (argv if argv is not None else sys.argv[1:])
    ecarts = 0
    for chemin, donnees in produire().items():
        if verifier:
            try:
                with open(chemin, "rb") as f:
                    identique = f.read() == donnees
            except OSError:
                identique = False
            if not identique:
                ecarts += 1
                print(f"différent : {os.path.relpath(chemin, ICI)}")
        else:
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            with open(chemin, "wb") as f:
                f.write(donnees)
            print(f"écrit : {os.path.relpath(chemin, ICI)}")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
