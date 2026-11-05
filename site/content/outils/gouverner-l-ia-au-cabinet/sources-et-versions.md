---
draft: true
title: "Sources et versions"
description: "Les textes cités par le toolkit, la date d'arrêt du droit, les points qui restent à vérifier, l'origine du toolkit et le journal de ses versions."
weight: 80
---

Cette page dit sur quels textes repose le toolkit, à quelle date le droit a été arrêté, ce qui n'a pas encore été vérifié et comment le toolkit a été produit.

## Date d'arrêt du droit

Date d'arrêt du droit pour la présente version : [À VÉRIFIER : date d'arrêt].

La version 0.1 indiquait que les vérifications externes avaient été arrêtées au 2 novembre 2026. La liste qui suit oriente la recherche documentaire. Elle ne constitue pas un examen complet de conformité, ni en droit belge ni dans une situation transfrontalière.

## Textes et références cités

### Règlement (UE) 2024/1689 sur l'intelligence artificielle

Dans le domaine de la justice, les systèmes d'IA à haut risque visés par le règlement (UE) 2024/1689 concernent l'administration de la justice, c'est-à-dire le travail des magistrats. La pratique d'un cabinet d'avocats ou de juristes n'en relève pas. Une règle en découle : aucune déviation de la destination du système d'IA utilisé ne doit être envisagée.

Le règlement a été modifié en 2026. [À VÉRIFIER : référence de l'acte modificatif, texte consolidé et date]

Les niveaux internes du toolkit (U1 à U4 pour les usages, S1 à S4 pour les contrôles, D0 à D4 pour les données) sont des outils d'organisation. Ils sont distincts des catégories du règlement.

### Règlement (UE) 2016/679 (RGPD)

Texte : [eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj). Selon le traitement, la version 0.1 invite à examiner spécialement les articles 5 et 6, 9 et 10, 12 à 14, 24 et 25, 28, 32 à 35, et 44 et suivants. [À VÉRIFIER : pertinence de chaque article pour les traitements décrits dans le toolkit, texte et date de la version consultée]

### Guide du CCBE sur l'IA générative

Conseil des barreaux européens (CCBE), *Guide on the use of generative AI for lawyers*, 2025 : [document PDF sur ccbe.eu](https://www.ccbe.eu/fileadmin/speciality_distribution/public/documents/IT_LAW/ITL_Guides_recommendations/EN_ITL_20251002_CCBE-guide-on-the-use-of-the-use-of-generative-AI-for-lawyers.pdf). C'est une référence professionnelle utile. Elle n'a pas valeur de loi belge.

### Avis 28/2024 du Comité européen de la protection des données

Comité européen de la protection des données (CEPD, en anglais EDPB), avis 28/2024 sur certains aspects de la protection des données liés aux modèles d'IA : [edpb.europa.eu](https://www.edpb.europa.eu/documents/opinion-of-the-board-art-64/opinion-282024-on-certain-data-protection-aspects-related-to_en).

## Ce qui reste à vérifier

Avant qu'une organisation adopte le toolkit, une revue juridique belge doit porter sur les points suivants.

- Les règles déontologiques du barreau concerné : secret professionnel, infrastructure numérique, relations avec le client, devoir de diligence, contrôle des actes. [À VÉRIFIER]
- La protection des données : base de licéité, sous-traitance, responsabilité du traitement, droits des personnes, nécessité éventuelle d'une analyse d'impact (AIPD), accès aux données par les prestataires et transferts. [À VÉRIFIER]
- L'information des clients. Il ne faut pas présumer une obligation uniforme de signaler chaque assistance rédactionnelle : le contrat, la déontologie, le droit des données et les règles de transparence propres au secteur sont à examiner. [À VÉRIFIER]
- Le contrôle du personnel : droit du travail, consultation des représentants et proportionnalité des journaux d'activité. [À VÉRIFIER]
- La propriété intellectuelle sur les instructions (*prompts*), les corpus et les résultats, les droits des tiers et les réutilisations possibles. [À VÉRIFIER]

## Règles suivies pour les sources

Chaque version annonce la date d'arrêt du droit, les juridictions couvertes et les hypothèses retenues. Un lien vers une source ne remplace pas la vérification de la disposition pertinente. Un avis technique ou déontologique n'est pas présenté comme une obligation de droit positif sans fondement identifié. Si un texte ou une jurisprudence change, une version corrigée ou un erratum est publié.

## D'où vient le toolkit

La version 0.1 date du 2 novembre 2026. Elle a été rédigée avec l'aide d'une IA et n'a pas été relue par un tiers. Elle comptait environ 19 000 mots, avait le statut de proposition non adoptée et ne concédait aucune licence. Ses fichiers CSV ne contenaient que leurs en-têtes.

Elle a été construite à partir d'une charte communiquée au cours de la conversation avec l'IA et des orientations discutées à cette occasion. Le texte complet de cette charte initiale n'y est pas joint. Ses principaux défauts et les corrections proposées figurent dans l'analyse de la charte initiale. Les références juridiques externes y sont données sous forme de liens et ne sont pas reproduites.

La version 0.1 reproduisait aussi, sans modification, deux documents de contexte de JERLASH Labs datés du 2 novembre 2026 : un document d'architecture du projet (modèle « Legal Technology Commons », statut de projet) et les consignes de la collection Research Papers (statut de politique proposée). Les droits sur ces deux documents sont à vérifier avant toute redistribution publique de l'archive. [À VÉRIFIER]

La version 0.2, en préparation, est une relecture réduite de la version 0.1, adaptée pour jerlash.labs. Elle est publiée par jerlash.labs sous licence CC BY-NC 4.0.

## Journal des versions

### 0.2, en préparation

- Relecture et réduction de la version 0.1, réécriture selon la charte éditoriale de jerlash.labs.
- Titre français : « Gouverner l'IA au cabinet ».
- Parcours réorganisé (décision du 3 novembre 2026) : la gouvernance se met en place d'abord ; la charte vient en dernier et ancre les choix faits dans les autres modules.
- Règlement IA ramené à un seul rappel (décision du 3 novembre 2026) : les développements sur les obligations des systèmes à haut risque sont retirés. La supervision humaine est traitée comme une exigence professionnelle et déontologique.
- Éditeur : jerlash.labs. Licence : CC BY-NC 4.0.
- Date d'arrêt du droit : [À VÉRIFIER : date d'arrêt].

### 0.1.0, 2 novembre 2026

- Première compilation du toolkit.
- Charte modèle en 16 articles, politique de gouvernance et matrice des responsabilités (RACI).
- Homologation d'un outil pour un cas d'usage déterminé, avec des conditions éliminatoires.
- Protocole de supervision S1 à S4, validation des livrables, contrôle des actions des agents.
- Classification des données D0 à D4, traçabilité, incidents et formation.
- Documents de projet, protocole de recherche H1 et modèles de registres.
- Intégration de deux documents de contexte de JERLASH Labs.

Restait à faire avant une version 1.0 : désigner l'éditeur (c'est fait depuis, voir la version 0.2), vérifier les droits et les licences, revoir la déontologie belge, valider les seuils fixés par chaque organisation, mettre le toolkit à l'épreuve auprès de cabinets pilotes et documenter les révisions.

Voir aussi [la gouvernance](../gouvernance/), [les données](../donnees/), [l'homologation](../homologation/), [la supervision](../supervision/), [les opérations](../operations/) et [la charte](../charte/).
