---
id: P05
titre: Contrôle avant envoi
type: outil public
statut: idée
priorité: haute (premier outil, ADR-011)
source: zenzen-sol/legal-prompts, skill send-ready-pass (v0.2.0)
licence_source: MIT
dépend_de: [P04, P10]   # version complète
dépend_de_mvp: []       # P05 Lite, à confirmer par prototype du lecteur .docx [À VÉRIFIER]
mise_a_jour: 2026-10-31
---

# Contrôle avant envoi

## 1. Origine

La skill send-ready-pass prend la copie de travail terminée et produit les copies à envoyer : une comparaison avec le dernier projet échangé et une version propre, commentaires renommés, notes internes retirées, en-tête et pagination réglés, avec un rapport de contrôle qualité qui liste chaque problème à corriger ou à accepter en connaissance de cause. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Envoyer à la partie adverse un document qui contient encore des commentaires internes, des métadonnées d'auteur ou des traces d'un autre dossier est un incident fréquent et sérieux.

## 3. Solution envisagée

Contrôle déterministe d'abord (commentaires, modifications non résolues, métadonnées, champs, noms de fichiers d'autres dossiers), contrôle par le modèle ensuite (incohérences de numérotation, renvois cassés, termes définis non utilisés), puis production des copies et du rapport.

Hors périmètre : envoi du courriel.

## 3 bis. Découpage (ADR-011, PLAN_AMELIORATIONS.md A06)

P05 Lite (MVP) : lecture et contrôle non destructifs d'un .docx, sans IA ni clé API, avec un rapport local et des recommandations. Le fichier d'entrée n'est jamais modifié. Chaque contrôle renvoie "détecté", "non détecté dans les contrôles réalisés", "non vérifié" ou "erreur" ; un échec de lecture ne produit jamais de feu vert.

P05 avancé : production de copies, contrôle assisté par un modèle, fonctions dépendant de P04 et P10.

## 4. Adaptation à iavocat.be

Liste de contrôle propre aux usages du cabinet [À COMPLÉTER par Florian].

## 5. Approche technique pressentie

Une grande partie du contrôle ne demande aucune IA : prévoir un mode "sans IA" utilisable sans clé.

## 6. Contraintes et risques

Déontologie : secret professionnel (métadonnées révélant d'autres clients).
Licence : MIT.

## 7. Critères d'acceptation

- [ ] Détecte 100 % des commentaires et métadonnées du jeu de test.
- [ ] Mode sans IA fonctionnel.
- [ ] Rapport lisible en moins d'une minute.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Quelles erreurs sont réellement arrivées au cabinet ? Elles constituent la meilleure liste de contrôle.

## 10. Prochaine étape

Lister les contrôles déterministes et les tester sur un .docx fictif chargé de pièges.
