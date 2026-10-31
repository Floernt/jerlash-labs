---
id: F01
titre: Méthode d'ingénierie de la Factory (inspirée de pstack)
type: outillage factory
statut: idée
priorité: haute
source: zenzen-sol/open-pstack (adaptation pour Claude Code du pstack de Lauren Tan)
licence_source: MIT
dépend_de: []
mise_a_jour: 2026-10-31
---

# Méthode d'ingénierie de la Factory

## 1. Origine

pstack est un plugin pour agents de développement : règles d'ingénierie, procédures par type de travail, skills ciblées et petits outils locaux. Il comprend le système existant avant de le changer, compare les conceptions quand le choix compte, préfère les changements petits et simples, fait contester les décisions importantes par plusieurs modèles, et vérifie le comportement réel au lieu de s'arrêter à des tests verts. Il recommande de commencer par du travail supervisé et de n'accorder plus d'autonomie qu'une fois que les vérifications l'ont justifié. open-pstack est la version maintenue par Sol Irvine pour Claude Code et Codex. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Sans méthode commune, chaque outil produit par un agent suit des conventions différentes et les vérifications sont inégales.

## 3. Solution envisagée

Deux options, à trancher (ADR-009) : installer open-pstack dans le dépôt, ou reprendre ses principes dans `factory/pipeline.md` et les agents de la Factory sans installer le plugin. Les principes sont déjà intégrés dans la Factory livrée.

## 6. Contraintes et risques

Le plugin évolue vite et dépend de versions précises de Claude Code ; une installation doit être figée sur une version.
Licence : MIT.

## 7. Critères d'acceptation

- [ ] Décision ADR-009 prise.
- [ ] Un premier outil produit en suivant la méthode, avec preuves de vérification.

## 10. Prochaine étape

Lire le guide de pstack et tester open-pstack sur un dépôt jetable.
