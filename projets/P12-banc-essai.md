---
id: P12
titre: Banc d'essai des outils sur cas fictifs
type: outillage factory (publiable ensuite)
statut: idée
priorité: moyenne
source: idée inspirée de LQ Assess (LegalQuants), connu uniquement par un extrait LinkedIn
licence_source: sans objet (aucun code repris)
dépend_de: []
mise_a_jour: 2026-10-31
---

# Banc d'essai des outils sur cas fictifs

## 1. Origine

Sur LinkedIn, Sol Irvine indique qu'avec Raymond Sun, au sein de LegalQuants, il a construit LQ Assess, une séance de travail bâtie autour de 127 problèmes d'IA juridique. Il y écrit aussi qu'une démonstration de "dialogue avec des documents" ne représente qu'une petite part de ce qu'une application juridique doit faire en production. Le contenu de LQ Assess n'a pas été consulté.

## 2. Problème ou opportunité

Sans cas de test fixes, impossible de savoir si une nouvelle version d'un outil ou un nouveau modèle fait mieux ou moins bien.

## 3. Solution envisagée

Un ensemble de dossiers fictifs belges (contrats, pièces, courriels) avec, pour chaque outil, les résultats attendus. La Factory exécute ce banc avant toute publication. Une version publique pourrait suivre.

Hors périmètre : classement de modèles du marché.

## 4. Adaptation à iavocat.be

Données entièrement inventées, droit belge, français.

## 5. Approche technique pressentie

Dossier `factory/jeux-de-test/`, un sous-dossier par jeu, fichier `attendu.md` par outil. Agent `testeur`.

## 6. Contraintes et risques

Aucune donnée réelle, même pseudonymisée.

## 7. Critères d'acceptation

- [ ] Un jeu de test par outil en cours.
- [ ] Résultats consignés à chaque version.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Ouvrir le banc à d'autres avocats pour contribution ?

## 10. Prochaine étape

Créer F-DOSSIER-01 (voir P01).
