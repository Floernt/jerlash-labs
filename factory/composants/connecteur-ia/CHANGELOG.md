# Changelog - connecteur-ia

## 0.1.0 - 2026-11-01

- Première version (ADR-019, ADR-020) : configuration avec préréglages (OpenAI, Anthropic, Mistral, API Gemini, modèle local), lecture de la clé (environnement ou `.env`), estimation du coût, écran d'envoi avec texte modifiable et case à cocher, appel au format Chat Completions, extraction du JSON.
- 18 tests contre un faux fournisseur local ; écran d'envoi vérifié par un essai automatique (annulation, envoi après correction du texte).
