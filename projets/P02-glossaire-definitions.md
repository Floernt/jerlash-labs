---
id: P02
titre: Glossaire des définitions d'un contrat
type: outil public
statut: vérification
priorité: à définir
source: zenzen-sol/legal-prompts, skill defined-terms-glossary (v0.1.0)
licence_source: MIT
dépend_de: [P10]
mise_a_jour: 2026-11-01
---

# Glossaire des définitions d'un contrat

## 1. Origine

La skill defined-terms-glossary déplace chaque terme défini d'un contrat vers une annexe unique, classée par ordre alphabétique, à laquelle le corps du contrat renvoie. Chaque terme n'est défini qu'une fois. Le contrat doit avoir exactement le même sens après l'opération. Un rapport sur les définitions accompagne le résultat. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Les contrats négociés accumulent des définitions dispersées, parfois redondantes ou contradictoires, et des termes utilisés avec une majuscule sans être définis.

## 3. Solution envisagée

L'outil reçoit un contrat .docx, repère les définitions, les doublons, les termes définis mais inutilisés et les termes utilisés sans définition, puis propose une version restructurée et un rapport.

Hors périmètre : réécriture des définitions sur le fond.

## 4. Adaptation à jerlash.labs

Gestion des conventions françaises (guillemets, "ci-après dénommé", définitions entre parenthèses), contrats bilingues FR/NL en option ultérieure.

## 5. Approche technique pressentie

Deux passes : détection déterministe des motifs de définition, puis contrôle par le modèle. Sortie .docx en copie, avec rapport séparé.

## 6. Contraintes et risques

Déontologie : rappel que l'avocat vérifie le résultat avant usage.
Technique : préservation de la mise en forme Word ; renvois croisés automatiques.
Licence : MIT.

## 7. Critères d'acceptation

- [ ] Sur trois contrats fictifs, aucune définition perdue ni ajoutée.
- [ ] Le rapport liste les termes non définis et les doublons.
- [ ] La mise en forme du document source est conservée.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Annexe en fin de contrat ou article "Définitions" en tête, selon l'usage du cabinet ?

## 10. Prochaine étape

P02 Lite 0.1.0 (rapport seul, par règles, ADR-016) est livré dans `outils/glossaire-definitions`, mesuré sur F-DEF-01. Prochaines étapes : test par Florian sur ses propres modèles ; la restructuration (annexe unique) attend P10.
