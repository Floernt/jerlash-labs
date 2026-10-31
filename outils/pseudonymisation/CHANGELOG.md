# Journal des versions

## 0.1.0 - 2026-10-31

Première version (P09 Lite).

- Détection par règles de douze catégories : personnes, sociétés, adresses, numéro national, numéro d'entreprise ou de TVA, IBAN, carte de paiement, courriel, téléphone, date de naissance, plaque, référence de dossier.
- Les numéros national, d'entreprise, IBAN et de carte ne sont retenus que si leur somme de contrôle est juste.
- Chaque nom trouvé, ou fourni par l'utilisateur, est recherché dans tout le texte, nom de famille seul compris.
- Un même marqueur désigne toujours la même donnée. La table de correspondance permet de rétablir les données dans la réponse de l'IA, même quand celle-ci a légèrement modifié les marqueurs.
- La fenêtre permet de relire, de corriger et d'ajouter une donnée. L'enregistrement n'est possible qu'une fois la relecture confirmée.
- Ligne de commande : `pseudonymiser` (avec `--liste`, `--termes`, `--exclure`) et `retablir`.
- Le texte peut être collé, ou lu dans un fichier .txt ou .md, ou dans le corps d'un .docx.
- Aucun fichier n'est jamais remplacé. Aucune dépendance hors de la bibliothèque standard. Aucun accès réseau.
- Mesure sur F-IDENT-01 v1.0, jeu de contrôle : rappel de 63 %, précision de 98 %. Détail dans la fiche.

Avant publication, corrections issues de la relecture indépendante du 2026-10-31 :

- la fenêtre n'enregistre que le texte pseudonymisé affiché et relu ; toute modification du texte d'origine décoche la case de relecture et bloque l'enregistrement ;
- un nom que les règles ne savent lire qu'en partie (lettres d'Europe centrale, apostrophe inhabituelle, McDonald) n'est plus tronqué : il est remplacé en entier ou pas du tout ;
- le texte est normalisé (Unicode NFC) avant la détection : un texte copié depuis un PDF ou un Mac n'est plus remplacé à moitié ;
- deux détections qui se chevauchent sont fusionnées au lieu que l'une efface l'autre ; une donnée conservée par l'utilisateur ne masque plus sa voisine ;
- un nom de famille n'est recherché ailleurs qu'avec sa majuscule (« Porte » ne remplace plus « porte ») et sous sa forme exacte (ß) ; le nom de famille retenu est le dernier, particules comprises ;
- le rétablissement ne prend plus « la personne 1 » pour un marqueur, et signale les formes approchées qu'il remplace ;
- les marqueurs déjà présents dans le texte ne sont jamais réutilisés ;
- un nouveau document ne reprend pas les choix faits sur le précédent ;
- un fichier texte en UTF-16 est lu correctement, et un texte illisible est refusé ;
- temps de calcul borné (1 Mo en environ 2 s, entrées hostiles comprises) et texte limité à 5 Mo ;
- un même numéro de téléphone écrit avec ou sans +32 reçoit un seul marqueur.
