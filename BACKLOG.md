# Backlog

Cadre depuis le 2026-11-03 (ADR-025, accepté comme cadre facultatif) : livrer plutôt que construire. Un projet livré par mois, en version de travail publique, plus une piste parallèle « Outils » sans échéance. Le calendrier est indicatif : Florian peut en sortir à tout moment. Ce qui est livré passe dans `CHANGELOG.md`.

## Maintenant : novembre 2026, P14 Gouvernance de l'IA v0.2 et refonte du site (ADR-024)

État relevé sur le dépôt le 2026-11-11 (ticket FLO-20), à partir de `main` au commit `69c7c29`. Les dix pages de la boîte à outils sont publiées et traduites, et plus aucun marqueur ne subsiste dans ce qui sera publié. Reste, pour la publication de fin novembre : les téléchargements, la rubrique Éthique, l'étape 3, et des arbitrages de Florian.

## Maintenant : recensions (avancé de décembre à novembre par Florian, 2026-11-04)

## Maintenant : Revue unifiée, sommaire et rubrique Recherche (ADR-032, 2026-11-07)

## Maintenant : piste parallèle Outils (sans échéance, par la Factory)

## Calendrier 2026-11 → 2027-10 (ADR-025)

Ordre fixé par Florian le 2026-11-03. Les mois de novembre à avril sont fermes ; la suite est indicative et sera revue en mai 2027. Chaque fiche est dans `projets/`, et ses sources hors dépôt, dans `../sources-proton/2026-11-03/`.

| Mois | Projet | Rubriques | Prérequis |
|---|---|---|---|
| Nov. 2026 | P14 Toolkit v0.2 + refonte du site | Outils, Éthique, Revue | ADR-024, D01, D02, vérification juridique |
| Déc. 2026 | Legal Agent Factory (décision de Florian du 2026-11-10, ticket FLO-24 ; P19 avancée en novembre le 2026-11-04) | [À VÉRIFIER] | Fiche projet v0.2 du 2026-11-09 (hors dépôt) ; récupérer le code C3 pour P18 |
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

Legal Agent Factory, découpage (ticket parent FLO-57, état relevé dans Vikunja le 2026-11-21). Les lots s'enchaînent : chacun attend le précédent.

| Lot | Tickets | Semaine proposée [À VÉRIFIER] | État au 2026-11-21 |
|---|---|---|---|
| 0 : périmètre et 40 cas, sources primaires, garanties publiées de Scaleway et Umans | FLO-59, FLO-60, FLO-63 | 16 nov. au 6 déc. | À relire par Florian |
| 1 : chaîne technique sans secrets | FLO-64 | 30 nov. au 13 déc. | Bloqué : attend FLO-59 |
| 2 : courriel AgentMail, rôles d'agents, routeur, deux skills de faillite | FLO-65 | 14 au 27 déc. | Bloqué : attend FLO-64 et FLO-60 |
| 3 : évaluation du benchmark faillite (40 cas) | FLO-66 | janvier 2027, à fixer | Bloqué : attend FLO-65, FLO-63, et trois apports de Florian (réponses de référence signées, accès Scaleway et Umans, plafond de dépense) |

Le premier verrou est la relecture de FLO-59 par Florian. Le calendrier d'origine sera probablement dépassé pour les lots 2 et 3 (FLO-24) : la charge de janvier 2027 (P18) est à revoir en conséquence [À VÉRIFIER].

## Ensuite

## Plus tard

## Tâches (copie de Vikunja)

<!-- debut-bloc-vikunja -->
> Généré depuis Vikunja (jerlash.labs) le 2026-11-21 07:41. Ne pas modifier : ce bloc est réécrit à chaque régénération.

### À trier

- [ ] Auditer mes agents IA avec ClawProof (#121)
- [ ] Garder en veille le skill « crash-test » de textes normatifs (A. Fiorentino) (#120)
- [ ] FLO-22 · [recension:bull] Recension Bull : « The 4 Es Inhouse AI Framework » — priorité 2 (#27)
- [ ] FLO-23 · [recension:legora] Recension Legora : entretien avec Jacob Lauritzen (podcast vidéo, 67 min) — priorité 2 — Vidéo (#32)
- [ ] FLO-24 · [mois:2026-12] Projet de décembre : Legal Agent Factory (décision de Florian du 2026-11-10) — priorité 1 (#42)
- [ ] FLO-62 · [factory:bilan-2026-12] Bilan du pilote Factory : rester en A ou passer à B — priorité 2 (#45)

### Bloqué

- [ ] FLO-57 · Projet jerlash.labs : planning et tickets — priorité 2 (#4)
- [ ] FLO-72 · Réaliser une recension et un working paper à partir du document source — priorité 2 (#12)
- [ ] FLO-64 · [laf:lot-1] Legal Agent Factory : chaîne technique sans secrets (dossier surveillé, runtime HTTP, modèle simulé) — priorité 2 (#56)
- [ ] FLO-65 · [laf:lot-2] Legal Agent Factory : email AgentMail, rôles d'agents, routeur et deux skills de faillite — priorité 2 (#59)
- [ ] FLO-66 · [laf:lot-3] Legal Agent Factory : évaluation du benchmark faillite (40 cas) — priorité 2 (#63)

### À relire

- [ ] FLO-61 · [factory:pilote-2026-11] Piloter la Factory via l'agent jerlash (P14 + second outil) — priorité 2 (#11)
- [ ] FLO-73 · [source:a23938c7-35c5-4db7-9d60-615d4e99debc] Dentons — recension et working paper — priorité 2 (#18)
- [ ] FLO-74 · [factory:P14] Étape 3 du circuit : téléchargements de la Gouvernance de l'IA — priorité 2 (#19)
- [ ] FLO-20 · [mois:2026-11] Projet de novembre : Legal AI Governance Toolkit P14 v0.2, état des lieux et reste à faire — priorité 2 (#25)
- [ ] FLO-63 · [laf:lot-0c] Legal Agent Factory : conditions de confidentialité Scaleway et Umans (sources publiques) — priorité 2 (#41)
- [ ] FLO-59 · [laf:lot-0a] Legal Agent Factory : périmètre, taxonomie et relecture des 40 cas — priorité 2 (#47)
- [ ] FLO-60 · [laf:lot-0b] Legal Agent Factory : registre des sources primaires — priorité 2 (#54)

### À faire

- [ ] Rythme : fréquence de publication réaliste, revue semestrielle des guides — priorité 1 — Agent (#242)
- [ ] Plan d'amélioration du 2026-10-31 (PLAN_AMELIORATIONS.md) — priorité 1 — Agent (#241)
- [ ] Factory : valider ADR-007 et le circuit ; AM-001, AM-002 ; essai d'un mois de la mémoire (F03) ; F01 — priorité 1 — Agent (#240)
- [ ] Décider si le tutoriel de veille Cowork, les fiches « avocat entrepreneur » et le livre blanc… — priorité 1 — Florian (#239)
- [ ] Rubrique « Automatiser une prestation » (ADR-012) — priorité 1 — Agent (#238)
- [ ] Règles de communication de l'Ordre applicables au site, mentions obligatoires — priorité 1 — Agent (#237)
- [ ] Mistral : point d'accès UE à confirmer ; matrice des fournisseurs, 22 points [À VÉRIFIER] — priorité 1 — Agent (#236)
- [ ] Bibliothèque : URL officielles et date des lignes directrices AVOCATS.BE et OVB, URL du guide CNB — priorité 1 — Agent (#235)
- [ ] Valider ADR-016, ADR-017, ADR-018 — priorité 1 — Florian (#234)
- [ ] P04, P06, P07, P08, P10, P11, P12, P13 — priorité 1 — Agent (#233)
- [ ] P09 : meilleure détection des noms de personnes (45 % sur le jeu de contrôle), avec un nouveau jeu… — priorité 1 — Agent (#232)
- [ ] P02 Glossaire, P03 Conditions, P05 Contrôle avant envoi, P09 Pseudonymisation — priorité 1 — Florian (#231)
- [ ] P01 Inventaire 0.2.0 — priorité 1 — Agent (#230)
- [ ] Annonce « The Rise of Legal Engineering » (Stanford Law School, 2026-09-04) — priorité 1 — Agent (#229)
- [ ] Article « Legal AI's Legibility Problem » (Stanford HAI, 2026-07-20) sur l'article PNAS « There's No… — priorité 1 — Florian (#228)
- [ ] Proposition de research paper « La capitalisation technique des savoirs juridiques » (H1 et C1) — priorité 1 — Florian (#227)
- [ ] Proposition de recherche « Identité professionnelle, savoirs et pouvoir d'agir » (H1, méthodes… — priorité 1 — Florian (#226)
- [ ] Décisions du Toolkit restées ouvertes — priorité 2 — Agent (#225)
- [ ] Page Outils et fiches, quand un outil est prêt (piste parallèle) — priorité 2 — Agent (#224)
- [ ] Rubrique Guides — priorité 2 — Agent (#223)
- [ ] Domaine : jerlash.eu choisi et DNS en place, HTTPS actif ; reste 2FA GitHub et registraire — priorité 2 — Agent (#222)
- [ ] relire l'anglais (accueil, À propos, articles), compléter `docs/glossaire-traduction.md` — priorité 2 — Florian (#221)
- [ ] relire la page d'accueil, les 9 articles importés (dont 4 aux en-têtes vides — priorité 2 — Florian (#220)
- [ ] Puis P09 Pseudonymisation, puis P01 Inventaire (détail dans « Plus tard ») — priorité 3 — Agent (#219)
- [ ] P05 Contrôle avant envoi — priorité 3 — Florian (#218)
- [ ] Ajouter une fiche dans `site/content/recherche/projets/` à chaque nouveau projet publié, puis… — priorité 3 — Agent (#217)
- [ ] valider ADR-033 (quatrième script `sommaire.js` ; parcours de la boîte à outils en trois branches)… — priorité 3 — Florian (#216)
- [ ] vérifier dans le navigateur (`hugo server --source site --buildDrafts --buildFuture`) — priorité 3 — Florian (#215)
- [ ] valider ADR-032 (troisième script `filtres.js`, programmes désignés par leur nom, visuel repris en… — priorité 3 — Florian (#214)
- [ ] Publication : `draft: false` sur la collection et les recensions prêtes, `python scripts/verifier.py… — priorité 3 — Agent (#213)
- [ ] Traduction anglaise (`/traduire`) ; slug anglais de la collection à décider… — priorité 3 — Agent (#212)
- [ ] Chaduteau (livre) — priorité 3 — Florian (#211)
- [ ] Legora, entretien avec Jacob Lauritzen (podcast vidéo, 67 min ; citations à minuter) — priorité 3 — Agent (#210)
- [ ] Bull, « The 4 Es Inhouse AI Framework » (article, entretien écrit) — priorité 3 — Agent (#209)
- [ ] Perspective « le cabinet AI-native en droit belge » — priorité 3 — Florian (#208)
- [ ] Grille « Où en est votre cabinet avec l'IA ? » — priorité 3 — Florian (#207)
- [ ] Inside Practice, « The AI-Native Law Firm » (rapport, juin 2026 ; `objet: "article"` faute de valeur… — priorité 3 — Florian (#206)
- [ ] l'année de la Summer School de P19, seule question du dossier de lecture restée sans réponse — priorité 3 — Florian (#203)
- [ ] l'hypothèse H1 de P19 — priorité 3 — Florian (#202)
- [ ] valider ADR-027 (une collection Recensions, champ `objet` — priorité 3 — Florian (#200)
- [ ] vérifier les droits sur les deux documents de contexte de `99_SOURCES` avant de les reprendre dans… — priorité 3 — Florian (#199)
- [ ] trancher ADR-034 (téléchargements reconstruits à la publication plutôt que versionnés) et vérifier… — priorité 3 — Florian (#198)
- [ ] lecture de la boîte à outils — priorité 3 — Florian (#197)
- [ ] « Pourquoi les chartes échouent », trois passages à reprendre — priorité 3 — Florian (#196)
- [ ] valider ADR-030 (référentiel unique, tableur généré, serveur MCP local) et ADR-031 (ouverture de la… — priorité 3 — Florian (#195)
- [ ] trancher les points relevés à la conversion — priorité 3 — Florian (#194)
- [ ] `python scripts/verifier.py --publication` vert, publication, entrée dans `CHANGELOG.md`, post… — priorité 3 — Agent (#193)
- [ ] Contrôle hreflang et plan du site, FR et EN (demande une construction Hugo). — priorité 3 — Agent (#192)
- [ ] Vérification juridique belge — priorité 3 — Agent (#191)
- [ ] `sources-et-versions.md` ligne 23 et sa traduction — priorité 3 — Agent (#190)
- [ ] Étape 3 : serveur MCP local et commande Claude Code (fiche P20 à créer, ADR-030) — priorité 3 — Agent (#189)
- [ ] Rubrique Éthique — priorité 3 — Agent (#188)

### Fait

- [x] Waldron, « AI Governance Must Keep Pace with Legal Practice » (article sponsorisé par LexisNexis ;… — priorité 3 — Florian (#205)
- [x] Tromans, « Will AI Change the Identity of Law Firm Partners? » (article) — priorité 3 — Florian (#204)
- [x] P19 lue et arbitrée par Florian le 2026-11-11 (ticket FLO-18) — priorité 3 — Florian (#201)
- [x] Téléchargements — priorité 3 — Florian (#187)
- [x] FLO-21 · [recension:waldron] Recension Waldron : « AI Governance Must Keep Pace with Legal Practice » — priorité 2 (#1)
- [x] FLO-17 · [recension:chaduteau] Recension Chaduteau : préparer la publication du 12 novembre — priorité 3 (#2)
- [x] FLO-19 · [recension:tromans] Recension Tromans : « Will AI Change the Identity of Law Firm Partners? » — priorité 2 (#14)
- [x] FLO-18 · [recension:p19] Recension P19 (Billion et Fasterling) : préparer la lecture de Florian — priorité 2 (#17)
- [x] FLO-71 · [gh-pages:jerlash] Pousser les brouillons jerlash.labs sur dev pour relecture — priorité 2 (#62)
<!-- fin-bloc-vikunja -->
