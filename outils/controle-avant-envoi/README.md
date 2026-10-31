# Contrôle avant envoi (P05 Lite)

Inspection non destructive d'un document Word (.docx) avant de l'envoyer à un confrère, un client ou une juridiction. L'outil cherche ce qui ne devrait pas partir avec le fichier (commentaires, modifications suivies, texte masqué, propriétés, chemins internes, noms d'autres dossiers…) et produit un rapport. Il ne modifie jamais le document.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`.

## Prérequis

Python 3.10 ou plus récent. Aucune autre dépendance : l'outil n'utilise que la bibliothèque standard (zipfile, xml.etree, tkinter, json, hashlib). Aucune clé API, aucun accès réseau.

## Utilisation

Fenêtre graphique (Windows) : double-cliquer sur `Controle avant envoi.pyw`.

Ligne de commande, depuis le dossier `src/` :

```
python -m controle_avant_envoi contrat.docx
python -m controle_avant_envoi *.docx --html rapports --termes ..\termes.txt
python -m controle_avant_envoi contrat.docx --json rapports --silencieux
python -m controle_avant_envoi --interface
```

Options :

- `--html DOSSIER` et `--json DOSSIER` : un rapport par document, nommé `<document> - controle avant envoi.html|json`.
- `--termes FICHIER` : liste de termes sensibles, un par ligne (modèle : `termes.example.txt`).
- `--config FICHIER` : remplace des réglages par défaut (modèle : `config.example.json`, valeurs par défaut : `src/controle_avant_envoi/defaut.json`).
- `--silencieux` : n'affiche que le verdict.

Codes de sortie : 0 rien détecté, 1 points à traiter, 2 analyse impossible ou incomplète. Un script ne doit traiter un document comme contrôlé que sur le code 0, et même dans ce cas la relecture reste nécessaire.

## Organisation du code

```
src/controle_avant_envoi/
  ooxml.py       lecture prudente du paquet (limites de taille, refus des DOCTYPE, format strict signalé)
  controles.py   les quatorze contrôles et leur catalogue (titre, gravité, explication, conseil)
  analyse.py     configuration, exécution, synthèse et verdict
  rapport.py     rapports texte, HTML autonome (CSP stricte, contenu échappé) et JSON
  interface.py   fenêtre tkinter
  __main__.py    ligne de commande
  defaut.json    marqueurs, domaines internes, champs révélateurs
tests/           tests unittest (jeu F-DOCX-01, sécurité, ligne de commande)
```

## Tests

Depuis le dossier de l'outil :

```
python -m unittest discover -s tests -v
```

Les tests utilisent le jeu fictif `factory/jeux-de-test/F-DOCX-01` (pièces, générateur, résultats attendus dans `attendu/P05.json`). Ils vérifient en outre l'absence de tout module réseau dans le code, l'absence d'accès réseau pendant l'analyse, l'intégrité du fichier analysé et le comportement face à des fichiers hostiles ou endommagés.

La vérification complète du dépôt se lance depuis la racine : `python outils/verifier.py`.

## Ajouter un contrôle

1. Écrire une fonction `controle_xxx(paquet, controle, cfg)` dans `controles.py` qui appelle `controle.ajouter(lieu, detail)` pour chaque constat.
2. L'inscrire dans `CATALOGUE` avec son titre, sa gravité, l'explication et le conseil.
3. Ajouter un piège correspondant dans `factory/jeux-de-test/F-DOCX-01/generer.py`, régénérer les pièces, compléter `attendu/P05.json`.
4. Vérifier que la pièce piégée s'ouvre toujours dans Word.
