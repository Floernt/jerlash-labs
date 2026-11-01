# jerlash.labs

Dépôt du site jerlash.labs : articles sur l'intelligence artificielle dans la pratique d'un cabinet d'avocats et, ensuite, les outils construits avec l'IA, avec leur code, leurs coûts et leurs limites (ADR-022).

Publié : le site Hugo de `site/` (accueil, blog, à propos, mentions légales, confidentialité). Les outils (`outils/`) et les autres rubriques restent en brouillon ; voir `BACKLOG.md` et `CHANGELOG.md`.

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
