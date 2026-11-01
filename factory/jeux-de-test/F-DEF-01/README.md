# F-DEF-01 — Contrats fictifs chargés de défauts de définition

Version 1.0, 1er novembre 2026. Les contrats sont entièrement fictifs : les personnes, les sociétés et leurs numéros d'entreprise sont inventés.

## Les contrats

Jeu de développement, rédigé avec l'outil et servant à écrire ses règles :
- un contrat de fourniture de bouteilles, avec un article « Définitions » ;
- une convention de cession de parts, dont les définitions sont regroupées dans un tableau en annexe ;
- une convention de confidentialité, avec des guillemets droits et courbes et des définitions énumérées a), b), c).

Jeu de contrôle, rédigé à part par un agent qui n'avait accès ni au code ni au jeu de développement :
- quatre contrats de 60 à 70 paragraphes ;
- 50 termes définis et 30 défauts annotés.
Il ne sert qu'à mesurer, et ses écarts ne sont pas affichés par défaut.

Chaque contrat contient, mêlés aux usages réels de rédaction, des défauts annotés :
- une définition répétée, divergente ou non ;
- un terme défini jamais employé ;
- un terme écrit avec des majuscules sans définition ;
- une graphie différente d'un terme défini ;
- un terme employé avant sa définition en cours de texte.

Il contient aussi des pièges qui ne sont pas des défauts : noms des parties, codes et juridictions, sigles, adresses, termes employés en minuscules dans leur sens courant, termes de l'article des définitions employés dans le préambule.

Le générateur reproduit trois habitudes de Word :
- espaces insécables à l'intérieur des guillemets français ;
- termes entre guillemets en gras, dans un fragment séparé ;
- définitions en tableau.

## Fichiers

```
sources/              un fichier par contrat : « fichier: <nom>.docx », « --- », puis un paragraphe par ligne (« | » : tableau)
sources-controle/     jeu de contrôle, même format
generer.py            produit pieces/ et pieces-controle/ (.docx)
attendu/P02.json      défauts attendus du jeu de développement, avec une note par défaut
attendu/P02-controle.json, attendu/P02-planchers.json   défauts attendus du contrôle ; planchers de non-régression
evaluer.py            mesure P02 sur les deux jeux, par catégorie (rappel et précision)
resultats/            un compte rendu par version mesurée
```

```
python -I factory/jeux-de-test/F-DEF-01/generer.py             régénérer
python -I factory/jeux-de-test/F-DEF-01/generer.py --verifier  contrôler que les .docx correspondent aux sources
python -I factory/jeux-de-test/F-DEF-01/evaluer.py             mesurer
```

## Conventions d'annotation

- Un terme est désigné par sa forme de définition, sans article ni guillemets. Le singulier et le pluriel sont un seul terme.
- Un emploi est une occurrence avec majuscule hors de la définition elle-même. Les titres d'articles et les lignes en capitales n'en sont pas.
- « Avant définition » ne vise qu'un terme défini en cours de texte (parenthèse, « ci-après », « on entend par » hors de l'article des définitions) et employé plus tôt.
- Un terme défini employé en minuscules dans son sens courant n'est ni un emploi ni une variante.
