# Glossaire des définitions (P02, mode local)

L'outil relève les définitions d'un contrat et produit un rapport :
- le glossaire : chaque terme défini, sa définition, l'endroit où il est défini et le nombre de ses emplois ;
- les points à examiner : définitions répétées (libellés identiques ou divergents), termes définis jamais employés, termes écrits avec des majuscules sans définition, graphies différentes d'un terme défini, termes employés avant leur définition en cours de texte.

Cette version fonctionne par règles, sans IA ni réseau. Elle ne modifie pas le contrat et ne restructure pas les définitions : la version qui déplacerait les définitions dans un article unique dépend du composant d'édition .docx (P10), qui n'existe pas encore.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`.

## Prérequis

Python 3.10 ou plus récent, sans autre dépendance.

## Utilisation

Fenêtre (Windows) : double-cliquer sur `Glossaire.pyw`, puis « Choisir le contrat… ». Le rapport est enregistré dans `Documents\Glossaire des definitions`.

Ligne de commande, depuis `src/` :

```
python -m glossaire_definitions "D:\Dossiers\Contrat de fourniture.docx" --liste
python -m glossaire_definitions "D:\Dossiers\Contrat de fourniture.docx" --sortie "D:\Rapports"
```

Le rapport est écrit en trois formats : `Glossaire - <contrat>.docx`, `.md` et `.json`. Aucun fichier existant n'est remplacé.

Codes de sortie :
- 0 : aucun point relevé ;
- 1 : points à examiner ;
- 2 : erreur.

## Formats lus

| Format | Ce qui est lu |
|---|---|
| .docx | corps du texte et tableaux ; ni le texte masqué, ni le texte supprimé en suivi des modifications |
| .txt, .md | texte ; les lignes `| a | b |` forment un tableau |

Les notes de bas de page, en-têtes et pieds de page ne sont pas lus. Un ancien .doc ou un PDF doit être enregistré en .docx.

## Tests et mesure

```
cd outils/glossaire-definitions && python -m unittest discover -s tests -v
python factory/jeux-de-test/F-DEF-01/evaluer.py        (depuis la racine du dépôt)
```

La mesure porte sur deux jeux de contrats fictifs. Le jeu de développement (3 contrats) a servi à écrire les règles. Le jeu de contrôle (4 contrats) a été rédigé à part, et ses écarts ne sont pas affichés par défaut. Les règles ne doivent jamais être réglées d'après lui.
