---
draft: true
title: "Ce que l'IA déplace entre juristes d'entreprise et cabinets d'avocats : quatre hypothèses à partir du rapport Dentons (2026)"
date: 2026-11-21
description: "IA, juristes d'entreprise et cabinets d'avocats : quatre hypothèses tirées des entretiens du rapport Dentons, avec leurs limites et pistes de vérification."
statut: "brouillon"
version: "0.1"
programme: "H1"
date_arret_recherches: 2026-11-21
controles: "Citations et renvois de page contrôlés sur le PDF du rapport (31 pages) le 2026-11-22 ; texte relu en entier par l'auteur le 2026-11-25 ; sources juridiques (RGPD, Code judiciaire, règles d'AVOCATS.BE) non collationnées ; aucune relecture externe."
usage_ia: "Claude (Anthropic, novembre 2026) a été utilisé pour rédiger une première version à partir du rapport et pour contrôler les citations et les renvois de page. L'auteur a relu le texte en entier et en a validé les hypothèses. [À VÉRIFIER : formulation à valider par Florian]"
licence: "CC BY 4.0"
financement: "aucun"
conflits_interets: "aucun"
---

<!--
Collection Revue › Research papers (ADR-024, point 4), créée le 2026-11-25. Le champ « type » (conceptuel) est noté ici et non dans le front matter, conformément à docs/politique-publication.md §4.

À la publication : draft : false, statut « working paper », identifiant JLL-RP-2026-001 (premier research paper publié), et passer la page d'index de la collection (_index.md et _index.en.md) en draft : false. Lever d'abord les marqueurs de vérification du texte (sections 5.2 et 6.2) et du champ usage_ia.

Maillage en attente : les perspectives « Taux horaire et intelligence artificielle » (/revue/perspectives/taux-horaire-avocat-ia/, pour la section 6) et « L'IA et l'avocat - déléguer le connu, penser l'inconnu » (/revue/perspectives/deleguer-ia-avocat-jugement/, pour la section 7) sont en brouillon (draft : true). Les lier quand elles seront publiées.
-->

## 1. La question

Le cabinet Dentons a publié en octobre 2026 un rapport fondé sur des entretiens avec des juristes d'entreprise d'organisations pour la plupart irlandaises, dont il cite sept (Dentons, 2026). Une [recension](/revue/recensions/ia-juristes-entreprise-dentons/) en présente le contenu et les limites dans la même collection de la Revue. Ce texte part d'une autre question, que le rapport pose dans sa conclusion sans la traiter : qu'est-ce que l'usage de l'IA, par les entreprises et par les cabinets, change dans ce que le client attend de son avocat et dans ce qu'il est prêt à payer ?

Le rapport y répond par une formule. Les clients attendraient des cabinets qu'ils utilisent les mêmes outils qu'eux, qu'ils les utilisent bien, et qu'ils soient « capables de montrer, de manière crédible, comment un être humain a relu le résultat » ; ce serait, conclut-il, « une question de confiance ». La formule est juste, à notre sens, mais elle laisse ouvert l'essentiel : ce que signifie montrer, à quel coût, et qui le supporte.

Nous ne chercherons pas ici à établir ce que pensent les juristes d'entreprises mais plutôt à formuler, à partir des témoignages qu'il rapporte, des hypothèses assez précises pour être vérifiées ensuite.

## 2. La source et la manière de la lire

### 2.1 Ce qu'est le rapport

*From AI Adoption to AI Advantage* compte 31 pages (Dentons, 2026). Il comprend un avant-propos de Carlo Salizzo et David Kirton, associés du bureau de Dublin, un résumé signé par Ann O'Dea, de Silicon Republic, cinq chapitres, une conclusion et une présentation des deux organisations.

Les entretiens ont été menés avec des responsables juridiques et de la conformité d'entreprises « dont eir, Flipdish, Gilead Sciences, IMRO, Mastercard, Uniphar et Wayflyer », et avec trois personnes de Dentons ; la liste n'est donc pas présentée comme complète. Neuf personnes extérieures au cabinet sont citées nommément. Le rapport ne donne ni le nombre d'entretiens, ni leurs dates, ni la grille de questions, ni les critères de choix, sinon la volonté de parler à « certaines des équipes juridiques les plus innovantes du marché ».

Le rapport est rédigé en anglais ; les passages cités dans ce texte sont traduits par nos soins.

### 2.2 Trois types d'énoncés

La valeur du rapport dépend du type d'énoncé. Nous en distinguons trois.

Les témoignages sont des propos attribués à une personne nommée, sur sa propre pratique (« j'ai construit un agent que j'appelle le “vérificateur final” »). Ils sont la matière la plus intéressante du rapport, avec une réserve : on ne connaît pas la question qui les a suscités ni ce qui a été coupé.

Les affirmations éditoriales sont des généralisations du rapport lui-même (« la question du volume a été évoquée par pratiquement toutes les personnes interrogées »). Elles résument les entretiens, sans qu'on puisse contrôler le résumé.

Les projections portent sur l'avenir (« je pense que toute l'économie des tokens fera que nous embaucherons probablement des personnes pour surveiller le coût de l'IA »). Elles disent ce que pense une personne.

### 2.3 Le classement de quelques énoncés clés

Le tableau ci-dessous classe les énoncés sur lesquels s'appuient les hypothèses qui suivent.

| Énoncé du rapport | Type | Appui dans le corps du texte |
|---|---|---|
| Le remplacement de postes ou de fonctions est l'exception | Affirmation éditoriale | Témoignages concordants |
| Les usages réussis sont des tâches étroites et retravaillées | Affirmation éditoriale | Exemples d'Uniphar, eir, IMRO, Mastercard |
| La gouvernance devient l'affaire de plusieurs fonctions | Affirmation éditoriale | eir (forum de gouvernance), Gilead |
| La rédaction assistée touche « la majorité » des demandes entrantes | Affirmation éditoriale | Aucun comptage ; témoignages |
| Le volume a été évoqué par « pratiquement toutes les personnes interrogées » | Affirmation éditoriale | Six témoignages |
| Hausse des coûts de l'IA de deux à cinq fois en deux ans | Projection attribuée à C. Grossmann | Absente du corps du texte, qui évoque une « falaise des coûts » sans chiffre |
| Un tableau de bord pourrait économiser 200 000 dollars sur un dossier | Projection de son auteur, non nommé | Absent du corps du texte |
| Personne n'a démontré de retour sur investissement | Témoignage (R. Dobson) | Repris par le rapport |
| Les clients attendent une démonstration crédible de la relecture | Affirmation éditoriale | Un témoignage proche (M. Neary) |

Deux enseignements de méthode en découlent. Les affirmations les plus générales et les plus chiffrées du rapport figurent dans le résumé et la conclusion, et ce sont les moins étayées. Et la projection la plus frappante, celle sur les coûts, vient d'un associé du cabinet éditeur.

## 3. Ce que le rapport permet de dire

Lu avec ces précautions, le rapport permet d'affirmer une chose modeste mais utile : dans un petit nombre d'équipes juridiques d'entreprise choisies pour leur avance, en Irlande pour l'essentiel, en 2026, les responsables décrivent tous un usage de l'IA par tâches délimitées, une gouvernance partagée avec d'autres fonctions, un afflux de correspondance rédigée avec l'IA, une incertitude sur les coûts et une relation avec les cabinets qui se renégocie. Il ne permet pas de dire que ces constats valent ailleurs, ni dans quelle proportion.

Les hypothèses qui suivent partent donc de témoignages, et leur portée est celle d'hypothèses. Chacune est suivie de ses limites.

## 4. Hypothèse 1 : la relecture humaine devient un élément à démontrer

### 4.1 Ce que dit le rapport

Trois passages vont dans le même sens. Máire Neary (Flipdish) attend des cabinets qu'ils utilisent l'IA, mais « je veux en voir un usage responsable ». Jessica Williams (Mastercard) envisage que les avocats extérieurs deviennent un jour « les auditeurs de notre production par l'IA ». Et la conclusion fait de la capacité à montrer comment un humain a relu le résultat la condition de la confiance.

### 4.2 Analyse proposée

L'avocat a toujours relu ce qu'il signait, et personne ne lui demandait de le prouver : la signature valait relecture. L'hypothèse que nous formulons est que l'IA fragilise cette présomption. Quand le client sait qu'un premier jet peut être produit en quelques secondes, et qu'il en produit lui-même, il ne peut plus déduire de la qualité apparente d'un texte qu'un avocat l'a examiné. Le rapport le dit à sa manière, à propos de la correspondance entrante : l'IA produit « des contenus qui ont parfois l'air bons, mais ne le sont pas toujours » (Deirdre MacCarthy, Wayflyer). Ce qui vaut pour les courriers reçus par l'entreprise vaut pour les avis qu'elle reçoit de ses avocats.

Si l'hypothèse est juste, la relecture change de statut. Elle reste une obligation de diligence, mais elle devient aussi un élément de la prestation que le client veut pouvoir constater. Plusieurs formes sont concevables, du plus léger au plus lourd : une mention dans la lettre de mission sur l'usage de l'IA et la relecture ; l'indication, dans chaque avis, de ce qui a été vérifié dans les sources et par qui ; une trace conservée des contrôles faits, que le client peut demander. La boîte à outils [Gouvernance de l'IA](/outils/gouvernance-ia/) de jerlash.labs propose déjà des contrôles de ce type à l'intérieur du cabinet ; l'hypothèse ici est qu'une partie d'entre eux pourrait devoir être montrée au client.

Le rapport fournit lui-même une piste sur la manière de rendre cette relecture plus fiable. Jessica Williams décrit l'empilement de deux outils, l'un qui rédige et l'autre, plus contraint, qui contrôle les modifications. Nous ne pensons pas qu'un contrôle automatisé puisse tenir lieu de relecture humaine, mais il peut en documenter une partie, ce qui touche directement à la question de la preuve.

### 4.3 Limites

Nous voyons trois limites à cette hypothèse. Elle repose sur deux témoignages et une phrase de conclusion. Elle suppose que le client veut une preuve, alors qu'il peut tout aussi bien se contenter de la confiance qu'il accorde à un avocat qu'il connaît, ce que le rapport suggère aussi (Seán Donegan, IMRO, sur la valeur de l'échange direct). Et une preuve de relecture peut devenir un rituel : une mention standard en bas d'un avis ne prouve rien de plus qu'une signature. Le programme [Autonomie & IA](/recherche/autonomie-ia/) s'intéresse précisément à cette distinction entre supervision réelle et supervision affichée.

## 5. Hypothèse 2 : l'IA déplace le coût de la correspondance vers son destinataire

### 5.1 Ce que dit le rapport

Le chapitre 3 est consacré à ce que le rapport appelle « le problème du volume ». Les demandes d'accès aux données personnelles, les plaintes de clients et les griefs de salariés rédigés avec l'IA arrivent plus nombreux et plus longs. L'avant-propos ajoute que la loi oblige souvent à y répondre « point par point, même lorsque seuls un ou deux points ont de la substance ». Sorcha Nic Mhurchú (eir) situe le coût : il faut établir « ligne par ligne, ce qui est pertinent ». Máire Neary (Flipdish) en tire une conséquence d'organisation : les ressources humaines devront avoir une approche plus juridique, et les juristes une approche plus attentive aux personnes. David Kirton (Dentons) ajoute que le demandeur n'y gagne pas forcément : une longue lettre au vocabulaire juridique « le plus souvent […] ne l'aidera pas réellement à faire avancer son dossier ».

### 5.2 Analyse proposée

L'hypothèse est la suivante : l'IA réduit fortement le coût de production d'une demande, mais pas celui de son traitement, et les règles qui imposent une réponse sont calibrées sur la demande, pas sur l'effort qu'elle a coûté à son auteur. Le coût marginal se déplace donc vers le destinataire.

Le droit d'accès du RGPD en est le meilleur terrain d'examen, parce qu'il s'applique en Irlande comme en Belgique et parce que le rapport le cite expressément. Le règlement fixe un délai de réponse et prévoit le cas des demandes « manifestement infondées ou excessives » ([À VÉRIFIER] art. 12, § 3 et § 5, du règlement (UE) 2016/679, à citer in extenso). La question que pose le rapport, sans la formuler, est de savoir si une demande longue, rédigée avec l'IA et chargée de points sans substance, peut être qualifiée d'excessive. Nous n'avons pas vérifié les lignes directrices du Comité européen de la protection des données sur ce point, ni la pratique de l'Autorité de protection des données belge [À VÉRIFIER]. Notre intuition, à confirmer, est que la longueur ou le mode de rédaction ne rendent pas en eux-mêmes une demande excessive, parce que le critère s'attache à la demande et non à son style, et que la réponse au problème du volume ne viendra donc pas de cette exception.

Si c'est le cas, la réponse est d'organisation, et le rapport en décrit deux. La première consiste à répondre avec les mêmes outils : IMRO a construit un agent conversationnel sur son site pour les questions courantes. La seconde consiste à externaliser : Dentons propose désormais un service géré pour les plaintes en grand nombre. Les deux réponses ont une conséquence qu'il faut nommer : on traite par l'IA des demandes produites par l'IA, ce qui pose à nouveau la question de la relecture (hypothèse 1), cette fois pour des réponses qui engagent l'entreprise vis-à-vis d'une personne qui exerce un droit.

Le rapport signale aussi un volume interne. Sergey Kinchin (Uniphar) décrit une réunion où cinq personnes sont venues avec six avis générés par l'IA sur une question réglementaire, et où l'outil, appelé à les concilier, « s'était pour ainsi dire embrouillé lui-même ». Pour un juriste d'entreprise, l'IA multiplie donc les avis non juridiques sur des questions juridiques, avant même que le juriste ne soit consulté.

### 5.3 Limites

Le rapport ne chiffre rien. L'affirmation du résumé selon laquelle la rédaction assistée touche « la majorité » des demandes entrantes n'a pas d'appui dans le corps du texte. L'hypothèse vaut pour les destinataires qui reçoivent beaucoup de demandes, grandes entreprises et administrations ; elle dit peu de chose d'un cabinet de quelques avocats. Enfin, le point de vue est exclusivement celui du destinataire. Le rapport ne donne pas la parole aux demandeurs, pour qui l'IA peut aussi être un moyen d'exercer un droit qu'ils n'auraient pas su formuler, ce que Seán Donegan reconnaît en passant (« si cela rétablit l'égalité des armes […], c'est une bonne chose pour la société »).

## 6. Hypothèse 3 : le coût à l'usage pose une question de frais que le débat sur le taux horaire ne traite pas

### 6.1 Ce que dit le rapport

Le rapport annonce le passage d'une tarification des outils par licence à une tarification à la consommation. Les témoignages décrivent l'incertitude qui en résulte : Jessica Williams (Mastercard) demande aux éditeurs des moyens de contrôle pour « établir une ligne budgétaire prévisible » ; Sorcha Nic Mhurchú (eir) craint d'entrer dans « un tapis roulant où l'on ne fait que payer toujours plus de frais » ; Deirdre MacCarthy (Wayflyer) annonce un travail sur le choix du modèle adapté à chaque tâche, au bon prix.

Sur le taux horaire, deux positions s'opposent. Cornelius Grossmann (Dentons) soutient que l'heure facturée répercute d'elle-même les gains de productivité au client, à condition d'être appliquée loyalement : « moins d'heures, des factures moins élevées ». Rebekah Dobson (Gilead Sciences) répond qu'elle ne paie pas le résultat mais la compétence, et que l'heure facturable « doit disparaître, d'un côté comme de l'autre ». David Kirton (Dentons) indique que la majorité du travail de son équipe est déjà facturée sur estimation ou au forfait.

### 6.2 Analyse proposée

Le raisonnement de Grossmann suppose que le coût de la prestation est du temps d'avocat. Le passage à une tarification à la consommation introduit un second coût, variable, qui ne dépend pas du temps passé mais du nombre de requêtes adressées à un modèle et du modèle choisi. L'hypothèse que nous formulons est que ce coût échappe aux deux positions du rapport. Avec l'heure facturée, les gains de temps passent au client, mais le coût des tokens reste à classer : frais généraux du cabinet, ou frais exposés pour le dossier et refacturés. Avec le forfait, le cabinet porte le risque d'une consommation imprévue, ce que Grossmann appelle la « falaise des coûts » (cost cliff).

En droit belge, la distinction entre honoraires et frais a des conséquences sur l'information due au client et sur la manière de facturer. Nous ne les exposons pas ici : elles demandent de citer l'article 446ter du Code judiciaire et les règles d'AVOCATS.BE sur les honoraires et les frais, que nous n'avons pas collationnées [À VÉRIFIER]. Le research paper sur la tarification alternative en préparation (fiche P17) est le lieu naturel de cet examen ; le présent texte se limite à signaler que la question des frais d'usage de l'IA devrait y figurer.

Un témoignage du rapport donne une indication pratique. Sergey Kinchin (Uniphar) observe qu'un outil agentique consomme beaucoup plus quand on lui donne un lien vers un dossier partagé que quand on lui joint les fichiers, parce qu'il cherche, vérifie et contrôle les autorisations, et il en conclut que la capacité à délimiter une tâche devient une compétence de gestion. Si cela se vérifie, le coût à l'usage dépend en partie de la compétence de celui qui utilise l'outil, ce qui complique encore sa répercussion au client.

### 6.3 Limites

Cette hypothèse repose sur une évolution des prix que le rapport annonce sans la démontrer. Le chiffre d'une hausse de deux à cinq fois en deux ans est une projection, absente du corps du texte, et ne doit pas être traité comme un fait. L'hypothèse suppose aussi que le cabinet paie à la consommation ; un cabinet qui utilise un outil sous licence par utilisateur n'est pas concerné, ou pas encore. Elle ne dit rien, enfin, des cabinets qui travaillent en BYOK (avec leur propre clé API, comme le prévoient les outils de jerlash.labs), pour lesquels le coût est directement visible et pourrait être affecté dossier par dossier.

## 7. Hypothèse 4 : le gain de l'IA dépend d'un jugement que son usage précoce peut empêcher de se former

### 7.1 Ce que dit le rapport

Cornelius Grossmann (Dentons) formule le risque d'un « écart de jugement » (judgement gap) : les gains actuels viennent de ce que des associés expérimentés utilisent l'IA et en repèrent les erreurs ; sans expérience ni formation, pas de jugement, et sans jugement, pas de bénéfice de l'IA. Les juristes débutants apprennent plus vite avec l'IA, ajoute-t-il, mais s'ils apprennent « trop vite », ils ne développent pas ce jugement. Le rapport précise que d'autres personnes interrogées ont exprimé la même préoccupation, sans les nommer. Máire Neary (Flipdish) présente de son côté l'IA comme « un collègue débutant », en rappelant que c'est le juriste qui reste « aux commandes ».

### 7.2 Analyse proposée

L'hypothèse est que le bénéfice de l'IA dans le travail juridique est autolimité : il repose sur un jugement formé par la pratique de tâches que l'IA prend désormais en charge. Si les tâches formatrices disparaissent sans être remplacées par autre chose, le jugement qui rend l'IA utile se forme moins bien, et le gain baisse à mesure que la génération formée sans IA quitte la profession. Grossmann le dit en une phrase : il n'y aura jamais « de moment où l'on tirera de l'IA autant de bénéfice qu'aujourd'hui ».

Cette hypothèse rejoint directement la question du programme Autonomie & IA : à quelles conditions l'usage de l'IA renforce-t-il le jugement plutôt que de le remplacer ? Le rapport apporte un élément qui va contre l'intuition : Rebekah Dobson (Gilead Sciences) observe que ni l'ancienneté, ni la géographie, ni le secteur ne prédisent qui adopte bien l'IA. Si l'adoption ne dépend pas de l'âge, le risque de l'écart de jugement ne concerne pas seulement les débutants ; il concerne quiconque délègue une tâche qu'il n'a jamais su faire lui-même.

### 7.3 Limites

L'hypothèse repose sur l'opinion d'une personne, partagée par d'autres que le rapport ne nomme pas. Elle suppose que le jugement se forme par la répétition de tâches simples, ce qui est une thèse sur l'apprentissage professionnel que le rapport n'examine pas et que nous n'avons pas confrontée à la littérature. Elle ne dit rien des formations qui pourraient compenser cette perte, et le rapport non plus.

## 8. Limites générales

Ce texte tire quatre hypothèses d'un seul rapport, fondé sur des entretiens dont la méthode n'est pas publiée, menés par un cabinet qui a un intérêt commercial à certaines conclusions (la [recension associée](/revue/recensions/ia-juristes-entreprise-dentons/) détaille ce point). Les témoignages viennent d'entreprises de taille moyenne à très grande, et de juristes d'entreprise, pas d'avocats exerçant en petit cabinet. La transposition au contexte belge est proposée sans examen des textes, qui restent à citer. Aucune des hypothèses n'est vérifiée ; leur formulation vise à permettre une vérification.


## 9. Bibliographie

Dentons (2026). *From AI Adoption to AI Advantage. How leading in-house legal teams are leveraging AI*. Leading Edge. Dublin, Dentons, en collaboration avec Silicon Republic, 31 p., https://insights.dentons.com/447/39125/uploads/from-ai-adoption-to-ai-advantage.pdf. PDF consulté le 2026-11-21. 

Règlement (UE) 2016/679 du Parlement européen et du Conseil du 27 avril 2016 relatif à la protection des personnes physiques à l'égard du traitement des données à caractère personnel et à la libre circulation de ces données (RGPD), art. 12 et 15. [version EUR-Lex collationnée.]

Code judiciaire, art. 446ter ; code de déontologie d'AVOCATS.BE, dispositions relatives aux honoraires et aux frais. 


## Historique

- 0.1 (2026-11-21) : premiere version, à partir de la seule lecture du rapport. Aucune source juridique collationnée.
