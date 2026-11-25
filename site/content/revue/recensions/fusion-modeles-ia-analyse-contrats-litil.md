---
draft: true
title: "Fusionner trois entraînements pour mieux lire les contrats : la note de recherche de Litil"
date: 2026-11-12
description: "Fusion de modèles d'IA pour l'analyse de contrats : Litil annonce 92,2 % de clauses bien repérées. Ce que ses propres tableaux nuancent."
objet: "article"
oeuvre:
  auteurs: ["LiTiL Research"]
  titre: "Soup du Jour"
  publication: "Litil, blog (Research notes)"
  date: 2026-11-05
  url: "https://litil.ai/blog/soup-du-jour"
  consulte_le: 2026-11-12
programme: "T1"
date_arret_recherches: 2026-11-12
controles: "Texte relu par l'auteur. Les chiffres sont repris des tableaux publiés dans la note ; les données d'expérience d'octobre 2026 citées par Litil ne sont pas publiées et n'ont pas été vues. L'article de Wortsman et al. (2022) n'a pas été relu pour cette recension. Aucune relecture externe."
usage_ia: "L'IA a été utilisée pour lire la note, proposer une rédaction et structurer le texte selon l'angle retenu par l'auteur. L'auteur a relu le texte."
licence: "CC BY 4.0"
financement: "aucun"
conflits_interets: "aucun"
---

Litil se présente comme un « laboratoire d'IA juridique » qui développe des modèles ouverts pour l'analyse de documents juridiques. Son équipe compte plusieurs avocats-développeurs. La note recensée, publiée le 5 novembre 2026 sans nom d'auteur, raconte une expérience technique précise : comment le laboratoire a amélioré son modèle de repérage de clauses contractuelles en faisant la moyenne de trois entraînements. Le texte est rédigé pour des ingénieurs. Nous le recensons parce qu'il fait une chose rare chez un acteur commercial : il publie ses tableaux, y compris ceux qui ne l'arrangent pas, ce qui permet de le discuter sur pièces.

## Le propos de la note

La technique décrite porte le nom de « model soup » (soupe de modèles). Elle a été proposée par Wortsman et al. en 2022. On entraîne plusieurs fois le même modèle, avec les mêmes données et les mêmes réglages, en ne changeant que la graine aléatoire (le paramètre qui fixe le hasard de l'entraînement). On fait ensuite la moyenne des poids obtenus. Le résultat est un modèle unique, qui ne coûte rien de plus à l'usage.

Litil applique la technique à un petit modèle ouvert, Qwen3-1.7B, adapté à deux tâches : retrouver dans un contrat le passage qui répond à une question, et répondre à des questions à choix fermé. Les données sont des jeux publics (CUAD, MAUD, ContractNLI) complétés par des tâches générées par le laboratoire.

Le récit suit trois temps. Le premier entraînement échoue à l'un des cinq contrôles fixés à l'avance : il obtient 0,612 sur une mesure pour laquelle le seuil était 0,80. Deux autres entraînements, avec d'autres graines, obtiennent 0,878 et 0,952. Les trois sont fusionnés, y compris celui qui avait échoué. Le modèle fusionné passe les cinq contrôles et devient le nouveau modèle du laboratoire.

Le résultat mis en avant : sur 320 couples contrat-clause, le bon passage arrive en première position dans 92,2 % des cas, contre 77,8 % pour le modèle précédent, et le nombre de fausses alertes par contrat tombe de 49,8 à 12,2.

La note contient aussi un développement mathématique sur la bonne manière de fusionner des adaptateurs LoRA (une méthode d'entraînement légère) et une mise en garde sur le calibrage : recalibrer un modèle sur ses propres données d'entraînement revient, selon les auteurs, à demander au cuisinier si le dîner était bon.

## La discussion

### Le gain vient surtout du réentraînement

Le chiffre de 77,8 % à 92,2 % compare le modèle fusionné au modèle précédent. Les tableaux de la note montrent que chacun des trois entraînements, pris isolément, fait déjà presque aussi bien : 93,4 %, 90,9 % et 91,3 %. Le premier entraînement, celui qui avait été écarté, fait même mieux que la fusion sur cette mesure.

Le saut de quinze points vient donc de la nouvelle recette d'entraînement, pas de la fusion. La fusion apporte autre chose, que la note démontre mieux : elle lisse les résultats et permet de passer tous les contrôles sans avoir à choisir le « bon » entraînement. Le sous-titre, qui attribue le gain à la soupe, nous paraît surévaluer la technique au détriment du travail qui l'a précédée.

### Ce que les tableaux nuancent

Plusieurs données publiées ne sont pas commentées dans le texte. Sur la mesure où le premier entraînement avait échoué, le modèle fusionné obtient 0,878, soit exactement le score de l'un des trois entraînements, et un peu moins que le modèle précédent (0,894, qui figure sur le graphique sans figurer dans le tableau). Sur le taux de réponses trouvées, le modèle fusionné (92,5 %) fait moins bien que le modèle précédent (94,4 %).

Le jeu de test de cette mesure comprend 51 questions, dont quatre cas positifs. Les intervalles de confiance publiés sont très larges, de 0,766 à 0,963 pour le modèle fusionné, et la note précise elle-même qu'ils ne reflètent pas la variation entre entraînements. Avec quatre cas positifs, un seul cas mal classé déplace sensiblement le score.

Enfin, la comparaison de calibrage oppose une valeur « reconstruite hors ligne » pour le modèle fusionné à des valeurs mesurées directement pour les trois entraînements. La note le signale dans son tableau, mais la phrase « trois fois mieux » ne le rappelle pas.

### La règle des contrôles fixés à l'avance

Nous retenons une pratique de méthode qui mérite d'être reprise : le laboratoire écrit ses contrôles avant chaque entraînement et s'interdit de les modifier après coup. C'est l'équivalent, pour un modèle, de la préinscription d'un protocole de recherche. La note ne les énumère pas tous et réintègre dans la fusion l'entraînement qui en avait raté un. Nous n'écrivons pas ici que c'est une erreur : la technique repose justement sur la moyenne de plusieurs entraînements. Mais la règle n'empêche pas de relancer des entraînements jusqu'à obtenir un résultat qui passe, et la note n'explique pas comment le nombre de trois a été fixé.

### Le statut du texte

La note est publiée par une société qui propose ses services (« Work with us », « Book a call ») et présente son propre modèle, sans le nommer. Les essais antérieurs évoqués en fin de note ne sont pas chiffrés et les données d'octobre ne sont pas publiées. Il s'agit d'un compte rendu d'expérience interne, pas d'une étude évaluée. Ce statut n'enlève rien à la transparence des tableaux, qui est réelle et que j'aimerais voir plus souvent.

## L'intérêt pour les juristes

Pour un avocat, la note n'a pas d'utilité directe : la fusion de modèles se pratique en amont, chez celui qui entraîne le modèle. Elle en a une indirecte, à notre sens importante. Elle montre de l'intérieur qu'avec les mêmes données et la même recette, un simple changement de hasard fait passer un modèle de « refusé » à « accepté » sur un critère de qualité. La performance d'un outil d'analyse de contrats n'est donc pas une propriété stable que l'on mesure une fois. Elle dépend de choix d'entraînement que l'utilisateur ne voit pas.

La conséquence pratique, pour un cabinet qui évalue un outil, est de demander au fournisseur sur quel jeu de test ses chiffres ont été mesurés, combien de cas positifs il contient et si les résultats ont été reproduits sur plusieurs entraînements. La plupart des fournisseurs ne publient pas ces informations ; Litil, ici, le fait.

Pour le programme IA & confiance de jerlash.labs, la note fournit un cas concret : un chiffre de titre exact mais attribué à la mauvaise cause, et des tableaux qui permettent au lecteur attentif de le rectifier. Nous nous en servirons dans la grille de lecture des annonces de performance que prépare le programme. [À VÉRIFIER : engagement à confirmer par l'auteur.]

## La référence

LiTiL Research, « Soup du Jour », Litil, blog, 5 novembre 2026, https://litil.ai/blog/soup-du-jour (consulté le 12 novembre 2026).

Article cité par la note : M. Wortsman et al., « Model soups : averaging weights of multiple fine-tuned models improves accuracy without increasing inference time », Proceedings of the 39th International Conference on Machine Learning (ICML), 2022, https://proceedings.mlr.press/v162/wortsman22a.html. [À VÉRIFIER : titre complet et liste des auteurs.]

La comparaison culinaire et l'expression « trois fois mieux » sont traduites par l'auteur de la recension.
