---
draft: false
title: "Pourquoi les chartes IA échouent"
description: "Ce qu'une charte IA de cabinet fait bien, ses dix faiblesses de structure et la correction proposée pour chacune."
weight: 10
---

La boîte à outils est née de l'analyse d'une charte IA de cabinet, soumise au projet comme point de départ. Son texte n'est pas reproduit ici. Elle ressemble à beaucoup d'autres : ses principes sont justes, mais on ne peut pas vérifier qu'ils sont respectés. Ce texte identifie ce qu'il faudrait garder, où elle s'arrête trop tôt, et comment les modules de la boîte à outils proposent d'y remédier.

## Ce qu'il faut garder

La charte analysée fait plusieurs choses utiles. Elle vise un cercle de personnes large, au-delà des seuls avocats. Elle affirme la primauté du jugement professionnel. Elle rappelle les exigences du secret professionnel et les précautions liées au RGPD. Elle demande de la vigilance sur la fiabilité des résultats et sur les sources. Elle traite de la responsabilité professionnelle, de la formation et du signalement des incidents.

Rien de cela n'est à abandonner. La difficulté tient à la manière dont ces principes sont formulés.

## Dix faiblesses et leur correction

| Clause de la charte | Ce qui ne va pas | Correction proposée |
| --- | --- | --- |
| Outils « autorisés » | L'autorisation est globale, sans périmètre ni seuil. | Une décision qui porte sur une combinaison précise : outil, configuration, usage, données, utilisateur et degré d'autonomie. Voir [l'homologation](../homologation/). |
| Sécurité et fiabilité | Des principes, sans tests ni critères éliminatoires. | Un référentiel contrôlable, une preuve documentaire et des cas de test. |
| Secret professionnel et données | La prudence est presque entièrement laissée à l'utilisateur. | Des classes de données, des droits d'accès, une politique de conservation et des contrats. Voir [les données](../donnees/). |
| Traçabilité de tout texte produit avec l'IA | Une charge excessive, et des journaux qui finissent par contenir des secrets. | Une traçabilité proportionnée, limitée aux usages déterminants et aux décisions. Voir [les opérations](../operations/). |
| Relecture humaine obligatoire | La présence d'un humain ne garantit pas que le contrôle a lieu. | Un contrôle qui permet de comprendre, détecter, contester, corriger, refuser et justifier. Voir [la supervision](../supervision/). |
| Copier-coller « interdit » | Le critère est trompeur : réécrire un texte ne vérifie rien. | L'appropriation intellectuelle du résultat et la vérification indépendante des points décisifs. |
| Responsabilité « seule » de l'avocat | Elle simplifie à l'excès les rapports entre le cabinet, son personnel et ses prestataires. | Une répartition des devoirs internes, sans préjuger des responsabilités légales. Voir [la gouvernance](../gouvernance/). |
| Incidents | Peu d'escalade, pas de statut de suspension, pas de retour d'expérience. | Un processus avec des rôles, la mise en sécurité, une revue et un suivi des corrections. |
| Contrôle continu | Un contrôle indifférencié des collaborateurs crée un risque en droit social et au regard du RGPD. | Des audits proportionnés et une gouvernance des traces. |
| Agents autonomes | Absents du texte. | Des droits réduits au minimum, l'approbation préalable de certaines actions, un mécanisme d'arrêt et des limites techniques. |

Deux de ces faiblesses méritent qu'on s'y arrête, parce qu'elles reviennent dans presque toutes les chartes.

La première concerne la relecture obligatoire. Qu'un avocat ait eu le document sous les yeux ne démontre pas ce qu'il a vérifié. Pour que le contrôle soit réel, la personne doit pouvoir comprendre ce que le système a fait, repérer une erreur (plausible), la contester et refuser le résultat. Il lui faut pour cela la compétence, le temps, l'accès aux sources et l'autorité nécessaires. La seconde est l'interdiction du copier-coller, qui repose sur l'idée qu'un texte reformulé a été pensé. Or un raisonnement erroné reste erroné une fois reformulé. La question utile porte sur ce qui a été vérifié, et non sur la forme du texte final.


## La clause qui remplace les deux

La correction proposée est reprise dans une clause, reprise dans [la charte](../charte/) :

> Tout contenu ou action soutenu par un système d'IA doit faire l'objet d'un contrôle proportionné à ses conséquences. Le contrôle vise les éléments déterminants de l'analyse et la capacité du professionnel à comprendre, justifier, modifier ou rejeter la proposition. Ni le copier-coller ni la reformulation ne prouvent, à eux seuls, la conformité ou la qualité de la prestation.

## Les limites de la correction

Ces corrections ont leurs propres limites, qu'il faut garder en tête.

Les règles internes ne créent aucune dispense générale du secret professionnel ou du RGPD. L'agrément d'un outil par le cabinet ne remplace pas les obligations réglementaires. Un score, même élevé, ne dispense pas de vérifier les conditions éliminatoires. Annoncer une « supervision humaine » ne prouve pas qu'elle est efficace.

Une seconde limite concerne l'absence de mise en œuvre de la charte. Aussi bien écrite qu'elle puisse être, on peut la contourner. Si personne n'a reçu le pouvoir de décider quels outils sont autorisés, si aucune décision n'est consignée et si rien ne permet de constater qu'une règle a été suivie ou écartée, la charte reste un texte de principe, que chacun applique selon sa propre lecture. C'est pourquoi la boîte à outils commence par [la gouvernance](../gouvernance/) et place [la charte](../charte/) à la fin du parcours : elle ancre des décisions déjà prises et des contrôles déjà en place.

Enfin, les distinctions proposées par la boîte à outils (classes d'usage, classes de données, niveaux de supervision) sont des hypothèses de conception. Elles doivent être traitées comme telles tant qu'elles n'ont pas été testées dans la pratique.
