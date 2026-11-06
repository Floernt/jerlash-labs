---
draft: false
title: "Gouvernance"
description: "Qui décide de l'usage d'un outil d'IA au cabinet, selon quelles règles, à quel moment on réexamine la décision et comment on la consigne."
weight: 20
aliases: ["/fr/outils/gouverner-l-ia-au-cabinet/gouvernance/"]
niveaux:
  - niveau: "Niveau 1"
    texte: "Un référent et une autre personne qui valide ses fiches : voir [la version réduite](#la-version-réduite-niveaux-1-et-2). Ni matrice des responsabilités, ni modèle de décision."
  - niveau: "Niveau 2"
    texte: "La version réduite, plus les [règles de décision](#les-règles-de-décision) et les [cas de réexamen](#quand-réexaminer-une-décision)."
  - niveau: "Niveau 3"
    texte: "Tout le module, y compris la matrice des responsabilités et le modèle de décision."
---

La gouvernance est la première étape du parcours. Sa première décision est de déterminer son [niveau](/outils/gouvernance-ia/#quel-niveau-pour-votre-organisation), qui fixe la profondeur de tout le reste. La [charte](../charte/) viendra, en fin de parcours, ancrer les choix faits par la gouvernance. Cette page propose une version réduite pour les niveaux 1 et 2, puis, pour le niveau 3, les rôles, les règles qui encadrent une autorisation, le parcours d'un usage depuis sa déclaration jusqu'à son retrait, une matrice des responsabilités et un modèle de décision. C'est un modèle à adapter.

## La version réduite (niveaux 1 et 2)

Trois rôles suffisent. Une même personne peut en tenir plusieurs, à condition que personne n'approuve seul sa propre demande.

| Rôle | Ce qu'il fait |
| --- | --- |
| Référent | Tient l'inventaire des outils et les fiches de conformité, au niveau 2 la matrice outils × données × usages ; refait le diagnostic du niveau ; reçoit les signalements d'incident. |
| Décideur | Valide les fiches et la matrice établies par le référent, décide d'un changement de niveau, d'un nouvel outil ou d'une suspension. Dans un cabinet, en principe un associé ou l'organe de gestion. |
| Responsable de dossier | Vérifie les productions utilisées dans ses dossiers et apprécie leurs conséquences professionnelles. |

Au niveau 2, le décideur s'appuie sur les [règles de décision](#les-règles-de-décision) ci-dessous, et le référent sur les [cas de réexamen](#quand-réexaminer-une-décision).

## Les rôles (niveau 3)

Le schéma résume qui décide, qui donne son avis et qui applique. Un petit cabinet peut confier plusieurs de ces rôles à la même personne.

![La direction ou le comité IA délègue au référent IA, qui lui soumet les usages U3 et U4. Le référent sollicite l'avis du juridique et de la déontologie, de la sécurité et de l'informatique, et du DPO. Il habilite les utilisateurs, qui déclarent les usages et signalent les incidents. Le responsable de dossier encadre l'utilisateur.](/images/toolkit/gouvernance-acteurs.svg)

La direction, ou un comité IA, fixe les finalités admises, le niveau de risque toléré, les catégories d'outils et de données, la politique d'approbation et la fréquence des revues. Elle peut déléguer par écrit, mais elle garde la surveillance générale.

Le référent IA reçoit les demandes, tient le registre et le calendrier des révisions, et vérifie que les conditions posées par chaque décision sont respectées. Il coordonne le traitement des incidents et les requalifications.

Le juridique ou la déontologie examine le secret professionnel, le droit de la profession, les conditions d'engagement, l'information du client et les droits intellectuels.

La sécurité ou l'informatique vérifie les accès, l'authentification, l'isolation, le chiffrement, les sous-traitants techniques, les connecteurs, les journaux et la continuité.

Le DPO, s'il y en a un, analyse les risques pour les données personnelles et conseille sur les contrats, les transferts et l'analyse d'impact lorsqu'elle est requise. Il exerce la fonction que la loi lui attribue, sans devenir pour autant le décideur de tous les traitements.

Le responsable de dossier définit les limites de l'usage dans son dossier, contrôle les éléments juridiques et apprécie les conséquences professionnelles.

L'utilisateur reste dans le périmètre homologué, applique les mesures prévues et signale les incidents et les dépassements.

## Les règles de décision

- Personne ne s'auto-homologue pour un usage significatif.
- Toute autorisation précise le périmètre, le niveau de risque, les données admises, les contrôles, la durée et l'approbateur.
- Les conditions éliminatoires de [l'homologation](../homologation/) l'emportent sur le score pondéré. L'absence d'incident connu ne prouve pas l'absence d'un risque critique.
- Chaque membre déclare ses conflits d'intérêts. Le membre concerné se déporte, ou la gouvernance consigne une mesure compensatoire proportionnée.
- Le référent ne peut bloquer techniquement un outil à titre conservatoire que si ce pouvoir lui a été délégué. Il en réfère alors sans délai à l'organe compétent.
- Le demandeur peut obtenir un réexamen s'il apporte des faits ou des garanties nouveaux.

## Le parcours d'un usage

1. Le demandeur déclare le cas d'usage et inventorie les données concernées.
2. On détermine les obligations juridiques applicables.
3. On passe la revue éliminatoire, puis les tests de performance, de sécurité et d'usage réel.
4. Les responsables spécialisés rendent leur avis et l'organe compétent prend une décision motivée.
5. Les utilisateurs sont habilités et informés des limites.
6. Le référent suit les versions, les incidents et les changements de contrat.
7. L'autorisation est renouvelée, modifiée, suspendue ou retirée.

Pour l'étape 2 : le règlement IA ne vise pas la pratique d'un cabinet comme un usage à haut risque, à condition de ne pas détourner le système d'IA de sa destination : voir [les sources](../sources-et-versions/).

## Quand réexaminer une décision

Une décision est réexaminée en cas de changement significatif du modèle, de nouvelles fonctions ou permissions, d'un nouveau prestataire ou d'un nouveau transfert, d'un changement des conditions de confidentialité, d'un incident, d'une dérive des performances, d'un nouveau type de données, d'une évolution des finalités ou d'un changement du droit.

## Fréquence des revues

Nous proposons une revue légère chaque trimestre pour les usages sensibles, une revue complète chaque année et un contrôle immédiat après un incident grave ou un changement essentiel. Ces fréquences sont à fixer par chaque organisation : le droit ne les impose pas de manière uniforme.

## La matrice des responsabilités

R réalise, A décide et en répond, C est consulté, I est informé. Une décision n'a qu'un seul A de référence, sauf particularité contractuelle. Les niveaux d'usage U1 à U4 sont décrits dans la page sur [l'homologation](../homologation/).

| Activité | Direction | Référent IA | Juridique et déontologie | Sécurité et informatique | DPO (s'il y en a un) | Responsable de dossier |
| --- | --- | --- | --- | --- | --- | --- |
| Politique et tolérance au risque | A | R | C | C | C | I |
| Critères d'homologation | A | R | C | C | C | C |
| Évaluation d'un outil | I | A/R | C | R | C | C |
| Approbation d'un usage U1 ou U2 (par délégation) | I | A | C | C | C | R |
| Approbation d'un usage U3 ou U4 | A | R | C | C | C | R |
| Qualification des données et du secret | I | C | A | C | C | R |
| Validation juridique d'un livrable | I | I | C | I | I | A/R |
| Suspension pour raison de sécurité | A (1) | R (1) | C | R | C | I |
| Analyse d'une violation de données | A | R | C | R | C (2) | C |
| Tenue du registre | I | A/R | I | C | C | I |

(1) Selon les délégations et les mesures d'urgence prévues.

(2) Le DPO conseille et contrôle selon son statut légal, sans devenir automatiquement le décideur des notifications (articles 37 à 39 du RGPD pour le DPO, 33 et 34 pour la notification des violations). La procédure locale précise qui est responsable du traitement et quelles sont ses obligations.

Ce tableau est un point de départ. Avant de l'adopter, vérifiez l'indépendance et les missions du DPO, les pouvoirs des associés et la séparation des décisions.

## Conserver la preuve

Les décisions, les versions et les synthèses des tests sont conservées dans un emplacement sécurisé, pendant la durée que l'organisation fixe. On ne recopie pas les dossiers clients dans les journaux d'audit ni dans des documents destinés à être partagés. La traçabilité au quotidien est décrite dans [les opérations](../operations/).

## Modèle de décision de gouvernance

Le modèle suivant sert à consigner une décision d'approbation, de refus, de suspension ou de retrait. Il renvoie à la politique de gouvernance (et à la [charte](../charte/) lorsqu'elle est adoptée), à la fiche de cas d'usage et à la fiche d'évaluation décrites dans [l'homologation](../homologation/).

```text
DÉCISION DE GOUVERNANCE DE L'IA

Organisation : [ ]
Organe : [ ]
Réunion : [date]
Référence : [ ]

CONTEXTE
Vu la politique de gouvernance du [date / version], le cas échéant la charte
du [date / version], la fiche de cas d'usage [ID],
l'évaluation du système [ID / version], les avis [références]
et les résultats des tests [ID].

DÉCLARATION D'INTÉRÊTS
Membres présents et invités ; conflits ou liens avec un fournisseur ;
abstentions et mesures compensatoires : [ ]

MOTIFS
- Usage, données, personnes habilitées et actions autorisées : [ ]
- Conditions éliminatoires et réserves : [ ]
- Vérifications de qualité et risques résiduels : [ ]
- Modalités de supervision effective et faculté d'interruption : [ ]
- Moyens, formation, audit et date de réévaluation : [ ]

DISPOSITIF
L'organe [approuve / approuve avec conditions / autorise un pilote /
refuse / suspend / retire] le système [identification] pour
[cas d'usage], exclusivement dans le périmètre décrit, sous réserve
de [conditions]. L'autorisation prend effet le [date] et expire ou
est réexaminée le [date / événement]. Toute extension substantielle
nécessite une réévaluation.

Exécution et suivi : [responsable]
Notification interne : [canal et date]
Voie de réexamen : [ ]
Signatures ou approbations : [ ]
```
