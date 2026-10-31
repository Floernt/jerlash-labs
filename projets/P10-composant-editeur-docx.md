---
id: P10
titre: Composant d'édition .docx dans le navigateur
type: composant
statut: idée
priorité: moyenne
source: eigenpal/docx-editor (forké par Sol Irvine)
licence_source: Apache-2.0
dépend_de: []
mise_a_jour: 2026-10-31
---

# Composant d'édition .docx dans le navigateur

## 1. Origine

docx-editor est un éditeur .docx open source pour React et Vue, qui travaille côté client, avec OOXML canonique, modifications suivies et collaboration en temps réel, présenté comme prêt pour les agents. Consulté le 2026-10-31.

## 2. Problème ou opportunité

P02 à P06 lisent et produisent du .docx. Sans composant commun, chaque outil réinvente le traitement Word.

## 3. Solution envisagée

Évaluer la bibliothèque comme composant Factory : ouverture d'un .docx, affichage, application de modifications suivies, export. Si elle convient, l'intégrer dans `factory/composants/`.

Hors périmètre : collaboration en temps réel (suppose un serveur).

## 4. Adaptation à iavocat.be

Utilisation hors ligne uniquement. Vérifier l'absence d'appel réseau.

## 5. Approche technique pressentie

Prototype minimal : charger un .docx fictif, insérer une modification suivie, exporter, ouvrir dans Word.

## 6. Contraintes et risques

Technique : taille du paquet, dépendance à React ou Vue, compatibilité avec la stack retenue (ADR-002).
Licence : Apache-2.0.

## 7. Critères d'acceptation

- [ ] Fichier exporté ouvert sans erreur dans Word.
- [ ] Modifications suivies reconnues par Word.
- [ ] Aucun appel réseau.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Comparer avec le moteur de modifications suivies de wargame-oss (MIT) et avec une solution Python côté script.

## 10. Prochaine étape

Prototype d'évaluation (agent `architecte`).
