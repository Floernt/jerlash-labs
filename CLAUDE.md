# CLAUDE.md - jerlash.labs

Ce fichier est lu par Claude Code au début de chaque session. Il donne le contexte du projet et les règles de travail. Le détail du projet se trouve dans `docs/cahier-des-charges.md`.

## Le projet en bref

Depuis le 2026-11-01 (ADR-022) : le projet s'appelle jerlash.labs. Priorité : livrer plutôt que construire. Depuis le 2026-11-03 (ADR-025, proposée) : un projet livré par mois, en version de travail publique, selon le calendrier de `BACKLOG.md`, plus une piste parallèle « Outils » sans échéance ; tout le reste attend au backlog. Ce qui est livré entre dans `CHANGELOG.md`. Architecture cible du site (ADR-024, proposée) : Recherche, Outils, Revue, Éthique, plus À propos et les pages légales. Une rubrique n'est publiée qu'avec un contenu prêt ; en attendant, les pages restent en brouillon (`draft: true`).

À terme, jerlash.labs est le site de Florian Ernotte, avocat (Avroy Avocats). Il publie :

1. Outils : des outils pour avocats construits avec l'IA, utilisables en local, sur lesquels l'avocat branche sa propre clé API (principe BYOK, "bring your own key") ; des toolkits (Legal AI Governance Toolkit, P14) ; des guides techniques et pratiques (clé API, facturation, données envoyées, installation).
2. Recherche : les programmes (H1 Human Agency & AI d'abord) et leurs protocoles.
3. Revue : Perspectives (essais, y compris la réflexion sur le droit et la technique, depuis ADR-024), Research papers, Notes techniques, Recensions, selon `docs/politique-publication.md`.
4. Éthique : principes, précautions d'usage, recherche avec participants.

Rien ne s'affiche comme « évalué » sans évaluation réellement faite. Les sources des livrables P14 à P19 sont hors dépôt (`../sources-proton/2026-11-03/`) ; le référentiel restreint et les tests adverses du kit MCP (P18) n'entrent jamais dans le dépôt.

## Documents de référence

- `docs/cahier-des-charges.md` : objectifs, périmètre, arborescence, exigences. À lire avant toute modification de structure.
- `docs/principes-outils.md` : règles que chaque outil doit respecter.
- `docs/securite-confidentialite.md` : modèle de menace, gestion des clés, secret professionnel, RGPD.
- `docs/charte-editoriale.md` : ton, style, règles d'écriture.
- `docs/politique-publication.md` : collections de la Revue, statuts (brouillon, working paper, évalué), métadonnées, déclaration d'usage de l'IA (ADR-024).
- `docs/decisions.md` : registre des décisions d'architecture (ADR). Les décisions au statut "Proposée" ne sont pas encore validées.
- `BACKLOG.md` : tâches à faire, par phase.
- `LOG.md` : journal des sessions de travail.
- `PLAN_AMELIORATIONS.md` : plan d'amélioration du 2026-10-31 (actions A01 à A18). Ses propositions ne s'appliquent pas automatiquement : voir sa section 12.
- `projets/` : fiches projet (index dans `projets/README.md`).
- `factory/` : organisation de la production des outils (voir ci-dessous).
- `docs/veille/` : notes de veille sur les sources d'idées.
- `docs/deontologie-ia.md` : risques et critères déontologiques pour tout envoi vers une IA distante (support de l'ADR-015).
- `../otf/` (hors dépôt) : dépôt au fil de l'eau de Florian ; `INDEX.md` y liste les fichiers en attente (ADR-028). Tri : `/otf` ; production : `/produire <sujet ou ID>`. Aucun matériau brut dans `site/content/`.
- `bibliotheque/` : textes de référence (lignes directrices AVOCATS.BE et OVB, guide du CNB), à citer par leur fiche.

## Règles de travail pour Claude Code

1. Ne rien inventer. Si une information manque ou peut avoir changé (nom de modèle, prix d'une API, paramètre d'API, règle déontologique, obligation légale), écrire `[À VÉRIFIER]` et le signaler dans la réponse plutôt que de deviner.
2. Avant d'écrire du code qui appelle une API d'IA, consulter la documentation officielle à jour du fournisseur. Les noms de modèles et les en-têtes changent : ils vont dans un fichier de configuration, jamais en dur dans plusieurs fichiers.
3. Aucune clé API, aucun secret, aucune donnée de client ou de dossier dans le dépôt. Les fichiers `.env` sont ignorés par git. En cas de doute sur un fichier, demander avant de le committer.
4. Aucun outil n'envoie de donnée vers un serveur contrôlé par jerlash.labs. Chaque outil intègre une connexion à une API d'IA en BYOK (ADR-019), par le composant commun `factory/composants/connecteur-ia` (ADR-020), jamais par un appel écrit dans l'outil. Les seuls flux sortants autorisés vont de la machine de l'utilisateur vers le fournisseur d'IA qu'il a choisi.
5. Pas de traceur tiers, pas de cookie non essentiel, pas de police ou de script chargé depuis un CDN sans décision consignée dans `docs/decisions.md`.
6. Toute décision d'architecture ou de structure est consignée dans `docs/decisions.md` (nouvelle entrée ADR), avec le statut "Proposée" tant que Florian ne l'a pas validée.
7. À la fin de chaque session, ajouter une entrée dans `LOG.md` (commande `/cloture-session`).
8. Un nouvel outil passe par la Factory : fiche dans `projets/`, puis `/factory-lancer <ID>`. La commande `/nouvel-outil <slug>` ne sert qu'à créer le dossier d'un outil dont la fiche est au statut "cadrage".
9. Changements limités à ce qui est demandé. Pas de refonte non sollicitée.
10. Chaque outil est autonome (ADR-021) : il ne dépend que de son propre dossier. Les composants communs y sont copiés par `python scripts/synchroniser_composants.py` et ne se modifient jamais dans l'outil.

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
  CHANGELOG.md              ce qui est livré, par date
  docs/                     cahier des charges et documents de référence
  bibliotheque/             textes de référence : catalogue et fiches versionnés, originaux non versionnés (ADR-018)
  templates/                gabarits (fiche projet, fiche outil, guide)
  projets/                  fiches projet (P14 à P19 : livrables Proton, sources hors dépôt dans ../sources-proton/)
  factory/                  pipeline, registre, standards, composants, jeux de test, mémoire
  contenus/                 textes sources à intégrer au site (rubriques éditoriales, ADR-012)
  site/                     code source du site jerlash.labs (Hugo)
  outils/<slug>/            un dossier autonome par outil
  scripts/                  vérification, empaquetage, détection de secrets
  .github/workflows/        CI (verifier.yml) et publication GitHub Pages (publier.yml)
  .githooks/                hook pre-commit (secrets)
  .claude/agents/           agents de la Factory
  .claude/commands/         commandes personnalisées Claude Code
  .claude/skills/           skills du projet
```

## Stack technique

- Site : Hugo extended 0.148.2, sans thème ni npm (ADR-002), hébergé sur GitHub Pages, domaine chez OVH (ADR-003). Pas de JavaScript ; CSP en balise meta.
- Outils : applications locales Python 3.10+, bibliothèque standard seule tant que possible (ADR-010). Tests `unittest`.

Commandes (depuis la racine du dépôt) :

- vérifier tout (secrets, tests, archive, site, liens) : `python scripts/verifier.py` ; avant publication : `--publication`
- prévisualiser le site : `hugo server --source site`
- blog : les articles sont dans `site/content/blog/` et se relisent et se corrigent là, nulle part ailleurs
- tests d'un outil : `cd outils/<slug> && python -m unittest discover -s tests -v` (outils : controle-avant-envoi, pseudonymisation, inventaire-dossier)
- mesurer la pseudonymisation sur F-IDENT-01 : `python factory/jeux-de-test/F-IDENT-01/evaluer.py` (ne jamais régler une règle d'après le jeu de contrôle)
- copier les composants communs dans les outils qui les déclarent (`COMPOSANTS.md`) : `python scripts/synchroniser_composants.py`
- archive d'un outil et mise à jour de sa fiche (version, taille, SHA-256) : `python scripts/empaqueter.py --fiche`
- régénérer un jeu de test : `python -I factory/jeux-de-test/<jeu>/generer.py` (F-DOCX-01, F-IDENT-01, F-DOSSIER-01) ; mesurer l'inventaire : `python factory/jeux-de-test/F-DOSSIER-01/evaluer.py`
- activer le contrôle des secrets avant commit (une fois par clone) : `git config core.hooksPath .githooks`
- traductions anglaises (ADR-023) : état `python scripts/traductions.py`, changements du français depuis la dernière traduction `--diff <fichier>`, mise à jour par la commande `/traduire` ; on corrige le français, jamais l'anglais (`x.en.md`)
- déployer : push sur `main` ; le workflow `.github/workflows/publier.yml` vérifie, construit et publie (bloqué tant qu'il reste des marqueurs `[À ...]` dans le contenu publié).

## Langue et style

Français de Belgique, version maître du site ; la version anglaise en est la traduction (ADR-023, `docs/glossaire-traduction.md`). Tous les textes publiés suivent `docs/charte-editoriale.md`. En résumé : phrases simples et précises, pas de formules creuses, pas de dramatisation, pas de tics d'écriture d'IA (liste dans la charte), pas de titres en gras suivis de deux-points dans les listes, guillemets droits dans le code.
