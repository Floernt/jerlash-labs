---
draft: false
title: "Outiller l'avocat : personnaliser plutôt que standardiser"
date: 2026-11-08
description: "Les avocats refusent de standardiser leur pratique, alors que l'automatisation exige de la découper en étapes. La sortie passe par des outils que l'avocat adapte lui-même, à partir d'une pratique qu'il a d'abord rendue explicite."
statut: "version de travail"
version: "0.2"
programme: "transversal"
date_arret_recherches: 2026-11-06
controles: "Version de travail, sans relecture externe."
usage_ia: "Claude Opus 5.5 (novembre 2026) a été utilisé pour rédiger un premier jet à partir de la transcription d'un entretien oral de l'auteur, selon l'angle qu'il a retenu."
licence: "CC BY 4.0"
financement: "aucun"


---

Nous échangeons régulièrement avec de jeunes entreprises de la legaltech qui cherchent à comprendre le marché juridique avant de construire leur produit. Une question revient souvent en fin d'entretien : quel problème mérite réellement d'être résolu pour les cabinets d'avocats ? La difficulté que ces équipes décrivent est presque toujours la même : chaque avocat rencontré veut quelque chose de différent, et la liste des fonctionnalités demandées ne cesse de s'allonger. Ce texte rassemble la réponse que nous leur donnons, parce qu'elle touche à une tension que nous rencontrons aussi chaque fois que nous construisons un outil.

## Une pratique qui refuse le moule

Les points de douleur ne manquent pas dans la profession. La difficulté tient cependant ailleurs : les avocats travaillent de manière très individuelle. Chacun a ses habitudes, sa manière d'aborder un dossier, ses propres raccourcis. Il est donc difficile de construire un outil qui convienne à tous.

À notre sens, la cause est plus profonde. Les avocats ne savent pas, et souvent ne veulent pas, standardiser leur pratique. Si l'on demande à un avocat de s'arrêter et de décrire ce qu'il fait à la première, à la deuxième puis à la troisième étape d'un dossier, l'exercice échoue la plupart du temps. Sa pratique est intuitive. Nous pensons que cette résistance a une raison : l'avocat vend, d'une certaine manière, une part de lui-même. Standardiser sa façon de travailler, c'est accepter qu'elle soit reproductible, donc qu'elle ne lui appartienne plus tout à fait.

Le résultat se voit sur le marché. Depuis des années, deux catégories d'outils se succèdent : des applications généralistes qui prétendent convenir à tout le monde, et des outils très spécialisés, qui optimisent une tâche si précise qu'ils servent rarement. Ni les unes ni les autres ne s'insèrent dans la pratique réelle d'un cabinet.

## Le workflow est dans la tête

L'avocat suit pourtant une méthode. Face à un client, il pose des questions ; les réponses l'amènent à d'autres questions. À force de pratiquer la même matière jour après jour, il finit par avoir une sorte d'algorithme en tête, qui guide l'entretien et la suite du dossier. C'est ce que nous appelons un workflow (un enchaînement d'étapes).

L'enjeu consiste à faire sortir cet algorithme de la tête, d'abord sur papier, ensuite dans un outil numérique. Il faut découper chaque séquence, identifier chaque étape. Qu'il y en ait dix, cent ou mille importe peu. Ce qui compte, c'est que chaque étape soit assez petite, « atomique », pour être automatisée.

Prenons deux exemples tirés de notre propre pratique. Le premier est très simple : un workflow qui permet aux clients de prendre rendez-vous pour un appel vidéo. Un courriel arrive, il est intégré dans un gabarit, et la suite se déroule seule. N'importe qui au cabinet peut s'en servir. Le second est plus élaboré : des tâches planifiées confiées à une IA, qui mènent une partie des recherches et dont les résultats sont ensuite repris par l'avocat. Dans les deux cas, nous appliquons le même principe : faire une chose une fois, pour pouvoir la refaire un million de fois. Une réponse adressée à un client par courriel peut souvent devenir un modèle pour d'autres.

## La tension

Le problème apparaît alors. L'automatisation exige précisément ce que l'avocat refuse : expliciter, découper, standardiser. Pour qu'une technologie résolve un point de douleur, il faut que la solution soit formalisée. Or la plupart des avocats n'ont ni l'envie ni, souvent, la souplesse d'esprit nécessaire pour penser leur pratique en processus. La formation juridique encourage une certaine rigidité, et nous ne nous excluons pas du constat.

Illustrons cet élément. Un avocat a récemment rendu public un serveur MCP (Model Context Protocol, un protocole qui permet de connecter une IA à des outils et à des sources externes). Nous l'avons branché à notre propre assistant : c'est une manière de communiquer avec son cabinet. Nous en déduisons qu'il a construit un système qui fait passer les éléments reçus d'un client par une série d'outils, pour mieux préparer son conseil. Ce qui nous retient dans cet exemple, c'est que cet avocat a dû penser sa manière de produire un conseil comme une chaîne d'étapes, ce que la plupart des avocats ne font jamais. Beaucoup aiment la technologie ; peu se demandent comment partager, construire ou optimiser leur savoir avec elle.

## Une piste : laisser l'avocat adapter l'outil

Si l'on ne peut pas imposer la standardisation, il reste une autre voie : ouvrir l'outil à la personnalisation.

L'IA rend cette adaptation beaucoup plus accessible qu'auparavant, puisqu'on peut désormais décrire en langage naturel ce que l'on veut créer ou modifier. Nous pensons que c'est par là que les outils trouveront leur place dans les cabinets : par la personnalisation plutôt que par la standardisation.

Nous n'affirmons pas ici que la personnalisation règle tout. Elle déplace la difficulté. Pour adapter un outil, l'utilisateur doit savoir dire ce qu'il veut, et beaucoup d'avocats n'ont jamais formulé leur pratique. Ils n'ont pas les éléments à fournir, parce qu'ils n'y ont jamais pensé. Personnaliser suppose donc un travail préalable d'extraction : faire sortir de la tête de l'avocat l'algorithme qu'il suit sans le savoir. C'est là que la tension se résout, au moins en partie. L'avocat n'a pas à se plier à la méthode d'un autre ; il lui suffit de rendre explicite la sienne, et l'outil s'y adapte.

## Ce que nous en retenons pour qui construit des outils

Aux équipes qui conçoivent des outils pour les cabinets, nous proposons trois pistes concrètes. Partir de la pratique explicitée d'un avocat plutôt que d'une liste de fonctionnalités, quitte à consacrer le premier temps de l'accueil d'un utilisateur à l'aider à décrire ses propres étapes. Laisser l'avocat modifier l'outil lui-même, en langage naturel, plutôt que de lui livrer une solution figée. Accepter enfin que ce travail d'extraction fait partie du produit, et qu'il demande d'accompagner l'utilisateur.

Cette question rejoint nos travaux sur la supervision humaine de l'IA. Superviser une IA autrement qu'en cliquant sur « valider » à la fin d'un traitement suppose, là aussi, que l'avocat sache décrire ce qu'il attend à chaque étape. Nous y reviendrons dans les travaux du programme H1.
