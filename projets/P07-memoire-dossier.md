---
id: P07
titre: Mémoire de dossier pour Claude
type: outil public
statut: idée
priorité: à définir
source: zenzen-sol/skillboxing
licence_source: MIT
dépend_de: []
mise_a_jour: 2026-10-31
---

# Mémoire de dossier pour Claude

## 1. Origine

Skillboxing est un plugin pour Claude et Codex qui maintient un dossier `brain/` de courts fichiers Markdown (décisions, faits clés, questions ouvertes, préférences). Un hook charge l'index au début de chaque session ; une commande "reflect" enregistre ce qui mérite d'être retenu à la fin d'une session ; une commande "meditate" audite le contenu et propose des nettoyages soumis à validation. Le dossier se lit aussi dans Obsidian. L'exemple donné pour un dossier contractuel : termes clés, positions des parties, points ouverts, historique des concessions. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Chaque nouvelle session d'IA sur un dossier repart de zéro. L'avocat réexplique le contexte.

## 3. Solution envisagée

Un guide et un paquet prêt à l'emploi pour utiliser une mémoire de dossier dans Claude Code ou Cowork, adapté au travail d'avocat : structure type de `brain/` pour un dossier contractuel et pour un dossier contentieux, règles de ce qui peut y figurer.

Hors périmètre : synchronisation dans le cloud.

## 4. Adaptation à jerlash.labs

La mémoire contient des informations couvertes par le secret professionnel. Le guide doit traiter : emplacement local, exclusion de tout dossier synchronisé non maîtrisé, pseudonymisation des noms dans la mémoire, durée de conservation, suppression en fin de dossier.

## 5. Approche technique pressentie

Deux voies à comparer : recommander l'installation du plugin d'origine avec une configuration type, ou publier une version adaptée en français (fork sous MIT). Voir ADR-009.

## 6. Contraintes et risques

Déontologie : secret professionnel, conservation.
Réglementation : RGPD (minimisation, durée).
Licence : MIT.

## 7. Critères d'acceptation

- [ ] Structure type validée par Florian sur un dossier réel (hors dépôt).
- [ ] Guide d'installation testé par une personne non technique.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Florian utilise-t-il déjà une mémoire de ce type dans Cowork ?

## 10. Prochaine étape

Tester skillboxing sur un dossier fictif dans Claude Code (voir F03, même test).
