# Journal des versions

## 0.1.0 - 2026-10-31

Première version (P05 Lite). Avant publication, corrections issues de la relecture indépendante du 2026-10-31 :

- liens relatifs, chemins réseau et serveurs intranet traités comme sensibles (auparavant classés comme liens publics) ;
- termes sensibles recherchés dans tout le fichier (codes de champ, textes alternatifs, customXml, SmartArt, graphiques), avec unification des apostrophes, tirets et traits d'union insécables ;
- texte masqué ou blanc détecté à travers l'héritage des styles et les valeurs par défaut du document ;
- propriétés trouvées par leur relation, quel que soit leur chemin ;
- contenu importé (altChunk), macros renommées, commentaires orphelins ou de casse différente détectés ;
- champs INFO, TITLE, SUBJECT, KEYWORDS, COMMENTS, IMPORT et HYPERLINK vers un fichier signalés ;
- déclarations XML refusées quel que soit l'encodage ; toute erreur de lecture produit « analyse impossible » ;
- deux documents de même nom produisent deux rapports distincts ;
- le verdict favorable signale l'absence de liste de termes.

- Quatorze contrôles sur un .docx : commentaires, modifications suivies, texte masqué ou invisible, marqueurs à compléter et surlignage, noms d'autres dossiers (liste fournie par l'utilisateur), macros, propriétés du document, personnes mentionnées, champs révélateurs, liens et chemins externes, objets incorporés, réglages et variables, métadonnées des images, notes.
- Statut explicite par contrôle : détecté, non détecté dans les contrôles réalisés, non vérifié, erreur.
- Rapport texte, HTML autonome et JSON ; fenêtre graphique ; ligne de commande avec codes de sortie.
- Fichier analysé ouvert en lecture seule ; empreinte SHA-256 comparée avant et après l'analyse.
- Aucune dépendance hors de la bibliothèque standard de Python ; aucun accès réseau.
