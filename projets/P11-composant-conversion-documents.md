---
id: P11
titre: Conversion locale des pièces en texte structuré
type: composant
statut: idée
priorité: haute (conditionne P01, P06, P08)
source: forks docling-serve et docling-api ; lector (visionneuse PDF) en option
licence_source: [À VÉRIFIER pour chaque projet]
dépend_de: []
mise_a_jour: 2026-10-31
---

# Conversion locale des pièces en texte structuré

## 1. Origine

Sol Irvine a forké deux projets autour de Docling : docling-api, serveur qui convertit PDF, DOCX, PPTX, HTML et images en Markdown, sur CPU ou GPU, et docling-serve, qui expose Docling comme service. Il a aussi forké lector, des primitives pour construire une visionneuse PDF. Descriptions lues dans la liste des dépôts le 2026-10-31 ; README non consultés.

## 2. Problème ou opportunité

Un modèle de langage travaille mieux sur du texte structuré que sur un PDF brut. Les pièces d'un dossier mélangent PDF natifs, scans, .docx et courriels.

## 3. Solution envisagée

Un composant Factory, appelable par les outils locaux, qui convertit un dossier de pièces en Markdown avec repères de page, pour permettre des citations précises.

Hors périmètre : service hébergé.

## 4. Adaptation à jerlash.labs

Exécution sur le poste de l'avocat, sans GPU. Installation documentée pour Windows et macOS.

## 5. Approche technique pressentie

Utiliser Docling directement en bibliothèque Python plutôt qu'en serveur, si possible [À VÉRIFIER]. Prévoir une solution de repli légère pour les PDF natifs.

## 6. Contraintes et risques

Technique : poids de l'installation, OCR des scans, temps de traitement.
Licence : [À VÉRIFIER].

## 7. Critères d'acceptation

- [ ] Conversion d'un jeu de 20 pièces fictives sans service distant.
- [ ] Numéros de page conservés.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Accepte-t-on une installation Python pour les utilisateurs, ou faut-il viser le navigateur uniquement ?

## 10. Prochaine étape

Lire la documentation de Docling et mesurer installation et temps de conversion.
