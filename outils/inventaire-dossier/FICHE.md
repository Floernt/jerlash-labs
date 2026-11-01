---
titre: Inventaire d'un dossier
slug: inventaire-dossier
version: 0.2.0
mise_a_jour: 2026-11-01
statut: test
mode: local
fournisseurs: [openai, anthropic, mistral, gemini, local]
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

Mode d'exécution : application locale (Python). Règles sur votre ordinateur pour le type, le statut, la date et le document qui fait foi ; modèle d'IA pour les parties et les rattachements.

Fournisseurs compatibles : OpenAI, Anthropic, Mistral AI, API Gemini, modèle local exposant une API compatible.

Clé API : la vôtre, obligatoire. Sans clé, l'outil ne fonctionne pas.

Données envoyées : un extrait pseudonymisé de chaque pièce lisible, en un seul envoi, après votre relecture et votre accord.

## Mesure

Règles seules (version 0.1.0, 31 octobre 2026), dossier fictif de contrôle de 16 pièces rédigé sans accès aux règles :
- type et statut exacts pour 14 pièces ;
- date exacte pour 13 ;
- parties exactes pour 11 ;
- rattachement exact pour 8 ;
- document qui fait foi exact pour 15.

Mode IA : [À COMPLÉTER : mesure réelle, trois exécutions, modèle, date et coût].

## Précautions

Le registre contient les noms des pièces et des parties. Il est aussi confidentiel que le dossier. Des extraits pseudonymisés partent chez le fournisseur que vous avez choisi : relisez-les avant l'envoi.

## Signaler un problème

[À COMPLÉTER : adresse de contact]
