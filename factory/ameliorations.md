# Améliorations de la Factory

Alimenté par `ops-factory` (et par tout agent qui rencontre un problème récurrent). Florian valide ou refuse. Une amélioration acceptée est appliquée dans le standard, le composant, l'agent ou la commande concernés, puis marquée "appliquée".

Format :

```
## AM-xxx - Titre
Date :
Constat : (faits observés, avec renvoi au projet ou au rapport)
Proposition :
Fichiers touchés :
Statut : proposée | acceptée | refusée | appliquée
```

---

## AM-001 - Charger la mémoire de la Factory au démarrage
Date : 2026-10-31
Constat : sans chargement automatique, la mémoire dépend de la discipline de chaque session.
Proposition : ajouter dans `.claude/settings.json` un hook de démarrage de session qui affiche `factory/memoire/index.md`, sur le modèle des hooks de skillboxing. Syntaxe à vérifier dans la documentation à jour de Claude Code avant écriture.
Fichiers touchés : .claude/settings.json
Statut : proposée

## AM-002 - Détection automatique de secrets avant commit
Date : 2026-10-31
Constat : la règle "aucun secret dans le dépôt" n'est vérifiée que par relecture.
Proposition : choisir un outil de détection de secrets en pré-commit.
Fichiers touchés : configuration git, standards/code.md
Statut : proposée

## AM-003 - Le circuit ignore la version de travail publique
Date : 2026-11-11
Constat : les dix pages de P14 sont en ligne depuis le 2026-11-06 alors que les étapes 4 et 5 du circuit n'ont pas été franchies (`outils/gouvernance-ia/verifications/` n'existe pas, aucune entrée dans `site/content/nouveautes/`). Ce n'est pas un contournement : ADR-025 pose « livrer plutôt que construire » et la publication en version de travail publique. Le circuit, lui, ne connaît qu'un statut « publié » qui suppose les quatre rapports et la validation de Florian. Tant que les deux textes disent des choses différentes, tout projet de contenu sera compté en passage d'étape raté (`metriques.md`, relevé du 2026-11-11).
Proposition : ajouter au circuit un statut « version de travail publique », entre prototype et publié, dont les critères de sortie seraient le bloc de statut sur la page, la date d'arrêt du droit et `python scripts/verifier.py --publication` au vert ; réserver « publié » à ce que décrit l'étape 5. À défaut, inscrire que le parcours léger s'arrête à l'étape 3 pour un projet de contenu.
Fichiers touchés : factory/pipeline.md, factory/registre.md
Statut : proposée
