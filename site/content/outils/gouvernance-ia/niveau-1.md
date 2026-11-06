---
draft: false
title: "Le niveau 1"
description: "La gouvernance minimale d'une organisation dont chaque outil d'IA est conforme ou ne reçoit que des données non sensibles : six éléments et une fiche de conformité."
weight: 15
---

Le niveau 1 s'applique lorsque chaque outil d'IA utilisé par l'organisation remplit l'une de ces deux conditions : sa conformité aux exigences déontologiques, éthiques et contractuelles a été vérifiée sur pièces, ou il ne reçoit que des données publiques ou internes non sensibles (classes D0 et D1). Le diagnostic figure sur [la page d'accueil](/outils/gouvernance-ia/#quel-niveau-pour-votre-organisation).

À ce niveau, le classement détaillé des données et l'homologation ont peu de sens. L'outil conforme offre les garanties que ces procédures chercheraient à établir. L'outil non vérifié, lui, ne reçoit rien qui mérite d'être protégé. La gouvernance se concentre donc sur ce qui reste : savoir quels outils sont en place, vérifier qu'ils sont conformes, contrôler ce qu'ils produisent et réagir en cas de problème.

## Les six éléments

1. **Un référent.** Une personne identifiée tient l'inventaire des outils, conserve les fiches de conformité et refait le diagnostic du niveau quand la situation change. Dans un petit cabinet, ce peut être un associé. Une autre personne valide les fiches qu'il établit : personne n'approuve seul sa propre demande.
2. **L'inventaire des outils.** Pour chaque outil : son nom, le fournisseur, la formule souscrite (gratuite, professionnelle, entreprise), les personnes qui l'utilisent et la date de la fiche de conformité. Une fonction d'IA intégrée à un logiciel déjà en place (traitement de texte, messagerie, logiciel de gestion) est un outil à inventorier.
3. **Une fiche de conformité par outil**, ou à défaut la règle D0/D1 : un outil sans fiche, ou dont la fiche n'est pas entièrement satisfaite, ne reçoit que des données D0 et D1. La fiche figure ci-dessous.
4. **Une règle de vérification des productions.** Tout résultat utilisé dans une prestation est vérifié par la personne qui l'utilise, selon la méthode décrite dans [Vérifier un livrable juridique](../supervision/#vérifier-un-livrable-juridique). Un résultat est écarté ou remonté lorsqu'il tombe dans l'un des [cas de refus](../supervision/#quand-refuser-ou-escalader).
5. **Un canal d'incident.** Chacun sait à qui signaler une fuite de données, une erreur importante ou un comportement imprévu de l'outil, et le référent applique la [procédure d'incident](../operations/#la-procédure).
6. **Une formation courte**, centrée sur les limites des outils, la vérification des sources et le refus d'un résultat (modules F1 à F3 des [opérations](../operations/#les-modules)).

Le référent revoit l'inventaire et les fiches au moins une fois par an, et immédiatement lorsqu'un outil change de contrat, de formule ou de fonctions, ou après un incident.

## La fiche de conformité d'un outil

La fiche se remplit sur pièces : conditions générales, contrat, accord de traitement des données, documentation de sécurité du fournisseur. Chaque point reçoit l'une de ces réponses : *oui* (avec la pièce qui l'établit), *non*, ou *à vérifier*. On n'invente pas une réponse que les pièces ne donnent pas.

| Code | Point vérifié |
| --- | --- |
| F01 | Un contrat écrit (conditions générales ou contrat particulier) est identifié, daté et conservé, pour la formule effectivement souscrite. |
| F02 | L'outil est utilisé conformément à la destination prévue par son fournisseur. |
| F03 | Le fournisseur ne réutilise pas les contenus pour entraîner ou améliorer ses modèles, ou cette réutilisation est désactivée de manière vérifiable. |
| F04 | Les accès du fournisseur et de ses sous-traitants aux contenus (assistance, surveillance des abus, journaux) sont limités et encadrés d'une manière compatible avec le secret professionnel. |
| F05 | Si des données à caractère personnel sont traitées, un accord de traitement des données conforme à l'article 28 du RGPD est en place. |
| F06 | La localisation du traitement, les transferts hors de l'Union européenne et leurs garanties sont connus. |
| F07 | La liste des sous-traitants ultérieurs est disponible, et le fournisseur informe de ses changements. |
| F08 | Les durées de conservation des contenus et des journaux sont connues, et l'effacement est possible. |
| F09 | Les comptes sont protégés (authentification à plusieurs facteurs, gestion des accès, révocation), et les échanges et le stockage sont chiffrés. |
| F10 | Le fournisseur s'engage à notifier les incidents de sécurité, et un contact est identifié. |
| F11 | L'outil propose sans agir seul : il n'envoie, ne dépose, ne signe ni ne modifie rien sans une intervention humaine. |

La conformité est **établie** lorsque tous les points sont à *oui*. Elle est **partielle** lorsque tous les points ont été examinés mais que l'un d'eux est à *non*, et **non établie** lorsque l'un d'eux reste *à vérifier*. Une conformité partielle ou non établie n'interdit pas l'outil : elle le cantonne aux données D0 et D1, ou fait passer l'organisation au niveau 2 ou 3.

```text
FICHE DE CONFORMITÉ D'UN OUTIL D'IA

Outil et formule souscrite : [ ]   Fournisseur : [ ]
Établie par : [ ]   Validée par : [ ]   Date : [ ]

F01 Contrat identifié et daté ............ [oui / non / à vérifier]  Pièce : [ ]
F02 Usage conforme à la destination ...... [oui / non / à vérifier]  Pièce : [ ]
F03 Pas de réutilisation des contenus .... [oui / non / à vérifier]  Pièce : [ ]
F04 Accès compatibles avec le secret ..... [oui / non / à vérifier]  Pièce : [ ]
F05 Accord de traitement des données ..... [oui / non / à vérifier / sans objet]  Pièce : [ ]
F06 Localisation et transferts ........... [oui / non / à vérifier]  Pièce : [ ]
F07 Sous-traitants ultérieurs ............ [oui / non / à vérifier]  Pièce : [ ]
F08 Conservation et effacement ........... [oui / non / à vérifier]  Pièce : [ ]
F09 Sécurité des comptes et chiffrement ... [oui / non / à vérifier]  Pièce : [ ]
F10 Notification des incidents ........... [oui / non / à vérifier]  Pièce : [ ]
F11 Pas d'action autonome ................ [oui / non / à vérifier]  Pièce : [ ]

Conformité : [établie / partielle / non établie]
Données admises : [D0 à D4 si établie ; D0 et D1 sinon]
Réexamen : [date, et au plus tard dans un an]
```

## Quand passer au niveau 2

L'organisation passe au niveau 2 dès qu'elle veut confier des données confidentielles ou couvertes par le secret (D2 à D4) à un outil dont la conformité n'est que partielle. Elle passe au niveau 3 si elle veut les confier à un outil dont la conformité n'est pas établie, ou si un outil doit agir seul. Le changement de niveau est une décision de la gouvernance, consignée par le référent.

## La charte au niveau 1

Une charte courte suffit. Les articles 1 (objet), 2 (principes), 3 (instances), 5 (données et secret), 7 (supervision), 8 (validation des productions), 14 (incidents) et 16 (adoption) de la [charte modèle](../charte/) couvrent l'essentiel. L'article 4 peut renvoyer à l'inventaire et aux fiches de conformité.
