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
Statut : Proposée
Contexte : site de contenu, majoritairement statique, rédigé en Markdown, avec quelques pages outils interactives.
Options : Astro, Eleventy, Hugo, HTML écrit à la main. `[À COMPARER au moment du choix, sur la base de la documentation à jour]`
Décision : à prendre.
Conséquences : conditionne les commandes indiquées dans CLAUDE.md.

## ADR-003 - Hébergement
Date : 2026-10-31
Statut : Proposée
Contexte : site statique, pas de backend. Contraintes : HTTPS, en-têtes de sécurité configurables, sous-domaines, localisation des journaux.
Options : hébergeur actuel de florianernotte.be `[À COMPLÉTER]`, Cloudflare Pages, Netlify, GitHub Pages, hébergeur européen.
Décision : à prendre.
Conséquences : GitHub Pages ne permet pas, à ma connaissance, de définir librement des en-têtes HTTP `[À VÉRIFIER]`, ce qui compte pour la Content-Security-Policy.

## ADR-004 - Outils locaux, clé de l'utilisateur, aucun backend
Date : 2026-10-31
Statut : Acceptée (brief initial), en révision (PLAN_AMELIORATIONS.md, A01 et A03 ; voir ADR-010)
Décision : chaque outil s'exécute chez l'utilisateur avec sa propre clé API. iavocat.be n'opère aucun serveur qui reçoit des données ou des clés.
Conséquences : pas de coût d'API pour le site. L'architecture supprime les flux de données de dossier vers iavocat.be, sans préjuger des qualifications et responsabilités juridiques de chaque acteur (éditeur du site, concepteur de l'outil, avocat utilisateur, fournisseur d'API, hébergeur), qui restent à vérifier par type d'outil [À VÉRIFIER, A03]. En contrepartie, l'installation et la configuration reposent sur l'utilisateur, d'où l'importance des guides.
Note de correction (2026-10-31) : la version initiale affirmait "pas de responsabilité de traitement des données de dossier". Cette conclusion ne découlait pas de l'absence de backend ; elle a été retirée.

## ADR-005 - Chemins ou sous-domaines pour les outils
Date : 2026-10-31
Statut : Proposée
Options : A) iavocat.be/outils/<slug> ; B) <slug>.iavocat.be ; C) fiches en chemins, outils exécutables en sous-domaines.
Recommandation : C, pour isoler chaque page qui manipule une clé API.
Décision : à prendre.

## ADR-006 - Publication et licence du code
Date : 2026-10-31
Statut : Proposée
Contexte : un outil local auquel on confie une clé et des documents inspire davantage confiance si son code est lisible.
Options : code ouvert (licence MIT, Apache 2.0, EUPL ou autre), code fermé, mixte.
Décision : à prendre.

## ADR-007 - Organisation de la production en Factory
Date : 2026-10-31
Statut : Proposée
Contexte : plusieurs outils à produire avec des agents Claude Code ; besoin de cohérence et de contrôle.
Décision proposée : circuit unique (factory/pipeline.md), agents spécialisés, agent ops-factory chargé des contrôles de passage et de l'amélioration de la Factory, validation de Florian aux étapes "prêt" et "publié".
Conséquences : chaque outil laisse une trace (spécification, rapports, rétrospective) ; la Factory s'enrichit à chaque projet.

## ADR-008 - Réutilisation de projets tiers
Date : 2026-10-31
Statut : Proposée
Contexte : plusieurs fiches reprennent des projets open source (MIT, Apache-2.0, AGPL-3.0) ou s'en inspirent.
Décision proposée : MIT et Apache-2.0 acceptés avec mentions de licence conservées et fichier TIERS.md par outil ; AGPL-3.0 exclu pour le code embarqué sauf décision contraire ; projet sans licence identifiée : aucun texte ni code repris, seulement l'idée.
Conséquences : vérification de licence obligatoire à l'étape "prêt".

## ADR-009 - Plugins tiers dans le dépôt (open-pstack, skillboxing)
Date : 2026-10-31
Statut : Proposée
Options : A) installer les plugins d'origine, figés sur une version ; B) reprendre leurs principes dans des agents et skills internes (solution livrée) ; C) B maintenant, réévaluer A après un mois d'usage.
Recommandation : C.
Décision : à prendre.

## ADR-010 - Modes d'exécution, BYOK et secrets
Date : 2026-10-31
Statut : Proposée (PLAN_AMELIORATIONS.md, A01)
Contexte : docs/principes-outils.md admettait l'appel direct d'une API depuis une page web avec une clé saisie dans le navigateur, sans décision spécifique ni modèle de menace.
Options à documenter : A) navigateur entièrement local, sans IA distante ; B) application ou service local sur le poste, qui appelle éventuellement une API distante ; C) modèle exécuté sur la machine de l'utilisateur. Appel direct depuis le navigateur avec clé : uniquement par décision spécifique, sur la base de la documentation officielle du fournisseur, du modèle de menace et de tests.
À produire avant arbitrage : matrice fournisseur x mode d'exécution x authentification x données envoyées x source officielle x date de vérification ; politique de secrets (clés dédiées, limites de dépense, révocation, absence de journalisation).
Mesure conservatoire en attendant : aucun outil ne manipule de clé API tant que son architecture n'a pas été approuvée.
Décision : à prendre.

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
