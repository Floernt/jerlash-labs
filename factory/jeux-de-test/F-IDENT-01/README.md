# F-IDENT-01 — Données d'identification dans des textes juridiques belges

Version 1.0, 31 octobre 2026. Toutes les personnes, sociétés, adresses et numéros sont fictifs. Les numéros à somme de contrôle sont valides, sinon la mesure serait faussée. Ils ont été tirés au hasard : une coïncidence avec un numéro réel reste théoriquement possible, mais elle n'aurait aucune signification.

Ce jeu sert à mesurer l'outil de pseudonymisation (P09) : rappel et précision par catégorie.

## Deux jeux

`sources/` contient le **jeu de développement** : 6 textes et 102 entités. Il a servi à écrire les règles et comporte un texte sans aucune donnée personnelle (`sans-donnees.txt`). Il est permis de l'enrichir pour ajouter une règle.

`sources-controle/` contient le **jeu de contrôle** : 8 textes et 186 entités. Il a été rédigé le 31 octobre 2026 par un agent distinct, sans accès au code de l'outil ni au jeu de développement. Il ne sert qu'à mesurer. Le corriger ou s'en servir pour régler une règle lui retire sa valeur. Dans ce cas, il faut le verser au jeu de développement et en rédiger un nouveau.

## Format

Une entité s'écrit `[[CATEGORIE:texte]]` dans les sources. `generer.py` retire les balises et écrit trois choses (les annotations du jeu de contrôle vont dans `attendu/annotations-controle.json`) :
- les textes nus dans `pieces/` (le jeu de contrôle dans `pieces/controle/`) ;
- une version .docx de `contrat-prestation` ;
- les positions attendues dans `attendu/annotations.json`.

Il refuse un numéro dont la somme de contrôle est fausse.

```
python -I factory/jeux-de-test/F-IDENT-01/generer.py              régénérer
python -I factory/jeux-de-test/F-IDENT-01/generer.py --verifier   contrôler que pieces/ correspond aux sources
python factory/jeux-de-test/F-IDENT-01/evaluer.py                 mesurer P09
```

## Règles d'annotation

- **PERSONNE** : le nom sans la civilité. Chaque occurrence est annotée, y compris le nom de famille seul, le prénom seul quand il désigne quelqu'un, et le nom en capitales. Les avocats, magistrats, experts et témoins nommés sont des personnes.
- **ORGANISATION** : le nom sans la forme sociale. Les juridictions et administrations ne sont pas annotées.
- **ADRESSE** : la rue, le numéro, la boîte, le code postal et la localité, en une seule entité quand ils se suivent. Une ville seule n'est pas annotée.
- **DATE_NAISSANCE** : la date seule, quand le texte la présente comme telle.
- **REFERENCE** : les numéros de rôle et les références de dossier qui identifient l'affaire. Les références de jurisprudence publiée ne sont pas annotées.
- **Autres catégories** : NUMERO_NATIONAL, NUMERO_ENTREPRISE, IBAN, CARTE_BANCAIRE, EMAIL, TELEPHONE et PLAQUE portent sur la valeur seule.

## Mesure

Une entité est « masquée » si tous ses caractères alphanumériques sont couverts par une détection, quelle qu'en soit la catégorie. Une couverture partielle compte comme un oubli. Une détection est « correcte » si elle chevauche une entité attendue.

Les résultats datés sont rangés dans `resultats/`. Les planchers de non-régression sont dans `attendu/P09.json` et sont contrôlés par les tests de l'outil.
