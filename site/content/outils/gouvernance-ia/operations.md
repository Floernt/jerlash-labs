---
draft: false
title: "Traçabilité, incidents et formation"
description: "Ce qu'un cabinet garde comme trace de ses usages de l'IA, comment il traite un incident et comment il forme et habilite les personnes qui utilisent ou supervisent ces outils."
weight: 60
aliases: ["/fr/outils/gouverner-l-ia-au-cabinet/operations/"]
niveaux:
  - niveau: "Niveau 1"
    texte: "[La procédure d'incident](#la-procédure) et les modules de formation F1 à F3."
  - niveau: "Niveau 2"
    texte: "Le niveau 1, plus [la preuve proportionnée](#une-preuve-proportionnée-au-niveau-dusage) et le registre des incidents."
  - niveau: "Niveau 3"
    texte: "Tout le module, y compris les registres et l'habilitation."
---

Ce module couvre le fonctionnement courant : quels éléments de traçabilité (preuve) garder, comment réagir à un incident, comment former et habiliter. Il s'appuie sur les niveaux d'usage U1 à U4 de [l'homologation](../homologation/), les niveaux de contrôle S1 à S4 de [la supervision](../supervision/) et les classes de données D0 à D4 décrites dans [les données](../donnees/). Les durées, fréquences et contenus proposés ici sont à fixer par chaque organisation.

## Traçabilité

### Ce que la preuve doit permettre

La preuve doit suffire à comprendre un usage significatif de l'IA, les décisions prises et les incidents, sans accumuler des copies de documents couverts par le secret professionnel. Une mention « assisté par IA » ne prouve pas qu'un contrôle a eu lieu, et rien n'impose de l'apposer uniformément à chaque petite tâche.

### Une preuve proportionnée au niveau d'usage

| Usage | Preuve proposée |
|---|---|
| U1, mise en forme | Pas de fiche individuelle, sauf incident ou exigence propre à l'activité |
| U2, analyse de travail | Outil, finalité et, lorsque c'est pertinent, contrôle des points décisifs |
| U3, conseil ou contenu engageant | Outil, source des points déterminants, décision et validation par une personne compétente |
| U4, action automatisée | Identifiant de l'action, autorisation, autorité, cible, résultat, point d'arrêt et incident éventuel |

### Quatre lieux 

Les informations ne vont pas toutes au même endroit.

| Lieu | Contenu |
|---|---|
| Registre de gouvernance | Métadonnées non confidentielles et décisions |
| Dossier professionnel sécurisé | Pièces, sources et contrôles détaillés liés à un client |
| Journal technique | Événements nécessaires à la sécurité et au diagnostic, avec des droits d'accès et un effacement adaptés |
| Espace public éventuel | Méthodes, formulaires vides, données synthétiques et résultats expurgés |

### Conservation, accès et surveillance

L'organisation désigne une personne responsable de la conservation. Elle fixe les durées de conservation en fonction de la finalité, de la base légale et des obligations professionnelles, et prévoit le traitement des demandes d'exercice des droits des personnes concernées ainsi que les mesures de sécurité. 

Une surveillance continue des collaborateurs au moyen de ces journaux ne peut pas être présumée licite. Elle s'apprécie au regard du droit du travail, de la transparence et de la proportionnalité. Un examen approfondi doit être réalisé sur cet aspect.

### Documenter une décision

Une décision relative à un usage ou à un outil se documente par les éléments suivants : identifiant, date, demandeur, outil et configuration, usage, catégories de données, niveau de risque, contrôles effectués, décision motivée, approbateur, échéance et changement majeur éventuel. On n'y joint jamais par réflexe la conversation complète avec l'outil lorsqu'elle contient des données couvertes par le secret.

## Incidents

### Quand signaler

On signale dès qu'il existe un soupçon sérieux de fuite de données, d'erreur juridique importante, de transmission inadéquate, de comportement imprévu d'un agent, de contournement des permissions, d'atteinte possible à des droits ou de sortie du périmètre homologué. Les quasi-incidents méritent aussi d'être signalés : ils permettent à l'organisation d'apprendre sans attendre le dommage.

### La procédure

1. Signaler sans délai injustifié au point de contact désigné (référent IA ou support sécurité).
2. Protéger : arrêter le flux ou révoquer les accès lorsqu'on y est autorisé, conserver les preuves nécessaires sans propager la donnée.
3. Qualifier : déterminer les dommages, les personnes, les systèmes et les données touchés, ainsi que les obligations professionnelles, contractuelles et réglementaires en jeu.
4. Escalader, selon le cas, vers le responsable du dossier, la direction, la sécurité, le délégué à la protection des données ou des conseils spécialisés, et déterminer qui notifie quoi, dans quel délai.
5. Remédier : corriger le livrable, prévenir les conséquences, informer le client ou les tiers si c'est requis, revoir les réglages ou les droits.
6. Réévaluer : suspendre ou modifier l'homologation de l'outil, enrichir les tests et les formations (voir [l'homologation](../homologation/)).
7. Clore en consignant les mesures prises, le responsable et le résultat, y compris ce qui n'a pas pu être établi.

### Notifications

Les délais et les destinataires d'une notification dépendent du type d'incident, de la qualité des parties, de la législation applicable et des obligations déontologiques. Il ne faut pas appliquer un délai unique à toute erreur liée à l'IA. Une violation de données à caractère personnel appelle une analyse spécifique au regard du RGPD, qui peut conduire à notifier l'autorité de contrôle et les personnes concernées lorsque les conditions légales sont réunies (articles 33 et 34 du RGPD).

### Fiche rapide d'incident

| Rubrique | À compléter |
|---|---|
| Identifiant | |
| Date et heure de la découverte | |
| Déclarant | |
| Outil et version | |
| Faits vérifiés | |
| Impact potentiel | |
| Classes de données | |
| Mesures de confinement | |
| Autorité de décision | |
| Analyse juridique et déontologique | |
| Notifications et leurs motifs | |
| Actions correctives (responsable, échéance) | |
| Sort de l'homologation (maintenue, limitée, suspendue, retirée) | |
| Retour d'expérience anonymisé | |
| Clôture | |

## Formation et habilitation

Le programme ci-dessous est une proposition. Les éventuelles exigences légales en matière de formation sont à vérifier.

### Les modules

| Module | Public | Compétence observable |
|---|---|---|
| F1, bases et limites des IA | Tous | Reconnaître une réponse plausible mais non fiable, expliquer les limites |
| F2, confidentialité et données | Tous | Classer un exemple en D0 à D4, décider si la transmission est permise |
| F3, sources et raisonnement | Juristes et avocats | Vérifier une citation, son actualité et l'exception pertinente |
| F4, supervision effective | Responsables de travaux | Contester, corriger, refuser et motiver |
| F5, agents et opérations | Utilisateurs d'agents, informatique | Paramétrer les permissions, reconnaître une action engageante, arrêter l'agent |
| F6, gouvernance et incidents | Décideurs, référent | Homologuer dans un périmètre, traiter une escalade |

### L'évaluation

L'évaluation proposée repose sur des mises en situation. Face à une étude de cas contenant une erreur juridique inventée ou une règle dépassée, la personne repère l'erreur et documente sa vérification. Face à un scénario impliquant des données couvertes par le secret, elle identifie le périmètre autorisé ou refuse le transfert. Pour un agent qui doit envoyer un courriel, elle détermine où se place l'approbation et qui peut refuser. Lors d'une simulation d'incident, elle applique la procédure et sait qui contacter.

Si l'organisation attribue des scores de formation, elle les définit elle-même et prévoit un rattrapage. Aucune attestation interne ne doit être présentée comme un agrément institutionnel ou réglementaire.

### Garder les capacités

La supervision suppose de savoir faire sans l'outil. L'organisation fait donc exercer, à une fréquence qu'elle fixe, des tâches de vérification sans assistance, organise des revues contradictoires et cherche à repérer une dépendance excessive aux réponses plausibles. Formation et habilitations sont revues lors d'un changement majeur de système ou de responsabilités.

## Les registres

Le toolkit fournit les registres sous forme de fichiers CSV vides, séparés par des points-virgules, qui ne contiennent que leurs en-têtes. Ils sont conçus pour le registre de gouvernance : les références de dossier y sont internes et les preuves détaillées restent dans le dossier sécurisé.

| Registre | Ce qu'il consigne | Colonnes |
|---|---|---|
| `REGISTRE_USAGES_SIGNIFICATIFS.csv` | Les usages significatifs et leur contrôle | identifiant, date, outil et version, cas d'usage, référence interne du dossier, niveau d'usage, contrôle S1 à S4, points déterminants vérifiés, références des sources, décision, validateur, réserve, lieu où la preuve est conservée de façon sécurisée |
| `REGISTRE_INCIDENTS.csv` | Les incidents et leur traitement | identifiant, dates de découverte et de signalement, outil et version, cas d'usage, catégorie, impact potentiel, classe de données, mesures immédiates, responsable, escalade, évaluation de la notification, mesures correctives, échéance, statut de l'homologation, date de clôture |
| `REGISTRE_FORMATIONS.csv` | Les formations et habilitations | identifiant interne de la personne, rôle, module, date de formation, date et modalité d'évaluation, habilitation, date de réexamen, validateur |

Le registre des formations contient des données sur les membres du personnel. L'accès y est limité et les droits des travailleurs sont respectés. Le registre des homologations est décrit dans [l'homologation](../homologation/).
