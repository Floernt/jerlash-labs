# Jeux de test

Dossiers entièrement fictifs. Aucune donnée réelle, même pseudonymisée.

Nommage : `F-<THÈME>-<NN>` (exemple : F-DOSSIER-01). Chaque jeu contient :

```
F-DOSSIER-01/
  README.md        description du dossier fictif
  pieces/          documents
  attendu/         un fichier <ID-outil>.md par outil : résultats attendus
  resultats/       un fichier par exécution : AAAA-MM-JJ-<ID>-v<version>.md
```

Jeux prévus :

- F-DOSSIER-01 : dossier contractuel de fourniture, avec avenants et échanges (P01, P02, P03), livré : dossier de développement et dossier de contrôle.
- F-DOCX-01 : contrat .docx chargé de pièges (commentaires, métadonnées, renvois cassés) (P04, P05).
- F-IDENT-01 : textes contenant des identifiants belges fictifs (P09), livré : jeu de développement et jeu de contrôle.
