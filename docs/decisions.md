# Registre des décisions (ADR)

Chaque décision structurante est consignée ici. Statuts : Proposée, Acceptée, Remplacée (par ADR-xxx), Abandonnée.

Gabarit :

```
## ADR-xxx - Titre
Date :
Statut :
Contexte :
Options :
Décision :
Conséquences :
```

---

## ADR-001 - Un domaine unique pour tous les projets
Date : 2026-10-31
Statut : Acceptée (choix exprimé par Florian dans le brief initial)
Contexte : le modèle observé chez Sol Irvine utilise un domaine par projet. Florian dispose d'iavocat.be.
Décision : tous les projets sont publiés sous iavocat.be.
Conséquences : un seul nom à faire connaître ; l'isolation technique entre outils passe par l'organisation interne (voir ADR-005).

## ADR-002 - Générateur de site
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Contexte : site de contenu, majoritairement statique, rédigé en Markdown, avec quelques pages outils interactives.
Options : Astro, Eleventy, Hugo, HTML écrit à la main.
Décision (2026-10-31) : Hugo extended, version figée 0.148.2 (celle installée sur le poste de Florian), sans thème tiers, gabarits écrits dans site/layouts. Raisons : binaire unique sans arbre de dépendances npm (surface d'attaque de la chaîne d'approvisionnement réduite, A02), Markdown natif, flux RSS et plan du site intégrés, aucune JavaScript produite par défaut. Astro et Eleventy demandent node_modules ; le HTML à la main ne gère ni RSS ni gabarits.
Conséquences : commandes dans CLAUDE.md ; toute montée de version de Hugo est un changement consigné.
Conséquences : conditionne les commandes indiquées dans CLAUDE.md.

## ADR-003 - Hébergement
Date : 2026-10-31
Statut : Acceptée (choix de Florian, 2026-10-31)
Contexte : site statique, pas de backend. Contraintes : HTTPS, en-têtes de sécurité, localisation des journaux.
Options : Cloudflare Pages, Netlify, GitHub Pages, hébergeur européen.
Décision : GitHub Pages, domaine iavocat.be enregistré chez OVH. Construction et déploiement par GitHub Actions (Hugo figé, ADR-002).
Conséquences :
- GitHub Pages ne permet pas de définir des en-têtes HTTP. La Content-Security-Policy et la Referrer-Policy sont posées en balises <meta> dans chaque page. Ne peuvent pas être appliqués : frame-ancestors, X-Frame-Options, Permissions-Policy, X-Content-Type-Options, HSTS configurable. Risque jugé acceptable parce que le site ne contient ni JavaScript, ni formulaire, ni clé API, et que les outils s'exécutent hors du site (ADR-010). À réexaminer si une page interactive est ajoutée.
- HTTPS : option "Enforce HTTPS" à activer dans les réglages du dépôt après validation du certificat [À VÉRIFIER lors du déploiement].
- DNS chez OVH : enregistrements A/AAAA de l'apex vers les adresses GitHub Pages et vérification du domaine dans GitHub [À VÉRIFIER dans la documentation GitHub au moment de la configuration] ; 2FA sur OVH et GitHub.
- Journaux et adresses IP traités par GitHub : à décrire dans la politique de confidentialité à partir de la déclaration de confidentialité de GitHub [À VÉRIFIER].
- Le dépôt doit être public (ou compte payant) ; cohérent avec la licence MIT (ADR-006).
- Remplace la décision Cloudflare Pages prise le même jour.

## ADR-004 - Outils locaux, clé de l'utilisateur, aucun backend
Date : 2026-10-31
Statut : Acceptée (brief initial), en révision (PLAN_AMELIORATIONS.md, A01 et A03 ; voir ADR-010)
Décision : chaque outil s'exécute chez l'utilisateur avec sa propre clé API. iavocat.be n'opère aucun serveur qui reçoit des données ou des clés.
Conséquences : pas de coût d'API pour le site. L'architecture supprime les flux de données de dossier vers iavocat.be, sans préjuger des qualifications et responsabilités juridiques de chaque acteur (éditeur du site, concepteur de l'outil, avocat utilisateur, fournisseur d'API, hébergeur), qui restent à vérifier par type d'outil [À VÉRIFIER, A03]. En contrepartie, l'installation et la configuration reposent sur l'utilisateur, d'où l'importance des guides.
Note de correction (2026-10-31) : la version initiale affirmait "pas de responsabilité de traitement des données de dossier". Cette conclusion ne découlait pas de l'absence de backend ; elle a été retirée.

## ADR-005 - Chemins ou sous-domaines pour les outils
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Options : A) iavocat.be/outils/<slug> ; B) <slug>.iavocat.be ; C) fiches en chemins, outils exécutables en sous-domaines.
Recommandation initiale : C, pour isoler chaque page qui manipule une clé API.
Décision (2026-10-31) : A, chemins (iavocat.be/outils/<slug>). Aucun outil ne s'exécute dans le navigateur avec une clé (ADR-010), l'argument d'isolation de l'option C tombe. Si un outil navigateur manipulant une clé est un jour admis par décision spécifique, il sera publié sur son propre sous-domaine.

## ADR-006 - Publication et licence du code
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Contexte : un outil local auquel on confie une clé et des documents inspire davantage confiance si son code est lisible.
Options : code ouvert (licence MIT, Apache 2.0, EUPL ou autre), code fermé, mixte.
Décision (2026-10-31) : code des outils sous licence MIT (compatible avec les sources MIT reprises, lisible, réutilisable par les cabinets) ; textes du site sous licence Creative Commons Attribution 4.0 (CC BY 4.0). Résultats de test publiés avec chaque outil.

## ADR-007 - Organisation de la production en Factory
Date : 2026-10-31
Statut : Acceptée avec modification (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Contexte : plusieurs outils à produire avec des agents Claude Code ; besoin de cohérence et de contrôle.
Décision proposée : circuit unique (factory/pipeline.md), agents spécialisés, agent ops-factory chargé des contrôles de passage et de l'amélioration de la Factory, validation de Florian aux étapes "prêt" et "publié".
Conséquences : chaque outil laisse une trace (spécification, rapports, rétrospective) ; la Factory s'enrichit à chaque projet.
Modification (2026-10-31, A05) : trois parcours, léger (contenu, correction mineure), standard (outil local sans IA distante ni donnée de dossier), renforcé (données de dossier, clés, IA distante). En cas de doute, renforcé. Un passage d'étape exige des preuves observables (commande exécutée, sortie, version) ; l'auteur d'une fonctionnalité ne certifie pas seul sa conformité.

## ADR-008 - Réutilisation de projets tiers
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Contexte : plusieurs fiches reprennent des projets open source (MIT, Apache-2.0, AGPL-3.0) ou s'en inspirent.
Décision proposée : MIT et Apache-2.0 acceptés avec mentions de licence conservées et fichier TIERS.md par outil ; AGPL-3.0 exclu pour le code embarqué sauf décision contraire ; projet sans licence identifiée : aucun texte ni code repris, seulement l'idée.
Conséquences : vérification de licence obligatoire à l'étape "prêt".

## ADR-009 - Plugins tiers dans le dépôt (open-pstack, skillboxing)
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable)
Options : A) installer les plugins d'origine, figés sur une version ; B) reprendre leurs principes dans des agents et skills internes (solution livrée) ; C) B maintenant, réévaluer A après un mois d'usage.
Recommandation : C.
Décision (2026-10-31) : C. Réévaluation fin novembre 2026.

## ADR-010 - Modes d'exécution, BYOK et secrets
Date : 2026-10-31
Statut : Acceptée (Décision déléguée par Florian le 2026-10-31 ("décide pour réaliser un projet abouti"), révisable), point 4 restant à exécuter
Contexte : docs/principes-outils.md admettait l'appel direct d'une API depuis une page web avec une clé saisie dans le navigateur, sans décision spécifique ni modèle de menace.
Options à documenter : A) navigateur entièrement local, sans IA distante ; B) application ou service local sur le poste, qui appelle éventuellement une API distante ; C) modèle exécuté sur la machine de l'utilisateur. Appel direct depuis le navigateur avec clé : uniquement par décision spécifique, sur la base de la documentation officielle du fournisseur, du modèle de menace et de tests.
À produire avant arbitrage : matrice fournisseur x mode d'exécution x authentification x données envoyées x source officielle x date de vérification ; politique de secrets (clés dédiées, limites de dépense, révocation, absence de journalisation).
Mesure conservatoire en attendant : aucun outil ne manipule de clé API tant que son architecture n'a pas été approuvée.
Décision (2026-10-31) :
1. Les outils sans IA distante s'exécutent en mode A (navigateur entièrement local) ou B (application locale). P05 Lite est une application locale Python, sans dépendance externe et sans aucun accès réseau (vérifié par test).
2. Un outil qui appelle une IA distante est une application locale (mode B). La clé est lue depuis une variable d'environnement ou un fichier .env local ignoré par git, jamais écrite dans un journal ni dans un rapport. L'application n'ouvre aucun port accessible depuis le réseau (écoute limitée à 127.0.0.1 si une interface web locale est nécessaire).
3. L'appel direct depuis une page web avec clé saisie dans le navigateur est exclu par défaut. Une exception exige une ADR propre.
4. Avant le premier outil à IA distante : matrice fournisseur x authentification x données envoyées x source officielle x date, établie à partir de la documentation officielle à jour. Établie le 2026-10-31 : docs/fournisseurs-ia.md (à revoir à chaque version d'un outil à IA).

## ADR-011 - Premier outil : P05 Lite
Date : 2026-10-31
Statut : Acceptée (choix de Florian, PLAN_AMELIORATIONS.md §13)
Contexte : P09 était proposé comme premier outil, mais sa fiabilité est difficile à démontrer sans le banc F-IDENT-01. P05 dispose d'un mode sans IA.
Décision : le premier outil produit est P05 Lite, contrôle non destructif d'un .docx avant envoi, sans IA ni clé API. P09 vient ensuite.
Conséquences : le premier outil ne dépend pas d'ADR-010. Le jeu de test F-DOCX-01 devient prioritaire. Le mode d'exécution de P05 Lite reste à choisir (A ou B d'ADR-010).

## ADR-012 - Rubrique "Automatiser une prestation"
Date : 2026-10-31
Statut : Acceptée (choix de Florian)
Contexte : deux articles rédigés pour iavocat.be en mars 2026 (grille en quatre critères, matrice standardisation x enjeu) ne trouvaient pas de place dans l'arborescence, et le cahier des charges excluait le contenu réflexif.
Décision : création d'une rubrique "Automatiser une prestation" pour les contenus pratiques sur le modèle économique du cabinet. Les textes sources sont conservés dans contenus/automatiser-une-prestation/ jusqu'à l'initialisation du site.
Conséquences : la charte éditoriale s'applique à ces textes ; leur relecture avant publication porte notamment sur les invitations à prendre contact en fin d'article, au regard des règles de communication de l'avocat [À VÉRIFIER]. Autres candidats à examiner : tutoriel de veille Claude Cowork, fiches "avocat entrepreneur", livre blanc (dossier parent).

## ADR-013 - Identité visuelle : police Inter auto-hébergée, accent brique
Date : 2026-10-31
Statut : Acceptée (choix de Florian, d'après l'examen de quickadd.obsidian.guide)
Contexte : le premier style (texte à empattement, titres système, aucun accent) était jugé trop strict.
Décision : police Inter 4.1 (InterVariable, romain et italique), servie par le site depuis site/static/fonts, licence SIL Open Font License 1.1 (fichier LICENSE-Inter.txt joint), téléchargée depuis la publication officielle github.com/rsms/inter (v4.1). Accent brique (#a23d24 en clair, #ef9478 en sombre), fond papier, cartes surélevées, page d'accueil en sections.
Conséquences : environ 740 Ko de polices, mises en cache par le navigateur ; aucune ressource externe (CSP font-src 'self' inchangée). Empreintes SHA-256 : InterVariable.woff2 693b77d4f32ee9b8bfc995589b5fad5e99adf2832738661f5402f9978429a8e3 ; InterVariable-Italic.woff2 e564f652916db6c139570fefb9524a77c4d48f30c92928de9db19b6b5c7a262a.

## ADR-014 - P09 Lite : pseudonymisation par règles, sans dépendance
Date : 2026-10-31
Statut : Proposée (décision déléguée par Florian le 2026-10-31 ("continue à build les outils"), à valider)
Contexte : la fiche P09 envisageait la bibliothèque stella anonymize (Rust, Apache-2.0). Le plan d'amélioration (A07) exige une mesure du rappel et de la précision par catégorie sur F-IDENT-01 avant toute mise à disposition.
Options : A) règles en Python, bibliothèque standard seule ; B) stella anonymize ; C) modèle local de reconnaissance d'entités.
Décision : A pour la version 0.1.0. Application locale (mode B d'ADR-010), sans IA ni réseau, relecture obligatoire avant enregistrement, table de correspondance locale pour rétablir les noms. F-IDENT-01 comporte un jeu de développement et un jeu de contrôle rédigé par un agent sans accès au code ; seul le second est publié comme mesure.
Conséquences : mesure publiée sur la fiche (jeu de contrôle : rappel 63 %, précision 98 % ; noms de personnes 45 %). B et C restent à qualifier sur F-IDENT-01 ; un nouveau jeu de contrôle sera nécessaire dès que l'actuel aura servi à régler l'outil.

## ADR-015 - P01 : mode avec IA distante
Date : 2026-10-31
Statut : Remplacée (par ADR-019, le 2026-11-01). Décision antérieure : option E, acceptée le 2026-11-01 puis abandonnée le même jour.
Contexte : P01 0.1.0 fonctionne par règles, en local. Sur le dossier de contrôle F-DOSSIER-01, le rattachement des pièces (8/16) et les parties (11/16) sont ses points faibles ; un modèle de langue y apporterait vraisemblablement le plus. La matrice des fournisseurs exigée par ADR-010 (point 4) est établie dans docs/fournisseurs-ia.md (sources officielles consultées le 2026-10-31, 22 points [À VÉRIFIER]).
Constats de la matrice utiles à la décision : l'API directe d'Anthropic ne documente pas de traitement dans l'UE ; OpenAI (point d'accès UE, sous condition de ZDR), Mistral (point d'accès UE) et Google Vertex AI (multirégion eu) en documentent un. Aucun fournisseur ne permet à l'outil de vérifier que le ZDR est actif : il ne peut afficher que la déclaration de l'utilisateur.
Cadre déontologique (révision du 2026-11-01, analyse complète dans docs/deontologie-ia.md, sources dans bibliotheque/) :
- AVOCATS.BE et OVB, lignes directrices sur l'IA : l'avocat pseudonymise les données personnelles (p. 2) et « ne communique jamais de documents ou d'informations couverts par le secret professionnel ou une obligation de confidentialité dans un outil d'IA », sauf s'il est « absolument certain » de travailler « dans un environnement fermé avec des garanties adéquates » (p. 3).
- CNB, guide du 13 mars 2026 (éclairant, non contraignant en Belgique) : les engagements de non-réutilisation ne sont « ni prouvables ni vérifiables » ; seules la pseudonymisation préalable et l'installation du modèle sur les systèmes du cabinet éliminent le risque de souveraineté (p. 15) ; vigilance sur la réidentification par recoupement (p. 13).
- Les extraits que P01 enverrait (intitulés, premières et dernières lignes des pièces, en-têtes de courriel) sont des informations du dossier. La pseudonymisation par P09 ne les fait pas sortir du secret à coup sûr, et P09 Lite 0.1.0 ne trouve aujourd'hui que 45 % des noms de personnes sur le jeu de contrôle.
Options :
A) pas de mode IA pour P01 ; améliorer les règles (avec un nouveau dossier de contrôle) ;
B) mode IA optionnel vers une API distante, tout fournisseur configuré, après pseudonymisation et confirmation ;
C) comme B, limité aux fournisseurs qui documentent un traitement dans l'UE ;
D) mode IA avec un modèle exécuté sur le poste de l'avocat (ADR-010 mode C) : aucune donnée ne quitte la machine ; c'est l'« environnement fermé » au sens strict ;
E) D en premier, puis, en complément optionnel, une API distante limitée aux « prestataires conformes » au sens de docs/deontologie-ia.md §4 (offre professionnelle, pas d'entraînement, ZDR ou conservation courte documentée, traitement UE, contrat article 28 RGPD, pas de fonction avec état), désactivée par défaut, après pseudonymisation, relecture du texte à envoyer et confirmation explicite.
Recommandation (révisée le 2026-11-01, à la demande de Florian : usage local, ou API vers un prestataire conforme) : E.
1. Le mode local sans IA reste le mode par défaut de P01.
2. Premier mode IA : modèle local (D). Il faut d'abord choisir l'environnement d'exécution et un modèle à poids ouverts, puis mesurer installation, temps et qualité sur F-DOSSIER-01 (lien avec P11). Les noms et versions sont `[À VÉRIFIER]` au moment du choix.
3. Mode distant ensuite, uniquement vers les fournisseurs admis (d'après la matrice du 2026-10-31 : Mistral point d'accès UE, Vertex AI multirégion eu, OpenAI point d'accès Europe avec ZDR ; l'API directe d'Anthropic est exclue faute de traitement UE). Condition préalable : améliorer la détection des noms par P09 et la mesurer sur un nouveau jeu de contrôle.
4. L'écran d'envoi dit clairement que l'outil ne peut ni vérifier les garanties du fournisseur ni certifier un « environnement fermé » : l'appréciation reste celle de l'avocat. Il affiche la nationalité du prestataire et le lieu de traitement déclaré.
5. Chaque proposition du modèle (local ou distant) est marquée comme telle et reste « à vérifier ».
Décision (2026-11-01) : E, telle que recommandée. Lecture retenue : « environnement fermé » = modèle local ; « garanties adéquates » d'une API distante = garanties contractuelles appréciées par l'avocat (docs/deontologie-ia.md §3). La nationalité du prestataire est affichée sur l'écran d'envoi, sans exclure. Ordre : modèle local d'abord ; le mode distant attend l'amélioration de la détection des noms par P09.
Conséquences : aucun code d'appel à une API distante pour P01 avant cette amélioration et sa mesure sur un nouveau jeu de contrôle. Prochaine étape : cadrer le mode IA local (environnement d'exécution, modèle à poids ouverts, mesure sur F-DOSSIER-01), ce qui demandera une ADR propre.

## ADR-016 - P02 Lite : rapport sur les définitions, par règles, sans modifier le contrat
Date : 2026-11-01
Statut : Proposée (décision déléguée par Florian le 2026-10-31 ("continue à build les outils"), à valider)
Contexte : la fiche P02 prévoit de regrouper les définitions d'un contrat dans une annexe unique, avec un rapport. Le regroupement exige de réécrire le .docx en conservant sa mise en forme et ses renvois, c'est-à-dire le composant P10, qui n'existe pas. La fiche prévoyait aussi un contrôle par un modèle de langue, que la décision ADR-015 n'a pas encore ouvert.
Options : A) attendre P10 ; B) une version « rapport » seule, par règles, en local, qui ne modifie pas le contrat ; C) B avec un contrôle par IA.
Décision : B pour la version 0.1.0. Application locale (mode B d'ADR-010), bibliothèque standard seule. Mesure sur F-DEF-01 : jeu de développement et jeu de contrôle rédigé par un agent sans accès au code ; seul le second est publié.
Conséquences : la question ouverte de la fiche (annexe en fin de contrat ou article « Définitions » en tête) ne se pose qu'avec la restructuration, reportée. C reste possible après la décision sur ADR-015. Les termes définis sans guillemets hors de l'article des définitions, et les définitions dans les notes de bas de page, ne sont pas reconnus.

## ADR-017 - P03 Lite : rapport de préparation, par règles, sans séparer le contrat
Date : 2026-11-01
Statut : Proposée (décision déléguée par Florian le 2026-10-31 ("continue à build les outils"), à valider)
Contexte : la fiche P03 prévoit de produire, à partir d'un contrat négocié, des conditions particulières et des conditions générales distinctes. Comme pour P02 (ADR-016), produire les deux .docx en conservant mise en forme et renvois exige le composant P10, qui n'existe pas. La partie la plus utile au cabinet est pourtant réalisable sans lui : savoir quelles clauses contiennent encore des données de l'opération avant de réutiliser un contrat comme modèle.
Options : A) attendre P10 ; B) un rapport par règles, en local, qui classe chaque bloc (particulières, générales, mixte) et liste les données propres à l'opération et les renvois internes ; C) B avec un classement par IA.
Décision : B pour la version 0.1.0. Application locale (mode B d'ADR-010), bibliothèque standard seule. Mesure sur F-CPCG-01, avec un jeu de contrôle rédigé par un agent sans accès au code.
Conséquences : la question ouverte de la fiche (produire en plus un modèle anonymisé) reste ouverte ; elle rejoint P09, qui pseudonymise déjà un texte. Le classement est une proposition : la question de savoir si une clause peut être déplacée sans changer l'effet du contrat (ordre de priorité entre documents, opposabilité des conditions générales) relève de l'avocat, pas de l'outil.

## ADR-018 - Bibliothèque de références
Date : 2026-11-01
Statut : Proposée (demande de Florian du 2026-11-01 : classer les textes de référence dans le dépôt pour les réutiliser, et préparer une curation de contenu par le site)
Contexte : les décisions et les fiches d'outils citent des textes déontologiques (lignes directrices AVOCATS.BE et OVB, guide du CNB). Ces textes appartiennent à leurs auteurs. Le dépôt est destiné à être public (ADR-003, ADR-006).
Options : A) copier les PDF dans le dépôt versionné ; B) dossier bibliotheque/ avec catalogue et fiches versionnés (métadonnées, résumé présenté comme tel, passages cités mot pour mot avec la page) et originaux dans bibliotheque/sources/, ignoré par git ; C) uniquement des liens externes.
Décision : B.
Conséquences : les documents du dépôt citent la fiche, pas le PDF. Les URL officielles et les dates d'adoption inconnues portent [À VÉRIFIER]. Une rubrique de veille sur le site (curation) et un script de synchronisation depuis OneDrive restent à cadrer ; ils feront l'objet d'une fiche projet le moment venu.

## ADR-019 - Tous les outils : connexion à une API d'IA, en BYOK
Date : 2026-11-01
Statut : Acceptée (décision de Florian du 2026-11-01 : « tous les produits doivent intégrer une connexion à une API pour inférence IA. On simplifie et on est en mode BYOK »)
Remplace : ADR-015. Complète : ADR-004, ADR-010 (point 2), ADR-016 et ADR-017 (option C désormais ouverte).
Contexte : ADR-015 réservait l'IA à un modèle local d'abord, puis à une liste de prestataires conformes, sous condition d'une meilleure détection des noms par P09. Florian simplifie : chaque outil intègre une connexion à une API d'IA, avec la clé de l'avocat.
Objection consignée (Claude, 2026-11-01) : les lignes directrices AVOCATS.BE et OVB n'admettent la communication d'informations couvertes par le secret à un outil d'IA que dans un « environnement fermé avec des garanties adéquates » (p. 3), et P09 Lite 0.1.0 ne trouve que 45 % des noms de personnes sur son jeu de contrôle. Florian maintient la décision : l'usage de l'IA « relève de la liberté et de la responsabilité de l'avocat(e) » (p. 1), et c'est l'avocat qui choisit son fournisseur et ce qu'il envoie.
Décision :
1. Chaque outil (P01, P02, P03, P05, P09 et les suivants) intègre une connexion à une API d'IA. Application locale (ADR-010, mode B) ; la clé de l'avocat est lue depuis une variable d'environnement ou un fichier .env ignoré par git, jamais journalisée.
2. Sans clé, l'outil ne fonctionne pas (révision de Florian du 2026-11-01 : « faire au plus simple »). Il l'indique clairement et renvoie au guide d'obtention d'une clé. Exception : la pseudonymisation locale de P09 reste sans IA, parce qu'elle est le filtre appliqué avant tout envoi (point 4) ; la faire passer par une API enverrait le texte non pseudonymisé.
3. Choix du fournisseur libre, y compris l'API directe d'Anthropic et un modèle local exposant une API. Pas de liste d'admission. La grille de docs/deontologie-ia.md §4 devient une information affichée.
4. Avant chaque envoi : pseudonymisation locale par P09, affichage du texte qui va partir (l'avocat peut corriger ce que P09 a manqué), écran d'envoi (fournisseur, point d'accès, lieu de traitement et conservation déclarés, nationalité du prestataire, coût estimé, rappel que l'outil ne vérifie pas les garanties du fournisseur), case à cocher. Rien ne part sans elle.
5. Seuls les extraits nécessaires à la tâche partent ; chaque proposition du modèle est marquée comme telle et reste « à vérifier ».
6. Plus de condition préalable liée à P09 ; l'amélioration de la détection des noms reste prioritaire.
Conséquences :
- Un composant commun « connecteur IA » (factory/composants/) porte l'appel aux fournisseurs, l'écran d'envoi et la configuration (fournisseur, point d'accès, modèle, tarifs datés, conservation déclarée), selon docs/fournisseurs-ia.md §5. Son architecture (API natives par fournisseur ou format commun, gestion des erreurs, estimation du coût, tests sans réseau) fera l'objet d'une ADR propre avant tout code.
- Chaque outil devra définir ce que l'IA y apporte et quels extraits partent ; c'est à préciser fiche par fiche.
- Les modes par règles de P01, P02, P03 et P05 cessent d'être des produits. Leur code peut servir de prétraitement ; les jeux de test devront mesurer le résultat avec IA, ce qui suppose une clé et un coût à chaque mesure, et des résultats qui varient d'une exécution à l'autre.
- Connecteur : le plus simple possible (décision de Florian). Piste à vérifier dans l'ADR du connecteur : un seul format d'appel compatible avec l'API d'OpenAI, si les fournisseurs retenus l'acceptent [À VÉRIFIER, notamment pour Anthropic].
- Les fiches du site devront décrire le mode IA, le fait que des données quittent le poste et la responsabilité de l'avocat.

## ADR-020 - Connecteur IA commun : un seul format d'appel (Chat Completions)
Date : 2026-11-01
Statut : Acceptée (Florian, 2026-11-01)
Contexte : ADR-019 impose une connexion à une API d'IA dans chaque outil, avec libre choix du fournisseur. Pour rester simple, le connecteur ne parle qu'un format d'appel : POST {adresse}/chat/completions, clé en `Authorization: Bearer`, réponse lue dans `choices[0].message.content` et `usage`. Vérification de la compatibilité sur la documentation officielle, consultée le 2026-11-01 :
- OpenAI : format natif (https://api.openai.com/v1).
- Anthropic : couche de compatibilité, adresse https://api.anthropic.com/v1/, statut « stable », mais « primarily intended to test and compare model capabilities, and is not considered a long-term or production-ready solution for most use cases ». Limites utiles : `response_format` n'accepte que `json_schema` avec `strict: true` ; `temperature` inférieure à 1 et `top_p` provoquent une erreur 400 sur les modèles récents ; pas d'entrée de fichier ; en-tête `anthropic-workspace-id` requis pour une clé non rattachée à un espace de travail. Source : https://platform.claude.com/docs/en/api/openai-sdk.
- Mistral : « The Mistral Chat Completions API follows the same request structure as OpenAI » ; adresse https://api.mistral.ai/v1. Le point d'accès UE (api.eu.mistral.ai) n'est pas mentionné dans ce guide [À VÉRIFIER]. Source : https://docs.mistral.ai/resources/migration-guides.
- Google, API Gemini : https://generativelanguage.googleapis.com/v1beta/openai/, clé Gemini en Bearer ; « still in beta ». Source : https://ai.google.dev/gemini-api/docs/openai.
- Google Vertex AI : « Only Google Cloud Auth is supported using the OpenAI library » ; jeton d'accès valable une heure, à renouveler. Incompatible avec une simple clé. Source : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/openai.
- Modèle local (Ollama) : http://localhost:11434/v1/ ; une valeur de clé est exigée par le client mais ignorée. Source : https://docs.ollama.com/api/openai-compatibility.
Options : A) un client par fournisseur, avec son API native ; B) un seul client au format Chat Completions, adresse configurable ; C) une bibliothèque tierce d'abstraction (contraire à ADR-010 : bibliothèque standard tant que possible).
Décision : B.
1. Composant factory/composants/connecteur-ia/, Python bibliothèque standard (urllib), une fonction d'appel unique.
2. Requête minimale : `model`, `messages` (un message système, un message utilisateur), `max_tokens`. Pas de `temperature`, de `top_p`, de `response_format`, d'outils ni de fonction avec état : c'est ce qui passe chez tous les fournisseurs listés. Le modèle est invité à répondre en JSON dans la consigne ; le connecteur extrait et valide ce JSON, et signale une réponse illisible au lieu de deviner.
3. Configuration par outil (fichier non versionné, `config.example` versionné) : adresse, modèle, nom de la variable qui contient la clé, en-têtes supplémentaires éventuels (`anthropic-workspace-id`), tarifs et date de relevé, et la fiche d'information du fournisseur (lieu de traitement, conservation déclarée, ZDR déclaré, nationalité) affichée sur l'écran d'envoi (ADR-019, point 4).
4. Préréglages fournis pour OpenAI, Anthropic, Mistral, API Gemini et modèle local. Vertex AI n'est pas proposé (pas de clé simple).
5. Coût estimé avant envoi à partir des tarifs configurés ; coût réel calculé après coup à partir de `usage`.
6. Tests sans réseau : un faux serveur sur 127.0.0.1 (http.server) qui imite les réponses et les erreurs (401, 429, 500, réponse non JSON). Aucun test n'appelle un vrai fournisseur ; une mesure réelle se lance à la main, avec la clé de Florian.
Conséquences :
- Anthropic prévient que cette couche n'est pas une solution de production à long terme ; un passage à l'API native resterait possible plus tard, sans changer les outils, puisque tout passe par le connecteur.
- L'API Gemini est en bêta ; les paramètres non listés y sont ignorés sans erreur.
- Le point d'accès UE de Mistral reste à confirmer avant de le proposer comme préréglage.
- La consigne JSON sans `response_format` peut produire des réponses mal formées : le connecteur doit le détecter et l'outil le signaler.

## ADR-021 - Outils autonomes : chaque outil embarque sa copie des composants
Date : 2026-11-01
Statut : Acceptée (principe posé par Florian le 2026-11-01)
Contexte : le connecteur IA (ADR-020) et la pseudonymisation (P09) servent à plusieurs outils. Florian : un avocat doit pouvoir télécharger et essayer un seul outil, sans les autres, « quitte à dupliquer les fonctionnalités de l'un vers l'autre ». L'objectif est de le rassurer sur un premier usage, avant qu'il élargisse sa boîte à outils.
Options : A) une bibliothèque commune à installer à côté des outils ; B) copie des composants ajoutée au moment de l'empaquetage seulement ; C) copie versionnée dans le dossier de chaque outil, synchronisée par un script et contrôlée par la vérification.
Décision : C.
1. Un outil ne dépend d'aucun autre outil ni d'aucun fichier hors de son dossier. Le dossier de l'outil dans le dépôt est exactement ce qui est téléchargé.
2. Les composants utilisés sont copiés dans `outils/<slug>/src/` et déclarés dans `outils/<slug>/COMPOSANTS.md` (nom, version, source).
3. Une copie ne se modifie jamais dans l'outil : on modifie la source (factory/composants/ ou l'outil d'origine, pour P09), puis `python scripts/synchroniser_composants.py`. `scripts/verifier.py` échoue si une copie s'écarte de sa source.
4. Un composant mis à jour impose de republier chaque outil qui l'embarque (nouvelle archive, nouvelle empreinte).
Conséquences :
- Chaque outil qui envoie un texte à une IA embarque le connecteur IA et la pseudonymisation de P09.
- L'archive de chaque outil grossit un peu ; la duplication est voulue.
- Les tests d'un composant restent dans sa source ; un outil teste son propre usage du composant.

## ADR-022 - jerlash.labs : nom, identité, site de base
Date : 2026-11-01
Statut : Acceptée (décision de Florian du 2026-11-01 : « livrer plutôt que construire »)
Contexte : après deux jours de travail, rien n'est publié. Le projet prend le nom jerlash.labs, avec une identité fournie (jerlash-identite.zip : design system et maquette).
Décision :
1. Le site est un site Hugo de base aux couleurs de jerlash : accueil, blog, à propos, mentions légales, confidentialité. Les sections outils, guides, automatiser, nouveautés et précautions sont conservées en brouillon, hors du site publié, jusqu'à ce qu'un contenu soit prêt.
2. Le blog reprend les articles du dossier `articles` marqués « statuts: à publier », par `scripts/importer_articles.py`. Le dossier source reste hors du dépôt public : les brouillons restent privés.
3. Remplace ADR-013 (identité visuelle) : polices Schibsted Grotesk et IBM Plex Mono (SIL OFL), auto-hébergées ; couleurs et composants du design system.
4. Amende ADR-002 : les seuls scripts sont `js/bundle.js` du design system et son lanceur `js/init.js` (une ligne), servis par le site (fonds pixel). CSP `script-src 'self'` ; aucun script en ligne, aucun script externe. La vérification le contrôle.
5. Dépôt GitHub public `jerlash-labs`, publication d'abord à l'adresse gratuite de GitHub Pages. Le domaine est choisi plus tard (« .labs » n'est pas une extension existante).
Conséquences : tout le reste passe au backlog. Le code des outils reste dans le dépôt, sans lien depuis le site.
