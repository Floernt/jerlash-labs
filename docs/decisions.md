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
Statut : Proposée (à trancher par Florian ; aucun code d'appel à une IA n'est écrit avant sa décision)
Contexte : P01 0.1.0 fonctionne par règles, en local. Sur le dossier de contrôle F-DOSSIER-01, le rattachement des pièces (8/16) et les parties (11/16) sont ses points faibles ; un modèle de langue y apporterait vraisemblablement le plus. La matrice des fournisseurs exigée par ADR-010 (point 4) est établie dans docs/fournisseurs-ia.md (sources officielles consultées le 2026-10-31, 22 points [À VÉRIFIER]).
Constats de la matrice utiles à la décision : l'API directe d'Anthropic ne documente pas de traitement dans l'UE ; OpenAI (point d'accès UE, sous condition de ZDR), Mistral (point d'accès UE) et Google Vertex AI (multirégion eu) en documentent un. Aucun fournisseur ne permet à l'outil de vérifier que le ZDR est actif : il ne peut afficher que la déclaration de l'utilisateur.
Options :
A) pas de mode IA pour P01 ; améliorer les règles (avec un nouveau dossier de contrôle) ;
B) mode IA optionnel, application locale (ADR-010 mode B) : seuls les extraits nécessaires partent (intitulé, premières et dernières lignes de chaque pièce, en-têtes de courriel), après pseudonymisation par P09 et confirmation explicite de l'utilisateur, avec affichage préalable du fournisseur, du point d'accès, de la taille, du coût estimé et de la déclaration de conservation ; fournisseur au choix dans un fichier de configuration ;
C) comme B, mais limité aux fournisseurs qui documentent un traitement dans l'UE.
Recommandation : B, avec un écran d'envoi qui affiche le lieu de traitement déclaré, et C comme réglage par défaut. Le mode local reste le mode par défaut ; le mode IA complète les champs « à vérifier » et propose les rattachements, chaque proposition étant marquée comme venant du modèle.
Points que Florian doit trancher : la compatibilité de principe de l'envoi d'extraits pseudonymisés avec le secret professionnel (docs/fournisseurs-ia.md §5.5) ; le choix entre B et C ; la liste des fournisseurs proposés.

## ADR-016 - P02 Lite : rapport sur les définitions, par règles, sans modifier le contrat
Date : 2026-11-01
Statut : Proposée (décision déléguée par Florian le 2026-10-31 ("continue à build les outils"), à valider)
Contexte : la fiche P02 prévoit de regrouper les définitions d'un contrat dans une annexe unique, avec un rapport. Le regroupement exige de réécrire le .docx en conservant sa mise en forme et ses renvois, c'est-à-dire le composant P10, qui n'existe pas. La fiche prévoyait aussi un contrôle par un modèle de langue, que la décision ADR-015 n'a pas encore ouvert.
Options : A) attendre P10 ; B) une version « rapport » seule, par règles, en local, qui ne modifie pas le contrat ; C) B avec un contrôle par IA.
Décision : B pour la version 0.1.0. Application locale (mode B d'ADR-010), bibliothèque standard seule. Mesure sur F-DEF-01 : jeu de développement et jeu de contrôle rédigé par un agent sans accès au code ; seul le second est publié.
Conséquences : la question ouverte de la fiche (annexe en fin de contrat ou article « Définitions » en tête) ne se pose qu'avec la restructuration, reportée. C reste possible après la décision sur ADR-015. Les termes définis sans guillemets hors de l'article des définitions, et les définitions dans les notes de bas de page, ne sont pas reconnus.
