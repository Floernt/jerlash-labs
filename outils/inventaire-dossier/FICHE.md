---
titre: Inventaire d'un dossier
slug: inventaire-dossier
version: 0.1.0
mise_a_jour: 2026-10-31
statut: test
mode: local
fournisseurs: []
licence: MIT
code_source: outils/inventaire-dossier
---

# Inventaire d'un dossier

L'outil parcourt le dossier d'une affaire contractuelle et produit un registre des pièces. Pour chacune, il indique :
- le type, le statut, la date et les parties ;
- la pièce à laquelle elle se rapporte ;
- si elle fait foi ;
- son empreinte.

Il signale aussi ce qui demande attention : pièce non lue, acte non signé, pièce d'un autre client, doublon, envoi recommandé sans preuve.

Ce qu'il ne fait pas : il n'analyse pas le contenu juridique et ne lit pas les PDF. Il ne remplace pas la relecture : chaque conclusion est une proposition accompagnée de l'indice qui l'a produite.

## Comment il fonctionne

Mode d'exécution : application locale (Python), par règles, sans IA.

Fournisseurs compatibles : aucun dans cette version.

Clé API : aucune.

## Mesure

La mesure a été faite le 31 octobre 2026 sur un dossier fictif de contrôle de 16 pièces, rédigé sans accès aux règles :
- type et statut exacts pour 14 pièces ;
- date exacte pour 13 ;
- parties exactes pour 11 ;
- rattachement exact pour 8 ;
- document qui fait foi exact pour 15.

## Précautions

Le registre contient les noms des pièces et des parties. Il est aussi confidentiel que le dossier.

## Signaler un problème

[À COMPLÉTER : adresse de contact]
