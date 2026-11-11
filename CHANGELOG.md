# Changelog

Ce qui est livré, par date : publié, ou prêt à l'être. Le détail des sessions est dans `LOG.md`, ce qui reste à faire dans `BACKLOG.md`.

## 2026-11-11 - Gouvernance de l'IA : les trois téléchargements (prêt à relire)

- Pack complet en zip, charte modèle en .docx et kit « petit cabinet » (les six éléments du niveau 1), en français et en anglais, proposés sur l'accueil de la boîte à outils. Le pack réunit les dix pages en Markdown, le kit, la charte, le tableur, le référentiel et les quatre registres vides que la page « Traçabilité, incidents et formation » annonçait sans les donner.
- Les fichiers sont reconstruits à partir des pages du site par `outils/gouvernance-ia/telechargements/generer_telechargements.py` (bibliothèque standard seule), étape de `scripts/verifier.py` : à chaque vérification et à chaque publication, leur contenu ne peut pas s'écarter de ce qui est publié (ADR-034). Reproductibles : à contenu égal, mêmes octets et même empreinte SHA-256.
- Journal des versions de la boîte à outils (`outils/gouvernance-ia/CHANGELOG.md`) et contrôles automatiques dans `outils/gouvernance-ia/tests/`, repris par `scripts/verifier.py`.

## 2026-11-12 - Recension Chaduteau, « L'impact de l'IA sur les juristes et les avocats d'affaires » (prêt à publier)

- Collection Recensions : recension du livre d'Olivier Chaduteau (LGDJ, coll. Forum, 2026), en français et en anglais. L'ouvrage lit l'IA comme une technologie à usage général et décrit ce qu'elle change aux modèles économiques des cabinets ; la recension prolonge la question vers les conditions dans lesquelles le juriste acquiert et conserve sa capacité de jugement.
- Front matter complet : objet, œuvre, programme H1, date d'arrêt des recherches, contrôles, déclaration d'usage de l'IA, licence, financement, conflits d'intérêts (ADR-024, ADR-027).
- Adresses : `/fr/revue/recensions/lintelligence-artificielle-transforme-t-elle-le-juriste/` et `/en/review/recensions/is-ai-transforming-the-lawyer/`.

## 2026-11-07 - Sommaire actif et parcours de gouvernance (prêt à publier)

- Le sommaire latéral des textes de la Revue et de la boîte à outils met en évidence l'intertitre en cours de lecture (`sommaire.js`, ADR-033).
- Gouvernance de l'IA : chaque page affiche à droite le parcours de gouvernance en trois branches (une par niveau), avec l'étape en cours, la charte toujours en dernier ; bloc repliable sur écran étroit.

## 2026-11-07 - Rubrique Recherche, Revue unifiée, pages de lecture (prêt à publier)

- Rubrique Recherche (FR et EN) au menu : vignettes des trois programmes, Autonomie & IA, Ingénierie juridique, IA & confiance, puis cartes des projets publiés (Gouvernance de l'IA, recension Billion et Fasterling) avec visuels pixelisés et filtre par programme ; une page par programme, qui relie ses projets et ses publications (ADR-032).
- Accueil : « Lire la revue » remplace « Lire le blog » ; section « Programmes de recherche ».
- Revue : tous les textes sur une page, filtrable par type de texte.
- Textes de la Revue et de la boîte à outils : visuel en tête de page, sommaire latéral, chapeau, statut replié, textes précédent et suivant.
- Nouvelle perspective « Outiller l'avocat : personnaliser plutôt que standardiser » (8 novembre 2026), traduite en anglais.

## 2026-11-06 - Gouvernance de l'IA 0.3 : trois niveaux de gouvernance (version de travail publiée)

- Le toolkit P14 devient « Gouvernance de l'IA » (`/fr/outils/gouvernance-ia/`, `/en/tools/ai-governance/`) ; les anciennes adresses redirigent (ADR-029).
- Trois niveaux de gouvernance, déterminés outil par outil ; nouvelle page « Le niveau 1 » et fiche de conformité F01 à F11 ; chaque module dit ce qu'il demande à chaque niveau. Les neuf pages sont publiées et traduites en anglais.
- Rubrique Outils ouverte et ajoutée au menu (FR et EN), avec la section « Boîtes à outils » (ADR-031).
- Tableur des niveaux 2 et 3 (`gouvernance-ia-matrices-0.3.xlsx`), téléchargeable depuis l'accueil du toolkit et disponible dans le dépôt avec son référentiel JSON et son script de génération (ADR-030).

## 2026-11-01 - Pages légales en ligne

- Mentions légales et confidentialité republiées en français et en anglais, liées depuis le pied de page. Le site ne fournissant aucun service, elles ne mentionnent ni BCE, ni TVA, ni adresse de contact.
- ADR-023 (site bilingue) acceptée.

## 2026-11-01 - Version anglaise du site, archives reproductibles

- Site bilingue `/fr/` et `/en/`, français maître, anglais traduit sur demande par `/traduire` (ADR-023) ; 35 pages traduites.
- Accueil : nouveau héros et section « Pourquoi jerlash.labs ? ».
- Archives des outils et jeux de test reproductibles sous Linux comme sous Windows.

## 2026-11-01 - Site jerlash.labs 0.1.0, publié sur jerlash.eu

- Identité jerlash (Schibsted Grotesk, IBM Plex Mono, fonds pixel), accueil, blog de 9 articles importés depuis `articles/`, page À propos (ADR-022).
- Publication GitHub Pages par GitHub Actions, domaine jerlash.eu.
- Retiré provisoirement : mentions légales, confidentialité, phrase de contact et security.txt (à remettre en priorité, voir `BACKLOG.md`).

## Historique antérieur (rien de publié)

- 2026-10-31 au 2026-11-01 : cadrage du projet, Factory, cinq outils en version d'essai (P01, P02, P03, P05, P09), connecteur IA, bibliothèque de références. Aucun n'a été publié ; voir `LOG.md` et `BACKLOG.md`.
