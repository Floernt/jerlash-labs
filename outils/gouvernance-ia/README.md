# Gouvernance de l'IA : référentiel et tableur

Ce dossier accompagne la boîte à outils [Gouvernance de l'IA](https://jerlash.eu/fr/outils/gouvernance-ia/) (P14). Il contient les éléments que d'autres outils lisent ou produisent ; la méthode elle-même est rédigée sur le site.

| Dossier | Contenu |
| --- | --- |
| `referentiel/gouvernance-ia.json` | Source unique des niveaux, de la règle de détermination du niveau, de la fiche de conformité (F01 à F11), des classes D0 à D4, des niveaux U1 à U4 et S1 à S4, des conditions E01 à E08, des critères C1 à C7 et des colonnes des registres. |
| `tableur/` | Le tableur des niveaux 2 et 3 (`gouvernance-ia-matrices-<version>.xlsx`) et le script qui le génère. |

Le serveur MCP local et la commande Claude Code (P20) s'appuieront sur le même référentiel.

## Le tableur

À télécharger tel quel : [`tableur/gouvernance-ia-matrices-0.3.xlsx`](tableur/gouvernance-ia-matrices-0.3.xlsx). L'onglet « Lisez-moi » en donne le mode d'emploi. Les cellules jaunes se remplissent, les grises se calculent. Le fichier ne contient qu'une ligne d'exemple fictive par onglet. N'y saisissez jamais de nom de client ni d'élément couvert par le secret professionnel.

Pour le régénérer après une modification du référentiel (depuis la racine du dépôt, avec openpyxl installé) :

```
python outils/gouvernance-ia/tableur/generer_tableur.py --copier-site
```

`--copier-site` place aussi une copie dans `site/static/telechargements/`, d'où le site la propose.

## Licence

CC BY-NC 4.0, éditeur jerlash.labs (ADR-026). Version de travail : ni charte adoptée, ni label de conformité, ni avis juridique individualisé.
