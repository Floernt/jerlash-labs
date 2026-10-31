"""Mise en forme du rapport : texte (terminal), HTML autonome, JSON."""

from __future__ import annotations

import json
from html import escape

from .analyse import Rapport
from .controles import A_EXAMINER, DETECTE, ERREUR, IMPORTANT, INFORMATION, NON_DETECTE, NON_VERIFIE

LIBELLES_STATUT = {
    DETECTE: "Détecté",
    NON_DETECTE: "Non détecté dans les contrôles réalisés",
    NON_VERIFIE: "Non vérifié",
    ERREUR: "Erreur : contrôle non réalisé",
}
LIBELLES_GRAVITE = {IMPORTANT: "Important", A_EXAMINER: "À examiner", INFORMATION: "Information"}
ORDRE = {IMPORTANT: 0, A_EXAMINER: 1, INFORMATION: 2}

LIMITES = [
    "Seuls les éléments listés dans ce rapport ont été recherchés. Le contenu juridique, l'orthographe, "
    "la numérotation et les renvois ne sont pas contrôlés.",
    "Le contenu des objets incorporés (par exemple un tableau Excel) n'est pas analysé : l'outil signale seulement leur présence.",
    "Les métadonnées des images ne sont recherchées que dans les formats JPEG et PNG.",
    "Le texte placé dans des zones de texte peut apparaître deux fois dans le rapport, Word le stockant en deux versions.",
    "Un document protégé par mot de passe ou au format Word 97-2003 (.doc) ne peut pas être analysé.",
    "Le fichier analysé n'est jamais modifié. Les corrections se font dans Word, sur la copie à envoyer.",
]


def _tri(rapport: Rapport):
    rang = {DETECTE: 0, ERREUR: 1, NON_VERIFIE: 2, NON_DETECTE: 3}
    return sorted(rapport.controles, key=lambda c: (rang[c.statut], ORDRE[c.gravite]))


def en_texte(rapport: Rapport) -> str:
    lignes = [f"Contrôle avant envoi {rapport.version} — {rapport.nom}", "", rapport.verdict, ""]
    if rapport.sha256:
        lignes.append(f"Empreinte SHA-256 : {rapport.sha256}")
    for c in _tri(rapport):
        etiquette = LIBELLES_GRAVITE[c.gravite] if c.statut == DETECTE else LIBELLES_STATUT[c.statut]
        lignes.append(f"\n[{etiquette}] {c.titre}" + (f" ({len(c.constats) + c.omis})" if c.statut == DETECTE else ""))
        for k in c.constats:
            lignes.append(f"  - {k.localisation} : {k.detail}")
        if c.omis:
            lignes.append(f"  … et {c.omis} autre(s).")
        if c.statut == DETECTE:
            lignes.append(f"  Que faire : {c.conseil}")
        if c.note:
            lignes.append(f"  Note : {c.note}")
    return "\n".join(lignes) + "\n"


def en_json(rapport: Rapport) -> str:
    return json.dumps(rapport.en_dict(), ensure_ascii=False, indent=2)


STYLE = """
:root{--fond:#fff;--texte:#1d1f21;--doux:#5b6168;--trait:#d9dce0;--imp:#9b1c1c;--imp-fond:#fdecec;
--exa:#7a4b00;--exa-fond:#fff4e0;--inf:#1f4e79;--inf-fond:#e8f1fa;--ok:#22543d;--ok-fond:#e6f4ea}
@media (prefers-color-scheme:dark){:root{--fond:#16181b;--texte:#e6e8eb;--doux:#a3a9b0;--trait:#33373c;
--imp:#ffb4b4;--imp-fond:#3a1d1d;--exa:#ffd591;--exa-fond:#3a2c14;--inf:#a9cdf0;--inf-fond:#18293a;
--ok:#9ee0b5;--ok-fond:#183024}}
*{box-sizing:border-box}body{margin:0;background:var(--fond);color:var(--texte);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:58rem;margin:0 auto;padding:1.5rem 1rem 3rem}
h1{font-size:1.5rem;margin:0 0 .25rem}h2{font-size:1.15rem;margin:0}.doux{color:var(--doux)}
.verdict{border-radius:8px;padding:1rem 1.25rem;margin:1.25rem 0;font-weight:600}
.v-a_traiter{background:var(--exa-fond);color:var(--exa)}.v-rien_detecte{background:var(--ok-fond);color:var(--ok)}
.v-erreur,.v-incomplet{background:var(--imp-fond);color:var(--imp)}
dl{display:grid;grid-template-columns:max-content 1fr;gap:.25rem 1rem;margin:0;font-size:.9rem}
dt{color:var(--doux)}dd{margin:0;overflow-wrap:anywhere}
section{border:1px solid var(--trait);border-radius:8px;padding:1rem 1.25rem;margin:1rem 0}
.entete{display:flex;gap:.75rem;align-items:baseline;flex-wrap:wrap}
.badge{font-size:.8rem;font-weight:700;padding:.1rem .5rem;border-radius:999px;white-space:nowrap}
.b-important{background:var(--imp-fond);color:var(--imp)}.b-a_examiner{background:var(--exa-fond);color:var(--exa)}
.b-information{background:var(--inf-fond);color:var(--inf)}.b-neutre{border:1px solid var(--trait);color:var(--doux)}
table{width:100%;border-collapse:collapse;margin:.75rem 0;font-size:.92rem}
th,td{text-align:left;vertical-align:top;padding:.4rem .5rem;border-top:1px solid var(--trait);overflow-wrap:anywhere}
th{width:30%;font-weight:600}.conseil{margin:.5rem 0 0}
details{margin-top:1.5rem}summary{cursor:pointer;font-weight:600}
@media print{.verdict,section{break-inside:avoid}}
"""


def en_html(rapport: Rapport) -> str:
    e = escape
    corps = []
    for c in _tri(rapport):
        if c.statut == DETECTE:
            badge = f'<span class="badge b-{c.gravite}">{LIBELLES_GRAVITE[c.gravite]}</span>'
        else:
            badge = f'<span class="badge b-neutre">{LIBELLES_STATUT[c.statut]}</span>'
        bloc = [f'<section><div class="entete"><h2>{e(c.titre)}</h2>{badge}</div>',
                f'<p class="doux">{e(c.pourquoi)}</p>']
        if c.constats:
            lignes = "".join(f"<tr><th>{e(k.localisation)}</th><td>{e(k.detail)}</td></tr>" for k in c.constats)
            bloc.append(f"<table><tbody>{lignes}</tbody></table>")
        if c.omis:
            bloc.append(f"<p>… et {c.omis} autre(s) élément(s) non affiché(s).</p>")
        if c.statut == DETECTE:
            bloc.append(f'<p class="conseil"><strong>Que faire :</strong> {e(c.conseil)}</p>')
        if c.note:
            bloc.append(f'<p class="doux">{e(c.note)}</p>')
        bloc.append("</section>")
        corps.append("".join(bloc))
    integrite = {True: "oui, empreinte identique avant et après l'analyse", False: "non : le fichier a changé pendant l'analyse",
                 None: "non mesuré"}[rapport.integre]
    meta = [("Fichier", rapport.nom), ("Taille", f"{rapport.taille} octets" if rapport.taille else "—"),
            ("Empreinte SHA-256", rapport.sha256 or "—"), ("Fichier inchangé", integrite),
            ("Analysé le", rapport.date), ("Outil", f"Contrôle avant envoi {rapport.version} (iavocat.be)")]
    limites = "".join(f"<li>{e(l)}</li>" for l in LIMITES)
    return f"""<!doctype html>
<html lang="fr-BE"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Contrôle avant envoi — {e(rapport.nom)}</title><style>{STYLE}</style></head>
<body><main>
<h1>Contrôle avant envoi</h1>
<p class="doux">Ce rapport est généré sur votre ordinateur. Il peut contenir des extraits confidentiels du document : ne le joignez pas à l'envoi.</p>
<div class="verdict v-{rapport.niveau}">{e(rapport.verdict)}</div>
<dl>{"".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in meta)}</dl>
{"".join(corps)}
<details><summary>Limites de ce contrôle</summary><ul>{limites}</ul></details>
</main></body></html>
"""
