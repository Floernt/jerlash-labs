---
titre: Pseudonymisation
slug: pseudonymisation
version: 0.1.0
mise_a_jour: 2026-10-31
statut: test
mode: local
fournisseurs: []
licence: MIT
code_source: outils/pseudonymisation
---

# Pseudonymisation

Avant de soumettre un texte à une IA, l'outil remplace les noms, sociétés, adresses et identifiants belges par des marqueurs comme `[PERSONNE_1]`. Il fait relire le résultat, puis remet les vrais noms dans la réponse de l'IA grâce à une table de correspondance qui reste sur l'ordinateur.

Ce qu'il ne fait pas : il n'anonymise pas. Il ne trouve pas tout : un nom cité sans civilité, un prénom seul ou un surnom lui échappent souvent. Il ne reprend ni les en-têtes, ni les notes, ni la mise en forme d'un document Word. La relecture est obligatoire, et la fenêtre l'exige avant d'enregistrer.

## Comment il fonctionne

Mode d'exécution : application locale (Python). Aucune IA n'est nécessaire pour détecter, et le texte d'origine ne doit pas quitter l'ordinateur.

Fournisseurs compatibles : tous, puisque c'est l'avocat qui copie le texte pseudonymisé vers l'IA de son choix. L'outil n'en appelle aucun.

Clé API : aucune.

## Mesure

Mesure réalisée sur le jeu fictif F-IDENT-01, jeu de contrôle rédigé sans accès aux règles, le 31 octobre 2026 :
- rappel de 63 % (118 données sur 186 entièrement masquées) ;
- précision de 98 % ;
- identifiants à somme de contrôle et courriels : 100 % ;
- noms de personnes : 45 % ;
- références de dossier : 20 %.

Le détail est dans `factory/jeux-de-test/F-IDENT-01/resultats/`.

## Précautions

Le texte pseudonymisé reste une donnée personnelle et reste couvert par le secret professionnel. La table de correspondance contient les données d'origine : ne l'envoyez jamais avec le texte.

## Signaler un problème

[À COMPLÉTER : adresse de contact]
