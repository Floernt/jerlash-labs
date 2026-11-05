---
draft: true
title: "Données"
description: "Classer les informations avant de les confier à un outil d'IA, se poser les bonnes questions avant le traitement et documenter l'analyse."
weight: 30
---

Avant de transmettre une information à un système d'IA, ou de lui y donner accès, on la classe. La classe détermine dans quel outil homologué elle peut entrer et à quelles conditions. Cette page propose une classification, une liste de questions à se poser avant le traitement et un questionnaire à joindre au dossier d'[homologation](../homologation/).

## Les cinq classes

La classification D0 à D4 est une politique interne propre au toolkit. Ce n'est pas une nomenclature légale.

| Classe | Exemples | Règle de base |
| --- | --- | --- |
| D0 Publique | Législation, documents librement diffusables | Utilisable dans un système homologué pour D0, selon sa finalité |
| D1 Interne | Procédure du cabinet, brouillon non sensible, budget interne non publié | Système homologué pour D1, contrôle des accès et du stockage |
| D2 Confidentielle | Documents commerciaux, informations de négociation non publiques, éléments non publics sur des tiers | Homologation explicite pour D2, finalité justifiée, transmission limitée |
| D3 Secret professionnel | Instructions des clients, correspondances et pièces couvertes par le secret, stratégie de défense | Analyse juridique et déontologique spécifique ; fournisseur, accès et traitement expressément autorisés |
| D4 Protection renforcée | Données sensibles ou pénales, dossiers particulièrement exposés, mineurs ou personnes vulnérables | Mesures renforcées, analyse juridique spécifique |

D3 et D4 peuvent se cumuler. D4 ne remplace pas la protection du secret. Les autres contraintes (secret des affaires, droit d'auteur, interdictions contractuelles) s'ajoutent à la classe comme des attributs.

## Avant le traitement

1. Quel est le minimum de données nécessaire à la tâche ?
2. La donnée entre-t-elle dans le périmètre de l'homologation, connecteurs et sous-traitants compris ?
3. Un exemple fictif, une synthèse non identifiante ou un autre environnement suffiraient-ils ?
4. Qui a accès aux requêtes, aux réponses, aux fichiers et aux journaux, y compris chez les prestataires ?
5. Les données sont-elles réutilisées pour l'entraînement, l'évaluation, la sécurité ou l'assistance humaine ?
6. Quels sont les délais d'effacement, les transferts et les garanties du contrat ?
7. S'il s'agit de données personnelles, faut-il un contrat de sous-traitance, une analyse d'impact, une information des personnes ou une autre mesure ?
8. Le responsable du dossier connaît-il et maîtrise-t-il les risques professionnels ?

## Points d'attention

Pseudonymiser n'est pas anonymiser. Le contexte d'un document suffit parfois à réidentifier une personne.

Un hébergement dans l'Union européenne ne garantit pas à lui seul la confidentialité. Il faut examiner le contrat, les sous-traitants, les accès et le droit applicable.

Un fournisseur qui n'entraîne pas ses modèles publics sur vos données peut quand même les traiter : il peut les conserver, consulter les journaux, les faire lire par une assistance humaine, les surveiller pour détecter les abus et les transférer.

Une source juridique librement accessible n'est pas automatiquement libre de droits d'auteur ou de restrictions d'usage.

Les demandes, les pièces et les décisions d'homologation qui contiennent des informations protégées ne sont jamais rendues publiques.

## L'autorisation locale

Pour chaque classe et chaque usage, l'organisation consigne la classe, les données admises, la minimisation requise, l'environnement, les services en aval, les interdictions, le validateur, les conditions de suppression, la durée et la date de réexamen. Les rôles chargés de cette qualification figurent dans [la gouvernance](../gouvernance/).

## Questionnaire d'analyse d'un traitement

Ce questionnaire se remplit avant l'homologation. Ce n'est pas une analyse d'impact complète. Lorsqu'une analyse d'impact est requise, elle est conduite selon les exigences applicables et la méthode de l'organisation.

```text
QUESTIONNAIRE DE TRAITEMENT DE DONNÉES AVANT HOMOLOGATION

Organisation et responsable : [ ]   Outil et cas d'usage : [ ]   Date : [ ]

1.  Nature des informations : [D0 / D1 / D2 / D3 / D4 ; cumul et justification]
2.  Données personnelles : [oui / non / à clarifier] ; catégories,
    personnes concernées, éventuelles données visées aux articles 9 ou 10
    du RGPD [À VÉRIFIER : texte et version consolidée] : [ ]
3.  But et nécessité du traitement : [ ]
4.  Rôles au sens du RGPD : responsable du traitement, sous-traitant(s),
    destinataires, éventuelle responsabilité conjointe : [ ]
5.  Fondement juridique, information et droits des personnes :
    [analyse à compléter si applicable]
6.  Secret professionnel et autres secrets : [qualification et avis]
7.  Contrat et sous-traitants : [contrat de sous-traitance, sécurité,
    assistance, réutilisation, modalités d'effacement]
8.  Localisation et transferts : [infrastructures, support,
    accès à distance, garanties]
9.  Sécurité : [authentification à plusieurs facteurs, chiffrement,
    isolation, contrôle des accès, journaux, sauvegarde, réponse aux incidents]
10. Durée de conservation et sortie : [ ]
11. Minimisation, pseudonymisation, données synthétiques : [ ]
12. Analyse d'impact ou consultation éventuelle : [nécessaire ? motifs et décision]
13. Risques résiduels et conditions : [ ]
14. Avis du DPO s'il y en a un, avis juridique, avis sécurité : [ ]
15. Décision et durée : [ ]
```
