---
id: F03
titre: Mémoire persistante de la Factory
type: outillage factory
statut: idée
priorité: haute
source: zenzen-sol/skillboxing
licence_source: MIT
dépend_de: []
mise_a_jour: 2026-10-31
---

# Mémoire persistante de la Factory

## 1. Origine

Voir P07 pour la description de skillboxing.

## 3. Solution envisagée

La Factory a besoin de se souvenir, d'une session à l'autre, des décisions, des erreurs rencontrées et des solutions trouvées. Une skill interne `memoire-projet` (dans `.claude/skills/`) reprend le principe : capter en fin de session, auditer périodiquement. L'agent `ops-factory` en est responsable.

Alternative : installer skillboxing tel quel (ADR-009).

## 6. Contraintes et risques

La mémoire de la Factory ne contient jamais de donnée de dossier.
Licence : MIT. La skill interne est rédigée indépendamment ; citer skillboxing comme inspiration.

## 7. Critères d'acceptation

- [ ] Après dix sessions, la mémoire tient en moins de 20 fichiers courts et à jour.

## 10. Prochaine étape

Utiliser la skill interne pendant un mois puis décider (ADR-009).
