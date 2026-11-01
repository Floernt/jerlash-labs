# Journal des versions

## 0.1.0 - 2026-11-01

Première version (P02 Lite : rapport seul, mode local).

- Lecture des .docx (corps du texte et tableaux, sans le texte masqué, supprimé ou déplacé), .txt et .md.
- Repérage des définitions : article ou annexe « Définitions », tableaux « Terme | Définition », « ci-après », « on entend par », « il faut entendre par », définitions entre parenthèses.
- Glossaire : définition, lieu et nombre d'emplois de chaque terme, singulier et pluriel confondus.
- Points à examiner :
  - définition répétée, avec libellés identiques ou divergents ;
  - terme défini jamais employé ;
  - terme écrit avec des majuscules sans définition ;
  - graphie différente d'un terme défini ;
  - terme employé avant sa définition en cours de texte.
- Rapport en .docx, Markdown et JSON, sans jamais remplacer un fichier. Fenêtre et ligne de commande avec codes de sortie. Aucune dépendance. Aucun accès réseau.

Avant publication, 18 corrections issues de la relecture indépendante du 2026-11-01 (détail dans `verifications/2026-11-01-revue.md`) :

- temps de calcul borné sur les contrats longs et les textes hostiles ;
- suivi des modifications, zones de texte, titres numérotés par Word et tableaux à trois colonnes correctement lus ;
- formules belges de définition et pluriels en -aux reconnus ;
- plus de faux « jamais employé » sur une ligne courte sans point ;
- erreurs toujours affichées dans la fenêtre ; rapport Markdown sans HTML actif.
