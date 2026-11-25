---
id: P12
titre: Banc d'essai des outils sur cas fictifs
type: outillage factory (publiable ensuite)
statut: idée
priorité: haute (A04)
source: idée inspirée de LQ Assess (LegalQuants), connu uniquement par un extrait LinkedIn ; méthode enrichie d'après la méthodologie publiée de Legal Benchmarks (consultée le 2026-11-12)
licence_source: sans objet (aucun code repris)
dépend_de: []
mise_a_jour: 2026-11-12
---

# Banc d'essai des outils sur cas fictifs

## 1. Origine

Sur LinkedIn, Sol Irvine indique qu'avec Raymond Sun, au sein de LegalQuants, il a construit LQ Assess, une séance de travail bâtie autour de 127 problèmes d'IA juridique. Il y écrit aussi qu'une démonstration de "dialogue avec des documents" ne représente qu'une petite part de ce qu'une application juridique doit faire en production. Le contenu de LQ Assess n'a pas été consulté.

Legal Benchmarks publie la méthode de ses classements de modèles et d'applications d'IA juridique. Pages lues le 2026-11-12 :

- <https://www.legalbenchmarks.ai/methodology>
- <https://www.legalbenchmarks.ai/methodology/models>
- <https://www.legalbenchmarks.ai/methodology/applications>
- <https://www.legalbenchmarks.ai/research/evaluation-framework>

La page du cadre d'évaluation annonce des critères et un processus par étapes, mais n'en donne pas le contenu ; son lien de téléchargement renvoie vers une page qui renvoie elle-même au cadre. Seule la méthodologie a donc été exploitée. Les éléments repris sont repérés « (LB) » ci-dessous. Leurs limites déclarées laissent un espace : tâches en anglais seulement, droit surtout américain et britannique, aucune référence humaine.

## 2. Problème ou opportunité

Sans cas de test fixes, impossible de savoir si une nouvelle version d'un outil ou un nouveau modèle fait mieux ou moins bien.

Les jeux actuels (F-DEF-01, F-IDENT-01, F-DOSSIER-01) mesurent bien les outils qui détectent des éléments à partir de règles : rappel et précision par catégorie, contre des annotations. Cette mesure ne convient pas aux outils qui produisent du texte (P04, P06, P08, mode IA de P01). Il manque une méthode pour eux.

## 3. Solution envisagée

Un ensemble de dossiers fictifs belges (contrats, pièces, courriels) avec, pour chaque outil, les résultats attendus. La Factory exécute ce banc avant toute publication. Une version publique pourrait suivre.

Deux modes de mesure selon l'outil :

1. Outils à règles : comparaison exacte avec les annotations, rappel et précision par catégorie (pratique actuelle, inchangée).
2. Outils génératifs : critères binaires par tâche (voir section 5).

Hors périmètre : classement de modèles du marché, certification d'outils de tiers.

## 4. Adaptation à jerlash.labs

Données entièrement inventées, droit belge, français.

Pratiques déjà en place, à conserver : jeu de développement et jeu de contrôle rédigé par un agent sans accès au code, écarts du contrôle non affichés, pièges qui ne sont pas des défauts, documents dans leur format réel (.docx avec commentaires et modifications suivies), plusieurs exécutions pour les outils qui appellent une IA avec publication du plus mauvais résultat (P01).

## 5. Approche technique pressentie

Dossier `factory/jeux-de-test/`, un sous-dossier par jeu, fichier `attendu/<ID>` par outil. Agent `testeur`.

Pour les outils génératifs :

1. Critères par tâche (LB). Chaque tâche reçoit une liste fixe de critères réussi/échoué, rédigés par un avocat : ce que la réponse doit contenir et ce qu'elle doit éviter. Un critère admet toute approche professionnellement défendable ; il ne récompense pas un style de rédaction.
2. Deux scores (LB). Taux de critères réussis, et taux de tâches réussies : une tâche ne réussit que si tous ses critères réussissent. Le second est le score principal. Une bonne performance sur certains critères ne compense pas une omission ou une erreur importante ailleurs.
3. Répétition (LB, rejoint P01). Un critère n'est réussi que s'il l'est dans toutes les exécutions. Nombre d'exécutions : trois, comme P01.
4. Fond et forme séparés (LB). La forme est notée à part, sur une échelle de 1 à 3 : 1, à retravailler avant usage ; 2, utilisable avec retouches ; 3, utilisable tel quel. Elle n'entre pas dans le score de fond.
5. Seule la production finale est notée (LB) : la réponse et les fichiers produits, pas le raisonnement.
6. Conditions figées et consignées dans chaque compte rendu (LB) : modèle, date, réglage de raisonnement, instruction identique d'une exécution à l'autre, aucune mémoire entre exécutions, durée et nombre d'appels maximum, coût. Une exécution qui n'aboutit pas compte comme un échec.

Si un juge IA est utilisé pour appliquer les critères (LB) :

- un appel par critère ;
- le juge du fond et celui de la forme ne voient pas les conclusions l'un de l'autre ;
- le juge est réglé contre des verdicts d'avocat sur un échantillon de critères, mesuré en exactitude équilibrée (moyenne du taux de réussites et du taux d'échecs correctement reconnus), réglage sur des tâches de développement, contrôle sur des tâches réservées ;
- tout verdict incertain qui changerait le résultat d'une tâche est tranché par l'avocat, sans savoir quelle version ou quel modèle a produit la réponse ; la décision humaine prévaut et reste consignée ;
- juge d'une autre famille de modèles que celui de l'outil, pour éviter qu'un modèle favorise les réponses de son fournisseur. Les jeux étant fictifs, cet envoi ne pose pas de question de secret professionnel.

Le juge IA ne sert pas pour les outils à règles.

Comptes rendus (LB) : chaque fichier de `resultats/` indique s'il est comparable au précédent et, sinon, pourquoi (changement de jeu, de critères, de conditions d'exécution). Il se termine par une section « Limites ».

## 6. Contraintes et risques

Aucune donnée réelle, même pseudonymisée.

Un jeu de contrôle dont les critères sont publiés devient un jeu de développement. Méthode publique, critères et résultats attendus du contrôle confidentiels (LB) ; ceux-ci restent hors du site.

Un juge IA non réglé contre des verdicts d'avocat ne permet pas d'afficher un outil comme « évalué ».

Le score de fond binaire est sévère par construction : il faut l'expliquer à côté du chiffre, faute de quoi un taux de tâches réussies bas sera mal lu.

## 7. Critères d'acceptation

- [ ] Un jeu de test par outil en cours.
- [ ] Résultats consignés à chaque version.
- [ ] Pour chaque outil génératif : critères binaires par tâche, rédigés et relus par un avocat.
- [ ] Gabarit de compte rendu avec conditions d'exécution, comparabilité et limites.
- [ ] Si juge IA : mesure d'accord avec les verdicts d'avocat consignée avant tout usage.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Ouvrir le banc à d'autres avocats pour contribution ?
2. Qui fixe ce qu'est une réponse « professionnellement défendable » pour un outil génératif : Florian seul, ou un groupe d'avocats ? La réponse décide si le banc reste interne ou devient publiable.
3. Faut-il une référence humaine (le même jeu traité par un avocat), que Legal Benchmarks ne fournit pas ?
4. Faut-il un standard `factory/standards/evaluation.md` reprenant la section 5 pour toute la Factory ?

## 10. Prochaine étape

Rédiger les critères binaires d'une première tâche générative (P04 ou mode IA de P01) sur F-DOSSIER-01, pour éprouver la méthode avant d'en faire un standard.
