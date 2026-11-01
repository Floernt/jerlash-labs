# F-CPCG-01 — Contrats fictifs à séparer en conditions particulières et générales

Version 1.0, 1er novembre 2026. Les contrats sont entièrement fictifs : les personnes, les sociétés et leurs numéros sont inventés.

## Les contrats

Jeu de développement, rédigé avec l'outil et servant à écrire ses règles :
- un contrat de fourniture de bouteilles, avec un tableau de prix ;
- un contrat de prestation d'audit, avec des titres numérotés « 1. Mission » et un montant en lettres.
Au total, 28 blocs et 42 données balisées.

Jeu de contrôle, rédigé à part par un agent qui n'avait accès ni au code ni au jeu de développement :
- trois contrats : prestation marketing, maintenance d'équipements frigorifiques, mise à disposition de locaux ;
- 46 blocs annotés et 92 données balisées.
Il ne sert qu'à mesurer, et ses écarts ne sont pas affichés par défaut.

Chaque donnée propre à l'opération est balisée dans la source : `[[MONTANT:12.500 euros]]`. Les six catégories sont PARTIE, ADRESSE, IDENTIFIANT, MONTANT, DATE et QUANTITE. Le générateur retire le balisage des .docx.

Chaque bloc est classé dans `attendu/` :
- `particulieres` ;
- `generales` : aucune donnée balisée ;
- `mixte` : clause de nature générale qui contient une donnée propre à l'opération.

Ne sont pas des données propres :
- les délais génériques et les taux légaux ;
- les dates des lois ;
- les numéros d'articles ;
- la juridiction et la ville du « Fait à ».

## Fichiers

```
sources/              un fichier par contrat : « fichier: <nom>.docx », « --- », un paragraphe par ligne, données balisées
sources-controle/     jeu de contrôle, même format
generer.py            produit pieces/ et pieces-controle/ (.docx, sans balisage)
attendu/P03.json      classement attendu des blocs du jeu de développement, avec des notes
attendu/P03-controle.json, attendu/P03-planchers.json   classement attendu du contrôle ; planchers de non-régression
evaluer.py            mesure P03 : données repérées, signalements exacts, blocs bien classés
resultats/            un compte rendu par version mesurée
```

```
python -I factory/jeux-de-test/F-CPCG-01/generer.py             régénérer
python -I factory/jeux-de-test/F-CPCG-01/generer.py --verifier  contrôler que les .docx correspondent aux sources
python -I factory/jeux-de-test/F-CPCG-01/evaluer.py             mesurer
```
