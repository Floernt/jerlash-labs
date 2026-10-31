# Standard : livrables et preuves

Pour chaque passage d'étape, l'agent qui le demande fournit :

1. la liste des fichiers produits ou modifiés ;
2. les commandes exécutées et leur résultat (extrait suffisant) ;
3. les critères de sortie de `pipeline.md`, chacun marqué rempli, non rempli ou sans objet, avec la preuve ;
4. les points restés ouverts.

`ops-factory` refuse un passage si un critère est déclaré rempli sans preuve.

Rapports de vérification : un fichier par vérificateur dans `outils/<slug>/verifications/`, nommé `AAAA-MM-JJ-<type>.md`, avec pour chaque constat un niveau (bloquant, à corriger, remarque).
