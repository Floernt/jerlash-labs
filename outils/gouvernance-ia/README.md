# Gouvernance de l'IA : référentiel, tableur et téléchargements

Ce dossier accompagne la boîte à outils [Gouvernance de l'IA](https://jerlash.eu/fr/outils/gouvernance-ia/) (P14). Il contient les éléments que d'autres outils lisent ou produisent ; la méthode elle-même est rédigée sur le site. Ce qui change d'une version à l'autre est dans [`CHANGELOG.md`](CHANGELOG.md).

| Dossier | Contenu |
| --- | --- |
| `referentiel/gouvernance-ia.json` | Source unique des niveaux, de la règle de détermination du niveau, de la fiche de conformité (F01 à F11), des classes D0 à D4, des niveaux U1 à U4 et S1 à S4, des conditions E01 à E08, des critères C1 à C7 et des colonnes des registres. |
| `tableur/` | Le tableur des niveaux 2 et 3 (`gouvernance-ia-matrices-<version>.xlsx`) et le script qui le génère. |
| `telechargements/` | Le script qui construit le pack complet, la charte en .docx et le kit « petit cabinet », en français et en anglais. |
| `tests/` | Les contrôles automatiques des téléchargements (`python -m unittest discover -s tests`). |

Le serveur MCP local et la commande Claude Code (P20) s'appuieront sur le même référentiel.

## Le tableur

À télécharger tel quel : [`tableur/gouvernance-ia-matrices-0.3.xlsx`](tableur/gouvernance-ia-matrices-0.3.xlsx). L'onglet « Lisez-moi » en donne le mode d'emploi. Les cellules jaunes se remplissent, les grises se calculent. Le fichier ne contient qu'une ligne d'exemple fictive par onglet. N'y saisissez jamais de nom de client ni d'élément couvert par le secret professionnel.

Pour le régénérer après une modification du référentiel (depuis la racine du dépôt, avec openpyxl installé) :

```
python outils/gouvernance-ia/tableur/generer_tableur.py --copier-site
```

`--copier-site` place aussi une copie dans `site/static/telechargements/`, d'où le site la propose.

## Les téléchargements

Trois fichiers par langue sont proposés depuis l'accueil de la boîte à outils : le pack complet en zip, la charte modèle en .docx et le kit « petit cabinet » (les six éléments du niveau 1). Ils sont reconstruits à partir des pages de `site/content/outils/gouvernance-ia/` et du référentiel : leur contenu ne peut pas s'écarter de ce qui est publié. Ils ne sont pas versionnés dans le dépôt (ADR-034) : `python scripts/verifier.py` les construit avant de vérifier le site, en local comme dans les deux workflows.

Pour les construire seuls :

```
python outils/gouvernance-ia/telechargements/generer_telechargements.py --copier-site
```

Bibliothèque standard seule : la commande fonctionne sans rien installer. Sans `--copier-site`, les fichiers sont écrits à côté du script (`--sortie` pour choisir un autre dossier).

Les fichiers produits sont reproductibles : à contenu égal, mêmes octets et même empreinte SHA-256, que la commande tourne sur un poste ou dans l'intégration continue. Le script s'arrête si un intertitre repris dans le kit a disparu d'une page, pour qu'une réécriture du site ne produise pas un kit incomplet.

Après une modification des pages, relancez les contrôles :

```
cd outils/gouvernance-ia && python -m unittest discover -s tests
```

## Licence

CC BY-NC 4.0, éditeur jerlash.labs (ADR-026). Version de travail : ni charte adoptée, ni label de conformité, ni avis juridique individualisé.
