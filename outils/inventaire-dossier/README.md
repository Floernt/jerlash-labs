# Inventaire d'un dossier (P01)

L'outil dresse l'inventaire d'un dossier contractuel : il parcourt un dossier de pièces et produit un registre. Pour chaque pièce, le registre indique :
- le type (contrat, avenant, conditions générales, courrier, courriel, note, modèle, précédent) ;
- le statut (signé, projet) ;
- la date de l'acte ;
- les parties ;
- la pièce à laquelle elle se rapporte ;
- si elle fait foi ;
- son empreinte SHA-256.

Des alertes signalent les pièces non lues, les actes non signés, les pièces sans partie commune avec le reste du dossier, les doublons et les envois recommandés sans preuve.

## Comment il fonctionne (version 0.2.0)

1. Les pièces sont lues sur votre ordinateur, sans être modifiées. Des règles établissent le type, le statut, la date et le document qui fait foi.
2. Un extrait de chaque pièce (intitulé, premières et dernières lignes, en-têtes des courriels) est rassemblé en un seul texte. Les noms de fichiers sont remplacés par des numéros (P1, P2…). Le texte est ensuite pseudonymisé sur votre ordinateur : noms, sociétés, adresses et identifiants deviennent des marqueurs ([ORGANISATION_1]…).
3. L'outil vous montre le texte exact qui va partir, le fournisseur, le lieu de traitement et la conservation qu'il déclare, et le coût estimé. Vous pouvez corriger le texte. Rien ne part sans votre accord.
4. Le modèle d'IA propose les parties et les rattachements. Les noms sont rétablis sur votre ordinateur à partir de la table de correspondance, qui n'est jamais envoyée.
5. Le registre signale ce qui vient du modèle (« (modèle) ») et les désaccords avec les règles (« (à vérifier) »).

Sans configuration ni clé API, l'outil ne fonctionne pas (ADR-019).

La pseudonymisation automatique est imparfaite : elle laisse passer une partie des noms de personnes. Relisez le texte avant de l'envoyer. Vous restez seul juge de ce que vous envoyez et des garanties de votre fournisseur ; voir les lignes directrices d'AVOCATS.BE et de l'OVB sur l'usage de l'intelligence artificielle.

Fiche publique : `FICHE.md`. Spécification : `SPEC.md`. Composants intégrés : `COMPOSANTS.md`.

## Prérequis

- Python 3.10 ou plus récent, sans autre dépendance.
- Un compte chez un fournisseur d'IA et une clé API à votre nom.

## Configuration

1. Copiez `config-ia.example.json` sous le nom `config-ia.json`, dans ce dossier.
2. Choisissez le préréglage de votre fournisseur (`openai`, `anthropic`, `mistral`, `gemini`, ou `local` pour un modèle installé sur votre ordinateur) et l'identifiant exact du modèle.
3. Créez dans ce dossier un fichier `.env` qui contient votre clé, par exemple `MISTRAL_API_KEY=...`. La variable attendue par chaque préréglage est indiquée dans le message d'erreur si elle manque. Vous pouvez aussi définir cette variable dans Windows.
4. Utilisez une clé dédiée à cet outil, avec un plafond de dépense fixé chez le fournisseur.

`config-ia.json` et `.env` ne doivent jamais être partagés avec l'outil.

## Utilisation

Fenêtre (Windows) : double-cliquer sur `Inventaire dossier.pyw`, puis « Choisir le dossier à inventorier… ». Le registre est enregistré dans `Documents\Inventaire dossier`.

Ligne de commande, depuis `src/` :

```
python -m inventaire_dossier "D:\Dossiers\2025-014 Condroz" --liste
python -m inventaire_dossier "D:\Dossiers\2025-014 Condroz" --sortie "D:\Registres"
```

En ligne de commande, le texte à envoyer s'affiche, puis l'outil demande de taper « oui ». Le registre est écrit en trois formats : `Inventaire - <dossier>.docx`, `.md` et `.json`. Il est refusé s'il doit être écrit dans le dossier inventorié, avant tout envoi, et aucun fichier existant n'est remplacé.

Codes de sortie :
- 0 : aucune alerte ;
- 1 : alertes à examiner ;
- 2 : erreur, configuration absente ou envoi refusé.

## Formats lus

| Format | Ce qui est lu |
|---|---|
| .docx, .docm | corps du texte, propriétés (auteur, dernière modification, création) |
| .eml | expéditeur, destinataires, date, objet, texte, noms des pièces jointes |
| .txt, .md | texte |
| autres (PDF, .doc, .msg, tableurs, images) | inventoriés avec leur empreinte, signalés « non lus », jamais envoyés |

Les fichiers de verrouillage de Word (`~$…`) et les fichiers cachés sont ignorés et mentionnés dans le registre.

## Tests et mesure

```
cd outils/inventaire-dossier && python -m unittest discover -s tests -v
python factory/jeux-de-test/F-DOSSIER-01/evaluer.py                    règles seules, gratuit
python factory/jeux-de-test/F-DOSSIER-01/evaluer.py --ia --executions 3   mode IA, payant
```

Les tests automatiques utilisent un faux fournisseur sur votre ordinateur et ne coûtent rien. La mesure avec IA appelle votre fournisseur : chaque exécution est facturée. La mesure porte sur deux dossiers fictifs. Le dossier de développement (12 pièces) a servi à écrire les règles et la consigne. Le dossier de contrôle (16 pièces) a été rédigé à part ; ses écarts ne sont pas affichés par défaut, et ni les règles ni la consigne ne doivent être réglées d'après lui.
