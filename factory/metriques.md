# Indicateurs de la Factory

Relevés par `ops-factory` lors de chaque `/factory-revue`. Pas d'indicateur sans mesure réelle ; si une donnée manque, l'écrire.

## Par projet

- durée passée à chaque étape (dates du registre) ;
- nombre de retours en arrière (étape refusée par le contrôle) ;
- coût d'une exécution sur le banc d'essai, par version ;
- résultats du banc d'essai par version.

## Par agent

- passages d'étape refusés pour un livrable de cet agent, et motif ;
- erreurs relevées par Florian après validation d'un contrôle (signal que le contrôle est trop faible).

## Règle d'autonomie

Un agent dont trois livrables consécutifs passent le contrôle sans correction peut se voir confier des tâches plus larges. Une erreur relevée par Florian après contrôle remet le compteur à zéro et donne lieu à une amélioration du standard concerné. Cette règle est une proposition [À VALIDER].

## Pilote du 2026-11-11 au 2026-12-11 (FLO-61)

Option A décidée par Florian sur FLO-58 : aucun recrutement, l'agent jerlash tient `ops-factory`. Quatre indicateurs relevés à chaque passage, et repris au bilan (FLO-62).

- tickets Paperclip ouverts par étape du circuit, identifiés `[factory:<ID>]` ;
- budget consommé par l'agent jerlash, rapporté au plafond mensuel ;
- blocages, avec la personne ou l'agent qui doit agir ;
- passages d'étape ratés : étape franchie sans que ses critères de sortie soient remplis.

### Relevé du 2026-11-11 (ouverture)

| Indicateur | Mesure | Source |
|---|---|---|
| Tickets `[factory:]` ouverts | 2 avant ce relevé : FLO-61 (pilote) et FLO-62 (bilan). Aucun ticket d'étape. | liste des tickets ouverts du projet jerlash.labs |
| Budget | plafond mensuel 12 000 centimes. Dépense réelle non relevée : `GET /api/agents/me` ne renvoie que `budgetMonthlyCents`. `[À VÉRIFIER]` | API Paperclip |
| Blocages | 3. Le parcours de P14 n'était pas choisi (proposé au registre, à confirmer par Florian). Le second outil du pilote n'est pas confirmé : le calendrier du `BACKLOG.md` donne P19 pour décembre, la décision de Florian du 2026-11-10 (FLO-24) donne la Legal Agent Factory. Enfin, l'environnement d'exécution de l'agent jerlash n'a pas d'interpréteur Python (`python` et `python3` absents) : ni `scripts/verifier.py`, ni `generer_tableur.py` ne peuvent y être exécutés, alors que le circuit fait de `verifier.py` un critère de sortie. | `factory/registre.md`, `BACKLOG.md`, FLO-24, `command -v python3` |
| Passages d'étape ratés | 1. Les dix pages de P14 ont été publiées le 2026-11-06 sans que les étapes 4 (vérification) et 5 (publication) aient été franchies : `outils/gouvernance-ia/verifications/` n'existe pas et aucune entrée n'a été créée dans `site/content/nouveautes/`. Voir AM-003. | dépôt, `main` au commit `69c7c29` |
| Durée par étape, P14 | non mesurable avant le 2026-11-11 : le registre ne portait aucune ligne P14, donc aucune date de passage. `[À VÉRIFIER]` | `factory/registre.md` |

## Relevés

| Date | Observation |
|---|---|
| 2026-10-31 | Factory créée, aucun relevé |
| 2026-11-11 | Ouverture du pilote : registre complété de P14 à P19, parcours de P14 proposé, relevé d'ouverture ci-dessus |
