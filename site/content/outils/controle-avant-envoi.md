---
draft: true
title: "Contrôle avant envoi"
description: "Vérifier un document Word avant de l'envoyer : commentaires, modifications suivies, texte masqué, propriétés, noms d'autres dossiers. Sans IA, sans réseau."
resume: "Avant d'envoyer un document Word, l'outil recherche ce qui ne devrait pas partir avec lui et localise chaque élément. Il ne modifie jamais le document."
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["vérifier", "préparer un document"]
mise_a_jour: 2026-10-31
telechargement: "/telechargements/controle-avant-envoi-0.1.0.zip"
taille: "33 Ko"
sha256: "20a10e6861584c6759439c0cd9b05d54c684d0c1da40b37e9475427af68abeaa"
---

## Ce que fait l'outil

Il lit le fichier .docx sur votre ordinateur et recherche :

- les commentaires, avec leur auteur ;
- les modifications suivies non acceptées, y compris dans les en-têtes, pieds de page et notes ;
- le texte masqué, écrit en blanc ou en taille minuscule ;
- les blancs à compléter (`[●]`, `[à compléter]`, `XXX`, `TODO`…) et le texte surligné ;
- les noms d'autres clients ou d'autres dossiers, à partir d'une liste que vous lui donnez ;
- les propriétés du document : auteur, dernière personne à l'avoir modifié, société, titre, propriétés personnalisées ;
- les champs qui affichent le nom ou le chemin du fichier ;
- les liens vers vos serveurs internes et le modèle attaché ;
- les objets incorporés, les macros, les variables de document ;
- les métadonnées des photos (EXIF) ;
- les notes de bas de page, pour une dernière relecture.

Le rapport donne, pour chaque élément, l'endroit où il se trouve et la manière de le corriger dans Word. Chaque contrôle porte un statut : détecté, non détecté dans les contrôles réalisés, non vérifié, ou erreur.

## Ce qu'il ne fait pas

Il ne modifie pas le document : les corrections se font dans Word, sur la copie à envoyer. Il ne vérifie ni le fond, ni l'orthographe, ni la numérotation, ni les renvois. Il signale un tableau Excel incorporé sans l'ouvrir. Il n'analyse pas les fichiers .doc, .odt ou PDF, ni un document protégé par mot de passe : dans ces cas, il indique que l'analyse est impossible et ne conclut rien.

Un rapport sans alerte veut dire que les éléments recherchés n'ont pas été trouvés. Il ne dispense pas de relire.

## Cas d'usage

Vous renvoyez au confrère la version révisée d'un contrat de prestation. Le fichier est parti d'un modèle du cabinet. Une collaboratrice y a laissé un commentaire sur votre marge de négociation, le champ « Auteur » contient le nom d'un stagiaire, et une référence à un autre dossier traîne dans une propriété personnalisée. Le rapport liste ces trois éléments en quelques secondes.

## Trajet des données

- Reste sur votre ordinateur : le document, la liste de termes, le rapport.
- Est envoyé à un fournisseur d'IA : rien. L'outil n'utilise pas d'IA.
- Est envoyé à jerlash.labs : rien.

Le code de l'outil n'importe aucun module capable de communiquer sur le réseau, et un test automatique le vérifie à chaque modification. Le rapport contient des extraits du document. Il est enregistré par défaut dans `Documents\Controle avant envoi`, et non à côté du document, pour éviter de le joindre par erreur.

## Tests réalisés

La version 0.1.0 a été testée le 31 octobre 2026 sur un jeu de documents fictifs :

- un contrat qui contient au moins un exemple de chaque piège recherché, et qui s'ouvre normalement dans Word ;
- le même contrat sans aucun piège ;
- un document avec macro et objet incorporé ;
- un fichier protégé par mot de passe et un fichier tronqué.

Tous les pièges plantés sont détectés. Le contrat sans piège ne déclenche aucune alerte. Les deux fichiers illisibles produisent « analyse impossible ». D'autres tests vérifient que le fichier analysé n'est pas modifié (empreinte identique avant et après), qu'aucun accès réseau n'a lieu, et que des fichiers piégés (archive de décompression démesurée, déclaration XML d'entité) sont refusés sans être interprétés.

Ces tests portent sur des documents produits pour l'occasion. Des documents réels, créés par d'autres versions de Word ou par d'autres logiciels, peuvent contenir des structures que l'outil ne connaît pas encore. Signalez-les : ils serviront à étendre le jeu de test.

## Coût

Gratuit : l'outil n'appelle aucun service payant.

## Précautions

- Relancez le contrôle après vos corrections : un « Accepter toutes les modifications » ne retire ni les commentaires ni les propriétés.
- La liste de termes contient des noms de clients. Gardez-la hors des dossiers partagés.
- Le rapport est aussi confidentiel que le document. Ne le joignez pas à l'envoi.
- Les règles générales d'usage sont sur la page [Précautions](/precautions/).

## Installation

Le guide [Utiliser un outil en local](/guides/utiliser-un-outil-en-local/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la, puis double-cliquez sur `Controle avant envoi.pyw`.
4. Cliquez sur « Choisir des documents… ».

Pour les utilisateurs à l'aise avec un terminal, l'outil fonctionne aussi en ligne de commande (`python -m controle_avant_envoi contrat.docx`), avec des codes de sortie exploitables dans un script. Le fichier `README.md` de l'archive décrit les options.

## Versions

0.1.0 (31 octobre 2026) : première version.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil, votre version de Word et le message obtenu. N'envoyez pas le document concerné : décrivez sa structure ou reproduisez le problème sur un document fictif.
