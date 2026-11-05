# Backlog

Règle depuis le 2026-11-03 (ADR-025, proposée) : livrer plutôt que construire. Un projet livré par mois, en version de travail publique, plus une piste parallèle « Outils » sans échéance. Tout le reste attend ici, et rien n'en sort sans décision de Florian. Ce qui est livré passe dans `CHANGELOG.md`.

## Maintenant : novembre 2026, P14 Legal AI Governance Toolkit v0.2 et refonte du site (ADR-024)

- [x] Florian : valider ADR-024 (2026-11-05)
- [ ] Florian : valider ADR-025
- [x] Florian : valider `docs/politique-publication.md` (2026-11-03)
- [x] Florian : D01 éditeur jerlash.labs, D02 licence CC BY-NC 4.0 (ADR-026)
- [ ] Florian : confirmer le nom français « Gouverner l'IA au cabinet » (provisoire)
- [x] Gabarit `revue/`, gabarits `toolkit/` et partiel « bloc de statut » ; menu Revue et permaliens anglais ; libellés dans `site/i18n/` (2026-11-03)
- [x] Migrer les 9 articles du blog vers `revue/perspectives/` avec leurs alias `/blog/`, `/fr/blog/`, `/en/blog/` (2026-11-03)
- [ ] Rubrique Éthique (`ethique/`, page Précautions) et entrées Outils et Éthique du menu, à la publication du Toolkit
- [x] Convertir le Toolkit en 9 pages, en brouillon, dans `outils/gouverner-l-ia-au-cabinet/` (2026-11-03) : présentation, « Pourquoi les chartes échouent », charte, gouvernance, homologation, supervision, données, opérations, sources et versions
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
- [x] Collection `revue/recensions/` en brouillon, regroupement par objet, bloc « Œuvre recensée », étiquette des vignettes ; `docs/politique-publication.md` §9 (2026-11-04)
- [x] P19 déposée en brouillon : `site/content/revue/recensions/ce-que-les-mots-font-a-lintelligence-artificielle.md` ; attributions comparées à la page EDHEC Vox (2026-11-04)
- [ ] Florian : lire P19 et prendre position sur les trois réserves de la Discussion (« biais » utile si le référentiel est explicité ; « un bout de code », simplification symétrique ; utilité opérationnelle d'« hallucination ») ; puis reprise dans sa voix
- [ ] Florian : remplir conflits d'intérêts, usage de l'IA et contrôles (marqueurs `[À COMPLÉTER]`)
- [x] Florian : autres recensions transmises (2026-11-04), en brouillon dans `site/content/revue/recensions/` ; front matter à convertir au format ADR-027 lors de la reprise
- [ ] Tromans, « Will AI Change the Identity of Law Firm Partners? » (article)
- [ ] Waldron, « AI Governance Must Keep Pace with Legal Practice » (article sponsorisé par LexisNexis ; chiffres d'enquête à vérifier)
- [ ] Bull, « The 4 Es Inhouse AI Framework » (article, entretien écrit)
- [ ] Legora, entretien avec Jacob Lauritzen (podcast vidéo, 67 min ; citations à minuter)
- [ ] Chaduteau (livre) : relue par Florian, publication prévue le 12 novembre 2026 ; front matter converti et traduit (2026-11-05). Reste : conflits d'intérêts, puis `draft: false` (FR et EN), et lancer le workflow Publication le 12 (la reconstruction automatique n'a lieu que le lundi)
- [x] Susskind (livre) : relue, déclarations complétées, traduite (2026-11-05) ; à publier avec le prochain push
- [x] Recension podcast « L'IA juridique en pratique », ép. 01 (Colliot, Zevra) : relue par Florian, publiée FR et EN (2026-11-05). Fiche : `../otf/traite/recension-colliot/`
- [ ] Traduction anglaise (`/traduire`) ; slug anglais de la collection à décider (`/en/review/recensions/` par défaut)
- [ ] Publication : `draft: false` sur la collection et les recensions prêtes, `python scripts/verifier.py --publication`, `CHANGELOG.md`, post LinkedIn

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

## Livré : site jerlash.labs 0.1.0 (ADR-022), restes à relire

- [x] Identité jerlash appliquée au site Hugo (polices, couleurs, logo, fonds pixel)
- [x] Rubrique Blog : 9 articles, relus et corrigés directement dans `site/content/blog/` (import supprimé le 2026-11-01)
- [x] Sections outils, guides, automatiser, nouveautés et précautions retirées du site publié (brouillons)
- [x] Florian : créer le dépôt GitHub public `jerlash-labs`, donner son URL et le nom du compte
- [x] Mentions légales et confidentialité remises en ligne (2026-11-01) : le site ne fournit aucun service, donc ni BCE, ni TVA, ni adresse de contact ; adresse de GitHub et journaux de GitHub Pages vérifiés sur la documentation de GitHub ; pas de phrase de contact ni de security.txt (décision de Florian)
- [x] Vérification complète sur Linux : archives zip reproductibles d'un système à l'autre (système d'origine fixé à Unix) et jeux de test reproductibles sous Linux (PR #2 et #3)
- [ ] Florian : relire la page d'accueil, les 9 articles importés (dont 4 aux en-têtes vides : titre tiré du nom de fichier) et leurs dates (date du fichier)
- [x] Pousser sur GitHub, activer Pages (source : GitHub Actions), publication verte : en ligne sur jerlash.eu le 2026-11-01
- [x] Accueil : nouveau héros et section « Pourquoi jerlash.labs ? »
- [x] Page À propos réécrite (mission, approche, communs, origine du nom) et traduite en anglais
- [x] Florian : cocher « Enforce HTTPS » dans Settings → Pages dès que le certificat est délivré, puis relancer la publication (liens canoniques en https) ; au 2026-11-01, `https://jerlash.eu` ne répond pas encore

## Livré : version anglaise du site (ADR-023), restes à relire

- [x] Hugo multilingue `/fr/` et `/en/`, libellés i18n, lien FR/EN, hreflang, redirections des anciennes adresses
- [x] `scripts/traductions.py` (état, diff, marquage) et commande `/traduire`
- [x] Traduction initiale des 35 pages
- [x] Florian : valider ADR-023 (acceptée le 2026-11-01)
- [ ] Florian : relire l'anglais (accueil, À propos, articles), compléter `docs/glossaire-traduction.md`
- [x] PR `dev` → `main` (PR #1, fusionnée)

## Ensuite

- [ ] Réorganiser le répertoire du projet (nom jerlash.labs, dossiers, fichiers hors dépôt)
- [ ] Domaine : jerlash.eu choisi et DNS en place ; reste HTTPS (voir plus haut), 2FA GitHub et registraire
- [ ] Rubrique Guides : compléter les quatre guides (clé API, facturation, données envoyées, installation locale)
- [ ] Page Outils et fiches, quand un outil est prêt (piste parallèle)
- [ ] Décisions du Toolkit restées ouvertes : D03 à D10 (registre dans les sources P14), dont D10 version publique et services payants

## Plus tard

Dépôts otf (ADR-028, `../otf/INDEX.md`) :
- [ ] Proposition de recherche « Identité professionnelle, savoirs et pouvoir d'agir » (H1, méthodes mixtes, terrain belge envisagé) : `../otf/JERLASH_Research_Proposal_Identite_Professionnelle_AI_2026-11-04.md` ; Florian : créer la fiche P20 ou non
- [ ] Proposition de research paper « La capitalisation technique des savoirs juridiques » (H1 et C1) : `../otf/JERLASH_Fiche_Recherche_Capitalisation_Expertise_Juridique.md` ; Florian : créer la fiche P21 ou non

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
- [ ] Décider si le tutoriel de veille Cowork, les fiches « avocat entrepreneur » et le livre blanc rejoignent le site

Factory et plan d'amélioration :
- [ ] Factory : valider ADR-007 et le circuit ; AM-001, AM-002 ; essai d'un mois de la mémoire (F03) ; F01
- [ ] Plan d'amélioration du 2026-10-31 (PLAN_AMELIORATIONS.md) : A01, A03, A05, A08 à A18 restent ouverts ; A02, A04, A06, A07 livrés
- [ ] Rythme : fréquence de publication réaliste, revue semestrielle des guides
