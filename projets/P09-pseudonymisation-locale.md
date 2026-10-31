---
id: P09
titre: Pseudonymisation locale avant envoi à une IA
type: outil public et composant
statut: vérification (P09 Lite 0.1.0)
priorité: haute (conditionne plusieurs outils)
source: stella/anonymize (bibliothèque tierce, repérée via le fork stella de Sol Irvine)
licence_source: Apache-2.0
dépend_de: []
mise_a_jour: 2026-10-31
---

# Pseudonymisation locale avant envoi à une IA

## 1. Origine

stella anonymize est une boîte à outils de détection et de remplacement de données personnelles, conçue pour fonctionner en local, avec un cœur en Rust et des liaisons pour Node.js, Python et le navigateur. Le traitement par défaut est déterministe et n'appelle aucun modèle ni service distant. La documentation précise elle-même qu'aucun détecteur ne trouve tout, que la couverture varie selon la langue, et que le remplacement réversible est une pseudonymisation dont la table de correspondance contient les données d'origine. Consulté le 2026-10-31.

## 2. Problème ou opportunité

C'est la première précaution que les avocats demandent avant d'envoyer une pièce à une IA.

## 3. Solution envisagée

Page navigateur hors ligne : coller ou charger un texte, voir les entités détectées, corriger à la main, exporter le texte pseudonymisé ; table de correspondance gardée en local pour rétablir les noms dans la réponse de l'IA.

Hors périmètre : garantie d'anonymisation au sens du RGPD.

## 4. Adaptation à iavocat.be

Couverture du français et des identifiants belges (numéro de registre national, numéro d'entreprise, IBAN BE) [À VÉRIFIER dans la bibliothèque ; à compléter par des règles propres si absent].

## 5. Approche technique pressentie

Liaison navigateur de la bibliothèque, aucun appel réseau. Composant réutilisé par P01, P08 et d'autres.

## 6. Contraintes et risques

Le risque principal est la fausse sécurité. L'interface doit obliger à relire et dire clairement qu'il s'agit de pseudonymisation.
Licence : Apache-2.0, fichier NOTICE et mentions à reprendre.

## 7. Critères d'acceptation

- [x] Aucun appel réseau (application locale : test statique des imports et parcours exécuté réseau neutralisé).
- [x] Taux de détection mesuré sur un jeu de test fictif belge, publié sur la fiche.
- [x] Avertissement sur les limites visible avant export.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Faut-il un mode avec modèle local pour améliorer la détection ?

## 10. Prochaine étape

P09 Lite 0.1.0 livré le 2026-10-31 (outils/pseudonymisation, ADR-014) : règles sans dépendance, mesure publiée sur F-IDENT-01. Ensuite : test de la fenêtre par Florian ; qualification de stella anonymize et d'un modèle local sur F-IDENT-01 avec un nouveau jeu de contrôle.
