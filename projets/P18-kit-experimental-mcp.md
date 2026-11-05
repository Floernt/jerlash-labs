---
id: P18
titre: Kit expérimental MCP (conditions C0 à C3)
type: contenu (recherche) et outillage
statut: idée
priorité: moyenne
source: archive Proton du 2026-11-03, JERLASH_MCP_Experimental_Kit v0.1, pack participants v0.1, extension C3 v0.2 (hors dépôt)
licence_source: non indiquée
dépend_de: [ADR-024]
mise_a_jour: 2026-11-03
---

# Kit expérimental MCP (conditions C0 à C3)

## 1. Origine

Le kit v0.1 du 2 novembre 2026 met en pratique un papier source sur MCP, outil d'orchestration de l'expertise dans un cabinet. Ce papier est un brouillon rédigé avec GPT-6, sans auteurs ni licence.

Le kit prévoit trois conditions de travail :
- C0 : sans IA ;
- C1 : IA à qui l'on donne les documents à la main ;
- C2 : même IA reliée aux outils par MCP, avec des droits minimaux.

Il contient 30 cas fictifs (contrats, insolvabilité, cyber ; en FR, EN et NL), 12 scénarios d'attaque, 6 erreurs injectées, et des scripts qui ne simulent que les règles métier. Le pack participants est un sous-ensemble identique du kit.

L'extension C3 v0.2 ajoute une quatrième condition : la même IA appelle les services directement, dans un déroulé fixe, sans MCP. Elle répond à la question « MCP est-il nécessaire ? ». Le code C3 annoncé dans les documents est absent de l'archive.

## 2. Problème ou opportunité

Une IA reliée aux outils du cabinet par MCP améliore-t-elle le traitement initial des demandes, sans dégrader la confidentialité, la qualité ou la supervision ? Le critère principal est le temps humain actif. La sûreté est un critère co-principal, qui ne peut pas être compensé par un gain de temps.

## 3. Solution envisagée

Projet de janvier 2027 : publier la partie publique du kit.
- Le protocole, publié comme article de type Protocol dans Revue et Recherche.
- La gouvernance (GO/NO-GO, RGPD, rôles), dans Éthique, rubrique « Recherche avec participants ».
- L'architecture, les scripts et les schémas, dans Outils.
- L'addendum C3.

Le tout porte la mention explicite « aucune donnée réelle, pilote non exécuté ». Le même mois, on lance G0 : la recherche des deux juristes relecteurs du corpus.

Étapes ultérieures, en dehors du projet de janvier :
- juin 2027 : serveur MCP synthétique C2 et orchestrateur C3 ;
- octobre 2027 au plus tôt : pilote, seulement si G3 est passé.

Hors périmètre : publier des résultats tant que le pilote n'a pas eu lieu. Les fichiers de `06_Demonstration` contiennent de fausses données et ne sont jamais présentés comme des résultats.

## 4. Adaptation à jerlash.labs

Les scripts suivent les principes des outils si on les publie : Python, bibliothèque standard, tests `unittest`.

RÉSERVÉ : `03_Corpus/referentiel_restreint/` (corrigé, guide des correcteurs, registre de conflits, cas de supervision) et `adversarial_tests.jsonl` n'entrent jamais dans le dépôt avant la fin de la collecte.

## 5. Approche technique pressentie

Les jalons du kit :
- G0 : relecture du corpus par deux juristes, puis empreinte SHA-256 figée ;
- G2 : serveur MCP avec un SDK figé, test d'intrusion, relecteur sécurité distinct du développeur ;
- G3 : notice RGPD, base légale, avis du DPO, avis d'éthique ;
- préenregistrement : non déposé aujourd'hui ;
- G4 : rapport.

## 6. Contraintes et risques

Personnes : c'est le chemin critique. Il faut 2 juristes relecteurs, un réviseur sécurité, un DPO, un avis d'éthique, 3 évaluateurs et 15 participants. Tous sont à nommer.

RGPD : la recherche avec des participants ne peut pas commencer avant G3.

Technique : le code C3 manque. Il faut le récupérer en décembre 2026.

## 7. Critères d'acceptation (janvier 2027)

- [ ] Partie publique en ligne, sans aucun fichier réservé (vérifié par `git ls-files`)
- [ ] Code C3 récupéré, ou son absence signalée sur la page
- [ ] Décision sur le préenregistrement OSF

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Où trouver deux juristes relecteurs, dont un praticien belge des conflits d'intérêts ?
2. Préenregistrer sur OSF avant ou après G0 ?

## 10. Prochaine étape

Décembre 2026 : demander le kit v0.2 complet, avec le code C3.
