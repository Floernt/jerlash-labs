# Journal des versions

## 0.1.0 - 2026-11-01

Première version (P03 Lite : rapport de préparation, mode local).

- Lecture des .docx (corps du texte et tableaux, sans le texte masqué, supprimé ou déplacé), .txt et .md.
- Découpage en blocs : comparution, articles, signatures.
- Repérage des données propres à l'opération : parties et personnes, adresses, identifiants, montants, dates, quantités.
- Classement proposé pour chaque bloc : conditions particulières, conditions générales, clause mixte à épurer.
- Liste des renvois internes.
- Rapport en .docx, Markdown et JSON, sans jamais remplacer un fichier. Fenêtre et ligne de commande avec codes de sortie. Aucune dépendance. Aucun accès réseau.

Avant publication, 20 corrections issues de la relecture indépendante du 2026-11-01 (détail dans `verifications/2026-11-01-revue.md`). Toutes empêchent qu'une clause qui contient encore une donnée de l'opération soit présentée comme réutilisable :

- montants, dates, identifiants et adresses écrits à la belge reconnus (« EUR 12.500 », « 1/3/26 », « BE0712345630 », « Rue de la Loi, 16 ») ;
- noms des parties retrouvés dans tout le contrat, même cités sans forme sociale ou en capitales ;
- intitulés et clauses en capitales analysés ;
- blocs de signatures et intitulés inhabituels (« Article 4bis », « § 5 ») correctement découpés ;
- un « Prix » ou un « Objet » reste en conditions particulières même sans donnée repérée ;
- temps de calcul borné (un texte hostile de 128 Ko : 104 s, puis 0,16 s) ;
- pas de rapport incomplet en cas d'échec d'écriture.
