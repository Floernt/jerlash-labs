# Journal de bord

Une entrée par session de travail, la plus récente en haut. Format :

```
## AAAA-MM-JJ - Titre court
Fait :
Décisions : (renvoi vers ADR si applicable)
Problèmes / points ouverts :
Prochaine étape :
```

## 2026-11-03 - Livrables Proton, calendrier mensuel, refonte du site, Toolkit P14
Fait :
- Archive Proton du 2026-11-03 examinée. Les sources sont rangées hors dépôt dans `../sources-proton/2026-11-03/` (voir son LISEZ-MOI ; référentiel restreint et tests adverses du kit MCP à ne jamais versionner). Fiches P14 à P19 créées. Calendrier d'un projet par mois dans BACKLOG.md : P14 → P19 → P18 → P16 → P17 → P15, puis la suite.
- Site : le blog devient Revue › Perspectives (`/fr/revue/perspectives/`, `/en/review/perspectives/`). Alias de redirection `/blog/`, `/fr/blog/` et `/en/blog/` vérifiés ; seul le flux RSS change d'adresse. Gabarits `revue/` et `toolkit/` créés, ainsi que le partiel `bloc-statut.html`. Menu « Revue ». Rubrique Éthique en brouillon, avec la page Précautions (liens des fiches outils mis à jour). `scripts/verifier.py` attend désormais `fr/revue/perspectives/index.xml`.
- Toolkit P14 « Gouverner l'IA au cabinet » (nom provisoire) converti en 9 pages dans `site/content/outils/gouverner-l-ia-au-cabinet/`. Parcours réordonné à la demande de Florian : la gouvernance d'abord, la charte en dernier, qui ancre les choix faits en chemin. Le rappel sur le règlement IA ne figure qu'à deux endroits (charte, sources). « Pourquoi les chartes échouent » : ajout d'une seconde limite, l'absence de mise en œuvre.
- Florian a relu « Pourquoi les chartes échouent » et l'a passée en `draft: false`. Les 8 autres pages du Toolkit restent en brouillon.
- `docs/politique-publication.md` créé et validé. Charte éditoriale, cahier des charges (§5, §7) et CLAUDE.md alignés.
Décisions : ADR-024 (architecture Recherche, Outils, Revue, Éthique ; point 6 : reflexions.florianernotte.be garde la réflexion généraliste), proposée. ADR-025 (un projet par mois, piste Outils en parallèle), proposée. ADR-026 (éditeur jerlash.labs par défaut ; Toolkit sous CC BY-NC 4.0), acceptée. Règlement IA limité à un rappel (décision de Florian). Politique de publication validée.
Problèmes / points ouverts :
- ATTENTION, avant tout push sur `main` : « Pourquoi les chartes échouent » est la seule page du Toolkit en `draft: false`. Elle serait publiée seule, sans sa page parente (en brouillon) et hors menu, et sans traduction anglaise. Il faut soit remettre `draft: true`, soit attendre que tout le Toolkit soit relu.
- Rien n'est commité. La branche est `dev`.
- Toolkit : relire les 8 autres pages ; lever les 21 marqueurs `[À VÉRIFIER]` / `[À COMPLÉTER]` ; trois passages de la page relue semblent inachevés (ligne 8 « où elle on s'arrête », ligne 31 « Deux de ces faiblesses spécifiques… », ligne 33 phrase sans verbe principal).
- Questions en attente de Florian : nom français définitif ; autorisation d'usage interne à côté de CC BY-NC ; une phrase sur le recrutement et les modes alternatifs de règlement des litiges (annexe III) ; points relevés à la conversion (voir BACKLOG) ; validation d'ADR-024 (libellés, slugs anglais) et d'ADR-025.
- Kit MCP (P18) : le code C3 annoncé est absent de l'archive ; à récupérer en décembre.
- Traductions : 16 pages à traiter, dont les 9 du Toolkit (à traduire après relecture du français) et 6 pages obsolètes, déjà signalées avant la session.
Prochaine étape : Florian poursuit la relecture du Toolkit dans l'ordre du parcours (gouvernance, données, homologation, supervision, opérations, charte, sources). Ensuite : levée des marqueurs, téléchargements (zip, charte .docx), traduction, entrées Outils et Éthique au menu, publication et post LinkedIn.

## 2026-11-01 - Blog : fin de l'import, retrait de Tayori
Fait : décision de Florian, les articles de site/content/blog/ sont la seule version et se relisent sur place. scripts/importer_articles.py et son contrôle dans verifier.py supprimés ; en-tête d'import retiré des 9 articles ; CLAUDE.md, ADR-022 (révisée) et backlog à jour. Mentions de Tayori retirées de « L'intelligence artificielle n'innovera pas à votre place » (FR/EN) : deux phrases supprimées, « y retrouve » devient « retrouve ainsi ». verifier.py --publication : 23/23. dev poussée.
Non fait : suppression des 9 fichiers sources de ../articles (projet: tayori), refusée par le contrôle des permissions ; à faire par Florian ou à autoriser.
Prochaine étape : fusion dev → main pour publier.

## 2026-11-01 - Pages légales remises en ligne, ADR-023 acceptée
Fait :
- Décisions de Florian : le site ne fournit aucun service, donc ni BCE, ni TVA, ni adresse de contact, ni référence aux règles de l'Ordre ; pas de phrase de contact ni de security.txt. ADR-023 acceptée. HTTPS activé.
- Mentions légales et confidentialité (FR/EN) réécrites, publiées et liées depuis le pied de page. Vérifié sur docs.github.com : adresse de GitHub, Inc. ; GitHub Pages journalise l'adresse IP des visiteurs « for security purposes », sans durée de conservation indiquée (rien d'affirmé à ce sujet).
- scripts/verifier.py --publication : 24/24. Branche dev poussée ; gh absent, PR dev → main à ouvrir sur GitHub.
Points ouverts (Florian) : fusionner dev dans main pour publier ; relire l'anglais et l'accueil ; glossaire de traduction. La traduction de outils/inventaire-dossier (brouillon) est obsolète.
Prochaine étape : le chantier « Maintenant » ne contient plus que des relectures ; choisir le prochain chantier dans « Ensuite ».

## 2026-11-01 - jerlash.labs : site de base, blog, cap sur la livraison
Fait :
- Décision de Florian : le projet devient jerlash.labs ; livrer plutôt que construire. ADR-022 (Acceptée). BACKLOG.md réécrit (Maintenant, Ensuite, Plus tard) ; CHANGELOG.md créé.
- Travail en cours commité (ADR-015 à 021, connecteur IA, P01 0.2.0).
- Identité jerlash (jerlash-identite.zip) appliquée au site Hugo : tokens et composants du design system, polices Schibsted Grotesk et IBM Plex Mono, logo, fonds pixel (bundle.js + init.js, CSP script-src 'self'). Nouvel accueil, en-tête, pied de page, gabarits du blog et des pages.
- 18 pages (outils, guides, automatiser, nouveautés, précautions) passées en brouillon ; taxonomie désactivée ; CNAME retiré ; pages légales et À propos renommées jerlash.labs.
- scripts/importer_articles.py : 9 articles « statuts: à publier » importés depuis ../articles (hors dépôt), mode --verifier branché dans scripts/verifier.py.
- Publication : adresse fournie par actions/configure-pages, liens internes compatibles avec un sous-chemin (vérifié en construisant sous /jerlash-labs/) ; archives des outils plus publiées. scripts/verifier.py : 23/23.
Points ouverts (Florian) : créer le dépôt public jerlash-labs ; 11 marqueurs des pages légales (adresse de contact, mentions légales, journaux GitHub) ; relire l'accueil et les articles.
Prochaine étape : push sur GitHub, activation de Pages, publication.

## 2026-11-01 - P01 0.2.0, mode IA
Fait :
- Spécification projets/P01-mode-ia-spec.md, validée par Florian : l'IA ne traite que les parties et le rattachement ; un seul envoi par dossier ; seuils 14/16 et 13/16 sur le dossier de contrôle (plus mauvais de trois exécutions).
- P01 embarque connecteur-ia et pseudonymisation (COMPOSANTS.md, ADR-021). analyse.inventorier découpé en classer et conclure. Nouveau module ia.py : extraits plafonnés (2 000 caractères par pièce, 80 000 au total), numéros à la place des noms de fichiers, pseudonymisation P09 avec une table unique, réponse JSON contrôlée (pièce inconnue, marqueur inconnu, auto-rattachement écartés et signalés), fusion (confirmé, « (modèle) », « (à vérifier) » avec alerte).
- Ligne de commande : confirmation « oui », registre refusé avant tout envoi ; fenêtre : écran d'envoi du connecteur, appel dans un fil d'exécution. Sans configuration ni clé, l'outil s'arrête.
- Tests : 50 (dont 12 du mode IA et 3 de la fenêtre) avec un faux fournisseur sur 127.0.0.1, tout autre accès réseau bloqué ; seul le connecteur importe des modules réseau. evaluer.py --ia mesure le mode IA (trois exécutions, plus mauvais résultat, coût), vérifié à blanc sur le faux fournisseur.
- Version 0.2.0 : README, CHANGELOG, SPEC, FICHE, TIERS, config-ia.example.json, page du site (trajet des données, coût, installation) ; archive reconstruite. config-ia.json ajouté au .gitignore. scripts/verifier.py : 22/22.
Non fait : aucun appel réel (il faut la clé de Florian) ; mesure du mode IA laissée en marqueur [À COMPLÉTER], qui bloque la publication.
Points ouverts (Florian) : créer config-ia.json et .env, lancer `python factory/jeux-de-test/F-DOSSIER-01/evaluer.py --ia --executions 3`, comparer aux seuils ; tester la fenêtre sur un dossier réel ; valider ADR-018.
Prochaine étape : selon la mesure, ajuster la consigne sur le seul dossier de développement, puis brancher le mode IA dans P02, P03, P05 et P09.

## 2026-11-01 - ADR-021 : outils autonomes, composants dupliqués
Fait : principe posé par Florian (un avocat doit pouvoir essayer un outil seul, sans télécharger les autres). ADR-021 (Acceptée) : chaque outil embarque dans son src/ une copie des composants qu'il utilise (connecteur IA, pseudonymisation de P09), déclarée dans COMPOSANTS.md. scripts/synchroniser_composants.py copie ; son mode --verifier est branché dans scripts/verifier.py. CLAUDE.md, règle 10.
Décisions : ADR-021 (Acceptée).
Prochaine étape : brancher le connecteur et la pseudonymisation dans P01 (premier outil à IA), puis essai réel avec la clé de Florian.

## 2026-11-01 - ADR-020 : connecteur IA commun (proposée)
Fait : compatibilité du format Chat Completions vérifiée sur la documentation officielle (OpenAI natif ; Anthropic, couche de compatibilité « stable » mais présentée comme non destinée à la production à long terme ; Mistral ; API Gemini en bêta ; Ollama local ; Vertex AI exclu faute de clé simple). ADR-020 : un seul client urllib, requête minimale sans temperature ni response_format, JSON demandé dans la consigne et validé, préréglages par fournisseur, tests sur faux serveur local.
Décisions : ADR-020 (Acceptée par Florian).
Réalisé ensuite : composant factory/composants/connecteur-ia 0.1.0 (configuration et préréglages, clé par environnement ou .env, estimation du coût, écran d'envoi tkinter avec texte modifiable et case à cocher, appel, extraction du JSON) ; 18 tests contre un faux fournisseur sur 127.0.0.1 ; essai automatique de l'écran d'envoi. scripts/verifier.py lance aussi les tests des composants.
Points ouverts (Florian) : point d'accès UE de Mistral [À VÉRIFIER] ; aucun appel réel encore fait (il faut une clé).
Prochaine étape : brancher le connecteur dans P01 (choisir comment inclure le composant dans l'archive de l'outil), puis un premier essai réel avec la clé de Florian.

## 2026-11-01 - ADR-019 : connexion API en BYOK dans tous les outils
Fait : décision de Florian de simplifier. ADR-019 (Acceptée) remplace ADR-015 : chaque outil intègre une connexion à une API d'IA avec la clé de l'avocat ; sans clé, l'outil ne fonctionne pas (révision du même jour ; exception : pseudonymisation locale de P09, filtre avant envoi) ; fournisseur au choix libre (Anthropic compris) ; avant envoi, P09, affichage du texte et case à cocher ; plus de condition préalable liée à P09. Objection consignée dans l'ADR (lignes directrices AVOCATS.BE et OVB, p. 3 ; P09 à 45 % sur les noms). docs/deontologie-ia.md : la grille des prestataires devient une information affichée. CLAUDE.md, règle 4, mise à jour.
Décisions : ADR-019 (Acceptée), ADR-015 (Remplacée).
Points ouverts (Florian) : valider ADR-018 ; URL et date des lignes directrices belges [À VÉRIFIER].
Prochaine étape : ADR d'architecture du connecteur IA commun (factory/composants/), puis, outil par outil, ce que l'IA apporte et quels extraits partent.

## 2026-11-01 - ADR-015 révisée (déontologie), bibliothèque de références
Fait :
- bibliotheque/ (ADR-018, Proposée) : catalogue, fiches avec passages cités et pages, originaux dans bibliotheque/sources/ ignoré par git. Deux documents : lignes directrices AVOCATS.BE et OVB sur l'IA ; guide du CNB du 13 mars 2026.
- docs/deontologie-ia.md : règle belge (pseudonymiser ; jamais d'information couverte par le secret dans un outil d'IA, sauf « environnement fermé avec des garanties adéquates »), risques d'un envoi vers une API, lecture proposée (modèle local = environnement fermé ; API distante = garanties contractuelles appréciées par l'avocat), critères d'un prestataire conforme, fournisseurs admis d'après la matrice.
- ADR-015 révisée : nouvelles options D (modèle local) et E (D d'abord, puis API limitée aux prestataires conformes, désactivée par défaut) ; recommandation E. L'API directe d'Anthropic est exclue faute de traitement UE. Le mode distant est conditionné à une meilleure détection des noms par P09 (45 % sur le jeu de contrôle).
Décisions : ADR-015 acceptée par Florian (option E : modèle local d'abord, nationalité affichée sans exclure), ADR-018 (Proposée).
Points ouverts (Florian) : valider ADR-018 ; URL officielles et date des lignes directrices belges [À VÉRIFIER].
Prochaine étape : cadrer le mode IA local de P01 (choix de l'environnement d'exécution et d'un modèle à poids ouverts, mesure sur F-DOSSIER-01).

## 2026-11-01 - P03 Lite Conditions particulières et générales, F-CPCG-01
Fait :
- Jeu F-CPCG-01 v1.0, en deux parties :
  - jeu de développement : 2 contrats, 28 blocs, 42 données propres balisées `[[CAT:…]]` ;
  - jeu de contrôle : 3 contrats, 46 blocs, 92 données, rédigé par un agent sans accès au code ;
  - générateur, évaluation (données repérées, signalements exacts, blocs bien classés), planchers.
- Outil outils/conditions-particulieres 0.1.0, rapport seul, sans IA :
  - découpage en blocs ;
  - repérage des données propres à l'opération (parties, adresses, identifiants, montants, dates, quantités) ;
  - classement : particulières, générales, clause mixte à épurer ; renvois internes ;
  - rapport .docx, .md, .json ; fenêtre et ligne de commande ;
  - 35 tests.
- Relecture indépendante : 5 défauts bloquants, 9 à corriger et 2 mineurs, tous corrigés et couverts par un test (verifications/2026-11-01-revue.md). Le relecteur a fermé par COM l'instance cachée de Word laissée par le test de P02 (démarrée à 11:09:08, sans fenêtre).
Mesure, jeu de contrôle : données repérées 80/92 sans faux signalement (quantités 4/13) ; blocs bien classés 41/46, dont une clause mixte proposée en conditions générales. Totaux inchangés par les corrections de la relecture.
Décisions : ADR-017 (P03 Lite, rapport seul), Proposée.
Points ouverts (Florian) : valider ADR-017 ; tester Conditions.pyw sur un contrat négocié réel ; trancher la question de la fiche (modèle anonymisé, qui rejoint P09).
Prochaine étape : selon ADR-015 (mode IA de P01) ; sinon P07 (mémoire de dossier), qui demande d'abord la réponse de Florian à la question de sa fiche.

## 2026-11-01 - P02 Lite Glossaire des définitions, F-DEF-01
Fait :
- Jeu F-DEF-01 v1.0, en deux parties :
  - jeu de développement : 3 contrats, 35 termes définis, défauts annotés ;
  - jeu de contrôle : 4 contrats, 50 termes définis, 30 défauts, rédigé par un agent sans accès au code ;
  - générateur .docx (insécables dans les guillemets, termes en gras dans un fragment séparé, tableaux), évaluation par catégorie, planchers.
- Outil outils/glossaire-definitions 0.1.0, rapport seul, sans IA :
  - glossaire et points à examiner (définition répétée ou divergente, terme jamais employé, majuscules sans définition, graphie différente, emploi avant définition en cours de texte) ;
  - rapport .docx (ouvert dans Word : 92 paragraphes, 1 tableau), .md, .json ; fenêtre et ligne de commande ;
  - 45 tests.
- Relecture indépendante : aucun défaut bloquant, 9 à corriger et 9 mineurs, tous corrigés et couverts par un test (verifications/2026-11-01-revue.md). Temps du pire cas mesuré : 45,9 s → 5,6 s.
- Fiche du site, nouveauté, archive et empreinte ; scripts/empaqueter.py. scripts/verifier.py : 19/19.
Mesure, jeu de contrôle : termes définis 48/50 sans faux terme ; répétitions, jamais employés, emplois avant définition : tous trouvés sans fausse alerte ; sans définition 5/6 (3 fausses alertes) ; graphies 5/6 ; 2 répétitions signalées divergentes à tort.
Neutralité du contrôle, consignée dans resultats/2026-11-01-P02-v0.1.0.md : la première exécution a affiché les totaux du contrôle de la version brute ; le réglage suivant a porté sur le seul jeu de développement, et les corrections de la relecture n'ont pas changé les totaux du contrôle.
Décisions : ADR-016 (P02 Lite, rapport seul, sans modifier le contrat), Proposée.
Points ouverts (Florian) :
- valider ADR-016 ; tester la fenêtre (Glossaire.pyw) sur un de ses modèles ;
- le dossier par défaut Documents peut être synchronisé par OneDrive : les rapports de tous les outils y seraient copiés ;
- une instance cachée de Word (lancée par le test d'ouverture du rapport) est restée ouverte : la fermer depuis le Gestionnaire des tâches si elle l'est encore.
Prochaine étape : selon ADR-015, mode IA de P01 ; sinon P03 (conditions particulières et générales) en version rapport, ou P07.

## 2026-10-31 - P01 Inventaire d'un dossier (mode local), F-DOSSIER-01, matrice des fournisseurs
Fait :
- Matrice des fournisseurs d'IA (ADR-010, point 4) dans docs/fournisseurs-ia.md :
  - Anthropic, OpenAI, Mistral, Google ; sources officielles consultées le 2026-10-31 ;
  - 22 points [À VÉRIFIER] ;
  - constat : l'API directe d'Anthropic ne documente pas de traitement dans l'UE ; OpenAI, Mistral et Vertex AI en documentent un.
- Jeu F-DOSSIER-01 v1.0, en deux parties :
  - dossier de développement : 12 pièces, docx, eml, txt et un scan PDF sans texte ;
  - dossier de contrôle : 16 pièces, rédigé par un agent sans accès au code ;
  - générateur, inventaire attendu, évaluation, planchers de non-régression.
- Outil outils/inventaire-dossier 0.1.0, mode local, sans IA :
  - registre .docx (vérifié dans Word), .md et .json ;
  - alertes ;
  - fenêtre et ligne de commande ;
  - 36 tests.
- Relecture indépendante : 4 défauts bloquants et 9 à corriger, tous corrigés et testés (verifications/2026-10-31-securite.md).
Mesure, dossier de contrôle : type 14/16, statut 14/16, fait foi 15/16, date 13/16, parties 11/16, rattachement 8/16.
Incident de méthode, consigné dans resultats/2026-10-31-P01-v0.1.0.md : une règle plus stricte, issue de la relecture, faisait régresser le contrôle. Le test de non-régression l'a bloquée et la règle mesurée a été rétablie. Les totaux du contrôle ont donc guidé ce choix.
Décisions : ADR-015 (mode IA de P01), Proposée, à trancher par Florian. Aucun code d'appel à une IA n'est écrit.
Points ouverts (Florian) :
- trancher ADR-015 : principe de l'envoi d'extraits pseudonymisés, options B ou C, fournisseurs proposés ;
- relire docs/fournisseurs-ia.md ;
- tester la fenêtre de P01.
Prochaine étape : selon ADR-015, mode IA de P01 avec P09 en amont, ou amélioration des règles avec un nouveau dossier de contrôle.

## 2026-10-31 - P09 Lite (pseudonymisation) et jeu F-IDENT-01
Fait :
- Jeu F-IDENT-01 v1.0, en deux parties :
  - jeu de développement : 6 textes, 102 entités ;
  - jeu de contrôle : 8 textes, 186 entités, rédigé par un agent sans accès au code ;
  - générateur avec contrôle des sommes de contrôle, et évaluation par catégorie. Le contenu du jeu de contrôle n'est jamais affiché par défaut.
- Outil outils/pseudonymisation 0.1.0 :
  - règles en bibliothèque standard, douze catégories, propagation des noms ;
  - marqueurs cohérents, table de correspondance locale, rétablissement ;
  - fenêtre qui impose la relecture, ligne de commande ;
  - 67 tests.
- Relecture indépendante du code : 4 défauts bloquants et 9 à corriger, tous corrigés et couverts par un test. Détail dans verifications/2026-10-31-securite.md.
- Fiche du site, nouveauté, archive et empreinte. Intégration à scripts/verifier.py (tests de tous les outils) et à scripts/empaqueter.py.
Mesure publiée, jeu de contrôle :
- rappel de 63 %, précision de 98 % ;
- identifiants à somme de contrôle et courriels : 100 % ;
- noms de personnes : 45 % ;
- références de dossier : 20 %.
Sur le jeu de développement, le rappel est de 100 %, ce qui ne mesure que l'ajustement des règles.
Décisions : ADR-014 (P09 Lite par règles, sans dépendance), Proposée.
Points ouverts (Florian) :
- valider ADR-014 et la manière de publier la mesure ;
- tester la fenêtre de P09 ;
- les deux adresses de contact des fiches portent les marqueurs n° 15 et 16.
Prochaine étape : choisir entre améliorer la détection des noms (modèle local, liste de noms des parties), ce qui imposera un nouveau jeu de contrôle, et passer à l'outil suivant (P01, F-DOSSIER-01).

---

## 2026-10-31 - Nouvelle identité visuelle du site
Fait : examen de quickadd.obsidian.guide (Astro, Inter, accent unique, cartes surélevées, accueil en sections) ; choix de Florian : Inter auto-hébergée, accent terracotta (brique #a23d24), accueil en sections. Nouvelle feuille de style (contrastes AA mesurés), page d'accueil (bandeau, trajet des données, trois règles, outils en cartes, démarrage en trois étapes, à lire), fiche outil avec carte d'identité en colonne latérale, catalogue en cartes, étapes numérotées dans les guides. scripts/typographie.py : espaces insécables du français, contrôlés par scripts/verifier.py (16/16).
Décisions : ADR-013.
Prochaine étape : inchangée (marqueurs, comptes GitHub et OVH).

## 2026-10-31 - Réalisation : P05 Lite, site, vérification, CI
Fait :
- Décisions déléguées par Florian (ADR-002 Hugo, ADR-005 chemins, ADR-006 MIT / CC BY 4.0, ADR-007 Factory avec trois parcours, ADR-008, ADR-009 option C, ADR-010 modes d'exécution). Décisions de Florian : éditeur à titre personnel, hébergement GitHub Pages, domaine chez OVH (ADR-003), P05 en application locale.
- outils/controle-avant-envoi : P05 Lite 0.1.0, Python bibliothèque standard, quatorze contrôles, fenêtre, ligne de commande, rapports texte/HTML/JSON, 42 tests. Relecture indépendante par un agent distinct : 3 défauts bloquants et 7 à corriger, tous corrigés et couverts par un test (verifications/2026-10-31-securite.md).
- factory/jeux-de-test/F-DOCX-01 : générateur reproductible, cinq pièces, résultats attendus ; pièces piégée et propre ouvertes sans erreur dans Word.
- site/ : Hugo, gabarits (agent), contenu : accueil, fiche P05, guide « Utiliser un outil en local », précautions, à propos, mentions légales, confidentialité, rubrique « Automatiser une prestation » (deux articles, invitations à prendre contact retirées), nouveautés et RSS ; trois guides API en brouillon (plan seulement).
- scripts/ : verifier.py (secrets, tests, archive, site, liens, marqueurs), empaqueter.py (archive reproductible, empreinte reportée sur la fiche), detecter_secrets.py ; hook pre-commit ; workflows GitHub (vérification, publication bloquée par les marqueurs).
Vérifications : python scripts/verifier.py : 15/15 ; --publication : échoue sur 17 marqueurs, comme attendu.
Décisions : ADR-002, 003, 005 à 010 acceptées.
Points ouverts (Florian) :
- lever les marqueurs [À COMPLÉTER] / [À VÉRIFIER] du site (contact, barreau, BCE, spécialisation, comités, mentions légales, journaux GitHub, libellés de l'installateur Python) ;
- trancher les cinq points de outils/controle-avant-envoi/verifications/2026-10-31-deontologie.md ;
- tester la fenêtre de P05 à la main et lister les incidents vécus au cabinet (nouveaux pièges pour F-DOCX-01) ;
- créer le dépôt GitHub public, activer Pages (source GitHub Actions), DNS OVH, Enforce HTTPS, 2FA ; revérifier les versions des actions GitHub ;
- relire les deux articles de la rubrique dans leur version site.
Prochaine étape : levée des marqueurs puis publication ; ensuite F-IDENT-01 et P09.

## 2026-10-31 - Préparation du projet : premiers arbitrages, rubrique, git
Fait : examen du dossier iavocat et des contenus du dossier parent ; fiche P05 découpée en P05 Lite / P05 avancé (priorité haute, dépendances du MVP séparées) ; rubrique "Automatiser une prestation" ajoutée au cahier des charges (v0.3) avec import des deux articles en Markdown dans contenus/automatiser-une-prestation/ ; backlog, registre, plan §13 et CLAUDE.md mis à jour ; dépôt git local initialisé, sans remote.
Décisions : ADR-011 (premier outil P05 Lite) et ADR-012 (rubrique "Automatiser une prestation"), acceptées par Florian.
Points ouverts : éditeur du site non tranché (Florian ou Avroy Avocats) ; ADR-002, 003, 005, 006, 010 toujours proposées ; articles importés à relire (charte, invitations à prendre contact en fin d'article) ; sort du tutoriel Cowork, des fiches "avocat entrepreneur" et du livre blanc.
Prochaine étape : choisir le mode d'exécution de P05 Lite et le générateur (ADR-002), puis créer F-DOCX-01 (Sprint 1).

## 2026-10-31 - Intégration du plan d'amélioration
Fait : ajout de PLAN_AMELIORATIONS.md à la racine ; 18 tâches A01 à A18 ajoutées au backlog ; ADR-010 créée au statut Proposée ; ADR-004 passée en révision et assertion "pas de responsabilité de traitement" retirée ; mode navigateur avec clé API suspendu dans docs/principes-outils.md et CLAUDE.md en attendant ADR-010.
Non fait volontairement : les autres modifications du plan (changement de priorités, parcours Factory, statuts, champs de fiche) demandent un arbitrage de Florian (plan §12 et §13).
Prochaine étape : Sprint 0 du plan (§10), en commençant par les décisions du §13.

## 2026-10-31 - Exploration zenzen-sol et création de la Factory
Fait : exploration de github.com/zenzen-sol (liste des dépôts, README des projets pertinents, en-têtes des skills legal-prompts) ; note de veille docs/veille/sol-irvine-zenzen-sol.md ; 16 fiches projet (P01 à P13, F01 à F03) ; mise en place de la Factory (pipeline, registre, standards, composants, jeux de test, rétrospectives, mémoire) ; 9 agents dont ops-factory ; commandes /factory, /factory-lancer, /factory-etape, /factory-revue, /factory-retro, /veille ; skill memoire-projet ; mise à jour de CLAUDE.md, du cahier des charges (v0.2) et du backlog.
Décisions : ADR-007, 008 et 009 proposées. AM-001 et AM-002 proposées.
Points ouverts : sites augustus.esq, wargame.esq et zenzen.io/sol non consultés ; objet de l'application Para inconnu (code privé) ; licence de laws-of-ux et des forks Docling non vérifiées ; format exact des agents et hooks Claude Code à vérifier.
Prochaine étape : /factory, puis valider ADR-007 et choisir le premier outil.

## 2026-10-31 - Cadrage initial
Fait : rédaction du cahier des charges v0.1, de CLAUDE.md, des principes outils, de la charte éditoriale, du document sécurité, du registre des décisions, du backlog, des gabarits et des commandes Claude Code.
Décisions : ADR-001 et ADR-004 acceptées (issues du brief). ADR-002, 003, 005 et 006 proposées.
Points ouverts : voir section 16 du cahier des charges. Le site de Sol Irvine cité comme modèle n'a pas été consulté.
Prochaine étape : valider le cahier des charges et trancher ADR-002, ADR-003 et ADR-005.

## JALON — 2026-11-02

**Renommage :** suppression des dernières références à « iavocat » dans l'état actuel du dépôt. Graphies retenues : `iavocat.be` → `jerlash.labs` ; `iavocat` en nom de fichier ou identifiant → `jerlash-labs` ; `window.IAvocat` → `window.JerlashLabs`. Élisions corrigées (« d'iavocat.be » → « de jerlash.labs »).

**Choix :** historique git non réécrit (anciens messages de commit inchangés) ; entrées passées de ce LOG.md laissées intactes (append-only). Empreintes des archives d'outils recalculées (`scripts/empaqueter.py --fiche`) ; `scripts/verifier.py` : 23/23.

**Hors dépôt :** dossiers `LEGALTECH/iavocat` et `iavocat/iavocat` à renommer en `jerlash-labs`, fichiers `iavocat-article-*.docx` et `iavocat.zip` du dossier parent renommés.

---

## JALON — 2026-11-03

**Livrables Proton intégrés au backlog.** Examen de l'archive `Proton Drive Download - 2026-11-03.zip` : Legal AI Governance Toolkit v0.1.0, kit expérimental MCP v0.1 et pack participants, extension C3 v0.2 (code annoncé absent), trois research papers H1, une recension, architecture « Legal Technology Commons » et Research Papers Guide. Sources rangées hors dépôt dans `../sources-proton/2026-11-03/` (doublons de la racine non recopiés ; référentiel restreint et tests adverses à ne jamais versionner).

**Arbitrages de Florian :** Revue avec Perspectives (la réflexion entre sur jerlash) ; « livré » = version de travail publique ; outils P01 à P13 en parallèle ; novembre = refonte du site + Toolkit ; ordre P14 → P19 → P18 → P16 → P17 → P15 ; chemins en français, anglais dupliqué sous `/en/` (pas de problème de référencement : hreflang, x-default et canonical par langue déjà en place).

**Fait :** fiches P14 à P19 et index ; ADR-024 (architecture Recherche, Outils, Revue, Éthique) et ADR-025 (un projet par mois, piste Outils), proposées ; `docs/politique-publication.md` ; `BACKLOG.md` (Maintenant = P14, piste Outils, calendrier 2026-11 → 2027-10) ; CLAUDE.md et cahier des charges (§5, §7) mis à jour.

**Prochaine étape :** Florian valide ADR-024, ADR-025 et la politique de publication, tranche D01 et D02 ; puis gabarits et migration du blog.

---

## JALON — 2026-11-06

**Gouvernance de l'IA : trois niveaux (étape 1 sur 3).** Florian renomme le toolkit P14 « Gouvernance de l'IA » et fixe trois niveaux de gouvernance proportionnés aux outils en place. Plan en trois étapes : 1) réorganiser et simplifier le site, 2) tableur Excel des niveaux 2 et 3, 3) serveur MCP local et commande Claude Code (inspiration : before-ai, qui n'est pas un MCP mais une commande). Arbitrages : niveau 1 = outil conforme OU données limitées à D0/D1 (voie alternative) ; MCP local en stdio + commande ; slug `gouvernance-ia`.

**Fait (étape 1) :** `git mv` vers `site/content/outils/gouvernance-ia/` avec alias des anciennes adresses ; accueil réécrit autour du diagnostic (tableau conformité × données) ; nouvelle page `niveau-1.md` (six éléments, fiche de conformité F01 à F11) ; encadré « Selon votre niveau » par module (paramètre `niveaux`, partiel `encadre-niveaux.html`) ; version réduite de la gouvernance ; article 4 de la charte adapté ; version 0.3 ; ADR-029 proposée ; P14 et BACKLOG à jour. `scripts/verifier.py` : 23/23.

**Prochaine étape :** Florian relit le français et valide la règle de détermination du niveau (dont le rattachement des agents au niveau 3) ; puis `/traduire`, et étape 2 (tableur, fiche P20).

---

## JALON — 2026-11-06 (suite)

**Gouvernance de l'IA : étapes 1 et 2 livrées.** Florian a relu le français et publié les neuf pages (`draft: false`). Relecture : alignement « trace » → « preuve » (dont l'ancre « La preuve minimale »), « quels éléments », « Nous proposons », journal des versions 0.2/0.3, références RGPD certaines substituées aux marqueurs (art. 28, 33-34, 37-39). Traduction anglaise des dix pages, toolkit renommé `/en/tools/ai-governance/` avec alias des anciennes adresses.

**Étape 2 :** référentiel unique `outils/gouvernance-ia/referentiel/gouvernance-ia.json` ; tableur `gouvernance-ia-matrices-0.3.xlsx` (Inventaire avec fiche F01-F11 et niveau calculé, Diagnostic, matrices données et usages, Rôles, Conditions E, Grille scores, quatre registres, Paramètres) généré par openpyxl, copié dans `site/static/telechargements/` ; formules contrôlées sur six profils fictifs avec la bibliothèque `formulas` (LibreOffice absent du poste). Hook `render-link.html` : les liens `/telechargements/` gardent leur adresse. ADR-030 proposée. `verifier.py` : 23/23 ; 234 liens à ancre FR/EN valides.

**Prochaine étape :** Florian teste le tableur dans Excel ; puis étape 3 (fiche P20, serveur MCP local, commande Claude Code).

---

## JALON — 2026-11-06 (publication)

**Gouvernance de l'IA 0.3 publiée** (PR #7 fusionnée par Florian). Page en ligne mais orpheline : rubrique Outils en brouillon (ADR-022) et absente du menu. Choix de Florian : ouvrir la rubrique Outils. Fait : entrée « Outils » / « Tools » au menu (avant la Revue, ADR-024), section « Boîtes à outils » dans `site/layouts/outils/section.html`, texte de la rubrique ajusté, ADR-031 proposée. Tableur et MCP toujours hors dépôt (`outils/gouvernance-ia/`, `publier.yml` modifié non commité).

---
