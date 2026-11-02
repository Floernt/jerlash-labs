# Factory jerlash.labs

La Factory organise la production des outils publiés sur jerlash.labs. Elle fixe un circuit unique (de l'idée à la publication), des rôles confiés à des agents Claude Code, des standards communs, des composants réutilisables et un banc d'essai. Un agent de supervision, `ops-factory`, suit la production, contrôle les étapes et améliore la Factory elle-même.

## Principes

1. Florian décide. Les agents proposent, produisent et vérifient ; aucun outil n'est publié, aucun standard n'est modifié sans sa validation.
2. Une seule source de vérité par sujet : `registre.md` pour l'état des projets, `projets/` pour les fiches, `standards/` pour les règles, `ameliorations.md` pour les évolutions de la Factory.
3. Preuves plutôt qu'affirmations. Une étape est franchie quand ses livrables existent et que les contrôles ont été exécutés, pas quand un agent dit qu'elle l'est (principe repris de legal-prompts et de pstack).
4. Petits changements, vérifiés sur le comportement réel, avec des données fictives.
5. Autonomie progressive : les agents travaillent d'abord sous supervision directe ; leur marge s'élargit quand leurs vérifications se sont montrées fiables (voir `metriques.md`).

## Organisation

```
factory/
  README.md            ce fichier
  pipeline.md          étapes, critères d'entrée et de sortie
  registre.md          état de chaque projet (tenu par ops-factory)
  metriques.md         indicateurs suivis
  ameliorations.md     propositions d'évolution de la Factory
  memoire/             mémoire persistante de la Factory (skill memoire-projet)
  standards/           règles communes : prompts, code, livrables
  composants/          catalogue des briques réutilisables
  jeux-de-test/        dossiers fictifs et résultats attendus
  retours/             rétrospectives après chaque publication
```

## Rôles (agents dans `.claude/agents/`)

| Agent | Rôle | Étapes |
|---|---|---|
| ops-factory | supervise, contrôle les passages d'étape, tient le registre, améliore la Factory | toutes |
| eclaireur | veille, repère des projets, rédige des fiches au statut "idée" | 0 |
| architecte | transforme une fiche en spécification technique, choisit les composants | 2 |
| developpeur | réalise l'outil selon la spécification | 3 |
| testeur | exécute le banc d'essai, rédige le rapport de test | 4 |
| verificateur-securite | contrôle clés, flux réseau, dépendances, secrets | 4 |
| relecteur-deontologie | relève les points de déontologie et de RGPD à trancher par Florian | 1 et 4 |
| designer-ux | relit l'interface (Laws of UX) | 3 et 4 |
| redacteur | rédige la fiche publique et le guide selon la charte | 5 |

## Comment la supervision fonctionne dans Claude Code

Les sous-agents de Claude Code sont appelés par la session principale. D'après ce que je sais de Claude Code, un sous-agent ne peut pas en lancer un autre [À VÉRIFIER dans la documentation à jour]. La supervision repose donc sur deux éléments :

1. La commande `/factory` met la session principale en mode supervision : elle lit le registre, choisit l'étape suivante, délègue au bon agent, puis fait contrôler le résultat.
2. L'agent `ops-factory` est appelé pour les contrôles de passage d'étape, l'audit de la Factory et les propositions d'amélioration. Il lit tout, écrit seulement dans `factory/` et ne modifie jamais le code d'un outil.

## Commandes

| Commande | Usage |
|---|---|
| `/factory` | point d'entrée de la supervision : état, prochaine action, délégation |
| `/factory-lancer <ID>` | fait entrer un projet dans le circuit |
| `/factory-etape <ID>` | demande le passage à l'étape suivante (contrôle par ops-factory) |
| `/factory-revue` | audit de la Factory et propositions d'amélioration |
| `/factory-retro <ID>` | rétrospective après publication |
| `/veille` | revue des sources suivies par l'éclaireur |
