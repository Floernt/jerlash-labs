---
titre: Glossaire des définitions
slug: glossaire-definitions
version: 0.1.0
mise_a_jour: 2026-11-01
statut: test
mode: local
fournisseurs: []
licence: MIT
code_source: outils/glossaire-definitions
---

# Glossaire des définitions

L'outil lit un contrat et dresse la liste de ses termes définis, avec leur définition et leurs emplois. Il signale :
- un terme défini deux fois, en précisant si les deux libellés diffèrent ;
- un terme défini qui n'est jamais employé ;
- un terme écrit avec des majuscules comme un terme défini, sans définition ;
- un terme défini employé sous une autre graphie ;
- un terme employé avant d'être défini en cours de texte.

Ce qu'il ne fait pas : il ne modifie pas le contrat, ne réécrit aucune définition et ne dit pas si une définition est juridiquement correcte.

## Comment il fonctionne

Mode d'exécution : application locale (Python), par règles, sans IA.

Fournisseurs compatibles : aucun dans cette version.

Clé API : aucune.

## Mesure

La mesure a été faite le 1er novembre 2026 sur quatre contrats fictifs de contrôle, rédigés sans accès aux règles (50 termes définis, 30 défauts) :
- 48 termes définis reconnus sur 50, sans faux terme ;
- définitions répétées, termes jamais employés et emplois avant définition : tous trouvés, sans fausse alerte ;
- termes sans définition : 5 sur 6, et 3 fausses alertes ;
- graphies différentes : 5 sur 6.

## Précautions

Le rapport reprend les définitions du contrat. Il est aussi confidentiel que le contrat.

## Signaler un problème

[À COMPLÉTER : adresse de contact]
