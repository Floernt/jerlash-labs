# Catalogue des composants

Briques communes à plusieurs outils. Un composant naît quand deux outils ont le même besoin. `ops-factory` repère ces doublons et propose la création d'un composant dans `ameliorations.md`.

| Composant | Rôle | Statut | Fiche |
|---|---|---|---|
| cle-api | saisie, conservation en mémoire, option de mémorisation avec avertissement | à concevoir | |
| fournisseurs | appel uniforme aux API (Anthropic, OpenAI, modèle local), modèles en configuration | à concevoir | |
| cout | estimation du coût avant lancement, tarifs datés | à concevoir | |
| docx | lecture, modifications suivies, export | évaluation | P10 |
| conversion | pièces vers texte structuré avec pages | évaluation | P11 |
| pseudonymisation | détection et remplacement local | évaluation | P09 |
| rapport | gabarit commun des rapports produits par les outils | à concevoir | |

Chaque composant a son dossier `factory/composants/<nom>/` avec README, CHANGELOG et tests dès sa création.
