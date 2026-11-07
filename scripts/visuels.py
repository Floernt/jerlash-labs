"""Visuels des projets de la rubrique Recherche : compositions géométriques pixelisées et tramées (Bayer 8x8),
dans la direction artistique du site (fonds pixel de site/static/js/bundle.js, ADR-022).

    python scripts/visuels.py              (re)génère site/static/images/projets/<code>.svg
                                           et site/static/images/programmes/<slug>.svg
    python scripts/visuels.py --verifier   n'écrit rien ; code 1 si un visuel manque ou n'est plus à jour

Chaque fiche de site/content/recherche/projets/ (champ « code ») reçoit un visuel déterministe : même code,
même image. La teinte dominante vient du premier programme du projet (champ « programmes », couleur définie
dans site/data/programmes.yaml) ; le motif et sa position sont tirés du code. Chaque programme reçoit aussi
un visuel, à sa couleur, nommé d'après son slug français (le code n'apparaît pas dans les adresses, ADR-032).
Aucune dépendance externe.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import sys

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHES = os.path.join(DEPOT, "site", "content", "recherche", "projets")
PROGRAMMES = os.path.join(DEPOT, "site", "data", "programmes.yaml")
SORTIE = os.path.join(DEPOT, "site", "static", "images", "projets")
SORTIE_PROGRAMMES = os.path.join(DEPOT, "site", "static", "images", "programmes")

LARGEUR, HAUTEUR, CELLULE = 600, 400, 10  # format 3:2, cellules de 10 px
PAPIER = "#FAF9F6"
TEINTES = {"brique": "#BD4A2A", "bleu": "#7F9CE3", "encre": "#1C1A16"}
ACCENT = {"brique": "bleu", "bleu": "brique", "encre": "brique"}
MOTIFS = ("orbe", "anneau", "colonnes", "diagonale", "constellation", "spirale")
FONDS = ("horizon", "nuage", "onde")

BAYER = [0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52, 20, 62, 30, 54, 22,
         3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31, 55, 23, 61, 29, 53, 21]


# --- Bruit, repris de bundle.js (arithmétique 32 bits) ------------------------------------------------
def _i32(v: int) -> int:
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def _hash(x: int, y: int, s: int) -> float:
    h = _i32(x * 374761393 + y * 668265263 + s * 2147483647)
    h = _i32((h ^ ((h & 0xFFFFFFFF) >> 13)) * 1274126177)
    return ((h ^ ((h & 0xFFFFFFFF) >> 16)) & 0xFFFFFFFF) / 4294967295


def _lisse(t: float) -> float:
    return t * t * (3 - 2 * t)


def _bruit(x: float, y: float, s: int) -> float:
    x0, y0 = math.floor(x), math.floor(y)
    fx, fy = _lisse(x - x0), _lisse(y - y0)
    a, b, c, d = _hash(x0, y0, s), _hash(x0 + 1, y0, s), _hash(x0, y0 + 1, s), _hash(x0 + 1, y0 + 1, s)
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy


def _borne(v: float) -> float:
    return 0.0 if v < 0 else 1.0 if v > 1 else v


# --- Champs : x, y en cellules, w, h taille de la grille, p paramètres tirés du code. Retour 0..1 -------
def fond(nom: str, x: int, y: int, w: int, h: int, p: dict) -> float:
    if nom == "horizon":
        return _borne((y / h) * 1.15 - 0.25 + (_bruit(x / 26, y / 26, p["graine"]) - 0.5) * 0.55)
    if nom == "nuage":
        n = _bruit(x / 20, y / 20, p["graine"]) * 0.65 + _bruit(x / 8, y / 8, p["graine"] + 1) * 0.35
        e = min(x, w - x, y, h - y) / (min(w, h) * 0.45)
        return _borne((n - 0.35) * 1.6 + _borne(1 - e) * 0.5)
    v = math.sin(x / 9 + p["phase"]) * 0.5 + math.sin((x + y) / 17) * 0.5  # onde
    return _borne(0.5 + v * 0.45 * (1 - y / h) + (y / h - 0.5) * 0.6)


def motif(nom: str, x: int, y: int, w: int, h: int, p: dict) -> float:
    cx, cy, r = w * p["cx"], h * p["cy"], min(w, h) * p["taille"]
    dx, dy = x - cx, y - cy
    d = math.hypot(dx, dy)
    if nom == "orbe":  # sphère éclairée par le haut à gauche, comme le héros de l'accueil
        if d > r:
            return 0.0
        lx, ly = dx + r * 0.38, dy + r * 0.38
        return _borne(0.1 + 0.9 * (1 - math.hypot(lx, ly) / (r * 1.9)))
    if nom == "anneau":
        return _borne(1 - abs(d - r * 0.8) / (r * 0.22)) * (0.55 + 0.45 * (1 - dy / (2 * r)))
    if nom == "colonnes":  # colonnes de hauteurs variables posées sur une ligne de base
        largeur = max(3, int(w / 9))
        rang = x // largeur
        if x % largeur >= largeur - 1:
            return 0.0
        haut = 0.25 + 0.6 * _hash(rang, 3, p["graine"])
        base = h * 0.86
        if y > base or y < base - h * haut:
            return 0.0
        return _borne(0.35 + 0.65 * (base - y) / (h * haut))
    if nom == "diagonale":
        t = (x / w) * p["sens"] + (y / h)
        bande = abs((t * 3 + p["phase"]) % 2 - 1)
        return _borne(1.2 - bande * 1.8) * _borne(1 - abs(t - 1) * 0.9)
    if nom == "constellation":  # sept points reliés dans l'ordre par des traits fins
        points = [(w * (0.12 + 0.76 * _hash(i, 1, p["graine"])), h * (0.15 + 0.7 * _hash(i, 2, p["graine"]))) for i in range(7)]
        v = 0.0
        for px, py in points:
            v = max(v, _borne(1 - math.hypot(x - px, y - py) / (r * 0.24)))
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            lx, ly = bx - ax, by - ay
            t = _borne(((x - ax) * lx + (y - ay) * ly) / (lx * lx + ly * ly or 1))
            if math.hypot(x - ax - t * lx, y - ay - t * ly) < 0.7:
                v = max(v, 0.6)
        return v
    # spirale
    a = math.atan2(dy, dx)
    tour = (d / r - (a + math.pi) / (2 * math.pi) * 0.5) % 0.5
    return _borne(1 - abs(tour - 0.25) * 8) * _borne(1.15 - d / (r * 1.3))


# --- Composition --------------------------------------------------------------------------------------
def parametres(code: str) -> dict:
    o = hashlib.sha256(code.encode("utf-8")).digest()
    return {
        "motif": MOTIFS[o[0] % len(MOTIFS)],
        "fond": FONDS[o[1] % len(FONDS)],
        "graine": o[2] * 256 + o[3],
        "cx": 0.38 + 0.3 * o[4] / 255,
        "cy": 0.42 + 0.16 * o[5] / 255,
        "taille": 0.34 + 0.1 * o[6] / 255,
        "phase": o[7] / 255 * math.pi,
        "sens": 1 if o[8] % 2 else -1,
    }


def _trace(cellules: list[tuple[int, int]]) -> str:
    """Regroupe les cellules allumées d'une même ligne en segments : un seul chemin SVG par couleur."""
    morceaux, par_ligne = [], {}
    for x, y in cellules:
        par_ligne.setdefault(y, []).append(x)
    for y in sorted(par_ligne):
        xs = sorted(par_ligne[y])
        debut = precedent = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == precedent + 1:
                precedent = x
                continue
            morceaux.append(f"M{debut * CELLULE} {y * CELLULE}h{(precedent - debut + 1) * CELLULE}v{CELLULE}h-{(precedent - debut + 1) * CELLULE}z")
            if x is not None:
                debut = precedent = x
    return "".join(morceaux)


def dessiner(code: str, couleur: str, motif_impose: str | None = None) -> str:
    p = parametres(code)
    if motif_impose in MOTIFS:
        p["motif"] = motif_impose
    w, h = LARGEUR // CELLULE, HAUTEUR // CELLULE
    principale, accent = [], []
    for y in range(h):
        for x in range(w):
            seuil = BAYER[(y & 7) * 8 + (x & 7)] / 64
            if motif(p["motif"], x, y, w, h, p) > seuil:
                principale.append((x, y))
            elif fond(p["fond"], x, y, w, h, p) * 0.38 > seuil:
                accent.append((x, y))
    teinte, teinte_accent = TEINTES[couleur], TEINTES[ACCENT[couleur]]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" width="{LARGEUR}" height="{HAUTEUR}" '
        f'shape-rendering="crispEdges" role="img" aria-hidden="true">'
        f'<rect width="{LARGEUR}" height="{HAUTEUR}" fill="{PAPIER}"/>'
        f'<path fill="{teinte_accent}" d="{_trace(accent)}"/>'
        f'<path fill="{teinte}" d="{_trace(principale)}"/>'
        f"</svg>\n"
    )


# --- Lecture des fiches et des programmes (front matter simple, sans dépendance YAML) ------------------
def lire_programmes() -> dict[str, dict]:
    """Code -> {"couleur", "slug", "motif"} (slug de la version française, premier « slug: » après le code)."""
    programmes, code = {}, None
    with open(PROGRAMMES, encoding="utf-8") as f:
        for ligne in f:
            m = re.match(r"-\s*code:\s*(\S+)", ligne)
            if m:
                code = m.group(1)
                programmes[code] = {"couleur": "brique", "slug": code.lower()}
                slug_lu = False
            m = re.match(r"\s+motif:\s*(\S+)", ligne)
            if m and code:
                programmes[code]["motif"] = m.group(1)
            m = re.match(r"\s+couleur:\s*(\S+)", ligne)
            if m and code:
                programmes[code]["couleur"] = m.group(1)
            m = re.match(r'\s+slug:\s*"?([^"\n]+)"?', ligne)
            if m and code and not slug_lu:
                programmes[code]["slug"] = m.group(1).strip()
                slug_lu = True
    return programmes


def projets() -> list[tuple[str, str | None]]:
    """(code, premier programme) de chaque fiche française de site/content/recherche/projets/."""
    resultat = []
    if not os.path.isdir(FICHES):
        return resultat
    for nom in sorted(os.listdir(FICHES)):
        if not nom.endswith(".md") or nom.startswith("_") or re.search(r"\.[a-z]{2}\.md$", nom):
            continue
        with open(os.path.join(FICHES, nom), encoding="utf-8") as f:
            entete = f.read().split("---")[1]
        code = re.search(r"^code:\s*\"?([^\"\n]+)\"?", entete, re.M)
        programmes = re.search(r"^programmes:\s*\[([^\]]*)\]", entete, re.M)
        if code:
            premier = programmes.group(1).split(",")[0].strip().strip("\"'") if programmes and programmes.group(1).strip() else None
            resultat.append((code.group(1).strip(), premier))
    return resultat


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verifier", action="store_true")
    args = parser.parse_args(argv)
    programmes = lire_programmes()
    os.makedirs(SORTIE, exist_ok=True)
    os.makedirs(SORTIE_PROGRAMMES, exist_ok=True)
    problemes = 0
    a_produire = [(os.path.join(SORTIE, f"{code.lower()}.svg"), code, programmes.get(programme or "", {}).get("couleur", "brique"), None)
                  for code, programme in projets()]
    a_produire += [(os.path.join(SORTIE_PROGRAMMES, f"{p['slug']}.svg"), f"programme-{code}", p["couleur"], p.get("motif"))
                   for code, p in programmes.items()]
    liste = a_produire
    for chemin, graine, couleur, motif_impose in a_produire:
        attendu = dessiner(graine, couleur, motif_impose)
        actuel = open(chemin, encoding="utf-8").read() if os.path.exists(chemin) else None
        if actuel == attendu:
            continue
        if args.verifier:
            print(("manquant : " if actuel is None else "pas à jour : ") + os.path.relpath(chemin, DEPOT))
            problemes += 1
        else:
            with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                f.write(attendu)
            print("généré : " + os.path.relpath(chemin, DEPOT))
    if args.verifier:
        if problemes:
            print("Lancer : python scripts/visuels.py")
            return 1
        print(f"{len(liste)} visuel(s) de projet et de programme à jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
