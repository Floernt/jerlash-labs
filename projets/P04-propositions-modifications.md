---
id: P04
titre: Propositions de modifications sur copie séparée
type: outil public
statut: idée
priorité: à définir
source: zenzen-sol/legal-prompts, skill working-copy-redlines (v0.1.0)
licence_source: MIT
dépend_de: [P10]
mise_a_jour: 2026-10-31
---

# Propositions de modifications sur copie séparée

## 1. Origine

Dans la skill working-copy-redlines, l'avocat garde une copie de travail qu'il est seul à modifier. À chaque tour, l'agent produit un fichier séparé : la dernière copie de travail, modifications acceptées, sur laquelle il propose ses changements en suivi des modifications avec leur justification en commentaire. L'avocat reporte à la main ce qu'il retient. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Laisser une IA écrire directement dans le document de travail fait perdre la maîtrise des versions. Copier-coller depuis un chat fait perdre la trace des changements.

## 3. Solution envisagée

L'avocat fournit sa copie de travail et une consigne. L'outil produit un .docx avec modifications suivies et commentaires, dans un sous-dossier dédié, et un résumé des choix opérés.

Hors périmètre : intégration automatique dans la copie de travail.

## 4. Adaptation à iavocat.be

Commentaires en français, auteur des modifications identifiable (par exemple "Proposition IA"), compatibilité avec Word tel qu'utilisé au cabinet.

## 5. Approche technique pressentie

Génération de vraies modifications suivies (OOXML). Évaluer P10 côté navigateur ou une bibliothèque Python côté script. wargame-oss contient un moteur de modifications suivies (packages/docx-redlines) sous MIT, à étudier.

## 6. Contraintes et risques

Technique : la fidélité des modifications suivies dans Word est le point dur.
Licence : MIT pour la skill et pour wargame-oss.

## 7. Critères d'acceptation

- [ ] Le fichier produit s'ouvre dans Word avec des modifications acceptables ou refusables une à une.
- [ ] La copie de travail n'est jamais modifiée.
- [ ] Chaque modification porte un commentaire justificatif.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Version de Word et usage éventuel de LibreOffice au cabinet ?

## 10. Prochaine étape

Prototype technique : produire une modification suivie valide dans un .docx fictif.
