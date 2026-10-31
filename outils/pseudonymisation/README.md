# Pseudonymisation (P09 Lite)

Pseudonymisation locale d'un texte avant de le soumettre à une IA. L'outil :
- repère les noms, sociétés, adresses et identifiants belges (numéro national, numéro d'entreprise, IBAN, téléphone…) ;
- les remplace par des marqueurs (`[PERSONNE_1]`, `[IBAN_1]`…) ;
- conserve sur l'ordinateur une table de correspondance, qui sert ensuite à rétablir les données dans la réponse de l'IA.

Le résultat est une pseudonymisation, et non une anonymisation : l'outil ne trouve pas tout, et le contexte peut suffire à reconnaître une personne. La relecture est obligatoire. La fenêtre ne permet pas d'enregistrer le texte avant que la relecture ait été confirmée.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`.

## Prérequis

Python 3.10 ou plus récent. Aucune autre dépendance : l'outil n'utilise que la bibliothèque standard (re, zipfile, xml.etree, tkinter, json). Il ne demande aucune clé API et n'accède pas au réseau.

## Utilisation

Fenêtre graphique (Windows) : double-cliquer sur `Pseudonymisation.pyw`.

1. Onglet « Pseudonymiser » : collez le texte ou ouvrez un fichier .txt, .md ou .docx.
2. Relisez le texte pseudonymisé affiché à droite.
3. Dans la liste, double-cliquez sur une ligne pour remplacer ou conserver une donnée. Ajoutez ce que l'outil a manqué.
4. Cochez la case de relecture, puis cliquez sur « Enregistrer et copier le texte ». Le texte pseudonymisé et la table de correspondance sont enregistrés dans `Documents\Pseudonymisation`.
5. Onglet « Rétablir » : collez la réponse de l'IA et cliquez sur « Rétablir ». La table du dernier texte enregistré est déjà chargée.

Ligne de commande, depuis le dossier `src/` :

```
python -m pseudonymisation pseudonymiser piece.docx --liste
python -m pseudonymisation pseudonymiser piece.docx --termes ..\termes.txt --exclure ..\exclus.txt --sortie D:\travail
python -m pseudonymisation retablir reponse.txt --table "D:\travail\piece - table.json" --sortie reponse-retablie.txt
```

Options de `pseudonymiser` :

- `--liste` affiche les détections sans rien écrire.
- `--termes FICHIER` donne les termes à remplacer en tout cas, un par ligne. Pour choisir la catégorie : `PERSONNE | Jean Dupont` (modèle : `termes.example.txt`).
- `--exclure FICHIER` donne les textes à ne jamais remplacer.
- `--sortie DOSSIER` indique le dossier où écrire `<nom> - pseudonymise.txt` et `<nom> - table.json`. Aucun fichier existant n'est remplacé : un numéro est ajouté au nom.

Codes de sortie : 0 réussi, 2 erreur.

## Organisation du code

```
src/pseudonymisation/
  detection.py     règles de détection, sommes de contrôle, propagation des noms, priorités
  remplacement.py  marqueurs, table de correspondance, rétablissement
  lecture.py       lecture des .txt et du corps des .docx (limites de taille, refus des DOCTYPE)
  interface.py     fenêtre tkinter (relecture obligatoire avant enregistrement)
  __main__.py      ligne de commande
tests/             tests unittest (règles, jeu F-IDENT-01, remplacement, sécurité, ligne de commande)
```

## Tests et mesure

Depuis le dossier de l'outil :

```
python -m unittest discover -s tests -v
```

La mesure de la détection sur le jeu fictif `factory/jeux-de-test/F-IDENT-01` se lance depuis la racine du dépôt :

```
python factory/jeux-de-test/F-IDENT-01/evaluer.py
```

Elle donne, pour chaque catégorie, le rappel et la précision, puis la liste des oublis et des fausses alertes (pour le jeu de contrôle, seulement leur nombre). Elle les calcule séparément pour le jeu de développement, qui a servi à écrire les règles, et pour le jeu de contrôle, rédigé à part. Seul le jeu de contrôle mesure la détection sur des textes inconnus de l'outil. Les seuils minimaux sont dans `attendu/P09.json`. Un test échoue si une modification les fait baisser.

## Ajouter une règle

1. Ajouter le cas qui manque dans un texte de `factory/jeux-de-test/F-IDENT-01/sources/` (jeu de développement), annoté `[[CATEGORIE:texte]]`.
2. Régénérer : `python -I factory/jeux-de-test/F-IDENT-01/generer.py`.
3. Écrire la règle dans `detection.py` et un test dans `tests/test_detection.py`.
4. Relancer la mesure. La règle n'est acceptée que si les fausses alertes du jeu de contrôle n'augmentent pas.
5. Ne jamais corriger une règle en regardant le jeu de contrôle : sinon la mesure perd sa valeur. Quand le jeu de contrôle a servi à corriger l'outil, il faut en rédiger un nouveau.
