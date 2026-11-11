# Backlog

Cadre depuis le 2026-11-03 (ADR-025, accepté comme cadre facultatif) : livrer plutôt que construire. Un projet livré par mois, en version de travail publique, plus une piste parallèle « Outils » sans échéance. Le calendrier est indicatif : Florian peut en sortir à tout moment. Ce qui est livré passe dans `CHANGELOG.md`.

## Maintenant : novembre 2026, P14 Legal AI Governance Toolkit v0.2 et refonte du site (ADR-024)

- [ ] Étape 3 : serveur MCP local et commande Claude Code (fiche P20 à créer, ADR-030)
- [ ] Rubrique Éthique (`ethique/`, page Précautions) et entrées Outils et Éthique du menu, à la publication du Toolkit
- [ ] Florian : trancher les points relevés à la conversion : charte qui vise « l'avocat » alors qu'elle s'adresse aussi aux directions juridiques (art. 2 et 8) ; « surveillance abusive » ambigu (données) ; champ « destination du système » ajouté à la fiche de cas d'usage ; phrase ajoutée sur les petits cabinets qui cumulent les rôles (gouvernance) ; noms d'axes alignés sur le référentiel ; contrôles « obligatoires » des agents présentés comme à préciser
- [ ] Lever les 21 marqueurs `[À VÉRIFIER]` / `[À COMPLÉTER]` des pages du Toolkit (date d'arrêt du droit, articles RGPD, acte modificatif du règlement IA, déclaration d'usage de l'IA, contrôles faits)
- [ ] Réduire le règlement IA à un rappel (haut risque = administration de la justice ; aucune déviation de la destination du système) ; vérifier le RGPD et le secret professionnel cités ; marquer ce qui ne peut pas l'être
- [ ] Téléchargements : zip reproductible, charte en .docx, kit « petit cabinet »
- [ ] Florian : lire tout le Toolkit (texte rédigé avec une IA, à faire sien avant publication). Relue : « Pourquoi les chartes échouent » (`draft: false`, 2026-11-03). Restent : gouvernance, données, homologation, supervision, opérations, charte, sources, présentation
- [ ] Avant tout push sur `main` : ne pas publier « Pourquoi les chartes échouent » seule (page parente en brouillon, pas de traduction) ; remettre `draft: true` ou attendre la fin de la relecture
- [ ] « Pourquoi les chartes échouent » : trois passages à reprendre (lignes 8, 31 et 33)
- [ ] Traduction anglaise (`/traduire`) ; contrôle hreflang et plan du site FR et EN
- [ ] `python scripts/verifier.py --publication` vert, publication, entrée dans `CHANGELOG.md`, post LinkedIn

## Maintenant : recensions (avancé de décembre à novembre par Florian, 2026-11-04)

- [ ] Florian : valider ADR-027 (une collection Recensions, champ `objet` : livre, article, podcast, conférence ; étiquette « Recension · <objet> » sur les vignettes)
- [x] P19 lue et arbitrée par Florian le 2026-11-11 (ticket FLO-18) : les trois réserves de la Discussion sont gardées telles quelles ; la page reste en ligne, Florian l'ayant relue avant sa mise en ligne du 2026-11-07 (§8 de `docs/politique-publication.md`) ; les déclarations ne sont pas obligatoires (`controles` et `conflits_interets` sont déjà facultatifs au §9). Aucun fichier de `site/` n'a été modifié : le texte publié et sa traduction restent dans l'état du 2026-11-07
- [ ] Florian : l'hypothèse H1 de P19. Le résumé de la carte `site/content/recherche/projets/p19.md` et celui de `p19.en.md` annoncent que « la recension en tire une hypothèse à éprouver dans le programme » ; le texte publié n'en formule aucune. Corriger les deux résumés (correction du français, puis `/traduire`), ou écrire l'hypothèse
- [ ] Florian : l'année de la Summer School de P19, seule question du dossier de lecture restée sans réponse. Le texte écrit « début septembre 2026 », la page EDHEC écrit « début septembre », sans année. Piste non confirmée : une « Executive Summer School 2026 » annoncée les 8, 9 et 10 septembre 2026 à Paris par l'Augmented Lawyer Academy (`https://alll.legal/programme/executive-summer-school-2026/`, page inaccessible depuis l'environnement de l'agent). Confirmer l'année, ou la retirer du texte
- [ ] Tromans, « Will AI Change the Identity of Law Firm Partners? » (article) : brouillon `../otf/JERLASH_Critical_Review_AI_Identite_Professionnelle_2026-11-04.md`
- [ ] Waldron, « AI Governance Must Keep Pace with Legal Practice » (article sponsorisé par LexisNexis ; chiffres d'enquête à vérifier) : brouillon `../otf/JERLASH_Labs_Critical_Review_AI_Governance.md`
- [ ] Bull, « The 4 Es Inhouse AI Framework » (article, entretien écrit) : brouillon `../otf/JERLASH_Labs_Critical_Review_Emily_Bull_4Es.md`
- [ ] Legora, entretien avec Jacob Lauritzen (podcast vidéo, 67 min ; citations à minuter) : brouillon `../otf/JERLASH_Critical_Review_Legora_Jacob_Lauritzen.md`
- [ ] Chaduteau (livre) : prête dans `main` depuis le 2026-11-07 (conflits d'intérêts, usage de l'IA et contrôles remplis le 2026-11-05 ; `draft: false` en FR et EN ; traduction à jour). Reste à Florian, le 12 novembre : lancer le workflow Publication (`workflow_dispatch`), la page étant datée du 12 et Hugo ne construisant pas les contenus futurs ; la reconstruction automatique n'a lieu que le lundi. Entrée `CHANGELOG.md` et projet de post LinkedIn préparés (FLO-17)
- [ ] Traduction anglaise (`/traduire`) ; slug anglais de la collection à décider (`/en/review/recensions/` par défaut)
- [ ] Publication : `draft: false` sur la collection et les recensions prêtes, `python scripts/verifier.py --publication`, `CHANGELOG.md`, post LinkedIn

## Maintenant : Revue unifiée, sommaire et rubrique Recherche (ADR-032, 2026-11-07)

- [ ] Florian : valider ADR-032 (troisième script `filtres.js`, programmes désignés par leur nom, visuel repris en tête de page)
- [ ] Florian : vérifier dans le navigateur (`hugo server --source site --buildDrafts --buildFuture`) : filtres de la Revue, sommaire latéral et repliable, visuels en tête de page, Recherche et pages de programme, en clair et en sombre, à 375, 768 et 1280 px
- [ ] Florian : valider ADR-033 (quatrième script `sommaire.js` ; parcours de la boîte à outils en trois branches) et vérifier dans le navigateur la surbrillance du sommaire et le parcours à 1440, 1200, 1100 et 390 px
- [ ] Ajouter une fiche dans `site/content/recherche/projets/` à chaque nouveau projet publié, puis `python scripts/visuels.py`

## Maintenant : piste parallèle Outils (sans échéance, par la Factory)

- [ ] P05 Contrôle avant envoi : essai de la fenêtre par Florian, puis publication dans Outils
- [ ] Puis P09 Pseudonymisation, puis P01 Inventaire (détail dans « Plus tard »)

## Calendrier 2026-11 → 2027-10 (ADR-025)

Ordre fixé par Florian le 2026-11-03. Les mois de novembre à avril sont fermes ; la suite est indicative et sera revue en mai 2027. Chaque fiche est dans `projets/`, et ses sources hors dépôt, dans `../sources-proton/2026-11-03/`.

| Mois | Projet | Rubriques | Prérequis |
|---|---|---|---|
| Nov. 2026 | P14 Toolkit v0.2 + refonte du site | Outils, Éthique, Revue | ADR-024, D01, D02, vérification juridique |
| Déc. 2026 | P19 Recension Billion et Fasterling (avancée en novembre, 2026-11-04) | Revue | Collection Recensions (ADR-027) ; récupérer le code C3 pour P18 |
| Janv. 2027 | P18 Kit MCP, partie publique (protocole, gouvernance, scripts, addendum C3) ; lancement de G0 | Recherche, Éthique, Outils | Code C3 ; préenregistrement OSF oui ou non ; référentiel restreint exclu |
| Févr. 2027 | P16 RP Modèles discriminatifs (`JLL-RP-2027-001`) | Revue, Recherche | Revérifier arXiv et URL |
| Mars 2027 | P17 RP Tarification alternative (`JLL-RP-2027-002`) | Revue | Relecture déontologique belge |
| Avr. 2027 | P15 RP Humain dans la boucle (`JLL-RP-2027-003`) ; lien depuis le module Supervision | Revue, Recherche | Relecture du §6.4 ; 9 000 mots ou moins |
| Mai 2027 | Toolkit v0.3 : deux homologations documentées ; revue du calendrier | Outils, Éthique | Choix des cas d'usage |
| Juin 2027 | P18 : serveur MCP synthétique C2 et orchestrateur C3 | Outils, Notes techniques | G0 ; réviseur sécurité distinct |
| Juil. 2027 | Human Agency Canvas et grille d'audit (H1.2) | Outils, Recherche | |
| Août 2027 | Pas de livraison | | |
| Sept. 2027 | Working paper Human Agency Framework (H1.1) | Revue, Recherche | |
| Oct. 2027 | Toolkit v1.0 (ou v0.4 sans relecteurs) ; pilote MCP seulement si G3 | Outils, Recherche | D08, G3 |

## Ensuite

Relectures du site :
- [ ] Florian : relire la page d'accueil, les 9 articles importés (dont 4 aux en-têtes vides : titre tiré du nom de fichier) et leurs dates (date du fichier)
- [ ] Florian : relire l'anglais (accueil, À propos, articles), compléter `docs/glossaire-traduction.md`

Autres :
- [ ] Domaine : jerlash.eu choisi et DNS en place, HTTPS actif ; reste 2FA GitHub et registraire
- [ ] Rubrique Guides : compléter les quatre guides (clé API, facturation, données envoyées, installation locale)
- [ ] Page Outils et fiches, quand un outil est prêt (piste parallèle)
- [ ] Décisions du Toolkit restées ouvertes : D03 à D10 (registre dans les sources P14), dont D10 version publique et services payants

## Plus tard

Dépôts otf (ADR-028, `../otf/INDEX.md`) :
- [ ] Proposition de recherche « Identité professionnelle, savoirs et pouvoir d'agir » (H1, méthodes mixtes, terrain belge envisagé) : `../otf/JERLASH_Research_Proposal_Identite_Professionnelle_AI_2026-11-04.md` ; Florian : créer la fiche P20 ou non
- [ ] Proposition de research paper « La capitalisation technique des savoirs juridiques » (H1 et C1) : `../otf/JERLASH_Fiche_Recherche_Capitalisation_Expertise_Juridique.md` ; Florian : créer la fiche P21 ou non
- [ ] Article « Legal AI's Legibility Problem » (Stanford HAI, 2026-07-20) sur l'article PNAS « There's No Free Benchmark » (Guha, Ho, Nyarko, Manning) : `../otf/SLS_2026-07-21_Legal_AI_Legibility_Problem.md` ; Florian : recension de l'article PNAS, ou simple appui pour P12 et l'homologation de P14
- [ ] Annonce « The Rise of Legal Engineering » (Stanford Law School, 2026-09-04) : `../otf/SLS_2026-09-04_Rise_of_Legal_Engineering.md` ; matériau de veille, rattachement à P14 (référent IA) à confirmer

Outils (état au 2026-11-01, tous au statut vérification, aucun publié) :
- [ ] P01 Inventaire 0.2.0 : config-ia.json et .env, mesure réelle `evaluer.py --ia --executions 3` (seuils 14/16 et 13/16), essai sur un dossier réel
- [ ] P02 Glossaire, P03 Conditions, P05 Contrôle avant envoi, P09 Pseudonymisation : essai de la fenêtre par Florian ; mode IA selon ADR-019
- [ ] P09 : meilleure détection des noms de personnes (45 % sur le jeu de contrôle), avec un nouveau jeu de contrôle
- [ ] P04, P06, P07, P08, P10, P11, P12, P13 : fiches dans `projets/`, rien de commencé (sauf P12, jeux de test livrés)

Décisions et vérifications :
- [ ] Valider ADR-016, ADR-017, ADR-018
- [ ] Bibliothèque : URL officielles et date des lignes directrices AVOCATS.BE et OVB, URL du guide CNB
- [ ] Mistral : point d'accès UE à confirmer ; matrice des fournisseurs, 22 points [À VÉRIFIER]
- [ ] Règles de communication de l'Ordre applicables au site, mentions obligatoires
- [ ] Rubrique « Automatiser une prestation » (ADR-012) : relire les deux articles
- [ ] Décider si le tutoriel de veille Cowork, les fiches « avocat entrepreneur » et le livre blanc rejoignent le site (fichiers dans `../documents/`)

Factory et plan d'amélioration :
- [ ] Factory : valider ADR-007 et le circuit ; AM-001, AM-002 ; essai d'un mois de la mémoire (F03) ; F01
- [ ] Plan d'amélioration du 2026-10-31 (PLAN_AMELIORATIONS.md) : A01, A03, A05, A08 à A18 restent ouverts ; A02, A04, A06, A07 livrés
- [ ] Rythme : fréquence de publication réaliste, revue semestrielle des guides
