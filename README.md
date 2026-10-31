# iavocat.be

Dépôt du site iavocat.be : outils pour avocats construits avec l'IA, utilisables en local avec la clé API de l'utilisateur, et guides techniques pour s'en servir correctement.

Auteur et éditeur : Florian Ernotte.

## Pour commencer

1. Lire `CLAUDE.md` (contexte et règles de travail).
2. Lire `docs/cahier-des-charges.md`.
3. Trancher les décisions ouvertes dans `docs/decisions.md`.
4. Suivre `BACKLOG.md`.

## Statut

Phase 2 (lancement) en préparation, 2026-10-31.

- Premier outil : `outils/controle-avant-envoi` (P05 Lite 0.1.0), testé sur le jeu F-DOCX-01.
- Site Hugo complet dans `site/` ; publication bloquée tant que les marqueurs `[À COMPLÉTER]` / `[À VÉRIFIER]` ne sont pas levés (`python scripts/verifier.py --publication`).
- Reste à faire par Florian : voir `LOG.md`, dernière entrée.
