# Spécification - Contrôle avant envoi (P05 Lite)

Version 0.1.0 - 2026-10-31 - Parcours Factory : renforcé (documents de dossier, ADR-007)

## Besoin

Avant d'envoyer un document Word à l'extérieur, l'avocat doit s'assurer qu'il ne contient ni commentaires internes, ni modifications révélant une négociation, ni métadonnées ou noms d'autres dossiers. L'inspecteur de document de Word existe mais n'est pas lancé systématiquement, ne cherche pas les noms d'autres clients et ne produit pas de trace du contrôle.

## Périmètre

Inclus : lecture d'un .docx ou .docm, quatorze contrôles (liste dans `src/controle_avant_envoi/controles.py`, `CATALOGUE`), rapport texte, HTML et JSON, fenêtre graphique, ligne de commande.

Exclus de la version Lite : toute modification du document (nettoyage, production d'une copie propre), contrôle par un modèle d'IA, contrôle des renvois et de la numérotation, analyse du contenu des objets incorporés, formats .doc, .odt et PDF.

## Mode d'exécution (ADR-010)

Application locale Python, mode B sans aucune IA distante. Comparaison faite :

| Option | Avantages | Inconvénients |
|---|---|---|
| Page web locale (navigateur) | rien à installer | analyse du .docx en JavaScript = dépendance tierce à figer ; rapport et fichiers moins faciles à enregistrer |
| Application Python, bibliothèque standard seule (retenue) | aucune dépendance, code court et lisible, testable en ligne de commande, fenêtre native | Python à installer |
| Exécutable empaqueté (PyInstaller) | rien à installer | dépendance de construction, exécutable non signé signalé par Windows ; prévu dans une version ultérieure |

## Trajet des données

Le document est lu une fois, en lecture seule, et traité en mémoire. Rien ne quitte la machine : le code n'importe aucun module réseau (vérifié par test statique), et l'analyse est testée avec les fonctions réseau neutralisées. La fenêtre graphique écrit le rapport par défaut dans `Documents\Controle avant envoi`, hors du dossier du document, pour éviter qu'il soit joint par erreur ; en ligne de commande, le dossier est celui passé en option. Deux documents de même nom produisent deux rapports distincts. Le rapport contient des extraits du document : il est aussi confidentiel que lui.

## Règles de résultat

- Chaque contrôle a un statut : détecté, non détecté dans les contrôles réalisés, non vérifié, erreur.
- Un fichier illisible, protégé, au format strict, ou une partie XML suspecte produit « analyse impossible » ou « analyse incomplète », jamais « rien détecté ».
- Le verdict favorable rappelle que seuls les contrôles listés ont été réalisés.
- L'empreinte SHA-256 est calculée avant et après l'analyse ; une différence rend l'analyse incomplète.

## Sécurité des entrées

Limites : 150 Mo par fichier, 60 Mo par partie, 400 Mo décompressés, 5 000 éléments, taux de compression 1 000. Toute partie XML est d'abord lue par expat, qui refuse une déclaration DOCTYPE ou ENTITY quel que soit l'encodage (UTF-8, UTF-16). Toute erreur de lecture de l'archive (CRC, compression non prise en charge) produit « analyse impossible ». Le rapport HTML échappe tout contenu issu du document et porte une Content-Security-Policy qui interdit tout script.

## Jeu de test

`factory/jeux-de-test/F-DOCX-01` : pièce piégée (ouvrable dans Word), pièce propre, pièce à macros (analyse seulement), pièce protégée, pièce tronquée. Résultats attendus : `attendu/P05.json`.

## Coût

Aucun : pas d'appel à un fournisseur d'IA.
