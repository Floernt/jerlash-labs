---
id: P03
titre: Séparer conditions particulières et conditions générales
type: outil public
statut: vérification
priorité: à définir
source: zenzen-sol/legal-prompts, skill order-form-restructure (v0.1.0)
licence_source: MIT
dépend_de: [P10]
mise_a_jour: 2026-11-01
---

# Séparer conditions particulières et conditions générales

## 1. Origine

La skill order-form-restructure transforme un contrat négocié en deux documents : un bon de commande qui regroupe tout ce qui est propre à l'opération, et des conditions générales réutilisables sans modification pour une autre opération. L'effet juridique doit rester identique ; tout changement que la restructuration semble imposer est signalé, jamais appliqué en silence. Consulté le 2026-10-31.

Sol Irvine relie cette structure à la dé-identification : quand les données propres au client sont regroupées en tête, il devient simple de les retirer avant de soumettre le reste à une IA (extrait de publication X, cité par trendshift.io, non consulté directement).

## 2. Problème ou opportunité

Les cabinets réutilisent des contrats négociés comme modèles, avec le risque d'y laisser des données de l'ancien client. Une structure conditions particulières / conditions générales réduit ce risque et facilite la pseudonymisation.

## 3. Solution envisagée

À partir d'un contrat .docx, produire des conditions particulières (parties, prix, durée, objet, contacts, dérogations) et des conditions générales, avec un rapport des points signalés.

Hors périmètre : contrat-cadre avec commandes multiples, renégociation.

## 4. Adaptation à jerlash.labs

Terminologie belge (conditions particulières, conditions générales, ordre de priorité entre documents). Rappel sur l'opposabilité des conditions générales [À VÉRIFIER : point de droit à rédiger par Florian, pas par l'outil].

## 5. Approche technique pressentie

Script local ou page navigateur avec P10 pour l'édition du résultat.

## 6. Contraintes et risques

Déontologie : l'outil ne doit pas présenter la restructuration comme juridiquement neutre sans relecture.
Technique : renvois internes à renuméroter.
Licence : MIT.

## 7. Critères d'acceptation

- [ ] Sur un contrat fictif, chaque clause se retrouve dans l'un des deux documents, une seule fois.
- [ ] Les données propres à l'opération sont toutes dans les conditions particulières.
- [ ] Les changements nécessaires sont listés dans le rapport, pas appliqués.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Faut-il produire en plus un modèle anonymisé prêt à réutiliser ?

## 10. Prochaine étape

P03 Lite 0.1.0 (rapport de préparation, par règles, ADR-017) est livré dans `outils/conditions-particulieres`, mesuré sur F-CPCG-01. Prochaines étapes : test par Florian sur un contrat négocié réel ; la production des deux documents attend P10.
