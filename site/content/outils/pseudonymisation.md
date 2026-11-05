---
draft: true
title: "Pseudonymisation"
description: "Remplacer les noms, adresses et identifiants belges d'un texte par des marqueurs avant de le soumettre à une IA, puis rétablir les noms dans la réponse. Sur votre ordinateur, sans réseau."
resume: "L'outil remplace les noms, adresses et numéros d'un texte par des marqueurs comme [PERSONNE_1], vous fait relire le résultat, puis remet les vrais noms dans la réponse de l'IA. Il ne trouve pas tout : la relecture est obligatoire."
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["préparer un document", "protéger des données"]
mise_a_jour: 2026-10-31
telechargement: "/telechargements/pseudonymisation-0.1.0.zip"
taille: "33 Ko"
sha256: "c45a4a7ac7719a46e3dc81120959b546dab8538050c0e9c460e4a6cacc071af3"
---

## Ce que fait l'outil

Vous collez un texte ou ouvrez un fichier (.txt ou .docx). L'outil repère :

- les noms de personnes précédés d'une civilité (M., Mme, Me…) ou écrits avec le nom en capitales, puis toutes les autres occurrences de ces noms ;
- les sociétés accolées à leur forme sociale (SRL, SA, ASBL, BV, NV…) ;
- les adresses (rue, numéro, code postal, localité) ;
- les numéros de registre national, numéros d'entreprise et de TVA, IBAN et numéros de carte, dont il vérifie la somme de contrôle ;
- les courriels, les numéros de téléphone, les dates de naissance, les plaques d'immatriculation et les numéros de rôle.

Chaque donnée est remplacée par un marqueur : `M. Thomas Wilmotte` devient `M. [PERSONNE_1]`, et chaque mention de Wilmotte dans le texte devient `[PERSONNE_1]`. L'IA peut ainsi suivre qui fait quoi sans connaître les noms.

Vous relisez le texte pseudonymisé à côté de l'original. Vous pouvez conserver une donnée que l'outil a remplacée à tort, ou ajouter un nom qu'il a manqué. Vous ne pouvez enregistrer le résultat qu'après avoir confirmé cette relecture.

Une fois la réponse de l'IA obtenue, l'onglet « Rétablir » remet les vrais noms à la place des marqueurs.

## Ce qu'il ne fait pas

L'outil pseudonymise, il n'anonymise pas. La différence est importante : un texte pseudonymisé peut encore permettre de reconnaître une personne. Les données remplacées sont conservées dans la table de correspondance, et le contexte (une fonction, une ville, une date, un fait marquant) suffit parfois à reconnaître quelqu'un. Le texte pseudonymisé reste donc une donnée personnelle, et il reste couvert par le secret professionnel. L'outil réduit ce qui part, il ne vous dispense pas de décider si la pièce peut être soumise à une IA.

Les règles de détection ne trouvent pas tout, et les mesures ci-dessous le montrent. Les noms cités sans civilité, les prénoms seuls, les surnoms et les initiales passent souvent à travers.

Pour un document Word, seul le corps du texte est repris : les en-têtes, pieds de page, notes et commentaires ne le sont pas. Le résultat est un texte brut, sans la mise en forme du document. L'outil ne lit pas les PDF : copiez-en le texte et collez-le dans la fenêtre.

## Cas d'usage

Vous voulez qu'une IA vous aide à structurer des conclusions dans un litige de bail. Vous collez l'exposé des faits. L'outil remplace les noms du bailleur et de la locataire, leurs adresses, le numéro national du bailleur et le compte bancaire. Vous constatez qu'il a manqué le prénom du voisin, cité seul au dernier paragraphe, et vous l'ajoutez. Vous envoyez le texte pseudonymisé à l'IA. Vous collez sa réponse dans l'onglet « Rétablir » et retrouvez vos noms.

Si vous connaissez les noms des parties, donnez-les à l'outil avant de lancer la détection. Il les recherche dans tout le texte, nom de famille seul compris. C'est le moyen le plus sûr de rattraper ce que les règles ne voient pas.

## Trajet des données

- Reste sur votre ordinateur : le texte d'origine, le texte pseudonymisé, la table de correspondance, la réponse rétablie.
- Est envoyé à un fournisseur d'IA : rien par l'outil. C'est vous qui copiez le texte pseudonymisé vers l'IA de votre choix.
- Est envoyé à jerlash.labs : rien.

Le code de l'outil n'importe aucun module capable de communiquer sur le réseau. Un test automatique le vérifie à chaque modification, et un autre exécute le parcours complet avec les fonctions réseau neutralisées.

La table de correspondance contient les données d'origine. Elle est enregistrée dans `Documents\Pseudonymisation`. Ne l'envoyez jamais avec le texte.

## Tests réalisés

La version 0.1.0 a été mesurée le 31 octobre 2026 sur le jeu de test fictif F-IDENT-01, en deux temps. Le **jeu de développement** a servi à écrire les règles : 6 textes, 102 données, toutes trouvées. Ce chiffre dit seulement que les règles couvrent les cas pour lesquels elles ont été écrites.

Le **jeu de contrôle** a été rédigé à part, sans accès aux règles. Il compte 8 pièces : jugement, échange de courriels entre confrères, mise en demeure, cession de parts, expertise médicale, procès-verbal d'audition, compte rendu d'entretien, et une note sans aucune donnée personnelle. Ce jeu mesure ce que l'outil trouve dans des textes qu'il ne connaît pas :

| Données | Trouvées entièrement |
|---|---|
| Numéros national, d'entreprise, IBAN, cartes | 21 sur 21 |
| Courriels | 8 sur 8 |
| Téléphones | 8 sur 9 |
| Adresses | 18 sur 21 |
| Sociétés | 18 sur 23 |
| Plaques | 3 sur 4 |
| Dates de naissance | 3 sur 7 |
| Noms de personnes | 37 sur 83 |
| Références de dossier | 2 sur 10 |
| **Total** | **118 sur 186 (63 %)** |

Sur 138 remplacements, 3 portaient sur autre chose qu'une donnée personnelle. Une seule de ces fausses alertes concerne la note sans donnée personnelle : l'outil y a pris une référence à la Cour européenne des droits de l'homme pour une adresse.

Autrement dit, l'outil est fiable pour les numéros. Il ne l'est pas pour les noms cités sans civilité. C'est la raison pour laquelle la relecture est obligatoire.

Avant publication, une relecture indépendante du code a relevé treize défauts, dont quatre bloquants. Le plus grave : la fenêtre pouvait enregistrer un texte modifié après la relecture, avec des noms en clair. Tous ont été corrigés, et chacun est couvert par un test.

D'autres tests automatiques vérifient que le fichier d'origine n'est jamais modifié, que les fichiers Word piégés sont refusés, qu'aucun fichier existant n'est remplacé et que le rétablissement retrouve les marqueurs même légèrement modifiés par l'IA (`[Personne_1]`, `PERSONNE 1`).

## Coût

Gratuit : l'outil n'appelle aucun service payant.

## Précautions

- Relisez toujours le texte pseudonymisé en entier avant de l'envoyer.
- Retirez aussi ce qui permet de reconnaître une personne sans la nommer : une fonction rare, une adresse décrite, une date et un lieu précis.
- Gardez la table de correspondance hors des dossiers partagés, et supprimez-la quand vous n'en avez plus besoin.
- Les règles générales d'usage sont sur la page [Précautions](/fr/ethique/precautions/).

## Installation

Le guide [Utiliser un outil en local](/guides/utiliser-un-outil-en-local/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la, puis double-cliquez sur `Pseudonymisation.pyw`.

L'outil fonctionne aussi en ligne de commande (`python -m pseudonymisation pseudonymiser piece.docx`). Le fichier `README.md` de l'archive décrit les options.

## Versions

0.1.0 (31 octobre 2026) : première version.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil et le type de donnée manquée ou remplacée à tort. N'envoyez pas le texte concerné : reproduisez le cas sur un exemple fictif. Chaque cas signalé sert à enrichir le jeu de test.
