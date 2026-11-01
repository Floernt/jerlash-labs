# Catalogue des composants

Briques communes à plusieurs outils. Un composant naît quand deux outils ont le même besoin. `ops-factory` repère ces doublons et propose la création d'un composant dans `ameliorations.md`.

| Composant | Rôle | Statut | Fiche |
|---|---|---|---|
| connecteur-ia | appel unique au format Chat Completions (OpenAI, Anthropic, Mistral, API Gemini, modèle local), configuration, écran d'envoi, coût | 0.1.0, à brancher (ADR-020) | connecteur-ia/README.md |
| docx | lecture, modifications suivies, export | évaluation | P10 |
| conversion | pièces vers texte structuré avec pages | évaluation | P11 |
| pseudonymisation | détection et remplacement local | évaluation | P09 |
| rapport | gabarit commun des rapports produits par les outils | à concevoir | |

Chaque composant a son dossier `factory/composants/<nom>/` avec README, CHANGELOG et tests dès sa création.
