# Fournisseurs d'API d'IA : matrice comparative

## 1. Objet, date, méthode et limites

Ce document répond au point 4 d'ADR-010 (`docs/decisions.md`) : avant le premier outil qui appelle une IA distante, établir une matrice fournisseur × authentification × données envoyées × source officielle × date. Il sert aux avocats qui se demandent s'ils peuvent envoyer des extraits de pièces de dossier à l'une de ces API.

Date de consultation de toutes les sources : **2026-10-31**.

Méthode : lecture des seules pages officielles des fournisseurs (documentation, centre de confidentialité, conditions, DPA, prix), par l'outil de consultation web de l'agent. Chaque affirmation renvoie à l'URL lue. Les extraits en anglais sont cités entre guillemets ; le reste est une traduction ou un résumé.

Limites, à garder en tête avant toute décision :

- L'outil de consultation restitue parfois un résumé de la page plutôt que le texte intégral. Les chiffres et noms de modèles ont été recopiés tels que restitués ; ils doivent être relus sur la page avant d'être repris dans un fichier de configuration ou une fiche publique.
- Certaines pages ont refusé la lecture automatique (HTTP 403 chez openai.com ; politique de confidentialité de Mistral tronquée). Les informations correspondantes viennent d'extraits de moteur de recherche limité aux domaines officiels, et sont marquées `[À VÉRIFIER]`.
- Les prix, noms de modèles et conditions changent souvent. Ce document est un relevé daté, pas une référence durable.
- Ce document décrit ce que disent les fournisseurs. Il ne tranche aucune question de secret professionnel, de déontologie ou de RGPD : ces questions sont listées comme points que l'avocat doit vérifier.

## 2. Tableau de synthèse

| Fournisseur | Authentification | Conservation par défaut (entrées/sorties API) | ZDR | Entraînement par défaut | DPA (art. 28 RGPD) | Résidence UE |
|---|---|---|---|---|---|---|
| Anthropic (API Claude) | `Authorization: Bearer` (ou `x-api-key`, ancien) + `anthropic-version` | Contradiction entre sources : « within 30 days » (centre de confidentialité) contre « not retained by default » (documentation) `[À VÉRIFIER]` | Oui, sur demande à l'équipe commerciale, par organisation ; exclu pour les « Covered Models » (Fable 5/5.1, Mythos) | Non (API commerciale) | Oui, incorporé automatiquement aux Commercial Terms, avec CCT | **Non** : inférence `global` ou `us` seulement ; stockage `us` seulement |
| OpenAI (API) | `Authorization: Bearer` | Journaux de surveillance des abus jusqu'à 30 jours ; état applicatif variable selon l'API | Oui, après approbation préalable d'OpenAI (ventes) | Non, sauf adhésion explicite | Oui, incorporé au Services Agreement ; lien « Execute » distinct `[À VÉRIFIER]` ; OpenAI Ireland pour l'EEE | Oui (Europe : EEE + Suisse), par projet, sous conditions (ZDR ou équivalent), +10 % |
| Mistral AI (La Plateforme) | `Authorization: Bearer` | 30 jours glissants pour surveillance des abus `[À VÉRIFIER, source indirecte]` | Oui, offres payantes, sur demande motivée, à la discrétion de Mistral ; points d'accès sans état seulement | Contradictoire selon les textes ; modèles « Labs » et « Preview » utilisables pour l'entraînement `[À VÉRIFIER]` | Oui, fait partie de l'accord commercial | Oui : point d'accès `api.eu.mistral.ai` (surcoût) ; défaut = point d'accès global sans engagement de lieu `[contradiction, À VÉRIFIER]` |
| Google (API Gemini, AI Studio) | `x-goog-api-key` | 55 jours (surveillance des abus) | Pas de ZDR garanti ; renvoi vers Vertex AI | Oui en gratuit, non en payant ; dans l'EEE, seules les offres payantes sont admises | Oui pour les services payants (« Data Processing Addendum for Products Where Google is a Data Processor ») | Non documenté pour l'API Gemini `[À VÉRIFIER]` |
| Google (Vertex AI) | IAM Google Cloud | Cache en mémoire 24 h (désactivable) ; journalisation pour abus possible, durée non indiquée `[À VÉRIFIER]` | Atteignable par configuration (liste de réglages) | Non sans permission | Cloud Data Processing Addendum | Oui : multirégion `eu` et régions `europe-west` |

## 3. Détail par fournisseur

### 3.1 Anthropic (API Claude)

**Accès par API.** Point d'accès de génération : `POST https://api.anthropic.com/v1/messages`. En-têtes : `Authorization: Bearer <clé>` (l'en-tête `x-api-key` reste accepté comme « Legacy fallback »), `anthropic-version` (obligatoire ; la page d'aperçu donne l'exemple `2026-10-21`, la page d'authentification `2023-06-01`), `content-type: application/json`, et `anthropic-workspace-id` pour une clé non rattachée à un espace de travail.
Sources : https://platform.claude.com/docs/en/api/overview ; https://platform.claude.com/docs/en/manage-claude/authentication (2026-10-31).

**Gestion des clés.** Création dans la console (`platform.claude.com/settings/keys`). Trois types : clé personnelle, clé de compte de service, clé d'espace de travail (« legacy »). Une clé peut être limitée à un seul espace de travail. Expiration choisie à la création (3 heures, 1 jour, 7 jours, 30 jours, durée libre ou « Never »), non modifiable ensuite. **Disable** est réversible, **Delete** est définitif. Limites de dépense mensuelles par espace de travail, avec alertes (pas sur le « Default Workspace »).
Sources : https://platform.claude.com/docs/en/manage-claude/authentication ; https://platform.claude.com/docs/en/manage-claude/workspaces (2026-10-31).

**Conservation.** Le centre de confidentialité indique que, pour les utilisateurs de l'API, Anthropic supprime automatiquement entrées et sorties « within 30 days of receipt or generation », sauf exceptions : arrangement contraire (dont un accord ZDR), violation de la politique d'usage (entrées et sorties jusqu'à 2 ans, scores de classification jusqu'à 7 ans), retours d'utilisateur (5 ans), obligation légale (page mise à jour le 1er juillet 2026). La documentation technique écrit de son côté : « Conversation content (your prompts and Claude's outputs) is not retained by default; the exception is Covered Models, which require 30-day retention. » Ces deux formulations ne disent pas la même chose `[À VÉRIFIER]`.
Fonctions qui conservent des données par nature : Batch (« 29-day retention »), Files API (jusqu'à suppression ou expiration), exécution de code (jusqu'à 30 jours).
Sources : https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data ; https://platform.claude.com/docs/en/manage-claude/api-and-data-retention (2026-10-31).

**Zero data retention.** « Under a ZDR arrangement, Anthropic does not store customer prompts or responses at rest after the API response is returned. » Sur demande à l'équipe commerciale, activé organisation par organisation. Exclusions : console et « playground », Managed Agents, offres grand public, fonctions marquées « No » (Batch, Files API, exécution de code). Les « Covered Models » (Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5) exigent une conservation de 30 jours et ne sont pas disponibles en ZDR « unless expressly authorized by Anthropic ». CORS n'est pas pris en charge pour les organisations sous ZDR.
Source : https://platform.claude.com/docs/en/manage-claude/api-and-data-retention (2026-10-31).

**Entraînement.** Produits commerciaux et API : pas d'utilisation des entrées et sorties pour l'entraînement par défaut, sauf retour explicite (pouce levé/baissé, signalement) ou accord de l'utilisateur (page mise à jour le 18 août 2026). La documentation ajoute : « Retained data is never used for model training without your express permission. »
Sources : https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training ; https://platform.claude.com/docs/en/manage-claude/api-and-data-retention (2026-10-31).

**DPA.** « Anthropic's DPA with Standard Contractual Clauses (SCCs) is automatically incorporated into our Commercial Terms of Service » (article du 16 mars 2026). DPA daté du 24 février 2025 : CCT module 2 ou 3, addenda britannique et suisse, droit irlandais pour les CCT de l'UE, sous-traitants listés à https://www.anthropic.com/subprocessors, suppression des données dans les 30 jours suivant la fin du contrat. Le Data Privacy Framework n'est pas mentionné dans le DPA tel que lu.
Sources : https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa ; https://www.anthropic.com/legal/data-processing-addendum ; https://www.anthropic.com/legal (2026-10-31).

**Localisation.** Deux réglages : « inference geo » (`global` par défaut, ou `us`, ce dernier facturé 1,1 fois) et « workspace geo » (stockage au repos ; « Currently, `"us"` is the only available workspace geo »). « Only `"us"` and `"global"` are available. » Aucune option UE sur l'API directe. Le DPA ne nomme pas de lieu de traitement.
Sources : https://platform.claude.com/docs/en/manage-claude/data-residency ; https://platform.claude.com/docs/en/about-claude/pricing (2026-10-31).

**Modèles (relevé du 2026-10-31).**

| Identifiant | Contexte | Entrée / 1 M jetons | Sortie / 1 M jetons | Remarque |
|---|---|---|---|---|
| `claude-opus-5-5` | 1M tokens | $4 | $20 | Modèle recommandé par défaut |
| `claude-sonnet-5-5` | 1M tokens | $2 | $10 | |
| `claude-haiku-5-5` | 1M tokens | $0.10 (≤ 100 000 jetons) ; $0.50 (> 100 000) | $0.50 ; $2.50 | |

Le contexte de 1M est facturé au tarif standard pour les modèles 4.6 et suivants, sauf Haiku 5.5. Claude Fable 5.1 (`claude-fable-5-1`, $10 / $50) n'est pas retenu ici : c'est un « Covered Model », incompatible avec le ZDR.
Sources : https://platform.claude.com/docs/en/about-claude/models/overview ; https://platform.claude.com/docs/en/about-claude/pricing (2026-10-31). Identifiants également confirmés par le skill `claude-api` (cache du 2026-10-06).

**Conditions d'utilisation.** La Usage Policy classe « Legal » parmi les domaines à haut risque (« advising an individual on their legal rights, obligations, or liability »). Exigences : revue humaine qualifiée (« A qualified person must meaningfully review a High-risk AI Recommendation ») et information de la personne (« must be clearly told that AI was used to produce it »). L'information juridique générale est exclue. La page indique une date d'effet au 12 novembre 2026, postérieure à la consultation `[À VÉRIFIER : version applicable au 31 octobre 2026]`.
Source : https://www.anthropic.com/legal/aup (2026-10-31).

### 3.2 OpenAI (API)

**Accès par API.** Point d'accès de génération : `POST https://api.openai.com/v1/responses` (l'ancien `POST /v1/chat/completions` existe toujours). Authentification : `Authorization: Bearer <clé>` ; en-têtes `OpenAI-Organization` et `OpenAI-Project` pour les clés utilisateur anciennes. OpenAI demande de ne pas exposer la clé dans un navigateur ou une application.
Sources : https://developers.openai.com/api/reference/overview ; https://developers.openai.com/api/reference/resources/responses/methods/create (2026-10-31).

**Gestion des clés.** Clés par projet. Limites par projet (budget mensuel, seuil d'alerte, plafond strict optionnel ; au plafond, erreur 429 `project_spend_limit_exceeded`, avec un léger décalage d'application). Révocation par suppression dans le tableau de bord ; dates d'expiration et durée maximale des clés recommandées. Lu via extraits de recherche `[À VÉRIFIER sur les pages]`.
Sources : https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform ; https://developers.openai.com/api/docs/guides/spend-limits ; https://developers.openai.com/api/docs/guides/production-best-practices (2026-10-31).

**Conservation.** « By default, abuse monitoring logs are generated for all API feature usage and retained for up to 30 days. » État applicatif selon l'API : `/v1/responses` conserve 30 jours par défaut (au moins 30 jours si `store` vaut `true`) ; `/v1/chat/completions` ne conserve en principe rien, sauf sorties audio (1 heure) ; `/v1/files` et `/v1/batches` jusqu'à suppression.
Source : https://developers.openai.com/api/docs/guides/your-data (2026-10-31).

**Zero data retention.** ZDR et « Modified Abuse Monitoring » : « Currently, these controls are subject to prior approval by OpenAI and acceptance of additional requirements. » Demande par l'équipe commerciale. Sous ZDR, `store` est toujours traité comme `false`.
Source : https://developers.openai.com/api/docs/guides/your-data (2026-10-31).

**Entraînement.** « data sent to the OpenAI API is not used to train or improve OpenAI models », sauf adhésion explicite.
Source : https://developers.openai.com/api/docs/guides/your-data (2026-10-31). La page « Enterprise privacy » (https://openai.com/enterprise-privacy/) a refusé la lecture (403).

**DPA.** Version v.010126 : le DPA « supplements, and is incorporated into, the OpenAI Services Agreement » ; pour un client établi dans l'EEE ou en Suisse, il est conclu avec OpenAI Ireland Ltd. ; OpenAI agit comme sous-traitant (section 1.1) ; transferts hors EEE par OpenAI Ireland « on the basis of agreements containing SCCs […] or an adequacy decision » (section 4.1) ; liste des sous-traitants : https://platform.openai.com/subprocessors ; objection possible dans les 30 jours. Le document renvoie aussi à un lien « Execute Data Processing Agreement » : savoir si une signature distincte est nécessaire en plus de l'acceptation du Services Agreement reste `[À VÉRIFIER]`.
Sources : https://cdn.openai.com/pdf/openai-data-processing-addendum.pdf ; https://openai.com/policies/data-processing-addendum/ (403 à la lecture) (2026-10-31).

**Localisation.** Résidence des données configurée par projet, à la création (choix de la région). Europe (EEE + Suisse) disponible, avec stockage et traitement régionaux, mais : « Requires Zero Data Retention, Modified Abuse Monitoring, Private Retention with PSP, or Safety Retention. » Point d'accès : `eu.api.openai.com`. `store=true` est impossible hors États-Unis. Surcoût : « Data residency endpoints are charged a 10% uplift » pour les modèles publiés à partir du 5 mars 2026.
Sources : https://developers.openai.com/api/docs/guides/your-data ; https://developers.openai.com/api/docs/pricing (2026-10-31).

**Modèles (relevé du 2026-10-31).**

| Identifiant | Contexte | Entrée / 1 M jetons | Sortie / 1 M jetons |
|---|---|---|---|
| `gpt-6-astra` | 1.05M | $10.00 (≤ 272K) ; $20.00 (> 272K) | $50.00 ; $75.00 |
| `gpt-6.1-sol` | 1.05M | $2.00 ; $4.00 | $10.00 ; $15.00 |
| `gpt-6.1-terra` | 1.05M | $1.00 ; $2.00 | $5.00 ; $7.50 |

Sources : https://developers.openai.com/api/docs/models ; https://developers.openai.com/api/docs/pricing (2026-10-31). La disponibilité de chacun de ces modèles sur le point d'accès européen n'est pas documentée sur les pages lues `[À VÉRIFIER]`.

**Conditions d'utilisation.** Les Usage Policies interdisent de « provide others with tailored advice that requires a license, without appropriate involvement by a licensed professional ». Les conditions demandent de ne pas utiliser les sorties « as a substitute for professional advice ». Lu via extraits de recherche, pages en 403 `[À VÉRIFIER]`.
Sources : https://openai.com/policies/usage-policies/ ; https://openai.com/policies/row-terms-of-use/ (2026-10-31).

### 3.3 Mistral AI (La Plateforme)

**Accès par API.** `POST https://api.mistral.ai/v1/chat/completions`, en-tête `Authorization: Bearer <clé>`. Points d'accès régionaux : `api.eu.mistral.ai`, `api.us.mistral.ai`.
Sources : https://docs.mistral.ai/api ; https://docs.mistral.ai/inference/regional-inference (2026-10-31).

**Gestion des clés.** Création dans Admin Panel › API › API Keys, avec date d'expiration ; espace de travail, portée et expiration non modifiables ensuite ; révocation par suppression. Politiques de durée maximale au niveau de l'organisation ou de l'espace de travail. Limite de dépense par espace de travail : à son atteinte, l'accès API de l'espace est suspendu jusqu'au mois suivant. Lu via extraits de recherche ; deux pages donnent des chemins différents pour régler la limite `[À VÉRIFIER]`.
Sources : https://docs.mistral.ai/admin/identity-access/api-keys ; https://docs.mistral.ai/admin/billing-usage/usage-limits ; https://docs.mistral.ai/getting-started/quickstarts/admin/manage-workspaces (2026-10-31).

**Conservation.** Politique de confidentialité, selon un extrait de recherche : « Except for specific APIs, we keep your Input and Output for the period necessary to generate the Output and then for thirty (30) rolling days to monitor abuse (unless zero data retention is activated). » La page n'a pas pu être lue en entier `[À VÉRIFIER]`.
Source : https://legal.mistral.ai/terms/privacy-policy (2026-10-31).

**Zero data retention.** « ZDR is available on paid plans for supported stateless API calls. » L'article d'aide précise « only with pay-as-you-go ». Demande motivée au support ; Mistral « may deny it ». Points d'accès couverts : `/v1/chat/completions`, `/v1/fim/completions`, `/v1/embeddings`, modération, classification, `/v1/ocr`, audio. Exclus : agents, batch, conversations, bibliothèques, `/v1/files`, modèles « Labs ».
Sources : https://docs.mistral.ai/admin/monitor-comply/zero-data-retention ; https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr (2026-10-31).

**Entraînement.** Les textes ne s'accordent pas.
- Commercial Terms (effet au 25 septembre 2026), section 4.2 : « Mistral AI will not use Customer Data or Outputs to train its artificial intelligence models except » en cas d'adhésion volontaire, de retour d'utilisateur, ou d'usage de modèles « Labs or Preview ». Section 4.3 : pour ces modèles, les préférences de refus choisies ailleurs ne s'appliquent pas.
- DPA (effet au 27 juillet 2026), section 2.3 : Mistral peut traiter des données personnelles comme responsable de traitement pour entraîner ses modèles, sauf si le client a refusé.
- Centre d'aide : refus possible dans Admin › Privacy, interrupteur « Anonymous improvement data ».
Le régime par défaut de l'API, et celui de l'offre gratuite (« Experiment »), restent `[À VÉRIFIER]`. Attention : `mistral-large-4` est en « Public Preview », donc concerné par la section 4.3.
Sources : https://legal.mistral.ai/terms/commercial-terms-of-service ; https://legal.mistral.ai/terms/data-processing-addendum ; https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training (2026-10-31).

**DPA.** Le DPA « forms part of and supplements the Agreement » et s'applique lorsque les produits tournent sur l'infrastructure de Mistral (Commercial Terms, section 12.3). Transferts vers des pays adéquats, sous garanties appropriées ou « pursuant to the SCCs » ; liste des sous-traitants : trust.mistral.ai/subprocessors ; délai d'objection de 10 jours ; données inaccessibles 30 jours après la fin de l'accès.
Sources : https://legal.mistral.ai/terms/data-processing-addendum ; https://legal.mistral.ai/terms/commercial-terms-of-service (2026-10-31).

**Localisation.** Le centre d'aide (12 août 2026) écrit : « By default, your data is hosted in the European Union », avec transferts temporaires possibles hors UE selon la fonction, et des CCT pour les pays sans adéquation. La documentation sur l'inférence régionale indique au contraire que le point d'accès par défaut (`api.mistral.ai`) est global, sans engagement de lieu d'inférence ; le point d'accès `api.eu.mistral.ai` vise un traitement dans l'UE et l'AELE, facturé avec un surcoût régional, mais sans agents, batch ni Files API, et la garantie tombe si une fonction non prise en charge est utilisée. Le réglage par défaut est donc `[À VÉRIFIER]`.
Sources : https://help.mistral.ai/en/articles/347629-where-do-you-store-my-data-or-my-organization-s-data ; https://docs.mistral.ai/inference/regional-inference (2026-10-31).

**Modèles (relevé du 2026-10-31).**

| Identifiant | Contexte | Entrée / 1 M jetons | Sortie / 1 M jetons | Statut |
|---|---|---|---|---|
| `mistral-large-4` (alias `mistral-large-4-0`) | 1M | $0.7 | $2.1 | Public Preview, publié le 2026-10-06 |
| Mistral Small 4 | `[À VÉRIFIER]` | $0.15 | $0.6 | identifiant exact et statut non lus `[À VÉRIFIER]` |

La FAQ de la page de prix indique « Mistral Large costs $0.5 /M tokens in and $1.5 /M tokens out », ce qui contredit la fiche du modèle `[À VÉRIFIER]`. `mistral-medium-3-5` (256k) est déprécié au 31 octobre 2026, avec renvoi vers Mistral Large 4.
Sources : https://docs.mistral.ai/models/mistral-large-4-0.md ; https://docs.mistral.ai/inference/pricing ; https://mistral.ai/pricing ; https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04 (2026-10-31).

**Conditions d'utilisation.** Commercial Terms, section 3.5 : ne pas utiliser les sorties « as a substitute for professional advice (e.g., legal, tax, or medical) ». Modèles « Labs » et « Preview » : « restricted to professional use only ». La Usage Policy (https://legal.mistral.ai/terms/usage-policy) n'a pas été lue `[À VÉRIFIER]`.
Source : https://legal.mistral.ai/terms/commercial-terms-of-service (2026-10-31).

### 3.4 Google (API Gemini via AI Studio, et Vertex AI)

**Accès par API (Gemini API).** Hôte `generativelanguage.googleapis.com`. L'exemple REST actuel de la documentation : `POST https://generativelanguage.googleapis.com/v1beta/interactions`. La méthode `generateContent` reste documentée, mais son URL exacte n'apparaît pas sur les pages lues `[À VÉRIFIER]`. En-tête : « All requests to the Gemini API must include a `x-goog-api-key` header with your API key. »
Sources : https://ai.google.dev/api ; https://ai.google.dev/gemini-api/docs/text-generation (2026-10-31).

**Gestion des clés.** Les clés sont créées dans un projet Google Cloud et héritent de son niveau et de sa facturation. Passage en offre payante : liaison d'un compte de facturation et prépaiement (minimum $5). Plafond mensuel par projet (« Monthly spend cap ») réglable dans AI Studio, décrit comme « experimental and limited in scope », dépassable pendant environ 10 minutes de latence de facturation. Plafonds par niveau de compte de facturation. Révocation et restrictions de clés : non lues `[À VÉRIFIER]`.
Source : https://ai.google.dev/gemini-api/docs/billing (mise à jour 2026-09-28, lue le 2026-10-31).

**Conservation (Gemini API).** « Google retains the following data for fifty-five (55) days » (prompts, informations contextuelles, sorties) pour détecter les violations de la politique d'usage. Ancrage par Google Search ou Maps : 30 jours, non désactivable. Cache implicite en mémoire, TTL de 24 heures. Interactions API : stockage d'état activé par défaut (`store`).
Sources : https://ai.google.dev/gemini-api/docs/usage-policies (mise à jour 2026-06-09) ; https://ai.google.dev/gemini-api/docs/zdr (2026-10-31).

**Zero data retention (Gemini API).** Pas d'option contractuelle : la page liste des réglages (mettre `store` à `false`, éviter le cache explicite, supprimer les fichiers, ne pas utiliser l'ancrage) et recommande Vertex AI « for guaranteed zero data retention or enterprise data processing agreements ». Elle ne dit pas comment échapper à la conservation de 55 jours `[À VÉRIFIER]`.
Source : https://ai.google.dev/gemini-api/docs/zdr (2026-10-31).

**Entraînement (Gemini API).** Offre gratuite : « Google uses the content you submit to the Services and any generated responses to provide, improve, and develop », avec relecture humaine possible. Offre payante : « Google doesn't use your prompts or responses to improve our products. » Pour les utilisateurs de l'EEE, de la Suisse et du Royaume-Uni, seules les offres payantes sont admises pour mettre une application à disposition, et les conditions des services payants s'appliquent à tous les services.
Sources : https://ai.google.dev/gemini-api/terms (effet au 23 mars 2026, mise à jour 2026-04-28) ; https://ai.google.dev/gemini-api/docs/pricing (2026-10-31).

**DPA (Gemini API).** Les prompts et réponses des services payants sont traités sous le « Data Processing Addendum for Products Where Google is a Data Processor » (version 10, 7 mai 2026). Transferts : le Data Privacy Framework « will apply to any Restricted European Transfer to a certified Google entity in the US » ; à défaut, CCT. La présence de l'API Gemini dans la liste des « Processor Services » (business.safety.google/services/) et le mode d'acceptation n'ont pas été vérifiés `[À VÉRIFIER]`.
Sources : https://ai.google.dev/gemini-api/terms ; https://business.safety.google/processorterms/ (2026-10-31).

**Localisation (Gemini API).** Aucune page lue ne précise le lieu de traitement, ni d'option de résidence UE pour l'API Gemini `[À VÉRIFIER]`.

**Vertex AI : règles différentes.** Entraînement : « Google won't use your data to train or fine-tune any AI/ML models without your prior permission or instruction. » Cache en mémoire supprimé au plus tard 24 heures après écriture, désactivable par projet (`disableCache`). Journalisation possible pour abus, durée non indiquée `[À VÉRIFIER]`. ZDR atteignable en combinant : journalisation des requêtes désactivée (défaut), `store = false`, cache désactivé, pas d'ancrage Google Search (3 jours) ni Maps (30 jours) ; pour certains modèles avancés, le ZDR « may not be possible ». Résidence : « The European Union multi-region (`eu`) endpoint strictly covers data residency within EU member states » ; régions `europe-west` possibles ; le point d'accès global n'offre aucune garantie. DPA : Cloud Data Processing Addendum, incorporé au contrat Google Cloud ; transferts par CCT ou « Alternative Transfer Solution » (dernière modification le 30 octobre 2026).
Sources : https://docs.cloud.google.com/vertex-ai/generative-ai/docs/vertex-ai-zero-data-retention ; https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency (mises à jour 2026-10-30) ; https://cloud.google.com/terms/data-processing-addendum (2026-10-31).

**Modèles (Gemini API, relevé du 2026-10-31).**

| Identifiant | Contexte | Entrée / 1 M jetons (payant) | Sortie / 1 M jetons (payant) | Gratuit |
|---|---|---|---|---|
| `gemini-4-argon` | 1M (« unified 1M context window ») | $2.00 jusqu'au 30 novembre 2026, puis $4.00 | $10.00, puis $20.00 | Non disponible |
| `gemini-3.8-flash` | 1 048 576 (sortie 65 536) | $0.75 jusqu'au 31 décembre 2026, puis $1.50 | $3.75, puis $7.50 | Oui (données utilisées pour améliorer les produits) |

Les prix Vertex AI n'ont pas été relevés `[À VÉRIFIER]`.
Sources : https://ai.google.dev/gemini-api/docs/models ; https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ; https://ai.google.dev/gemini-api/docs/pricing (2026-10-31).

**Conditions d'utilisation.** Ne pas se fier aux services pour des conseils « medical, mental health, legal, financial, or other professional advice ». Interdiction de l'usage clinique.
Source : https://ai.google.dev/gemini-api/terms (2026-10-31).

## 4. Accès par un nuage d'entreprise avec résidence UE

Seul ce que la documentation officielle établit est repris ici.

**Microsoft Foundry (Azure OpenAI et autres « Models sold by Azure »).** Les prompts et réponses ne sont pas accessibles à OpenAI ni utilisés pour entraîner les modèles. Avec un déploiement standard, traitement dans la géographie choisie. Avec un déploiement « DataZone » créé dans une ressource située dans un État membre de l'UE, « prompts and responses may be processed in that or any other European Union Member Nation ». Un déploiement « Global » peut traiter les données dans n'importe quelle géographie. Données au repos dans la géographie désignée. Surveillance des abus avec relecture humaine possible, par des employés situés dans l'EEE pour les déploiements dans l'EEE ; la « modified abuse monitoring » est accordée sur formulaire, sous critères d'accès limité. La durée de conservation des données retenues pour relecture n'est pas indiquée sur les pages lues `[À VÉRIFIER]`. DPA : Microsoft Products and Services Data Protection Addendum (https://aka.ms/DPA).
Sources : https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy ; https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/abuse-monitoring (2026-10-31).
Pour Claude sur Foundry, Anthropic est le sous-traitant, et seule une « US Data Zone » est mentionnée (https://platform.claude.com/docs/en/manage-claude/data-residency) ; aucune zone UE n'est documentée pour Claude sur Foundry `[À VÉRIFIER]`.

**AWS Bedrock.** Les fournisseurs de modèles n'ont pas accès aux journaux ni aux prompts et réponses. Profils d'inférence géographiques (préfixe `eu`) : les requêtes restent dans la géographie, mais peuvent quitter la région source. Conservation réglable par région ou projet (`none` = zéro conservation ; `default` ; `aws_review`). Claude Fable 5 et 5.1 exigent `aws_review` (conservation jusqu'à 30 jours, relecture humaine par AWS possible) ; le ZDR des modèles Claude relève d'Anthropic.
Sources : https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html (2026-10-31).

**Google Vertex AI.** Voir 3.4 : multirégion `eu` limitée aux États membres de l'UE, ZDR par configuration.

Ces trois voies supposent un contrat et un compte d'entreprise chez le fournisseur de nuage. Elles changent l'architecture du futur outil (authentification IAM plutôt que clé simple) et méritent une décision distincte.

## 5. Conséquences pour la conception des outils

### 5.1 Ce qu'un outil local affiche avant l'envoi

Avant le premier envoi, puis à chaque changement de fournisseur ou de modèle, l'outil affiche :

1. le fournisseur, le point d'accès exact (par exemple `api.anthropic.com` ou `api.eu.mistral.ai`) et l'identifiant du modèle lus dans la configuration ;
2. le texte qui va partir, ou au minimum sa taille en caractères et en jetons estimés, et l'indication qu'une pseudonymisation a été appliquée ou non ;
3. le coût estimé, avec la date des tarifs utilisés ;
4. un résumé daté de ce que le fournisseur déclare (conservation par défaut, ZDR actif ou non selon la déclaration de l'utilisateur, entraînement, lieu de traitement), avec les URL de la section 3, sans reformulation qui irait au-delà de la source ;
5. une case à cocher explicite avant l'envoi ; sans elle, rien ne part.

L'outil n'affirme pas que le ZDR est actif : il ne peut pas le vérifier. Il affiche ce que l'utilisateur a déclaré dans la configuration.

### 5.2 Réglages recommandés à l'utilisateur

- Une clé dédiée à l'outil, dans un projet ou espace de travail dédié, avec la durée de vie la plus courte acceptable (Anthropic, Mistral, OpenAI le permettent).
- Une limite de dépense sur ce projet ou cet espace (Anthropic : par espace de travail, pas sur le Default Workspace ; OpenAI : par projet ; Mistral : par espace de travail ; Google : plafond par projet, expérimental).
- Le ZDR si le fournisseur l'accorde (Anthropic, OpenAI, Mistral sur demande ; Vertex par configuration). Chez Anthropic, éviter les « Covered Models », incompatibles avec le ZDR.
- Chez Google, n'utiliser l'API Gemini qu'en offre payante (règle des conditions pour l'EEE) et éviter l'ancrage Google Search.
- Chez Mistral, viser le point d'accès `api.eu.mistral.ai` si l'objectif est un traitement dans l'UE, et éviter les modèles « Preview » et « Labs » tant que la question de l'entraînement n'est pas levée.
- Révocation immédiate de la clé en cas de doute (Anthropic : « Disable » réversible ou « Delete » définitif).
- Côté outil : clé lue depuis une variable d'environnement ou un `.env` ignoré par git, jamais journalisée (ADR-010, point 2). Ne pas utiliser les fonctions avec état (Files API, Batch, Responses avec `store=true`, agents) : elles sortent du ZDR chez Anthropic, OpenAI et Mistral.

### 5.3 Où ranger les noms de modèles

Dans le fichier de configuration de chaque outil (`config.example` versionné, configuration réelle non versionnée), conformément à `docs/principes-outils.md`. Exemple de structure, sans clé :

```toml
[fournisseur]
nom = "anthropic"                         # anthropic | openai | mistral | google
point_acces = "https://api.anthropic.com/v1/messages"
modele = "claude-sonnet-5-5"
variable_cle = "ANTHROPIC_API_KEY"         # nom de la variable, jamais la valeur
zdr_declare = false                        # déclaration de l'utilisateur, non vérifiable
tarif_entree_usd_par_million = 2.00
tarif_sortie_usd_par_million = 10.00
tarifs_releves_le = "2026-10-31"
source_tarifs = "https://platform.claude.com/docs/en/about-claude/pricing"
```

Aucun identifiant de modèle ni tarif dans le code. Le tableau de la section 2 et les relevés de la section 3 sont repris dans ce fichier, avec leur date, et revus à chaque version de l'outil.

### 5.4 Matrice ADR-010 (mode B, application locale)

| Fournisseur | Authentification | Données envoyées | Source officielle principale | Date |
|---|---|---|---|---|
| Anthropic | `Authorization: Bearer` + `anthropic-version` | Texte (et PDF en ligne, éligible ZDR) via `/v1/messages` ; pas de Files API | platform.claude.com/docs/en/manage-claude/api-and-data-retention | 2026-10-31 |
| OpenAI | `Authorization: Bearer` | Texte via `/v1/responses` avec `store=false`, ou `/v1/chat/completions` | developers.openai.com/api/docs/guides/your-data | 2026-10-31 |
| Mistral | `Authorization: Bearer` | Texte via `/v1/chat/completions` (point d'accès UE possible) | docs.mistral.ai/admin/monitor-comply/zero-data-retention | 2026-10-31 |
| Google Gemini API | `x-goog-api-key` | Texte via Interactions/generateContent, offre payante, `store=false`, sans ancrage | ai.google.dev/gemini-api/docs/zdr | 2026-10-31 |

### 5.5 Points que l'avocat doit vérifier (sans conclusion à sa place)

Les règles déontologiques applicables et les critères d'un « prestataire conforme » sont analysés dans `docs/deontologie-ia.md` (2026-11-01).


- La compatibilité de l'envoi d'extraits de pièces avec le secret professionnel et les règles déontologiques applicables (dont les règlements de l'OVB ou d'AVOCATS.BE sur l'usage des outils informatiques), au regard de la conservation déclarée par chaque fournisseur.
- Sa qualité au regard du RGPD (responsable de traitement pour les données de dossier, en principe), la base de licéité, et la présence éventuelle de catégories particulières (art. 9) ou de données pénales (art. 10).
- La validité de l'acceptation du DPA par simple acceptation des conditions, et les sous-traitants ultérieurs listés.
- Les transferts hors UE : mécanisme invoqué (CCT, Data Privacy Framework), et la nécessité d'une analyse d'impact du transfert.
- L'opportunité d'une analyse d'impact (art. 35 RGPD).
- L'information du client sur l'usage d'une IA, notamment au regard de la Usage Policy d'Anthropic pour les domaines juridiques.
- Les obligations éventuelles au titre du règlement (UE) 2024/1689 sur l'IA.

## 6. Points `[À VÉRIFIER]` regroupés

1. **Anthropic, conservation par défaut** : « within 30 days » (centre de confidentialité, 1er juillet 2026) contre « not retained by default » (documentation). Demander une clarification ou lire les Commercial Terms en vigueur.
2. **Anthropic, Usage Policy** : date d'effet affichée au 12 novembre 2026 ; identifier la version applicable au 31 octobre 2026.
3. **Anthropic, résidence UE** : aucune option sur l'API directe (inférence `global`/`us`, stockage `us`) ; à recontrôler avant chaque version.
4. **OpenAI, DPA** : incorporé au Services Agreement, mais un lien « Execute Data Processing Agreement » existe ; vérifier si une signature distincte est requise.
5. **OpenAI, pages en 403** : Enterprise privacy, page DPA HTML, Usage Policies, Services Agreement lus via extraits ; relire directement.
6. **OpenAI, gestion des clés et limites** : lu via extraits de recherche ; relire les pages.
7. **OpenAI, modèles disponibles sur `eu.api.openai.com`** : non documenté sur les pages lues.
8. **Mistral, conservation de 30 jours** : extrait de recherche de la politique de confidentialité, page non lue en entier.
9. **Mistral, entraînement par défaut** sur l'API et sur l'offre gratuite « Experiment » : Commercial Terms, DPA et centre d'aide ne s'accordent pas.
10. **Mistral, modèles « Preview »** : `mistral-large-4` est en Public Preview ; les Commercial Terms autorisent l'entraînement sur ces modèles malgré un refus.
11. **Mistral, localisation par défaut** : « hosted in the European Union » (centre d'aide) contre point d'accès global sans engagement (documentation).
12. **Mistral, prix de Mistral Large** : $0.5 / $1.5 (FAQ) contre $0.7 / $2.1 (fiche du modèle et page de prix de la documentation).
13. **Mistral Small 4** : identifiant exact, contexte et statut non lus.
14. **Mistral, Usage Policy** : non lue.
15. **Mistral, limite de dépense** : deux chemins différents dans l'interface selon les pages.
16. **Google Gemini API, ZDR** : aucune option documentée pour échapper à la conservation de 55 jours.
17. **Google Gemini API, localisation et résidence UE** : non documentées sur les pages lues.
18. **Google Gemini API, DPA** : présence dans la liste des « Processor Services » et mode d'acceptation.
19. **Google Gemini API, URL exacte de `generateContent`**, révocation et restrictions de clés.
20. **Vertex AI** : durée de journalisation pour abus ; prix non relevés.
21. **Microsoft Foundry** : durée de conservation des données retenues pour relecture humaine ; absence de zone UE documentée pour Claude sur Foundry.
22. **Ensemble** : chiffres et identifiants restitués par l'outil de consultation, parfois sous forme de résumé ; relecture humaine de chaque page avant reprise dans une configuration ou une fiche publique.
