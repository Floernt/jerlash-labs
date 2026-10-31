---
id: P08
titre: Revue tabulaire de documents
type: outil public
statut: idée
priorité: à définir
source: stella (fonction Tabular Review), et skill tabular-review déjà installée chez Florian
licence_source: Apache-2.0 (stella)
dépend_de: [P11]
mise_a_jour: 2026-10-31
---

# Revue tabulaire de documents

## 1. Origine

stella, espace de travail juridique open source que Sol Irvine a forké, propose une "revue tabulaire" : extraire des réponses structurées d'un ensemble de documents vers un tableau propre à un dossier (audit, communication de pièces, recherche). Consulté le 2026-10-31 (README).

Florian dispose déjà d'une skill de revue tabulaire (tabular-review-lawvable) qui produit un Excel avec citations.

## 2. Problème ou opportunité

Comparer une même clause dans vingt contrats, ou relever des dates et montants dans un lot de pièces.

## 3. Solution envisagée

Outil local : l'avocat définit ses colonnes (questions), désigne un dossier, obtient un tableau .xlsx avec pour chaque cellule la réponse et la référence précise dans la pièce.

Hors périmètre : base de données de dossiers, interface collaborative.

## 4. Adaptation à iavocat.be

Partir de la skill existante plutôt que de stella, beaucoup plus lourd. Ajouter le contrôle de coût et la pseudonymisation optionnelle.

## 5. Approche technique pressentie

Script local, traitement document par document, reprise possible après interruption, citations vérifiables.

## 6. Contraintes et risques

Technique : fiabilité des citations ; une réponse sans citation doit être marquée comme telle.
Licence : vérifier la licence de la skill tabular-review-lawvable avant publication [À VÉRIFIER].

## 7. Critères d'acceptation

- [ ] Chaque cellule renseignée porte une référence vérifiable.
- [ ] Coût affiché avant lancement.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Publier un outil ou un guide d'utilisation de la skill existante ?

## 10. Prochaine étape

Décider entre outil et guide.
