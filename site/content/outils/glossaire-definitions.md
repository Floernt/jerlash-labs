---
draft: true
title: "Glossaire des définitions"
description: "Vérifier les définitions d'un contrat : termes définis deux fois ou de façon divergente, jamais employés, majuscules sans définition."
resume: "L'outil lit un contrat Word et produit son glossaire, avec les points à examiner : définition répétée ou divergente, terme défini jamais employé, terme écrit avec des majuscules sans définition, graphie différente."
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["relire un contrat", "vérifier"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/glossaire-definitions-0.1.0.zip"
taille: "28 Ko"
sha256: "e53f971d3efecbbf57adacba7579440254bf33598586a5a3d75ccd356b57c075"
---

## Ce que fait l'outil

Vous choisissez un contrat. L'outil le lit sur votre ordinateur, sans le modifier, et produit un rapport en Word. Le rapport contient d'abord le glossaire du contrat : chaque terme défini, sa définition, l'article où elle se trouve et le nombre de fois où le terme est employé.

Il signale ensuite les points à examiner :

- un terme défini deux fois, en précisant si les deux définitions diffèrent ; les deux libellés sont cités côte à côte ;
- un terme défini qui n'est employé nulle part ;
- un terme écrit avec des majuscules comme un terme défini (« les Spécifications Techniques »), sans définition dans le contrat ;
- un terme défini employé sous une autre graphie (« Date d'entrée en vigueur » pour « Date d'Entrée en Vigueur ») ;
- un terme employé à l'article 4 alors qu'il n'est défini, en passant, qu'à l'article 10.

Chaque point indique l'article concerné.

## Ce qu'il ne fait pas

L'outil ne modifie pas le contrat et ne réécrit aucune définition. Il ne dit pas si une définition est correcte, complète ou opportune. Il lit les documents Word (.docx) et les fichiers texte, mais pas les notes de bas de page, les en-têtes ni les pieds de page. Un PDF ou un ancien .doc doit d'abord être enregistré en .docx.

Le repérage repose sur des règles, sans IA. Il reconnaît les manières courantes de définir un terme :
- l'article ou l'annexe « Définitions », tableaux compris ;
- « (ci-après « le Prestataire ») » et « ci-après dénommée » ;
- « on entend par » ;
- « (ensemble, les « Parties ») ».

Un terme défini autrement peut lui échapper.

## Cas d'usage

Vous reprenez un contrat de prestation négocié en cinq tours. Avant de l'envoyer à la signature, le rapport vous apprend que :
- « Informations Confidentielles » est défini deux fois, à l'article 1 et à l'article 9, avec des périmètres différents ;
- « Période d'Essai » apparaît trois fois sans définition ;
- « Force Majeure » est défini mais plus jamais employé depuis la suppression de l'ancien article 14.

## Trajet des données

- Reste sur votre ordinateur : le contrat, qui n'est jamais modifié, et le rapport.
- Est envoyé à un fournisseur d'IA : rien. Cette version n'utilise pas d'IA.
- Est envoyé à jerlash.labs : rien.

Le code de l'outil n'importe aucun module capable de communiquer sur le réseau. Un test automatique le vérifie, et un autre exécute l'analyse complète avec les fonctions réseau neutralisées. Le rapport est enregistré dans `Documents\Glossaire des definitions`.

## Tests réalisés

La version 0.1.0 a été mesurée le 1er novembre 2026 sur deux jeux de contrats fictifs. Le premier, de trois contrats, a servi à écrire les règles, qui le traitent sans erreur. Le second, de quatre contrats, a été rédigé à part, sans accès aux règles. Il compte 50 termes définis et 30 défauts. Sur ce second jeu :

| Point relevé | Trouvés | Signalés à tort |
|---|---|---|
| Termes définis | 48 sur 50 | aucun |
| Définitions répétées | 5 sur 5 | aucune |
| Termes jamais employés | 5 sur 5 | aucun |
| Emplois avant définition | 5 sur 5 | aucun |
| Graphies différentes | 5 sur 6 | aucune |
| Termes sans définition | 5 sur 6 | 3 |

Deux définitions répétées dont les libellés disent la même chose en d'autres mots sont signalées comme divergentes : la comparaison porte sur les mots, pas sur le sens. Les fausses alertes « sans définition » sont des expressions écrites avec des majuscules qui ne sont pas des termes définis : elles se reconnaissent d'un coup d'œil.

Avant publication, une relecture indépendante du code a relevé dix-huit défauts, aucun bloquant. Deux exemples : un texte déplacé en suivi des modifications était lu deux fois, ce qui faisait apparaître une fausse définition répétée ; un terme employé seulement au pluriel en « -aux » était dit « jamais employé ». Tous ont été corrigés et chacun est couvert par un test.

D'autres tests vérifient trois choses :
- le contrat n'est pas modifié (contenu et date) ;
- les fichiers Word piégés sont refusés avec un message ;
- aucun rapport existant n'est remplacé.

## Coût

Gratuit : l'outil n'appelle aucun service payant.

## Précautions

- Le rapport reprend les définitions du contrat : il est aussi confidentiel que le contrat.
- Un contrat sans point signalé n'est pas pour autant exempt de défaut de définition.
- Les règles générales d'usage sont sur la page [Précautions](/fr/ethique/precautions-outils-ia-avocat/).

## Installation

Le guide [Utiliser un outil en local](/guides/installer-outil-python-windows/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la, puis double-cliquez sur `Glossaire.pyw`.

L'outil fonctionne aussi en ligne de commande (`python -m glossaire_definitions "chemin du contrat.docx"`). Le fichier `README.md` de l'archive décrit les options.

## Versions

0.1.0 (1er novembre 2026) : première version.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil et la formulation mal traitée, recopiée sans nom ni donnée du client. N'envoyez pas de contrat réel.
