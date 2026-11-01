# Bibliothèque de références

Textes de référence (déontologie, lignes directrices, guides d'autorités) que le projet cite et réutilise : dans les décisions (`docs/decisions.md`), dans les fiches des outils, et plus tard dans une rubrique de veille du site (ADR-018).

## Organisation

```
bibliotheque/
  README.md        ce fichier
  catalogue.md     une ligne par document
  fiches/          une fiche par document : métadonnées, résumé, passages cités, usage dans le projet
  sources/         les fichiers originaux (PDF) - NON versionnés
```

## Règles

1. Les fichiers originaux restent dans `sources/`, qui est ignoré par git. Le dépôt est destiné à être public et ces textes appartiennent à leurs auteurs : on cite et on renvoie à la source officielle, on ne redistribue pas.
2. Chaque document a une fiche dans `fiches/` et une ligne dans `catalogue.md`. La fiche est versionnée ; c'est elle que les autres documents du dépôt citent.
3. Les passages repris dans une fiche sont cités mot pour mot, entre guillemets, avec la page. Pas de paraphrase de la règle (charte éditoriale) ; un résumé, s'il y en a un, est présenté comme tel.
4. La date de consultation et l'URL officielle figurent dans la fiche. Tant que l'URL n'a pas été vérifiée, elle porte le marqueur `[À VÉRIFIER]`.
5. Nom des fichiers : `AAAA-MM-JJ_AUTEUR_objet.pdf` quand la date est connue, `AUTEUR_objet.pdf` sinon. Même nom de base pour la fiche (`.md`).

## Synchronisation

La copie de travail des originaux est tenue par Florian dans OneDrive (`PRO/Intelligence artificielle/Ressources/LEGAL/`). Après un clone neuf, recopier les PDF dans `sources/` sous le nom indiqué par la fiche. Un script de synchronisation sera écrit quand la rubrique de veille du site sera lancée (ADR-018).
