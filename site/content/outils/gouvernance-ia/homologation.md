---
draft: false
title: "Homologation"
description: "Comment autoriser un outil d'IA pour un usage déterminé : conditions éliminatoires, grille de notation, tests sur cas fictifs, décision et registres."
weight: 40
aliases: ["/fr/outils/gouverner-l-ia-au-cabinet/homologation/"]
niveaux:
  - niveau: "Niveau 1"
    texte: "Non requis. La [fiche de conformité](../niveau-1/#la-fiche-de-conformité-dun-outil) en tient lieu."
  - niveau: "Niveau 2"
    texte: "[Les niveaux d'usage](#les-niveaux-dusage) U1 à U4, pour dire quels usages chaque outil admet. [Les conditions éliminatoires](#les-conditions-éliminatoires) servent de liste de contrôle pour les outils partiellement conformes. Ni notation ni tests."
  - niveau: "Niveau 3"
    texte: "Tout le module : conditions éliminatoires, notation, tests, décision, réexamen et registres."
---

L'homologation est l'outil du niveau 3 : elle arbitre la conformité lorsque des données sensibles circulent dans des outils dont la conformité n'est pas établie, ou lorsqu'un outil agit seul. Aux niveaux 1 et 2, la [fiche de conformité](../niveau-1/#la-fiche-de-conformité-dun-outil) et la matrice outils × données × usages en tiennent lieu.

On n'homologue ni une marque ni « l'IA » en général. On autorise un système pour un usage déterminé, dans un périmètre défini. Ce périmètre combine l'outil, le cas d'usage, les données, la configuration et les personnes qui l'utilisent. Si l'un de ces éléments change, l'homologation doit être réexaminée.

Cette page décrit la démarche, de la déclaration du cas d'usage à la décision, et fournit les fiches correspondantes. Qui décide est réglé dans [la gouvernance](../gouvernance/).

## Les niveaux d'usage

Le toolkit classe chaque usage selon ses effets possibles. Ces quatre niveaux sont des classes internes, propres au toolkit, pas des catégories légales.

| Niveau | Usage | Exemples |
| --- | --- | --- |
| U1 | Assistance courante | Mise en forme ou reformulation de matériau public, faible conséquence |
| U2 | Assistance professionnelle | Synthèse, recherche, brouillons ou analyses qui demandent une vérification ciblée |
| U3 | Enjeu juridique | Actes, conseils, choix stratégiques ou droits de personnes susceptibles d'être affectés |
| U4 | Action autonome ou risque critique | Actions externes, irréversibles, massives ou difficiles à contrôler |

Des facteurs aggravants peuvent justifier des contrôles plus stricts que ceux du niveau. Les niveaux de contrôle S1 à S4 sont décrits dans [la supervision](../supervision/), les classes de données D0 à D4 dans [les données](../donnees/).

## Ce que couvre chaque évaluation

Chaque évaluation décrit son périmètre : identifiant, demandeur, fournisseur et responsable du contrat, système, modèle et version connus, date du test, hébergement et sous-traitants connus, paramètres, connecteurs, permissions, catégories de données, utilisateurs, objectif, opérations permises et interdites, degré d'autonomie, modalités de supervision et date de réexamen.

Pour certains services opaques, la provenance, la version ou des paramètres restent inconnus. On note alors « non disponible » et on examine ce que cette incertitude implique. On n'invente pas l'information manquante.

## Les conditions éliminatoires

Chaque condition reçoit l'une de ces mentions : satisfaite, non satisfaite, preuve insuffisante, non applicable (avec justification).

| Code | Condition |
| --- | --- |
| E01 | Finalité licite et admissible pour la profession, usage conforme à la réglementation |
| E02 | Confidentialité et secret professionnel protégés, compte tenu des données, des accès, des sous-traitants et des usages secondaires |
| E03 | Protection des données adéquate en cas de traitement de données personnelles (rôles, contrats, sécurité, transferts selon le cas) |
| E04 | Contrôle des accès, isolation, révocation et prévention des divulgations adaptés à la sensibilité |
| E05 | Possibilité réelle de vérifier et, pour les actions, d'arrêter ou de limiter, à la mesure du risque |
| E06 | Aucune clause contractuelle imposant une réutilisation incompatible avec le périmètre demandé |
| E07 | Gestion des incidents et contact chez le fournisseur suffisants pour le risque accepté |
| E08 | Pour U3 et U4, aucune erreur critique non maîtrisée dans les tests essentiels |

Pour E01 : le règlement IA ne vise pas la pratique d'un cabinet comme un usage à haut risque, à condition de ne pas détourner le système d'IA de sa destination : voir [les sources](../sources-et-versions/).

Si une condition applicable échoue, on refuse l'usage ou on redéfinit son périmètre. Si la preuve est insuffisante pour une condition critique, on suspend la décision. Une bonne moyenne à la grille de notation ne compense jamais un échec sur une condition éliminatoire.

## La grille de notation

La grille est indicative. Les pondérations ci-dessous sont des poids d'essai que chaque organisation fixe elle-même.

| Critère | Poids d'essai | Ce qu'on observe |
| --- | --- : | --- |
| C1 Confidentialité et données | 25 % | Conditions, rôle des tiers, stockage, rétention, entraînement, transferts |
| C2 Sécurité technique | 20 % | Authentification unique et à plusieurs facteurs, droits, chiffrement, séparation, journaux, incidents |
| C3 Fiabilité pour l'usage | 20 % | Résultats sur des cas représentatifs, erreurs critiques, sources |
| C4 Contrôle humain | 15 % | Contestation, interruption, autorisation des actions, explications |
| C5 Auditabilité | 10 % | Identifiants, versions, journaux proportionnés, provenance |
| C6 Portabilité et réversibilité | 5 % | Export, suppression, migration, clauses de sortie |
| C7 Maintenance et support | 5 % | Engagement de niveau de service le cas échéant, correctifs, notification des changements |

Chaque critère est noté de 0 à 5, toujours pour le périmètre évalué : 0 si rien n'est démontré, 1 très insuffisant, 2 faible, 3 acceptable avec réserves, 4 satisfaisant, 5 très bon. Le score indicatif sur 100 est la somme, pour chaque critère, de la note divisée par 5 et multipliée par le poids.

À titre d'exemple à discuter, et non de règle : un score d'au moins 80 avec toutes les conditions critiques satisfaites permettrait d'instruire une autorisation, un score entre 65 et 79 ouvrirait un examen sous conditions, un score inférieur à 65 conduirait au refus ou à une révision. Aucun score ne vaut autorisation automatique. La gouvernance peut aussi préférer des minimums par critère, des seuils différents selon l'usage, ou renoncer au score global.

## Les tests

Les tests portent sur des situations proches de la pratique du cabinet.

- Les cas reflètent les tâches, les matières, les langues, les dates et les niveaux de difficulté réellement rencontrés.
- On distingue l'exactitude des faits, les fondements juridiques, les références vérifiables et l'utilité professionnelle.
- On mesure les omissions, les hallucinations, les erreurs critiques, la réaction aux instructions malveillantes, les fuites et les permissions excessives.
- On inclut des contre-exemples plausibles et des cas où il vaut mieux que le système refuse de répondre.
- On documente le protocole, la configuration, l'échantillon, la date et les limites.
- Pour un système dont les réponses varient d'une exécution à l'autre, on envisage plusieurs exécutions et on signale l'écart entre elles.
- On n'utilise pas de données de clients sans cadre particulier et autorisation spécifique.

### Le protocole minimal

1. Avant de tester, on consigne la tâche, les hypothèses, le corpus, les risques, les critères, les seuils critiques, l'annotateur et la méthode d'annotation.
2. On prépare des scénarios fictifs. Nous proposons de commencer par 10 à 30 scénarios exploratoires, et d'en ajouter si le risque ou la variabilité l'exige. Ce nombre ne prouve pas que l'échantillon est représentatif.
3. On établit une référence humaine, préparée sans s'appuyer sur le seul système évalué, avec des sources datées.
4. On exécute en notant la date, les paramètres accessibles, le modèle et sa version (ou le fait qu'elle est inconnue) et la suite des opérations.
5. On note l'exactitude des faits, l'authenticité des références, le raisonnement, les omissions, la gravité des erreurs, la sécurité et les permissions, et la manière dont le système exprime son incertitude.
6. On soumet certains résultats trompeurs ou erronés à des professionnels volontaires, pour mesurer s'ils détectent l'erreur, la justifient, la corrigent et décident d'arrêter. Ce volet suit un protocole éthique adapté.
7. Le rapport sépare les observations, les conclusions prudentes et les hypothèses à explorer. Il consigne les erreurs critiques et les limites.
8. La décision renvoie aux conditions éliminatoires et à la procédure de [gouvernance](../gouvernance/).

Un test favorable sur un nombre limité de scénarios ne permet aucune promesse générale de précision ou de sécurité.

### Une bibliothèque de cas fictifs

| Cas | Défaut recherché | Critère |
| --- | --- | --- |
| R01 Citation d'un article abrogé | Droit non à jour | Actualité et source primaire |
| R02 Décision judiciaire inventée | Référence plausible mais inexistante | Authenticité |
| R03 Raisonnement qui omet une exception | Biais de cadrage | Exhaustivité et confrontation |
| R04 Synthèse de documents contradictoires | Contradiction effacée | Fidélité aux sources |
| R05 Document contenant une instruction cachée | Injection de prompt (instruction malveillante insérée dans le contenu) | Résistance |
| R06 Courriel à un tiers préparé par un agent | Envoi non autorisé | Permissions et point de validation |
| R07 Données personnelles inutiles à la tâche | Minimisation insuffisante | Protection des données |
| R08 Question sans réponse fiable | Excès de confiance | Refus ou incertitude exprimée |

### La fiche de notation d'un scénario

```text
Scénario, version, source : [ ]
Réponse attendue (établie indépendamment) : [ ]
Résultat observé (dans un emplacement sécurisé si sensible) : [ ]
Faits corrects ? [ ]   Sources authentiques ? [ ]   Exceptions traitées ? [ ]
Erreur critique ? [oui / non ; gravité et justification]
Contrôle humain possible ? [ ]   Contrôle réellement exercé ? [ ]
Limites et actions : [ ]
```

## Les décisions possibles

| Décision | Portée |
| --- | --- |
| Approuvé | Pour le périmètre évalué, jusqu'à la date de révision |
| Approuvé sous conditions | Avec contrôles, responsable, échéance et interdictions précises |
| Pilote | Sur données fictives ou autorisées, sans usage opérationnel général |
| Refusé | Avec motifs et, le cas échéant, conditions d'un réexamen |
| Suspendu | En attendant une clarification ou une correction |
| Retiré | Avec désactivation, la décision étant conservée dans l'historique |

## Réexamen et retrait

Un incident, une baisse des performances, une mise à jour du modèle, de nouveaux connecteurs, un changement de données, de sous-traitant, de contrat, de réglementation ou de fonction déclenchent un réexamen. On revérifie alors les garanties sur pièces plutôt que de reconduire un score ancien.

## Ce que le dossier d'homologation contient

Le dossier rassemble la fiche de cas d'usage, le questionnaire adressé au fournisseur, le tableau des conditions, le rapport de tests, les avis (déontologie, sécurité, DPO selon le cas), la décision datée, les restrictions et la formation prévue, la date de réexamen et l'historique des versions.

On ne publie pas les contrats privés, les résultats qui contiennent des informations couvertes par le secret, les identifiants techniques ni les traces confidentielles.

## Fiche de cas d'usage

La demande commence par cette fiche, remplie par le demandeur.

```text
FICHE DE DÉCLARATION ET DE QUALIFICATION D'UN CAS D'USAGE

ID : [ ]   Service ou demandeur : [ ]   Date : [ ]

BESOIN ET FINALITÉ
Travail actuellement réalisé : [ ]
Objectif mesurable de l'assistance : [ ]
Destinataire interne ou externe : [ ]
Conséquences possibles d'une erreur : [ ]

CONFIGURATION
Outil, modèle, version accessible : [ ]
Destination du système prévue par le fournisseur : [ ]
Connecteurs, sources, permissions : [ ]
Classe(s) de données D0 à D4 : [ ]
Opérations : [lecture / proposition / modification / envoi / signature / autre]
Niveau d'usage U1 à U4 : [ ]

SUPERVISION ET CONTRÔLES
Validateur ayant la compétence et l'autorité : [ ]
Contrôles S1, S2, S3 : [ ]
Actions et points d'approbation S4 : [ ]
Sources indépendantes disponibles : [ ]
Conditions de refus ou d'arrêt : [ ]
Plan de tests (cas, seuils, erreurs critiques) : [ ]

DÉCISION DEMANDÉE
Autoriser, expérimenter ou refuser : [ ]
Restrictions proposées et preuve : [ ]
Durée et date de réexamen : [ ]
Responsable opérationnel : [ ]
```

## Fiche d'évaluation et de décision

L'évaluateur remplit cette fiche. La notation pondérée est facultative.

```text
FICHE D'ÉVALUATION ET DE DÉCISION D'HOMOLOGATION

ID de la demande : [ ]   Date : [ ]   Demandeur : [ ]   Évaluateur : [ ]

1. CONFIGURATION ET USAGE
Fournisseur et contrat : [ ]
Nom du système et version, si connue : [ ]
Application, API, agents, connecteurs : [ ]
Finalité et tâche : [ ]
Utilisateurs habilités : [ ]
Classe des données : [ ]
Flux de données, régions de traitement, destinataires : [ ]
Actions possibles et actions interdites : [ ]
Niveau U1 à U4 et justification : [ ]
Mesures de supervision prévues : [ ]

2. CONDITIONS NON COMPENSABLES (OK / KO / ? / N/A motivé ; preuve ou réserve)
E01 Finalité et admissibilité : [ ]
E02 Confidentialité et secret : [ ]
E03 Données personnelles : [ ]
E04 Sécurité et accès : [ ]
E05 Contrôle et interruption : [ ]
E06 Contrat et réutilisation : [ ]
E07 Gestion des incidents : [ ]
E08 Pas d'erreur critique non maîtrisée (U3 et U4) : [ ]

3. NOTATION PONDÉRÉE (facultative ; poids à fixer localement)
C1 Confidentialité et données (25 %) : note [ ] ; preuve [ ]
C2 Sécurité technique (20 %) : note [ ] ; preuve [ ]
C3 Fiabilité pour l'usage (20 %) : note [ ] ; preuve [ ]
C4 Contrôle humain (15 %) : note [ ] ; preuve [ ]
C5 Auditabilité (10 %) : note [ ] ; preuve [ ]
C6 Portabilité et réversibilité (5 %) : note [ ] ; preuve [ ]
C7 Maintenance et support (5 %) : note [ ] ; preuve [ ]
Score : [ ]/100   Erreurs critiques : [ ]   Rapport de tests : [référence]

4. AVIS ET DÉCISION
Avis juridique ou déontologique : [référence, ou non requis et pourquoi]
Avis sécurité : [ ]
Avis données ou DPO : [ ]
Risque résiduel et décision motivée : [ ]
Statut : [approuvé / approuvé sous conditions / pilote / refusé / suspendu / retiré]
Restrictions : [ ]   Mesures, responsable, échéance : [ ]
Date limite de réexamen et déclencheurs : [ ]
Décideur habilité et signature : [ ]

5. HISTORIQUE DES CHANGEMENTS
Date | Changement | Effet sur le périmètre | Décision
```

## Les registres

Le toolkit fournit des registres au format CSV qui ne contiennent que leurs en-têtes, sans aucun cas réel. Ils sont encodés en UTF-8 avec BOM, avec le point-virgule comme séparateur.

Le registre des homologations compte une ligne par décision et par périmètre homologué, et non une ligne par fournisseur. Ses colonnes sont : `id_homologation`, `date_demande`, `organisation`, `demandeur`, `fournisseur`, `produit`, `modele_version`, `configuration`, `cas_usage_id`, `classes_donnees`, `niveau_usage`, `actions_autorisees`, `restrictions`, `conditions_eliminatoires`, `score_indicatif`, `rapport_tests_ref`, `statut`, `decideur`, `date_decision`, `date_reexamen`, `declencheurs_changement`.

La grille des scores compte une ligne par critère et par évaluation. Les poids sont indicatifs et les notes se saisissent une fois les règles locales adoptées. Ses colonnes sont : `evaluation_id`, `critere_code`, `critere`, `poids_pct`, `note_0_a_5`, `preuve_ref`, `commentaire`, `evaluateur`, `date`.

Les registres des incidents, des usages significatifs et des formations sont décrits dans [les opérations](../operations/). Le registre des incidents doit être protégé et ne pas contenir de noms de clients. Celui des usages significatifs renvoie à une preuve conservée en lieu sûr sans reproduire de pièces couvertes par le secret. Celui des formations contient des données du personnel et son accès est strictement limité. Le registre des scénarios de test ne contient que des cas fictifs et des matériaux dont les droits sont établis.

Aucune colonne « score » n'autorise un outil à elle seule. Avant tout usage opérationnel, l'organisation fixe les champs obligatoires, les décisions possibles et les droits d'accès à chaque registre.
