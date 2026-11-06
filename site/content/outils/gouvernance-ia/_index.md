---
draft: false
title: "Gouvernance de l'IA"
description: "Une boîte à outils pour décider quels outils d'IA une organisation juridique utilise, pour quoi, avec quelles données, et comment le prouver, avec une profondeur proportionnée aux outils réellement en place."
aliases: ["/fr/outils/gouverner-l-ia-au-cabinet/"]
statut: "version de travail"
version: "0.3"
licence: "CC BY-NC 4.0"
programme: "H1"
usage_ia: "L'IA a été utilisée pour la rédaction et la structuration de cette version de travail."
controles: "Version de travail, sans relecture externe ni évaluation."
cascade:
  type: "toolkit"
---

Les chartes d'utilisation de l'IA reprennent souvent les mêmes consignes : « utiliser des outils sécurisés », « faire relire », « ne pas copier-coller ». Ces consignes sont justes, mais on ne peut pas toujours les vérifier. Elles ne disent ni à quelles conditions un outil a été autorisé, ni ce que doit savoir faire la personne qui relit, ni comment montrer qu'un contrôle a réellement eu lieu.

Une gouvernance est donc nécessaire. Sa profondeur, en revanche, ne doit pas être la même partout. Un cabinet qui travaille avec un seul outil dont il a vérifié le contrat, les garanties de confidentialité et le respect du secret professionnel n'a pas besoin d'une procédure d'homologation, d'une grille de notation et de six registres : l'outil offre lui-même les garanties que ces procédures chercheraient à établir. À l'inverse, une organisation dont les dossiers circulent dans plusieurs outils aux garanties inégales doit pouvoir arbitrer, outil par outil et donnée par donnée.

Cette boîte à outils propose donc trois niveaux de gouvernance. La première décision de la gouvernance est de déterminer le sien. Tout le reste en découle.

## Quel niveau pour votre organisation ?

Le niveau se détermine outil par outil, puis l'organisation retient le niveau le plus élevé de ses outils.

Pour chaque outil, deux questions suffisent.

1. **Sa conformité a-t-elle été vérifiée sur pièces ?** La [fiche de conformité](niveau-1/#la-fiche-de-conformité-dun-outil) passe en revue une dizaine de points : contrat, secret professionnel, réutilisation des données, protection des données, sous-traitants, effacement, incidents. La conformité est *établie* si tous les points sont satisfaits, *partielle* si tous ont été examinés mais que certains ne le sont pas, *non établie* si des points restent à vérifier.
2. **Quelles données y entrent ?** Seulement des données publiques ou internes non sensibles (classes D0 et D1 de la [classification](donnees/)), ou aussi des données confidentielles, couvertes par le secret ou particulièrement protégées (D2 à D4) ?

| Conformité de l'outil | Données D0 et D1 seulement | Données D2 à D4 |
| --- | --- | --- |
| Établie | Niveau 1 | Niveau 1 |
| Partielle | Niveau 1 | Niveau 2 |
| Non établie | Niveau 1 | Niveau 3 |

Un outil qui agit seul (envoyer, déposer, modifier un registre, signer) relève du niveau 3 pour cet usage, quelle que soit sa conformité, parce que ses actions doivent être autorisées une à une ([les agents](supervision/#agents-et-actions-externes)).

Ce tableau est une proposition de travail. Chaque organisation peut le modifier, par exemple en plaçant au niveau 2 tout usage d'un outil partiellement conforme.

## Les trois niveaux

| Niveau | Situation | Ce qu'il faut produire |
| --- | --- | --- |
| 1 | Chaque outil est conforme, ou ne reçoit que des données D0 et D1 | Un référent, l'inventaire des outils, une fiche de conformité par outil, une règle de vérification des productions, un canal d'incident, une formation courte. Le tout tient en [une page](niveau-1/). |
| 2 | Plusieurs outils, avec des niveaux de conformité différents | Le niveau 1, plus une matrice qui dit quelles classes de données et quels usages sont admis dans chaque outil, des rôles identifiés et une supervision graduée. |
| 3 | Des données sensibles circulent dans des outils dont la conformité n'est pas établie, ou des outils agissent seuls | Une gouvernance détaillée et une [homologation](homologation/) qui arbitre la conformité de chaque outil pour chaque usage, avec ses conditions éliminatoires, ses tests et ses registres. |

Le niveau n'est pas acquis une fois pour toutes. Un nouvel outil, un nouveau contrat, une nouvelle catégorie de données ou un incident peuvent faire monter (ou descendre) l'organisation d'un niveau. Le référent refait le diagnostic à chacun de ces changements, et au moins une fois par an.

## Le parcours selon le niveau

**Niveau 1.** Lire [la page du niveau 1](niveau-1/) et l'appliquer. Les autres modules servent de référence, chacun indiquant en tête ce qu'il demande au niveau 1. La [charte](charte/) peut se limiter à quelques articles.

**Niveau 2.** Faire le niveau 1, puis classer les données avec [le module données](donnees/), répartir les rôles avec [la gouvernance](gouvernance/), dresser la matrice outils × données × usages, et graduer [la supervision](supervision/) selon les usages.

**Niveau 3.** Mettre en place [la gouvernance](gouvernance/) complète, [les données](donnees/), [l'homologation](homologation/), [la supervision](supervision/) et [les opérations](operations/), puis rédiger et adopter [la charte](charte/), qui consigne les choix faits en chemin. Enregistrer ensuite les incidents, les changements et les revues, et réviser la charte quand ces choix changent.

À tous les niveaux, la charte vient en dernier : adoptée d'emblée, elle resterait une déclaration de principes que rien ne permet de vérifier, ce que décrit la page [Pourquoi les chartes échouent](pourquoi-les-chartes-echouent/).

## Le tableur des niveaux 2 et 3

Aux niveaux 2 et 3, les fiches et les matrices deviennent vite difficiles à tenir dans un document texte. Le [tableur Gouvernance de l'IA](/telechargements/gouvernance-ia-matrices-0.3.xlsx) (format Excel) les rassemble : l'inventaire des outils avec leur fiche de conformité, le calcul du niveau de chaque outil et de l'organisation, les matrices outils × données et outils × usages, les rôles, puis, pour le niveau 3, les conditions éliminatoires, la grille de notation et les registres. Les cellules jaunes se remplissent, les grises se calculent, et les listes de choix se règlent dans l'onglet « Paramètres ». Le fichier ne contient qu'une ligne d'exemple fictive. Il est aussi disponible, avec le script qui le génère, dans le [dépôt du projet](https://github.com/Floernt/jerlash-labs/tree/main/outils/gouvernance-ia).

## Ce que contient la boîte à outils

| Module | Contenu | À partir du niveau |
| --- | --- | --- |
| [Pourquoi les chartes échouent](pourquoi-les-chartes-echouent/) | L'analyse d'une charte de cabinet type, ce qu'il faut en garder et ses dix faiblesses de structure | Lecture conseillée |
| [Le niveau 1](niveau-1/) | La gouvernance minimale et la fiche de conformité d'un outil | 1 |
| [La gouvernance](gouvernance/) | Qui décide, qui répond de quoi, comment contester une décision | 1 (version réduite), 3 (complète) |
| [Les données](donnees/) | La classification D0 à D4 et les questions à se poser avant le traitement | 2 |
| [L'homologation](homologation/) | Les conditions éliminatoires, la notation, les tests et la décision pour un outil et un usage | 3 |
| [La supervision](supervision/) | Le contrôle des résultats et des actions, et sa preuve | 1 (vérification d'un livrable), 2 (niveaux de contrôle) |
| [Les opérations](operations/) | Les incidents, la formation, la traçabilité et les registres | 1 (incidents et formation), 3 (registres) |
| [La charte](charte/) | Le document normatif interne, qui consigne les choix faits dans les modules | 1 (version courte), 3 (seize articles) |
| [Les sources](sources-et-versions/) | Les sources juridiques et les points à confirmer | Référence |

## Statut de cette version

Il s'agit d'une version de travail. L'ensemble n'est ni une charte adoptée, ni un label de conformité, ni un avis juridique individualisé. Les niveaux, seuils, pondérations, fréquences et rôles proposés dans les modules sont des propositions de travail. Chaque organisation les fixe elle-même, par sa propre gouvernance. Ce ne sont ni des obligations légales, ni des critères scientifiquement validés.

Le premier public est celui des cabinets d'avocats belges, de toutes tailles. Viennent ensuite les directions juridiques, dans le contexte du droit continental européen. Une adaptation reste nécessaire pour chaque organisation et chaque ordre juridique.

La supervision humaine est au centre de l'ensemble. Elle ne consiste pas à attendre qu'un professionnel clique sur « Valider » : elle suppose une compétence, un accès aux éléments pertinents et le pouvoir de contester, de modifier ou de refuser. La boîte à outils cherche à réunir les conditions dans lesquelles ce jugement peut s'exercer. Elle ne le remplace pas. Un protocole de recherche, destiné à mesurer la capacité des superviseurs à détecter une erreur, à la corriger, à contester un résultat et à justifier leur choix, l'accompagne. Il n'a été ni validé ni exécuté.

Une règle vaut à tous les niveaux : les exemples et les jeux de tests ne contiennent jamais de données réelles de clients ni d'éléments couverts par le secret professionnel. Ils reposent sur des scénarios fictifs.
