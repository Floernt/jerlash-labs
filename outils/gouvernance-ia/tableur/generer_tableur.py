"""Génère le tableur des niveaux 2 et 3 de « Gouvernance de l'IA » à partir du référentiel.

    python outils/gouvernance-ia/tableur/generer_tableur.py [--copier-site]

Lit ../referentiel/gouvernance-ia.json et écrit gouvernance-ia-matrices-<version>.xlsx à côté
de ce script ; avec --copier-site, le copie aussi dans site/static/telechargements/.
Dépendance de génération : openpyxl (ADR-030). Le fichier produit ne contient aucune donnée
réelle : des en-têtes, des listes de choix, des formules et une ligne d'exemple fictive.
"""

import argparse
import json
import shutil
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

ICI = Path(__file__).resolve().parent
REFERENTIEL = ICI.parent / "referentiel" / "gouvernance-ia.json"
RACINE = ICI.parents[2]

LIGNES = 200  # lignes préparées (validations et formules) dans chaque onglet de saisie
POLICE = "Arial"
F_TITRE = Font(name=POLICE, size=14, bold=True)
F_ENTETE = Font(name=POLICE, bold=True, color="FFFFFF")
F_NORMAL = Font(name=POLICE)
F_GRAS = Font(name=POLICE, bold=True)
F_EXEMPLE = Font(name=POLICE, italic=True, color="7F7F7F")
F_NOTE = Font(name=POLICE, italic=True, size=9)
P_ENTETE = PatternFill("solid", fgColor="7A2E1F")  # brique jerlash.labs
P_SAISIE = PatternFill("solid", fgColor="FFF2CC")  # cellules à remplir
P_CALCUL = PatternFill("solid", fgColor="EDEDED")  # cellules calculées
P_ALERTE = PatternFill("solid", fgColor="F8CBAD")
P_OK = PatternFill("solid", fgColor="E2EFDA")
TRAIT = Side(style="thin", color="BFBFBF")
CADRE = Border(left=TRAIT, right=TRAIT, top=TRAIT, bottom=TRAIT)
EXEMPLE = "EXEMPLE FICTIF, à supprimer"


def libelle(colonne):
    return colonne.replace("_", " ").capitalize()


def entetes(ws, ligne, valeurs, largeurs=None):
    for i, v in enumerate(valeurs, start=1):
        c = ws.cell(row=ligne, column=i, value=v)
        c.font, c.fill, c.border = F_ENTETE, P_ENTETE, CADRE
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(i)].width = (largeurs or {}).get(i, max(14, min(40, len(v) + 4)))
    ws.freeze_panes = ws.cell(row=ligne + 1, column=1)


def zone(ws, premiere, colonnes, remplissage):
    for col in colonnes:
        for r in range(premiere, premiere + LIGNES):
            c = ws.cell(row=r, column=col)
            c.fill, c.border, c.font = remplissage, CADRE, F_NORMAL


def liste(ws, nom_plage, colonnes, premiere):
    dv = DataValidation(type="list", formula1=f"={nom_plage}", allow_blank=True)
    dv.error, dv.errorTitle = "Choisissez une valeur de la liste (onglet Paramètres).", "Valeur hors liste"
    ws.add_data_validation(dv)
    for col in colonnes:
        lettre = get_column_letter(col)
        dv.add(f"{lettre}{premiere}:{lettre}{premiere + LIGNES - 1}")


def parametres(wb, ref):
    ws = wb.create_sheet("Paramètres")
    ws["A1"], ws["A1"].font = "Paramètres (modifiables par la gouvernance)", F_TITRE
    ws["A2"] = "Ces listes alimentent les choix proposés dans les autres onglets. Les poids et seuils sont des propositions de travail, à fixer par chaque organisation."
    ws["A2"].font = F_NOTE
    listes = {
        "L_REPONSES": ref["conformite"]["reponses"],
        "L_STATUTS": ["établie", "partielle", "non établie"],
        "L_CLASSES": [c["code"] for c in ref["classes_donnees"]],
        "L_USAGES": [u["code"] for u in ref["niveaux_usage"]],
        "L_CONTROLES": [s["code"] for s in ref["niveaux_controle"]],
        "L_AUTORISATIONS": ref["autorisations_donnees"],
        "L_MENTIONS_E": ref["conditions_eliminatoires"]["mentions"],
        "L_DECISIONS": ref["decisions"],
        "L_OUINON": ["oui", "non"],
        "L_NOTES": ["0", "1", "2", "3", "4", "5"],
    }
    for col, (nom, valeurs) in enumerate(listes.items(), start=1):
        c = ws.cell(row=4, column=col, value=nom)
        c.font, c.fill = F_ENTETE, P_ENTETE
        for r, v in enumerate(valeurs, start=5):
            ws.cell(row=r, column=col, value=v).font = F_NORMAL
        lettre = get_column_letter(col)
        wb.defined_names[nom] = DefinedName(nom, attr_text=f"'Paramètres'!${lettre}$5:${lettre}${4 + len(valeurs)}")
        ws.column_dimensions[lettre].width = 22

    # Pondérations de la grille et seuils indicatifs (cellules nommées, réutilisées par les formules)
    ws["A18"], ws["A18"].font = "Pondérations de la grille (en %)", F_GRAS
    for i, cr in enumerate(ref["criteres"]):
        r = 19 + i
        ws.cell(row=r, column=1, value=cr["code"]).font = F_NORMAL
        ws.cell(row=r, column=2, value=cr["nom"]).font = F_NORMAL
        p = ws.cell(row=r, column=3, value=cr["poids"])
        p.font, p.fill = Font(name=POLICE, color="0000FF"), P_SAISIE
    fin = 19 + len(ref["criteres"]) - 1
    wb.defined_names["POIDS"] = DefinedName("POIDS", attr_text=f"'Paramètres'!$C$19:$C${fin}")
    ws.cell(row=fin + 1, column=2, value="Total (doit faire 100)").font = F_GRAS
    ws.cell(row=fin + 1, column=3, value=f"=SUM(C19:C{fin})").font = F_GRAS
    ws.cell(row=fin + 3, column=1, value="Seuils indicatifs du score").font = F_GRAS
    seuils = ref["notation"]["seuils_exemple"]
    for k, (nom, txt, val) in enumerate([("SEUIL_INSTRUIRE", "Instruire une autorisation à partir de", seuils["instruire"]),
                                         ("SEUIL_CONDITIONS", "Examen sous conditions à partir de", seuils["sous_conditions"])]):
        r = fin + 4 + k
        ws.cell(row=r, column=2, value=txt).font = F_NORMAL
        c = ws.cell(row=r, column=3, value=val)
        c.font, c.fill = Font(name=POLICE, color="0000FF"), P_SAISIE
        c.comment = Comment("Exemple à discuter, pas une règle (page Homologation, « La grille de notation »).", "jerlash.labs")
        wb.defined_names[nom] = DefinedName(nom, attr_text=f"'Paramètres'!$C${r}")
    ws.column_dimensions["B"].width = 40


def lisez_moi(wb, ref):
    ws = wb.active
    ws.title = "Lisez-moi"
    ws.column_dimensions["A"].width = 120
    lignes = [
        (f"{ref['nom']} : matrices et registres (version {ref['version']})", F_TITRE),
        (f"Éditeur : {ref['editeur']}. Licence : {ref['licence']}. Méthode complète : {ref['source']}", F_NORMAL),
        (ref["avertissement"], F_GRAS),
        ("", F_NORMAL),
        ("À quoi sert ce tableur", F_GRAS),
        ("Au niveau 1, la page « Le niveau 1 » suffit. Ce tableur sert aux organisations des niveaux 2 et 3 : plusieurs outils de conformité différente, ou des données sensibles dans des outils dont la conformité n'est pas établie.", F_NORMAL),
        ("", F_NORMAL),
        ("Mode d'emploi", F_GRAS),
        ("1. Inventaire : une ligne par outil. Remplissez la fiche de conformité (F01 à F11), la classe de données la plus sensible que l'outil reçoit et s'il agit seul. Le statut de conformité et le niveau de l'outil se calculent.", F_NORMAL),
        ("2. Diagnostic : le niveau de l'organisation (le plus élevé de ses outils) et le décompte par niveau se calculent.", F_NORMAL),
        ("3. Niveau 2 : Matrice données et Matrice usages disent ce que chaque outil peut recevoir et pour quoi. Rôles désigne le référent, le décideur et les responsables de dossier.", F_NORMAL),
        ("4. Niveau 3 : Conditions E et Grille scores instruisent chaque homologation ; Homologations, Incidents, Usages significatifs et Formations sont les registres.", F_NORMAL),
        ("", F_NORMAL),
        ("Légende", F_GRAS),
        ("Cellules jaunes : à remplir. Cellules grises : calculées, ne pas modifier. Les listes de choix se règlent dans l'onglet Paramètres.", F_NORMAL),
        (f"La ligne grise en italique marquée « {EXEMPLE} » montre le format attendu. Supprimez-la avant usage.", F_NORMAL),
        ("", F_NORMAL),
        ("Règles", F_GRAS),
        (ref["regle_niveau"]["explication"], F_NORMAL),
        (ref["notation"]["regle"], F_NORMAL),
        ("Ne saisissez jamais de nom de client ni d'élément couvert par le secret professionnel : utilisez des références internes. Les preuves détaillées restent dans le dossier sécurisé.", F_NORMAL),
    ]
    for r, (texte, police) in enumerate(lignes, start=1):
        c = ws.cell(row=r, column=1, value=texte)
        c.font, c.alignment = police, Alignment(wrap_text=True, vertical="top")


def inventaire(wb, ref):
    ws = wb.create_sheet("Inventaire")
    points = ref["conformite"]["points"]
    cols = ["Outil", "Fournisseur", "Formule souscrite", "Utilisateurs"] + [f"{p['code']} {p['court']}" for p in points] + \
           ["Conformité (calculée)", "Classe la plus sensible reçue", "Agit seul ?", "Niveau de l'outil (calculé)", "Date de la fiche", "Validée par", "Réexamen"]
    entetes(ws, 1, cols, {1: 22, 2: 18, 3: 16, 4: 18})
    n = len(points)
    c_f1, c_fn = 5, 4 + n
    c_statut, c_classe, c_agit, c_niveau = c_fn + 1, c_fn + 2, c_fn + 3, c_fn + 4
    for i, p in enumerate(points):
        ws.cell(row=1, column=c_f1 + i).comment = Comment(p["libelle"], "jerlash.labs")
    zone(ws, 2, list(range(1, c_statut)) + [c_classe, c_agit] + list(range(c_niveau + 1, len(cols) + 1)), P_SAISIE)
    zone(ws, 2, [c_statut, c_niveau], P_CALCUL)
    liste(ws, "L_REPONSES", range(c_f1, c_fn + 1), 2)
    liste(ws, "L_CLASSES", [c_classe], 2)
    liste(ws, "L_OUINON", [c_agit], 2)
    f1, fn = get_column_letter(c_f1), get_column_letter(c_fn)
    st, cl, ag = get_column_letter(c_statut), get_column_letter(c_classe), get_column_letter(c_agit)
    for r in range(2, 2 + LIGNES):
        plage = f"{f1}{r}:{fn}{r}"
        ws.cell(row=r, column=c_statut, value=(
            f'=IF(COUNTA({plage})<{n},"",IF(COUNTIF({plage},"à vérifier")>0,"non établie",'
            f'IF(COUNTIF({plage},"non")>0,"partielle","établie")))'))
        ws.cell(row=r, column=c_niveau, value=(
            f'=IF(OR(A{r}="",{st}{r}="",{cl}{r}=""),"",IF({ag}{r}="oui",3,'
            f'IF(OR({cl}{r}="D0",{cl}{r}="D1"),1,IF({st}{r}="établie",1,IF({st}{r}="partielle",2,3)))))'))
    exemple = ["Assistant de rédaction X", "Fournisseur fictif", "professionnelle", "Associés et collaborateurs"] + \
              ["oui"] * (n - 1) + ["non", None, "D3", "non", None, "2026-11-06", "Associé gérant", "2027-11-06"]
    for col, v in enumerate(exemple, start=1):
        if v is not None:
            ws.cell(row=2, column=col, value=v)
    for col in range(1, len(cols) + 1):
        ws.cell(row=2, column=col).font = F_EXEMPLE
    ws.cell(row=2, column=1).comment = Comment(EXEMPLE, "jerlash.labs")
    niv = get_column_letter(c_niveau)
    ws.conditional_formatting.add(f"{niv}2:{niv}{1 + LIGNES}", FormulaRule(formula=[f"{niv}2=3"], fill=P_ALERTE))
    ws.conditional_formatting.add(f"{niv}2:{niv}{1 + LIGNES}", FormulaRule(formula=[f"{niv}2=1"], fill=P_OK))
    return niv, st


def diagnostic(wb, col_niveau):
    ws = wb.create_sheet("Diagnostic", 1)
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 18
    ws["A1"], ws["A1"].font = "Diagnostic du niveau de gouvernance", F_TITRE
    ws["A2"] = "Calculé à partir de l'onglet Inventaire. L'organisation retient le niveau le plus élevé de ses outils."
    ws["A2"].font = F_NOTE
    plage = f"Inventaire!${col_niveau}$2:${col_niveau}${1 + LIGNES}"
    lignes = [
        ("Outils inventoriés", "=COUNTA(Inventaire!$A$2:$A$%d)" % (1 + LIGNES)),
        ("Outils au niveau 1", f'=COUNTIF({plage},1)'),
        ("Outils au niveau 2", f'=COUNTIF({plage},2)'),
        ("Outils au niveau 3", f'=COUNTIF({plage},3)'),
        ("Niveau de gouvernance de l'organisation", f'=IF(COUNT({plage})=0,"",MAX({plage}))'),
    ]
    for r, (txt, f) in enumerate(lignes, start=4):
        ws.cell(row=r, column=1, value=txt).font = F_GRAS if r == 8 else F_NORMAL
        c = ws.cell(row=r, column=2, value=f)
        c.fill, c.border, c.font = P_CALCUL, CADRE, F_GRAS if r == 8 else F_NORMAL
    ws["A10"] = "Le niveau n'est pas acquis une fois pour toutes : refaites le diagnostic à chaque nouvel outil, contrat, catégorie de données ou incident, et au moins une fois par an."
    ws["A10"].font = F_NOTE


def matrice_donnees(wb, ref, col_statut):
    ws = wb.create_sheet("Matrice données")
    classes = [c["code"] for c in ref["classes_donnees"]]
    cols = ["Outil", "Conformité (reprise)"] + [f"{c['code']} {c['nom']}" for c in ref["classes_donnees"]] + \
           ["Classe la plus sensible admise (calculée)", "Contrôle de cohérence (calculé)", "Conditions et motifs"]
    entetes(ws, 1, cols, {1: 24, 2: 18, 8: 22, 9: 44, 10: 40})
    for i, c in enumerate(ref["classes_donnees"]):
        ws.cell(row=1, column=3 + i).comment = Comment(f"{c['exemples']}. Règle de base : {c['regle']}.", "jerlash.labs")
    c_max, c_ctrl = 3 + len(classes), 4 + len(classes)
    zone(ws, 2, [1] + list(range(3, 3 + len(classes))) + [c_ctrl + 1], P_SAISIE)
    zone(ws, 2, [2, c_max, c_ctrl], P_CALCUL)
    liste(ws, "L_AUTORISATIONS", range(3, 3 + len(classes)), 2)
    d = [get_column_letter(3 + i) for i in range(len(classes))]  # C..G = D0..D4
    for r in range(2, 2 + LIGNES):
        ws.cell(row=r, column=2, value=(
            f'=IF(A{r}="","",IFERROR(INDEX(Inventaire!${col_statut}$2:${col_statut}${1 + LIGNES},MATCH(A{r},Inventaire!$A$2:$A${1 + LIGNES},0)),"absent de l\'inventaire"))'))
        admise = '""'
        for lettre, code in zip(d, classes):
            admise = f'IF(AND({lettre}{r}<>"",{lettre}{r}<>"interdit"),"{code}",{admise})'
        ws.cell(row=r, column=c_max, value=f'=IF(A{r}="","",{admise})')
        sensibles = f'COUNTIF({d[2]}{r}:{d[4]}{r},"autorisé")+COUNTIF({d[2]}{r}:{d[4]}{r},"sous conditions")'
        ws.cell(row=r, column=c_ctrl, value=(
            f'=IF(A{r}="","",IF({sensibles}=0,"Cohérent",IF(B{r}="établie","Cohérent",'
            f'IF(B{r}="partielle","Niveau 2 : conditions à motiver","Niveau 3 : homologation requise"))))'))
    for col, v in enumerate(["Assistant de rédaction X", None, "autorisé", "autorisé", "sous conditions", "interdit", "interdit",
                             None, None, "D2 pseudonymisé seulement ; voir fiche F09"], start=1):
        if v is not None:
            ws.cell(row=2, column=col, value=v)
    for col in range(1, len(cols) + 1):
        ws.cell(row=2, column=col).font = F_EXEMPLE
    ws.cell(row=2, column=1).comment = Comment(EXEMPLE, "jerlash.labs")
    lc = get_column_letter(c_ctrl)
    ws.conditional_formatting.add(f"{lc}2:{lc}{1 + LIGNES}", FormulaRule(formula=[f'LEFT({lc}2,6)="Niveau"'], fill=P_ALERTE))


def matrice_usages(wb, ref):
    ws = wb.create_sheet("Matrice usages")
    usages = ref["niveaux_usage"]
    cols = ["Outil"] + [f"{u['code']} {u['nom']}" for u in usages] + ["Contrôle S appliqué", "Validateur habilité", "Conditions et motifs"]
    entetes(ws, 1, cols, {1: 24, 7: 22, 8: 40})
    for i, u in enumerate(usages):
        ws.cell(row=1, column=2 + i).comment = Comment(u["exemples"], "jerlash.labs")
    zone(ws, 2, range(1, len(cols) + 1), P_SAISIE)
    liste(ws, "L_AUTORISATIONS", range(2, 2 + len(usages)), 2)
    liste(ws, "L_CONTROLES", [2 + len(usages)], 2)
    for col, v in enumerate(["Assistant de rédaction X", "autorisé", "autorisé", "sous conditions", "interdit", "S3",
                             "Responsable de dossier", "U3 : relecture S3 par un avocat"], start=1):
        ws.cell(row=2, column=col, value=v).font = F_EXEMPLE
    ws.cell(row=2, column=1).comment = Comment(EXEMPLE, "jerlash.labs")
    r0 = 4 + LIGNES
    ws.cell(row=r0, column=1, value="Niveaux de contrôle (rappel)").font = F_GRAS
    for i, s in enumerate(ref["niveaux_controle"], start=1):
        ws.cell(row=r0 + i, column=1, value=f"{s['code']} {s['nom']}").font = F_NORMAL
        ws.cell(row=r0 + i, column=2, value=f"{s['declenchement']}. Exigences : {s['exigences']}.").font = F_NORMAL


def roles(wb, ref):
    ws = wb.create_sheet("Rôles")
    entetes(ws, 1, ["Rôle", "Mission", "Personne (fonction)", "Suppléant", "Date de désignation"], {1: 22, 2: 70, 3: 26, 4: 22, 5: 18})
    for r, role in enumerate(ref["roles_reduits"], start=2):
        ws.cell(row=r, column=1, value=role["role"]).font = F_GRAS
        c = ws.cell(row=r, column=2, value=role["mission"])
        c.font, c.alignment = F_NORMAL, Alignment(wrap_text=True)
        for col in (3, 4, 5):
            cell = ws.cell(row=r, column=col)
            cell.fill, cell.border = P_SAISIE, CADRE
    ws.cell(row=6, column=1, value="Personne n'approuve seul sa propre demande. Au niveau 3, voir la matrice des responsabilités du module Gouvernance.").font = F_NOTE


def conditions_e(wb, ref):
    ws = wb.create_sheet("Conditions E")
    conds = ref["conditions_eliminatoires"]["liste"]
    cols = ["Évaluation (ID)", "Outil et usage"] + [c["code"] for c in conds] + ["Résultat (calculé)", "Preuves et réserves"]
    entetes(ws, 1, cols, {1: 16, 2: 30, 11: 34, 12: 40})
    for i, c in enumerate(conds):
        ws.cell(row=1, column=3 + i).comment = Comment(c["libelle"], "jerlash.labs")
    c_res = 3 + len(conds)
    zone(ws, 2, [1, 2] + list(range(3, c_res)) + [c_res + 1], P_SAISIE)
    zone(ws, 2, [c_res], P_CALCUL)
    liste(ws, "L_MENTIONS_E", range(3, c_res), 2)
    plage_l = lambda r: f"C{r}:{get_column_letter(c_res - 1)}{r}"
    for r in range(2, 2 + LIGNES):
        p = plage_l(r)
        ws.cell(row=r, column=c_res, value=(
            f'=IF(A{r}="","",IF(COUNTIF({p},"non satisfaite")>0,"Refus ou redéfinition du périmètre",'
            f'IF(COUNTIF({p},"preuve insuffisante")>0,"Décision suspendue",IF(COUNTA({p})<{len(conds)},"Incomplet","Conditions franchies"))))'))
    for col, v in enumerate(["EV-001", "Outil fictif Y, synthèse de pièces (U2)"] + ["satisfaite"] * 7 + ["non applicable", None,
                             "E08 sans objet en U2"], start=1):
        if v is not None:
            ws.cell(row=2, column=col, value=v)
    for col in range(1, len(cols) + 1):
        ws.cell(row=2, column=col).font = F_EXEMPLE
    ws.cell(row=2, column=1).comment = Comment(EXEMPLE, "jerlash.labs")
    lr = get_column_letter(c_res)
    ws.conditional_formatting.add(f"{lr}2:{lr}{1 + LIGNES}", FormulaRule(formula=[f'OR({lr}2="Refus ou redéfinition du périmètre",{lr}2="Décision suspendue")'], fill=P_ALERTE))
    return lr


def grille(wb, ref, col_resultat_e):
    ws = wb.create_sheet("Grille scores")
    crit = ref["criteres"]
    cols = ["Évaluation (ID)"] + [f"{c['code']} {c['nom']}" for c in crit] + \
           ["Score indicatif /100 (calculé)", "Conditions E (reprise)", "Lecture indicative (calculée)", "Évaluateur", "Date", "Preuves"]
    entetes(ws, 1, cols, {1: 16, 9: 16, 10: 30, 11: 40, 14: 30})
    for i, c in enumerate(crit):
        ws.cell(row=1, column=2 + i).comment = Comment(f"Poids d'essai {c['poids']} %. Observer : {c['observe']}. Note de 0 à 5 : {ref['notation']['echelle']}.", "jerlash.labs")
    n = len(crit)
    c_score, c_e, c_lect = 2 + n, 3 + n, 4 + n
    zone(ws, 2, [1] + list(range(2, 2 + n)) + [c_lect + 1, c_lect + 2, c_lect + 3], P_SAISIE)
    zone(ws, 2, [c_score, c_e, c_lect], P_CALCUL)
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="5", allow_blank=True)
    dv.error, dv.errorTitle = "Note entière de 0 à 5.", "Note invalide"
    ws.add_data_validation(dv)
    dv.add(f"B2:{get_column_letter(1 + n)}{1 + LIGNES}")
    dern = get_column_letter(1 + n)
    sc, ce = get_column_letter(c_score), get_column_letter(c_e)
    for r in range(2, 2 + LIGNES):
        ws.cell(row=r, column=c_score, value=(
            f'=IF(OR(A{r}="",COUNT(B{r}:{dern}{r})<{n}),"",ROUND(('
            + "+".join(f"{get_column_letter(2 + i)}{r}*INDEX(POIDS,{i + 1})" for i in range(n)) + ')/5,1))'))
        ws.cell(row=r, column=c_e, value=(
            f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Conditions E'!${col_resultat_e}$2:${col_resultat_e}${1 + LIGNES},"
            f"MATCH(A{r},'Conditions E'!$A$2:$A${1 + LIGNES},0)),\"Conditions non instruites\"))"))
        ws.cell(row=r, column=c_lect, value=(
            f'=IF(OR(A{r}="",{sc}{r}=""),"",IF({ce}{r}<>"Conditions franchies","Bloqué : conditions éliminatoires",'
            f'IF({sc}{r}>=SEUIL_INSTRUIRE,"Autorisation à instruire",IF({sc}{r}>=SEUIL_CONDITIONS,"Examen sous conditions","Refus ou révision"))))'))
    exemple = ["EV-001", 4, 4, 3, 4, 3, 3, 3, None, None, None, "Référent IA", "2026-11-06", "Rapport de tests RT-001"]
    for col, v in enumerate(exemple, start=1):
        if v is not None:
            ws.cell(row=2, column=col, value=v)
    for col in range(1, len(cols) + 1):
        ws.cell(row=2, column=col).font = F_EXEMPLE
    ws.cell(row=2, column=1).comment = Comment(EXEMPLE, "jerlash.labs")
    ll = get_column_letter(c_lect)
    ws.conditional_formatting.add(f"{ll}2:{ll}{1 + LIGNES}", FormulaRule(formula=[f'LEFT({ll}2,6)="Bloqué"'], fill=P_ALERTE))
    ws.cell(row=3 + LIGNES, column=1, value=ref["notation"]["regle"]).font = F_NOTE


def registre(wb, titre, colonnes, validations=None):
    ws = wb.create_sheet(titre)
    entetes(ws, 1, [libelle(c) for c in colonnes])
    zone(ws, 2, range(1, len(colonnes) + 1), P_SAISIE)
    for nom_col, nom_plage in (validations or {}).items():
        liste(ws, nom_plage, [colonnes.index(nom_col) + 1], 2)
    return ws


def generer(copier_site=False):
    ref = json.loads(REFERENTIEL.read_text(encoding="utf-8"))
    wb = Workbook()
    lisez_moi(wb, ref)
    col_niveau, col_statut = inventaire(wb, ref)
    diagnostic(wb, col_niveau)
    matrice_donnees(wb, ref, col_statut)
    matrice_usages(wb, ref)
    roles(wb, ref)
    col_e = conditions_e(wb, ref)
    grille(wb, ref, col_e)
    reg = ref["registres"]
    registre(wb, "Homologations", reg["homologations"], {"niveau_usage": "L_USAGES", "statut": "L_DECISIONS"})
    registre(wb, "Incidents", reg["incidents"], {"classe_donnees": "L_CLASSES"})
    registre(wb, "Usages significatifs", reg["usages_significatifs"], {"niveau_usage": "L_USAGES", "controle_s1_s2_s3_s4": "L_CONTROLES"})
    registre(wb, "Formations", reg["formations"])
    parametres(wb, ref)
    sortie = ICI / f"gouvernance-ia-matrices-{ref['version']}.xlsx"
    wb.save(sortie)
    print(f"écrit : {sortie}")
    if copier_site:
        cible = RACINE / "site" / "static" / "telechargements" / sortie.name
        shutil.copyfile(sortie, cible)
        print(f"copié : {cible}")
    return sortie


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--copier-site", action="store_true", help="copier aussi le fichier dans site/static/telechargements/")
    generer(parser.parse_args().copier_site)
