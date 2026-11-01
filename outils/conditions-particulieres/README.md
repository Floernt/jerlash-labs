# Conditions particulières et générales (P03, mode local)

L'outil prépare la séparation d'un contrat négocié en conditions particulières et conditions générales. Il découpe le contrat en blocs (comparution, chaque article, signatures) et repère dans chacun les données propres à l'opération :
- parties et personnes ;
- adresses ;
- identifiants : numéro d'entreprise, IBAN, courriel, téléphone, référence ;
- montants, dates et quantités.

Pour chaque bloc, il propose :
- conditions particulières : le bloc est propre à l'opération (comparution, objet, prix, durée, coordonnées…) ;
- conditions générales : le bloc ne contient aucune donnée propre à l'opération ;
- clause mixte : clause de nature générale qui contient une donnée propre à l'opération, à extraire avant de réutiliser la clause.

L'usage principal : savoir ce qu'il faut retirer d'un contrat négocié avant de le réutiliser comme modèle. Les renvois internes (« article 5 ») sont listés, car ils devront être vérifiés après la séparation.

Cette version fonctionne par règles, sans IA ni réseau. Elle ne modifie pas le contrat et ne produit pas les deux documents séparés : cela dépend du composant d'édition .docx (P10), qui n'existe pas encore.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`.

## Prérequis

Python 3.10 ou plus récent, sans autre dépendance.

## Utilisation

Fenêtre (Windows) : double-cliquer sur `Conditions.pyw`, puis « Choisir le contrat… ». Le rapport est enregistré dans `Documents\Conditions particulieres`.

Ligne de commande, depuis `src/` :

```
python -m conditions_particulieres "D:\Modèles\Contrat de prestation.docx" --liste
python -m conditions_particulieres "D:\Modèles\Contrat de prestation.docx" --sortie "D:\Rapports"
```

Le rapport est écrit en trois formats : `Conditions - <contrat>.docx`, `.md` et `.json`. Aucun fichier existant n'est remplacé.

Codes de sortie :
- 0 : aucune clause mixte ;
- 1 : clauses mixtes à épurer ;
- 2 : erreur.

## Formats lus

| Format | Ce qui est lu |
|---|---|
| .docx | corps du texte et tableaux ; ni le texte masqué, ni le texte supprimé ou déplacé en suivi des modifications |
| .txt, .md | texte ; les lignes `| a | b |` forment un tableau |

Les notes de bas de page, en-têtes et pieds de page ne sont pas lus. Un en-tête qui porte le nom du client n'est donc pas signalé : vérifiez-le à la main.

## Tests et mesure

```
cd outils/conditions-particulieres && python -m unittest discover -s tests -v
python factory/jeux-de-test/F-CPCG-01/evaluer.py        (depuis la racine du dépôt)
```

La mesure porte sur deux jeux de contrats fictifs. Le jeu de développement (2 contrats) a servi à écrire les règles. Le jeu de contrôle (3 contrats) a été rédigé à part, et ses écarts ne sont pas affichés par défaut. Les règles ne doivent jamais être réglées d'après lui.
