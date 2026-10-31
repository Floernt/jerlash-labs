# CLAUDE.md - iavocat.be

Ce fichier est lu par Claude Code au début de chaque session. Il donne le contexte du projet et les règles de travail. Le détail du projet se trouve dans `docs/cahier-des-charges.md`.

## Le projet en bref

iavocat.be est le site de Florian Ernotte, avocat (Avroy Avocats). Il publie deux choses :

1. Des outils pour avocats construits avec l'IA, utilisables en local, sur lesquels l'avocat branche sa propre clé API (principe BYOK, "bring your own key").
2. Des guides techniques et pratiques : comment obtenir et sécuriser une clé API, comment fonctionne la facturation, ce que devient une donnée envoyée à un fournisseur, comment installer et utiliser un outil.

Le site est fonctionnel et opérationnel. Il ne contient pas de réflexion philosophique sur le droit ou la technologie (ce contenu a sa place sur reflexions.florianernotte.be). Les mises en garde et précautions d'usage sont en revanche bienvenues et attendues.

## Documents de référence

- `docs/cahier-des-charges.md` : objectifs, périmètre, arborescence, exigences. À lire avant toute modification de structure.
- `docs/principes-outils.md` : règles que chaque outil doit respecter.
- `docs/securite-confidentialite.md` : modèle de menace, gestion des clés, secret professionnel, RGPD.
- `docs/charte-editoriale.md` : ton, style, règles d'écriture.
- `docs/decisions.md` : registre des décisions d'architecture (ADR). Les décisions au statut "Proposée" ne sont pas encore validées.
- `BACKLOG.md` : tâches à faire, par phase.
- `LOG.md` : journal des sessions de travail.
- `PLAN_AMELIORATIONS.md` : plan d'amélioration du 2026-10-31 (actions A01 à A18). Ses propositions ne s'appliquent pas automatiquement : voir sa section 12.
- `projets/` : fiches projet (index dans `projets/README.md`).
- `factory/` : organisation de la production des outils (voir ci-dessous).
- `docs/veille/` : notes de veille sur les sources d'idées.

## Règles de travail pour Claude Code

1. Ne rien inventer. Si une information manque ou peut avoir changé (nom de modèle, prix d'une API, paramètre d'API, règle déontologique, obligation légale), écrire `[À VÉRIFIER]` et le signaler dans la réponse plutôt que de deviner.
2. Avant d'écrire du code qui appelle une API d'IA, consulter la documentation officielle à jour du fournisseur. Les noms de modèles et les en-têtes changent : ils vont dans un fichier de configuration, jamais en dur dans plusieurs fichiers.
3. Aucune clé API, aucun secret, aucune donnée de client ou de dossier dans le dépôt. Les fichiers `.env` sont ignorés par git. En cas de doute sur un fichier, demander avant de le committer.
4. Aucun outil n'envoie de donnée vers un serveur contrôlé par iavocat.be. Aucun outil ne manipule de clé API avant l'approbation de son architecture (ADR-010). Les seuls flux sortants autorisés vont de la machine de l'utilisateur vers le fournisseur d'IA qu'il a choisi.
5. Pas de traceur tiers, pas de cookie non essentiel, pas de police ou de script chargé depuis un CDN sans décision consignée dans `docs/decisions.md`.
6. Toute décision d'architecture ou de structure est consignée dans `docs/decisions.md` (nouvelle entrée ADR), avec le statut "Proposée" tant que Florian ne l'a pas validée.
7. À la fin de chaque session, ajouter une entrée dans `LOG.md` (commande `/cloture-session`).
8. Un nouvel outil passe par la Factory : fiche dans `projets/`, puis `/factory-lancer <ID>`. La commande `/nouvel-outil <slug>` ne sert qu'à créer le dossier d'un outil dont la fiche est au statut "cadrage".
9. Changements limités à ce qui est demandé. Pas de refonte non sollicitée.

## Factory

La production des outils suit `factory/pipeline.md`. Les rôles sont confiés aux agents de `.claude/agents/`. L'agent `ops-factory` contrôle chaque passage d'étape, tient `factory/registre.md` et propose les améliorations de la Factory dans `factory/ameliorations.md`. Point d'entrée : `/factory`.

Règles :
- aucun passage d'étape sans contrôle par `ops-factory` ;
- les passages vers "prêt" et "publié" demandent la validation de Florian ;
- une amélioration de la Factory n'est appliquée qu'après acceptation par Florian ;
- en fin de session, appliquer la skill `memoire-projet`.

## Structure du dépôt (cible)

```
/
  CLAUDE.md                 ce fichier
  README.md                 présentation du dépôt
  LOG.md                    journal des sessions
  BACKLOG.md                tâches par phase
  docs/                     cahier des charges et documents de référence
  templates/                gabarits (fiche projet, fiche outil, guide)
  projets/                  fiches projet
  factory/                  pipeline, registre, standards, composants, jeux de test, mémoire
  contenus/                 textes sources à intégrer au site (rubriques éditoriales, ADR-012)
  site/                     code source du site iavocat.be
  outils/<slug>/            un dossier autonome par outil
  .claude/agents/           agents de la Factory
  .claude/commands/         commandes personnalisées Claude Code
  .claude/skills/           skills du projet
```

## Stack technique

À décider (voir `docs/decisions.md`, ADR-002 et ADR-003). Tant que ce n'est pas tranché, ne pas initialiser de framework.

Commandes (à compléter une fois la stack choisie) :

- installer : `[À COMPLÉTER]`
- lancer en local : `[À COMPLÉTER]`
- construire : `[À COMPLÉTER]`
- déployer : `[À COMPLÉTER]`

## Langue et style

Français de Belgique. Tous les textes publiés suivent `docs/charte-editoriale.md`. En résumé : phrases simples et précises, pas de formules creuses, pas de dramatisation, pas de tics d'écriture d'IA (liste dans la charte), pas de titres en gras suivis de deux-points dans les listes, guillemets droits dans le code.
