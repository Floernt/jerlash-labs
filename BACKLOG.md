# Backlog

## Phase 0 - Cadrage
- [ ] Relire et valider docs/cahier-des-charges.md
- [ ] Répondre aux questions ouvertes (section 16)
- [x] Trancher ADR-002 (Hugo), ADR-003 (GitHub Pages, OVH), ADR-005 (chemins), ADR-006 (MIT / CC BY 4.0)
- [ ] Lister les comités, boards et interventions pour la page À propos
- [ ] Vérifier les règles de communication applicables aux avocats et les mentions obligatoires
- [x] Choisir le premier outil : P05 Lite (ADR-011), puis P09
- [x] Trancher ADR-007 (Factory, trois parcours), ADR-008 (projets tiers), ADR-009 (plugins, option C)

## Phase 1 - Socle
- [x] Initialiser le dépôt git local (sans remote)
- [x] Initialiser le site dans site/
- [x] Gabarits de page : accueil, catalogue, fiche outil, guide, page simple
- [x] Mode clair / sombre, responsive, accessibilité de base
- [x] Sécurité des pages : CSP et Referrer-Policy en balises meta (GitHub Pages n'accepte pas d'en-têtes, ADR-003)
- [x] security.txt (adresse de contact à compléter)
- [ ] Déploiement et DNS : créer le dépôt GitHub public, activer Pages (source : GitHub Actions), DNS OVH, "Enforce HTTPS", 2FA GitHub et OVH

## Phase 2 - Lancement
- [ ] Guide : obtenir une clé API et la protéger (plan en brouillon)
- [ ] Guide : comprendre la facturation à l'usage (plan en brouillon)
- [ ] Guide : ce que devient une donnée envoyée à un fournisseur d'IA (plan en brouillon)
- [x] Guide : utiliser un outil en local (libellés de l'installateur Python à vérifier sur poste vierge)
- [x] Page Précautions d'usage
- [ ] Premier outil publié avec sa fiche : P05 Lite 0.1.0 prêt, au statut vérification (registre)
- [ ] Mentions légales et confidentialité : rédigées, à compléter et relire (marqueurs)
- [x] Flux RSS des nouveautés
- [ ] Rubrique "Automatiser une prestation" : relire les deux articles importés (contenus/automatiser-une-prestation/) selon la charte éditoriale et les règles de communication (ADR-012)
- [ ] Décider si le tutoriel de veille Cowork, les fiches "avocat entrepreneur" et le livre blanc rejoignent le site

## Phase 3 - Rythme
- [ ] Définir une fréquence de publication réaliste
- [ ] Revue semestrielle des guides (dates de vérification)

## Factory
- [ ] Valider ADR-007 et le circuit factory/pipeline.md
- [ ] Vérifier dans la documentation à jour de Claude Code le format des agents, commandes, skills et hooks, et la possibilité pour un sous-agent d'en appeler un autre
- [ ] Décider AM-001 (hook mémoire) et AM-002 (détection de secrets)
- [ ] Concevoir les composants cle-api, fournisseurs et cout
- [ ] Créer les jeux de test F-DOSSIER-01, F-IDENT-01 (F-DOCX-01 livré)

## Projets issus de l'exploration de github.com/zenzen-sol (2026-10-31)

Fiches dans projets/. Ordre proposé, à valider.

Composants et fondations
- [ ] P09 Pseudonymisation locale (stella/anonymize) - priorité haute, premier outil candidat
- [ ] P11 Conversion locale des pièces (Docling) - conditionne P01, P06, P08
- [ ] P10 Édition .docx dans le navigateur (docx-editor) - conditionne P02 à P06
- [ ] P12 Banc d'essai sur cas fictifs

Outils (inspirés de legal-prompts, MIT)
- [x] P05 Contrôle avant envoi - P05 Lite 0.1.0 (outils/controle-avant-envoi)
- [ ] P01 Inventaire d'un dossier contractuel
- [ ] P02 Glossaire des définitions
- [ ] P03 Conditions particulières et générales
- [ ] P04 Propositions de modifications sur copie séparée

Outils plus lourds
- [ ] P06 Simulateur de négociation (wargame-oss) - nécessite une réécriture locale
- [ ] P08 Revue tabulaire - décider outil ou guide

Guides et contenus
- [ ] P07 Mémoire de dossier pour Claude (skillboxing)
- [ ] P13 Guide des plateformes juridiques open source (mike, stella)

Outillage Factory
- [ ] F01 Méthode d'ingénierie (open-pstack)
- [x] F02 Revue UX intégrée dans l'agent designer-ux
- [ ] F03 Mémoire de la Factory : essai d'un mois de la skill memoire-projet

## Plan d'amélioration du 2026-10-31 (PLAN_AMELIORATIONS.md)

Traiter les P0 avant les P1, sauf dépendance technique justifiée par écrit. Chaque tâche n'est terminée que lorsque la vérification correspondante a réellement réussi (plan, §2 et §12).

- [ ] A01 (P0) : Clarifier les modes d'exécution et sécuriser le BYOK ; rédiger puis faire arbitrer ADR-010. Voir PLAN_AMELIORATIONS.md §3.
- [x] A02 (P0, socle livré : secrets en pré-commit et CI, audit des imports réseau, test sans réseau) : Modèle de menace et contrôles de sécurité exécutables (secrets en pré-commit et CI, flux réseau testés, dépendances). Voir PLAN_AMELIORATIONS.md §3.
- [ ] A03 (P0) : Corriger les assertions de conformité et de responsabilité (ADR-004, cahier des charges, sécurité, fiche outil). Voir PLAN_AMELIORATIONS.md §3.
- [~] A04 (P0, F-DOCX-01 et CI bloquante livrés ; F-IDENT-01 et F-DOSSIER-01 restent) : Passer P12 en priorité haute ; créer F-DOCX-01, F-IDENT-01, F-DOSSIER-01 ; CI bloquante. Voir PLAN_AMELIORATIONS.md §4.
- [ ] A05 (P0) : Parcours léger / standard / renforcé ; preuves observables ; pas d'auto-certification. Voir PLAN_AMELIORATIONS.md §4.
- [x] A06 (P0, P05 Lite 0.1.0 développé et testé ; pilote à faire) : P05 Lite comme premier outil candidat : contrôle .docx non destructif, sans IA ni clé. Voir PLAN_AMELIORATIONS.md §5.
- [ ] A07 (P0) : P09 après P05 ; mesurer rappel et précision par catégorie sur F-IDENT-01. Voir PLAN_AMELIORATIONS.md §5.
- [ ] A08 (P0) : Prototypes de faisabilité ciblés pour P04, P10, P11 avant tout composant complet. Voir PLAN_AMELIORATIONS.md §5.
- [ ] A09 (P1) : Validation du besoin avant le statut prêt (nouveaux champs de fiche projet). Voir PLAN_AMELIORATIONS.md §6.
- [ ] A10 (P1) : Contrat de confiance public dans la fiche outil. Voir PLAN_AMELIORATIONS.md §6.
- [ ] A11 (P1) : Supervision humaine comme propriété de chaque outil. Voir PLAN_AMELIORATIONS.md §6.
- [ ] A12 (P1) : Positionnement éditorial et catalogue organisé par tâches. Voir PLAN_AMELIORATIONS.md §6.
- [ ] A13 (P1) : Vérifier les capacités de la version installée de Claude Code ; simplifier les agents. Voir PLAN_AMELIORATIONS.md §7.
- [ ] A14 (P1) : Unifier statuts et dépendances (intégré, en essai ; dépendances du MVP ; types de blocage). Voir PLAN_AMELIORATIONS.md §7.
- [ ] A15 (P1) : Mesurer efficacité de production et qualité après publication. Voir PLAN_AMELIORATIONS.md §7.
- [ ] A16 (P2) : Composants partagés seulement après deux usages réels. Voir PLAN_AMELIORATIONS.md §8.
- [ ] A17 (P2) : Maintenance, versions et fin de vie. Voir PLAN_AMELIORATIONS.md §8.
- [ ] A18 (P2) : Diffusion : groupe pilote et retours structurés. Voir PLAN_AMELIORATIONS.md §8.

Décisions humaines ouvertes : plan §13.
