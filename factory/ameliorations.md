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
