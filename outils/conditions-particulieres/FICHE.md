---
titre: Conditions particulières et générales
slug: conditions-particulieres
version: 0.1.0
mise_a_jour: 2026-11-01
statut: test
mode: local
fournisseurs: []
licence: MIT
code_source: outils/conditions-particulieres
---

# Conditions particulières et générales

L'outil lit un contrat négocié et repère, article par article, les données propres à l'opération : parties et personnes, adresses, identifiants, montants, dates, quantités. Il propose pour chaque article un classement : conditions particulières, conditions générales, ou clause générale qui contient une donnée de l'opération, à épurer avant réutilisation. Il liste aussi les renvois internes.

Ce qu'il ne fait pas : il ne produit pas les deux documents séparés, ne modifie pas le contrat et ne lit pas les en-têtes ni les pieds de page. Il ne dit pas si une clause peut être déplacée sans changer l'effet du contrat.

## Comment il fonctionne

Mode d'exécution : application locale (Python), par règles, sans IA.

Fournisseurs compatibles : aucun dans cette version.

Clé API : aucune.

## Mesure

La mesure a été faite le 1er novembre 2026 sur trois contrats fictifs de contrôle, rédigés sans accès aux règles (92 données, 46 blocs) :
- 80 données repérées sur 92, sans faux signalement ;
- quantités : 4 sur 13 ;
- 41 blocs bien classés sur 46.

## Précautions

Le rapport reprend les données de l'opération. Il est aussi confidentiel que le contrat. Une clause classée « générale » se relit encore avant réutilisation.

## Signaler un problème

[À COMPLÉTER : adresse de contact]
