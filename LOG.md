# Journal de bord

Une entrée par session de travail, la plus récente en haut. Format :

```
## AAAA-MM-JJ - Titre court
Fait :
Décisions : (renvoi vers ADR si applicable)
Problèmes / points ouverts :
Prochaine étape :
```

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
