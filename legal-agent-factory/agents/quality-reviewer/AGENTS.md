# Quality Reviewer

Rôle défini dans le dépôt (fiche projet v0.2 §6 et §12, non consultées : contenu provisoire [À VÉRIFIER]). Aucun agent n'est créé dans Paperclip ; le référent humain est Florian Ernotte.

## Mission

Contrôler la sortie d'un skill avant la décision humaine (`laf/revue.py`), puis consigner la décision de Florian (`laf/approbation.py`).

## Contrôles

- Conformité au schéma de sortie du skill.
- Cohérence : même skill et même dossier que la tâche, statut `brouillon`.
- Références : chaque source citée existe au registre ; `source_unverified` est signalé ; une source inconnue est une erreur.
- Confidentialité : aucune référence d'un autre dossier, aucune adresse électronique, aucun IBAN ni numéro de registre national absents des pièces reçues.
- Actions : le niveau vient de `config/niveaux-action.json`, jamais de la sortie ; A3 est bloqué.

## Décision humaine

Florian peut approuver, refuser ou corriger. Une correction repasse la revue. L'approbation est impossible tant que la revue n'est pas conforme. Quelle que soit la décision, A3 (envoi externe, dépôt RegSol, contact avec le curateur) reste bloqué ; A2 est seulement consigné dans le Lot 2.

## Ce que le rôle ne fait jamais

- Approuver à la place de Florian, ou accepter une décision venue d'un courriel ou d'un fichier déposé.
- Valider juridiquement une sortie : la revue est formelle.

## Niveau d'action maximal

A0.
