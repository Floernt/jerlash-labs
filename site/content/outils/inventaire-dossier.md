---
draft: true
title: "Inventaire d'un dossier"
description: "Dresser le registre des pièces d'un dossier contractuel : type, statut, date, parties, version qui fait foi, et ce qui ne devrait pas s'y trouver. Règles sur votre ordinateur, parties et rattachements proposés par un modèle d'IA, avec votre clé."
resume: "L'outil parcourt le dossier d'une affaire contractuelle et produit un registre des pièces en Word, avec des alertes : acte non signé, pièce d'un autre client, scan illisible, envoi recommandé sans preuve."
version: "0.2.0"
statut: "test"
mode: "local"
ia: true
cle_api: true
licence: "MIT"
taches: ["reprendre un dossier", "vérifier"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/inventaire-dossier-0.2.0.zip"
taille: "67 Ko"
sha256: "ff2ecc390093653b97e656f5f633564f383f0202b881c8ee50111d63542f1204"
---

## Ce que fait l'outil

Vous désignez le dossier d'une affaire contractuelle. L'outil lit chaque pièce sur votre ordinateur, sans la modifier, et produit un registre en Word. Pour chaque pièce, le registre indique :

- son type : contrat, avenant, conditions générales, courrier, courriel, note, modèle, précédent ;
- son statut : signé ou projet ;
- la date de l'acte, et non celle du fichier ;
- les sociétés parties ;
- la pièce à laquelle elle se rapporte (un avenant à son contrat, un courriel à l'avenant qu'il négocie) ;
- si elle fait foi ;
- son empreinte SHA-256, qui permet de prouver plus tard que la pièce n'a pas changé.

En tête du registre, des alertes signalent ce qui demande attention :

- une pièce que l'outil n'a pas pu lire ;
- un contrat ou un avenant non signé ;
- une pièce sans aucune partie commune avec le reste du dossier, qui appartient peut-être à un autre client ;
- un doublon ;
- une lettre annoncée comme recommandée sans preuve de dépôt au dossier.

Chaque conclusion est accompagnée de l'indice qui l'a produite, par exemple « mention (signé) sous la signature » ou « référence au contrat du 15 mars 2023 ». Vous pouvez ainsi la vérifier rapidement.

## Ce qu'il ne fait pas

L'outil n'analyse pas les clauses et ne donne aucun avis juridique. Il lit les documents Word (.docx), les courriels (.eml) et les fichiers texte. Les PDF, les anciens .doc, les courriels Outlook (.msg) et les images sont repris au registre avec leur empreinte, mais signalés « non lus » : l'outil ne devine jamais le contenu d'une pièce qu'il n'a pas lue.

Le type, le statut, la date et le document qui fait foi reposent sur des règles. Les parties et le rattachement entre pièces, points faibles des règles (voir les mesures ci-dessous), sont proposés par un modèle d'IA. Le registre signale ce qui vient du modèle et les désaccords avec les règles. Il se relit comme une proposition.

L'outil ne fonctionne pas sans clé API : il faut un compte chez un fournisseur d'IA.

## Cas d'usage

Une consœur vous transmet un dossier de fourniture en cours depuis trois ans, rangé dans un seul dossier :
- des projets et des versions signées ;
- deux avenants ;
- des courriels exportés ;
- un scan ;
- un contrat d'un autre client, gardé « comme exemple ».

En quelques secondes, le registre identifie le contrat principal, les versions qui font foi et l'avenant resté à l'état de projet. Il signale la pièce de l'autre client et le scan qu'il faudra ouvrir à la main. Il note aussi que la lettre de résiliation est annoncée par recommandé, sans preuve de dépôt au dossier.

## Trajet des données

- Reste sur votre ordinateur : les pièces, qui ne sont jamais modifiées, le registre, et la table qui relie chaque marqueur au nom d'origine.
- Est envoyé au fournisseur d'IA que vous avez choisi, avec votre clé : un seul texte pour tout le dossier. Il contient, pour chaque pièce lisible, l'intitulé, les quinze premières et les quinze dernières lignes, et les en-têtes des courriels. Les noms de fichiers sont remplacés par des numéros. Noms, sociétés, adresses et identifiants sont remplacés par des marqueurs sur votre ordinateur avant l'envoi.
- Est envoyé à jerlash.labs : rien.

Avant l'envoi, l'outil affiche le texte exact, le fournisseur, le lieu de traitement et la conservation qu'il déclare, et le coût estimé. Vous pouvez corriger le texte ; rien ne part sans votre accord. L'outil ne vérifie pas les déclarations du fournisseur.

La pseudonymisation automatique est imparfaite : sur notre jeu de contrôle, elle trouve un peu moins de la moitié des noms de personnes. Relisez le texte. Une pièce pseudonymisée peut rester couverte par le secret professionnel, et le choix d'envoyer vous appartient (voir les lignes directrices d'AVOCATS.BE et de l'OVB sur l'usage de l'intelligence artificielle).

Seul le connecteur intégré à l'outil peut communiquer sur le réseau ; un test le vérifie, et un autre exécute l'inventaire complet avec un faux fournisseur, tout autre accès réseau étant bloqué. Le registre est enregistré dans `Documents\Inventaire dossier`, jamais dans le dossier inventorié.

## Tests réalisés

La version 0.1.0 a été mesurée le 31 octobre 2026 sur deux dossiers fictifs. Le premier, de 12 pièces, a servi à écrire les règles, qui le classent sans erreur. Le second, de 16 pièces, a été rédigé à part, sans accès aux règles. Sur ce second dossier :

| Information | Exacte pour |
|---|---|
| Type de pièce | 14 pièces sur 16 |
| Statut (signé ou projet) | 14 sur 16 |
| Document qui fait foi | 15 sur 16 |
| Date de l'acte | 13 sur 16 |
| Sociétés parties | 11 sur 16 |
| Pièce à laquelle elle se rapporte | 8 sur 16 |

Le contrat principal est correctement identifié.

Ces chiffres sont ceux des règles seules. Mode IA (version 0.2.0) : [À COMPLÉTER : mesure réelle sur le même dossier, plus mauvais résultat de trois exécutions, avec le modèle, la date et le coût].

Avant publication, une relecture indépendante du code a relevé treize défauts, dont quatre bloquants. Deux exemples : le registre pouvait être écrit dans le dossier inventorié par un chemin détourné, et un fichier nommé « NON signé » passait pour signé. Tous ont été corrigés et chacun est couvert par un test. Une pièce que seul son nom de fichier dit signée n'est jamais présentée comme faisant foi : le registre indique « à vérifier ».

D'autres tests vérifient trois choses :
- les pièces ne sont pas modifiées (contenu et date) ;
- les fichiers Word piégés sont signalés comme non lus sans interrompre l'inventaire ;
- le registre ne peut pas être écrit dans le dossier inventorié.

Le registre Word a été ouvert dans Word pour vérifier qu'il s'affiche sans erreur.

## Coût

L'outil est gratuit ; l'appel au modèle est facturé par votre fournisseur, sur votre compte. L'outil affiche le coût maximal estimé avant l'envoi, et le coût réel dans le registre. À titre indicatif, un dossier de seize pièces représente environ 25 000 caractères, soit quelques centimes avec les tarifs relevés le 31 octobre 2026.

## Précautions

- Le registre contient les noms des pièces et des parties : il est aussi confidentiel que le dossier.
- Utilisez une clé dédiée à l'outil, avec un plafond de dépense fixé chez le fournisseur.
- Les alertes ne disent pas tout. Une pièce sans alerte reste une pièce à relire.
- Les règles générales d'usage sont sur la page [Précautions](/precautions/).

## Installation

Le guide [Utiliser un outil en local](/guides/utiliser-un-outil-en-local/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la. Copiez `config-ia.example.json` sous le nom `config-ia.json` et choisissez votre fournisseur et votre modèle.
4. Créez un fichier `.env` qui contient votre clé (par exemple `MISTRAL_API_KEY=...`), dans le même dossier.
5. Double-cliquez sur `Inventaire dossier.pyw`.

L'outil fonctionne aussi en ligne de commande (`python -m inventaire_dossier "chemin du dossier"`). Le fichier `README.md` de l'archive décrit les options.

## Versions

0.2.0 (1er novembre 2026) : parties et rattachements proposés par un modèle d'IA, avec votre clé ; écran d'envoi.

0.1.0 (31 octobre 2026) : première version, par règles seules.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil et la pièce mal classée, décrite sans son contenu. N'envoyez pas de pièce réelle.
