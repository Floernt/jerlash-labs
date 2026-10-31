# Journal des versions

## 0.1.0 - 2026-10-31

Première version (P01, mode local).

- Lecture des .docx (corps du texte et propriétés), .eml et .txt. Les autres formats sont inventoriés avec leur empreinte et signalés « non lus ».
- Classement par règles : type, statut, date, parties, rattachement, document qui fait foi. Chaque conclusion garde son indice.
- Alertes :
  - pièce non lue ;
  - acte non signé ;
  - pièce sans partie commune avec le dossier ;
  - précédent ;
  - statut à vérifier ;
  - doublon ;
  - envoi recommandé sans preuve ;
  - fichiers techniques ignorés.
- Registre en .docx (vérifié dans Word), en Markdown et en JSON, écrit hors du dossier inventorié, sans jamais remplacer un fichier.
- Fenêtre et ligne de commande avec codes de sortie. Aucune dépendance. Aucun accès réseau.

Avant publication, corrections issues de la relecture indépendante du 2026-10-31 (détail dans `verifications/2026-10-31-securite.md`) :

- le registre ne peut aboutir dans le dossier inventorié par aucun chemin : autre casse, nom court, jonction, lecteur substitué ;
- « signé » n'est plus déduit d'un « NON signé », d'un verbe, d'une citation ou d'un texte masqué ; une pièce dite signée par son seul nom de fichier n'est jamais présentée comme faisant foi ;
- un courrier qui cite un contrat reste un courrier ; un courrier qui conteste une résiliation n'est plus lu comme une résiliation ;
- dates impossibles écartées ; date d'un courriel prise dans son en-tête ;
- pièces jointes des courriels, dossiers cachés, liens et dossiers illisibles signalés ; liens et jonctions non suivis ;
- un fichier verrouillé ou corrompu n'arrête plus l'inventaire ; toute erreur imprévue donne le code 2 ;
- registre toujours lisible par Word, quels que soient les caractères des noms de fichiers ;
- temps de calcul borné ; fenêtre qui affiche toute erreur ; dossier vide signalé ; texte UTF-16 lu.
