# IA dans les outils et autonomie des outils

Cap depuis le 2026-11-01 (ADR-022) : le projet s'appelle jerlash.labs ; livrer plutôt que construire. Un seul chantier à la fois (BACKLOG.md, « Maintenant ») ; ne pas relancer de développement d'outil sans décision de Florian. Hugo : `relURL` ne préfixe pas un chemin qui commence par « / » (publication sous /jerlash-labs/) ; retirer le « / » avant.

Décisions de Florian du 2026-11-01 et leurs raisons. Voir aussi [[contexte]].

## Choix de Florian
- Tous les outils se connectent à une API d'IA, en BYOK (ADR-019). Sans clé, l'outil ne fonctionne pas : « faire au plus simple ».
- Le fournisseur est au libre choix de l'avocat, API directe d'Anthropic comprise. La grille déontologique (docs/deontologie-ia.md) informe, elle ne filtre pas.
- L'objection déontologique est consignée dans l'ADR-019 : lignes directrices AVOCATS.BE et OVB, « environnement fermé avec des garanties adéquates », et P09 qui ne trouve que 45 % des noms. Ne pas la reformuler : Florian l'a entendue et a tranché.
- Chaque outil est autonome et téléchargeable seul (ADR-021). Un avocat doit pouvoir en essayer un sans les autres. La duplication de code est voulue.

## Garde-fous gardés
- Avant tout envoi : pseudonymisation locale par P09, texte affiché et modifiable, case à cocher.
- P09 reste sans IA : c'est le filtre avant l'envoi.

## Comment on travaille
- Composants communs : on modifie la source (factory/composants/ ou outils/pseudonymisation), puis `python scripts/synchroniser_composants.py`. On ne modifie jamais la copie dans un outil.
- Connecteur IA (ADR-020) : un seul format, Chat Completions, avec une requête minimale (model, messages, max_tokens). Pas de temperature ni de response_format : la couche de compatibilité d'Anthropic les refuse.
- Tests : faux fournisseur sur 127.0.0.1 (outils/inventaire-dossier/tests/aide.py). Jamais d'appel réel dans les tests.
- Mesure du mode IA : `evaluer.py --ia`, payant, on retient le plus mauvais de trois exécutions. On ne règle jamais la consigne d'après le dossier de contrôle.
- Une fiche d'outil ou un .md ajouté dans outils/<slug>/ change l'archive : relancer `python scripts/empaqueter.py --fiche`. Les brouillons vont dans projets/.

## Pièges rencontrés
- typographie.py insère des espaces insécables avant « : » et « ; ». Un remplacement scripté doit accepter aussi ces espaces.
- Un `cat > fichier` sans entrée bloque la commande Bash : ne pas l'utiliser.
