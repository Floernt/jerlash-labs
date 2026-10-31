# F-DOSSIER-01 — Dossier contractuel fictif

Version 1.0, 31 octobre 2026. Ce dossier est entièrement fictif : les personnes, les sociétés et leurs numéros d'entreprise sont inventés. Les numéros d'entreprise ont une somme de contrôle valide.

## Le dossier

Brasserie du Condroz SRL, cliente du cabinet, s'approvisionne chez Embouteillages de la Meuse SA. Douze pièces racontent la relation :
- un projet de contrat ;
- le contrat signé en mars 2023 ;
- un avenant de prix signé ;
- un second avenant resté à l'état de projet ;
- les conditions générales du fournisseur, que le contrat n'applique qu'en partie ;
- une réclamation et une négociation par courriel ;
- une note de réunion ;
- la lettre de résiliation de juin 2025.

S'y mêlent trois pièces qu'un inventaire doit écarter ou signaler :
- un modèle du cabinet ;
- le contrat d'un autre client ;
- un PDF sans couche texte, qui imite un scan.

Ce jeu sert à mesurer P01, l'inventaire d'un dossier contractuel. Il pourra aussi servir à P02 (glossaire des définitions) et à P03 (conditions particulières et générales).

## Fichiers

```
sources-controle/   dossier de contrôle (16 pièces), rédigé à part, sans accès à l'outil : ne sert qu'à mesurer
pieces-controle/    le dossier de contrôle tel que l'outil le reçoit
attendu/P01-controle.json, attendu/P01-planchers.json   inventaire attendu du contrôle ; planchers de non-régression
evaluer.py          mesure P01 sur les deux dossiers (écarts du contrôle non affichés par défaut)
sources/            un fichier par pièce : en-tête (nom, auteur, champs du courriel), puis texte
generer.py          produit pieces/ (.docx avec propriétés, .eml, .txt, PDF sans texte)
pieces/             le dossier tel que l'outil le reçoit
attendu/P01.json    inventaire attendu : type, statut, date, parties, rattachement, document qui fait foi, alertes
```

```
python -I factory/jeux-de-test/F-DOSSIER-01/generer.py             régénérer
python -I factory/jeux-de-test/F-DOSSIER-01/generer.py --verifier  contrôler que pieces/ correspond aux sources
```

## Ce qui rend le dossier difficile

- **Le projet v3 contredit le contrat signé** (prix, durée, conditions générales). L'inventaire doit retenir le contrat signé comme celui qui fait foi.
- **L'avenant 2 n'est ni signé ni daté**, et la lettre de résiliation le déclare sans objet.
- **Les conditions générales ne s'appliquent que pour leur article 7**, ce que seul l'article 4 du contrat révèle.
- **La résiliation n'est prouvée par aucun accusé d'envoi recommandé** au dossier.
- **Le contrat d'un autre client** se trouve dans le dossier, sous le nom « Précédent » : c'est une alerte de confidentialité.
- **Le scan PDF n'a pas de texte** : l'outil doit le dire, au lieu de deviner son contenu d'après son nom.
