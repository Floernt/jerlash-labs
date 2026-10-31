# Principes applicables à chaque outil

Tout outil publié sur iavocat.be respecte ces règles. Une exception est possible, à condition d'être consignée dans `docs/decisions.md` et expliquée sur la fiche de l'outil.

## Exécution locale

L'outil tourne sur la machine de l'utilisateur. Trois modes sont admis :

1. Page web exécutée dans le navigateur. Sans IA distante : admis. Avec appel direct à l'API d'un fournisseur et clé saisie dans la page : suspendu jusqu'à l'arbitrage d'ADR-010 (PLAN_AMELIORATIONS.md, A01).
2. Application ou script téléchargé (HTML hors ligne, Python, Node) lancé localement.
3. Outil branché sur un modèle local (par exemple Ollama), sans aucun appel externe.

La fiche indique le mode utilisé et pourquoi.

## Clé API (BYOK)

- La clé est fournie par l'utilisateur et n'est jamais transmise ailleurs qu'au fournisseur concerné.
- Par défaut, la clé reste en mémoire et disparaît à la fermeture de la page. La mémorisation locale (stockage du navigateur ou fichier `.env`) est une option explicite, accompagnée d'un avertissement.
- L'interface recommande une clé dédiée à l'outil, avec un plafond de dépenses fixé chez le fournisseur.
- Appels directs depuis le navigateur : certains fournisseurs l'autorisent sous conditions (par exemple un en-tête spécifique chez Anthropic) `[À VÉRIFIER dans la documentation à jour de chaque fournisseur]`.

## Données

- Aucune télémétrie, aucun journal envoyé à iavocat.be.
- L'outil affiche, avant le premier envoi, ce qui va partir vers le fournisseur.
- Les politiques de conservation des données des fournisseurs ne sont pas résumées de mémoire : la fiche renvoie vers la page officielle du fournisseur, avec la date de consultation.
- Les exemples et jeux de test sont fictifs. Jamais de pièce réelle, même anonymisée, dans le dépôt.

## Configuration

- Fournisseur, modèle et paramètres sont regroupés dans un seul fichier de configuration par outil.
- Aucun nom de modèle en dur dans la logique.
- Le coût estimé d'un appel est affiché quand c'est possible, avec la date des tarifs utilisés.

## Dépendances

- Le moins possible. Chaque dépendance est justifiée dans le README de l'outil.
- Versions figées. Pas de chargement depuis un CDN dans une page qui manipule une clé API, sauf décision consignée.

## Structure d'un dossier outil

```
outils/<slug>/
  README.md        installation et usage technique
  FICHE.md         fiche publique (gabarit templates/fiche-outil.md)
  CHANGELOG.md     versions de l'outil
  config.example   configuration type, sans clé
  src/             code
  exemples/        données fictives
```

## Avant publication

- [ ] La fiche est complète.
- [ ] Le trajet des données est décrit et exact.
- [ ] Testé avec des données fictives.
- [ ] Aucun secret dans l'historique git.
- [ ] Précautions spécifiques rédigées.
- [ ] Coût estimé et daté.
- [ ] Relu par Florian.
