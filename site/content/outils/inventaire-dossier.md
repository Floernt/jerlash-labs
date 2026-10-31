---
title: "Inventaire d'un dossier"
description: "Dresser le registre des pièces d'un dossier contractuel : type, statut, date, parties, version qui fait foi, et ce qui ne devrait pas s'y trouver. Sur votre ordinateur, sans IA."
resume: "L'outil parcourt le dossier d'une affaire contractuelle et produit un registre des pièces en Word, avec des alertes : acte non signé, pièce d'un autre client, scan illisible, envoi recommandé sans preuve."
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["reprendre un dossier", "vérifier"]
mise_a_jour: 2026-10-31
telechargement: "/telechargements/inventaire-dossier-0.1.0.zip"
taille: "27 Ko"
sha256: "090b4964b4c348d4162ddb6d17a544d5d68979ba69d18b01fc070ed94350cc79"
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

Le classement repose sur des règles, sans IA. Il se trompe dans les cas que les règles ne prévoient pas, et le rattachement entre pièces est son point le plus faible (voir les mesures ci-dessous). Le registre se relit comme une proposition.

## Cas d'usage

Une consœur vous transmet un dossier de fourniture en cours depuis trois ans, rangé dans un seul dossier :
- des projets et des versions signées ;
- deux avenants ;
- des courriels exportés ;
- un scan ;
- un contrat d'un autre client, gardé « comme exemple ».

En quelques secondes, le registre identifie le contrat principal, les versions qui font foi et l'avenant resté à l'état de projet. Il signale la pièce de l'autre client et le scan qu'il faudra ouvrir à la main. Il note aussi que la lettre de résiliation est annoncée par recommandé, sans preuve de dépôt au dossier.

## Trajet des données

- Reste sur votre ordinateur : les pièces, qui ne sont jamais modifiées, et le registre.
- Est envoyé à un fournisseur d'IA : rien. Cette version n'utilise pas d'IA.
- Est envoyé à iavocat.be : rien.

Le code de l'outil n'importe aucun module capable de communiquer sur le réseau. Un test automatique le vérifie, et un autre exécute l'inventaire complet avec les fonctions réseau neutralisées. Le registre est enregistré dans `Documents\Inventaire dossier`, jamais dans le dossier inventorié.

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

Avant publication, une relecture indépendante du code a relevé treize défauts, dont quatre bloquants. Deux exemples : le registre pouvait être écrit dans le dossier inventorié par un chemin détourné, et un fichier nommé « NON signé » passait pour signé. Tous ont été corrigés et chacun est couvert par un test. Une pièce que seul son nom de fichier dit signée n'est jamais présentée comme faisant foi : le registre indique « à vérifier ».

D'autres tests vérifient trois choses :
- les pièces ne sont pas modifiées (contenu et date) ;
- les fichiers Word piégés sont signalés comme non lus sans interrompre l'inventaire ;
- le registre ne peut pas être écrit dans le dossier inventorié.

Le registre Word a été ouvert dans Word pour vérifier qu'il s'affiche sans erreur.

## Coût

Gratuit : l'outil n'appelle aucun service payant.

## Précautions

- Le registre contient les noms des pièces et des parties : il est aussi confidentiel que le dossier.
- Les alertes ne disent pas tout. Une pièce sans alerte reste une pièce à relire.
- Les règles générales d'usage sont sur la page [Précautions](/precautions/).

## Installation

Le guide [Utiliser un outil en local](/guides/utiliser-un-outil-en-local/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la, puis double-cliquez sur `Inventaire dossier.pyw`.

L'outil fonctionne aussi en ligne de commande (`python -m inventaire_dossier "chemin du dossier"`). Le fichier `README.md` de l'archive décrit les options.

## Versions

0.1.0 (31 octobre 2026) : première version.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil et la pièce mal classée, décrite sans son contenu. N'envoyez pas de pièce réelle.
