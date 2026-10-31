# F-DOCX-01 - Contrat de prestation fictif chargé de pièges

Version du jeu : 1.0 (2026-10-31). Données entièrement fictives : les noms suivis de « (fictif) », Fictivia SRL, Durand Fictif SA, Cabinet Fictif SRL et serveur-fictif n'existent pas.

Utilisé par : P05 (contrôle avant envoi). Prévu pour : P04.

## Pièces

Toutes produites par `generer.py` (bibliothèque standard, résultat identique octet par octet à chaque exécution). Pour modifier une pièce, modifier le générateur, puis lancer `python -I generer.py` ; un test vérifie que les pièces versionnées correspondent au générateur.

| Pièce | Contenu | Ouverture dans Word |
|---|---|---|
| contrat-pieges.docx | Au moins un exemple de chaque piège : commentaire ; insertion, suppression et changement de mise en forme suivis (corps et en-tête) ; texte masqué, en blanc, en 1 pt, masqué par style ; `[●]`, `[À COMPLÉTER : lieu]`, `XXX`, « note interne », surlignage ; champs FILENAME \p et AUTHOR (et PAGE, qui ne doit pas être signalé) ; lien SharePoint et lien public ; modèle attaché sur un chemin réseau ; propriétés (auteur, dernière modification, titre, mots-clés, société, responsable, propriété personnalisée NumeroDossier) ; relecteur dans people.xml ; suivi des modifications activé ; variable de document ; photo JPEG avec segment EXIF ; note de bas de page ; nom d'un autre dossier (« Autre-Client SA ») | Vérifiée le 2026-10-31 (Word, automatisation COM, lecture seule, sans message de réparation) |
| contrat-propre.docx | Le même type de contrat sans aucun piège, propriétés vides | Vérifiée le 2026-10-31 |
| contrat-macros.docm | Projet de macros et classeur incorporé factices | Non : contenus factices, pièce destinée à l'analyseur seulement |
| contrat-protege.docx | En-tête de conteneur chiffré (format des documents protégés par mot de passe) | Non (attendu) |
| contrat-tronque.docx | Les 400 premiers octets de contrat-propre.docx | Non (attendu) |

Empreintes SHA-256 (version 1.0) :

```
94d90cfe8196f301b5e8ce1aa445e30886cf29a71c9e6b12f6dafd5c7ef6c1b7  contrat-pieges.docx
c815ad124d4388dc1ab0f7c9c0dafc281dc47aaea0caa56c2fe555e07663332a  contrat-propre.docx
9bc57d9e887a1519579e0813a87db1bf94c287e4207c1b9162759eb6f3f41cd8  contrat-macros.docm
a899fb4496afa7230c378d5be03cf3461990994993110fd2dad3257111081275  contrat-protege.docx
a52f3c3117e31c1633eb36b3d86fa668b053b63355a201f8ae94527d760e0b5b  contrat-tronque.docx
```

## Résultats attendus

`attendu/P05.json` : niveau global attendu par pièce, statut attendu par contrôle, fragments qui doivent figurer (ou ne pas figurer) dans les constats. Lu directement par `outils/controle-avant-envoi/tests/test_jeu_f_docx_01.py`.

## Limites du jeu

Les pièces sont écrites à la main au format OOXML. Des documents produits par d'autres versions de Word, par LibreOffice ou par des outils de génération peuvent contenir des structures absentes d'ici (zones de texte, contrôles de contenu, commentaires modernes, glossaire). À compléter à partir des cas signalés par les utilisateurs, reproduits sur des documents fictifs.
