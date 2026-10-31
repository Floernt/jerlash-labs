# Inventaire d'un dossier (P01, mode local)

L'outil dresse l'inventaire d'un dossier contractuel : il parcourt un dossier de pièces et produit un registre. Pour chaque pièce, le registre indique :
- le type (contrat, avenant, conditions générales, courrier, courriel, note, modèle, précédent) ;
- le statut (signé, projet) ;
- la date de l'acte ;
- les parties ;
- la pièce à laquelle elle se rapporte ;
- si elle fait foi ;
- son empreinte SHA-256.

Des alertes signalent les pièces non lues, les actes non signés, les pièces sans partie commune avec le reste du dossier, les doublons et les envois recommandés sans preuve.

Cette version fonctionne par règles, sans IA ni réseau. Chaque conclusion est accompagnée de l'indice qui l'a produite, et le registre se relit comme une proposition. Un mode avec IA est envisagé (ADR-015, proposée) ; il n'est pas développé.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`.

## Prérequis

Python 3.10 ou plus récent, sans autre dépendance.

## Utilisation

Fenêtre (Windows) : double-cliquer sur `Inventaire dossier.pyw`, puis « Choisir le dossier à inventorier… ». Le registre est enregistré dans `Documents\Inventaire dossier`.

Ligne de commande, depuis `src/` :

```
python -m inventaire_dossier "D:\Dossiers\2025-014 Condroz" --liste
python -m inventaire_dossier "D:\Dossiers\2025-014 Condroz" --sortie "D:\Registres"
```

Le registre est écrit en trois formats : `Inventaire - <dossier>.docx`, `.md` et `.json`. Le registre est refusé s'il doit être écrit dans le dossier inventorié, et aucun fichier existant n'est remplacé.

Codes de sortie :
- 0 : aucune alerte ;
- 1 : alertes à examiner ;
- 2 : erreur.

## Formats lus

| Format | Ce qui est lu |
|---|---|
| .docx, .docm | corps du texte, propriétés (auteur, dernière modification, création) |
| .eml | expéditeur, destinataires, date, objet, texte, noms des pièces jointes |
| .txt, .md | texte |
| autres (PDF, .doc, .msg, tableurs, images) | inventoriés avec leur empreinte, signalés « non lus » |

Les fichiers de verrouillage de Word (`~$…`) et les fichiers cachés sont ignorés et mentionnés dans le registre.

## Tests et mesure

```
cd outils/inventaire-dossier && python -m unittest discover -s tests -v
python factory/jeux-de-test/F-DOSSIER-01/evaluer.py        (depuis la racine du dépôt)
```

La mesure porte sur deux dossiers fictifs. Le dossier de développement (12 pièces) a servi à écrire les règles. Le dossier de contrôle (16 pièces) a été rédigé à part, et ses écarts ne sont pas affichés par défaut. Les règles ne doivent jamais être réglées d'après lui.
