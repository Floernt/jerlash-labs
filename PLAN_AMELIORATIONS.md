# iavocat.be — Plan d'amélioration du projet et de la Factory

**Date :** 31 octobre 2026  
**Statut :** propositions à arbitrer, non encore mises en œuvre  
**Périmètre examiné :** archive `iavocat.zip` fournie le 31 octobre 2026  
**Destination conseillée dans le dépôt :** `PLAN_AMELIORATIONS.md` (racine)

> **Objectif.** Transformer le cadrage documentaire actuel en une chaîne de production capable de livrer des outils juridiques fiables, utiles, contrôlables et réellement utilisables par des avocats belges. Ce document est un plan d'exécution, **pas** une instruction d'appliquer automatiquement toutes les décisions proposées. Les décisions d'architecture, de publication, de licence et de conformité restent soumises à validation humaine.

## 1. Diagnostic synthétique

### Points forts constatés

- Cahier des charges, principes d'outils et architecture éditoriale déjà documentés.
- Registre de décisions d'architecture (`docs/decisions.md`).
- Pipeline Factory, agents spécialisés et principe de validation humaine.
- Volonté de préserver les fichiers d'origine, de travailler avec des données fictives et de documenter les flux.
- Catalogue initial de projets avec composants mutualisables.

### Limites observées dans l'archive

1. **Absence d'implémentation :** `site/` et `outils/` sont vides ; les mécanismes de sécurité, de test et de publication ne sont pas encore éprouvés par du code.
2. **Architecture BYOK non arbitrée :** les appels directs depuis une page web avec une clé utilisateur font l'objet d'un traitement trop permissif ; les contraintes diffèrent selon les fournisseurs et l'environnement d'exécution.
3. **Contrôles surtout documentaires :** le pipeline prévoit des rapports d'agents, sans suite de tests, CI ni critères de sécurité exécutables dans l'archive.
4. **Processus uniforme :** neuf agents et un pipeline complet, même pour de petites modifications ; le coût d'orchestration n'est pas encore justifié par des mesures.
5. **Priorités discutables :** P09 est proposé comme premier outil alors que sa fiabilité est délicate à démontrer ; P05 dispose d'un mode déterministe qui pourrait fournir une première livraison plus simple.
6. **Mesure de la valeur insuffisante :** les fiches décrivent les solutions mais pas systématiquement la fréquence du besoin, le gain attendu ni les indicateurs d'adoption.
7. **Certaines assertions juridiques trop catégoriques :** l'ADR-004 assimile l'absence de backend à l'absence de responsabilité pour les traitements de données de dossier ; la qualification juridique doit être nuancée et vérifiée au cas par cas.
8. **Incohérences de statuts :** `factory/registre.md` utilise « intégré » et « en essai », absents de la liste des statuts de `factory/pipeline.md`.

## 2. Conventions de réalisation

**Priorités**

- **P0 — Bloquant :** traiter avant la publication d'un premier outil manipulant des données sensibles ou des clés.
- **P1 — Important :** intégrer dans le socle et lors des deux premières livraisons.
- **P2 — Évolution :** une fois un premier outil publié et testé par des utilisateurs.

**Chaque action doit comporter :** responsable, modification documentaire ou technique, preuve vérifiable, décision humaine requise le cas échéant, date et résultat.

**Principe de pilotage :** une tâche n'est pas terminée parce qu'un agent a généré un rapport ; elle est terminée quand le livrable existe et que les vérifications pertinentes ont réellement réussi.

---

## 3. P0 — Sécurité, architecture et responsabilité

### A01 — Clarifier les modes d'exécution et sécuriser le BYOK

**Constat :** `docs/principes-outils.md` admet l'appel API directement depuis une page web, avec clé saisie dans le navigateur ; `docs/decisions.md` a accepté le principe « local + BYOK + aucun backend » sans distinguer suffisamment les risques et les conditions techniques.

**Fichiers à modifier :**

- `docs/principes-outils.md`
- `docs/securite-confidentialite.md`
- `docs/decisions.md` (ajouter **ADR-010 — Modes d'exécution, BYOK et secrets**)
- `docs/cahier-des-charges.md`
- `templates/fiche-outil.md`
- `CLAUDE.md` (après décision)

**Travaux :**

- [ ] Distinguer explicitement **exécution locale du code**, **traitement local des données** et **transmission de données à un fournisseur externe**. Ces notions ne sont pas synonymes.
- [ ] Définir trois architectures de référence : **(A)** navigateur entièrement local sans IA distante ; **(B)** application ou service local sur le poste, qui appelle éventuellement une API distante ; **(C)** exécution d'un modèle sur la machine de l'utilisateur.
- [ ] N'admettre l'appel direct depuis le navigateur avec clé permanente que sur la base d'une **décision spécifique**, étayée par la documentation officielle du fournisseur, le modèle de menace et les tests ; ne jamais présumer sa sécurité ou son support.
- [ ] Évaluer la faisabilité d'une application de bureau ou d'un service local à accès restreint, sans exposer librement une interface sur le réseau ; documenter également les risques propres à ce service local.
- [ ] Définir une politique de secrets : clés dédiées, permissions minimales quand possibles, limites de dépense, stockage sécurisé si nécessaire, révocation et absence de journaux contenant la clé.
- [ ] Établir une matrice « fournisseur × mode d'exécution × authentification × données envoyées × compatibilité × source officielle × date de vérification ».
- [ ] Décrire les limites des extensions navigateur, injections de scripts, compromissions de dépendances, XSS, redirections et extensions de navigateur ; envisager CSP, isolation d'origine et verrouillage réseau sans présenter ces mesures comme une garantie absolue.

**Critères de validation :**

- [ ] ADR-010 rédigée, puis arbitrée et datée.
- [ ] Aucun outil ne manipule de clé API avant l'approbation explicite de son architecture.
- [ ] Un schéma du trajet des données et des secrets est fourni par outil, et testé.
- [ ] Les fournisseurs et mécanismes d'authentification autorisés sont documentés à partir de sources officielles à jour.

### A02 — Créer un modèle de menace et des contrôles de sécurité vérifiables

**Fichiers à modifier/créer :** `docs/securite-confidentialite.md`, `factory/standards/code.md`, `factory/pipeline.md`, `.github/workflows/ci.yml` (si GitHub est retenu), configuration de contrôle des secrets.

**Travaux :**

- [ ] Créer une grille de menaces par classe d'outil : fuite de clé, exfiltration de documents, injection d'instructions dans une pièce, dépendance compromise, extraction de données par sortie, persistance inattendue, journalisation, fichier DOCX malveillant, falsification de résultat.
- [ ] Définir les canaux réseau autorisés pour chaque application et tester leur respect en conditions d'exécution ; ne pas s'en remettre à la seule CSP.
- [ ] Installer un contrôle de secrets **pré-commit** et **en CI** ; prévoir une procédure de révocation si un secret a été commité.
- [ ] Ajouter contrôle de dépendances, vérification des licences, audit de vulnérabilités et génération d'une nomenclature des dépendances si cela est proportionné à la stack.
- [ ] Tester les entrées non fiables : documents, noms de fichiers, métadonnées, prompts intégrés dans les pièces et sorties potentiellement dangereuses.
- [ ] Introduire une grille des risques résiduels, avec décision d'acceptation nominative et datée avant publication.

**Critères de validation :**

- [ ] Le pipeline échoue effectivement lorsqu'un secret de test est introduit.
- [ ] Les tests détectent au moins un appel réseau non autorisé injecté dans un environnement de test.
- [ ] Toute dépendance ajoutée est identifiée avec version et licence.
- [ ] Aucun rapport « sécurité conforme » ne peut remplacer des preuves de contrôles réalisés.

### A03 — Corriger les assertions de conformité et de responsabilité

**Constat précis :** `docs/decisions.md` (ADR-004) indique « pas de responsabilité de traitement des données de dossier ». Cette conclusion n'est pas déductible du seul fait de ne pas exploiter de backend.

**Fichiers à modifier :** `docs/decisions.md`, `docs/cahier-des-charges.md`, `docs/securite-confidentialite.md`, `templates/fiche-outil.md`, pages légales futures.

**Travaux :**

- [ ] Remplacer cette assertion par une formule conditionnelle : l'architecture réduit ou supprime certains flux vers iavocat.be, **sans préjuger** des qualifications et responsabilités juridiques de chaque acteur.
- [ ] Distinguer éditeur du site, concepteur/distributeur de l'outil, utilisateur avocat, fournisseur d'API, hébergeur et éventuels sous-traitants.
- [ ] Vérifier, pour chaque type d'outil, la confidentialité, le secret professionnel, les rôles RGPD, les transferts internationaux et, le cas échéant, les obligations relatives à l'IA.
- [ ] Vérifier les obligations de communication professionnelle et les mentions légales selon les règles applicables à l'éditeur du site.
- [ ] Documenter les traitements éventuellement réalisés par le site lui-même : journaux d'hébergement, contact par courriel, sécurité et mesure d'audience si activée.
- [ ] Éviter les garanties absolues telles que « aucun traitement » ou « aucun risque » lorsque la preuve technique ou juridique n'existe pas.

**Critères de validation :**

- [ ] Les assertions juridiques publiques ont été relues sur leur fondement, leur portée et leurs exceptions.
- [ ] Les pages « Confidentialité » et « Précautions » correspondent aux traitements et flux réellement constatés.
- [ ] Le rôle de l'avocat utilisateur est décrit sans transfert automatique de responsabilité ni exonération artificielle.

---

## 4. P0 — Un banc d'essai et une CI avant la première publication

### A04 — Promouvoir P12 en infrastructure prioritaire

**Constat :** `projets/P12-banc-essai.md` est en priorité « moyenne » alors que le banc d'essai conditionne la vérification des outils.

**Fichiers à modifier/créer :**

- `projets/P12-banc-essai.md` : priorité **haute**.
- `BACKLOG.md` : P12 dans les fondations à réaliser avant publication.
- `factory/jeux-de-test/` : fixtures entièrement fictives, oracles et manifestes.
- `factory/standards/livrables.md` : format de preuve de test.
- `factory/pipeline.md` et `.github/workflows/ci.yml` : exécution automatique.

**Travaux :**

- [ ] Créer `F-DOCX-01` : DOCX fictif comportant commentaires, suivi des modifications, métadonnées, auteurs, notes, champs et objets à contrôler.
- [ ] Créer `F-IDENT-01` : identifiants belges fictifs, noms, adresses, quasi-identifiants, variantes typographiques et faux positifs.
- [ ] Créer `F-DOSSIER-01` : dossier fictif de droit belge comportant contradictions, versions, dates et sources identifiables.
- [ ] Définir, pour chaque fixture, **résultats attendus**, interdictions, cas limites et version du jeu de données.
- [ ] Automatiser au moins : installation, compilation, vérification statique, tests unitaires, tests d'intégration, scan des secrets et contrôle des sorties réseau quand pertinent.
- [ ] Pour les outils génératifs : mesurer exactitude, complétude, erreurs critiques, hallucinations, traçabilité et variations sur plusieurs exécutions ; dissocier les contrôles déterministes des jugements humains.
- [ ] Publier les conditions de test et les limites des mesures, sans divulguer de données réelles.

**Critères de validation :**

- [ ] Une commande documentée lance la suite de vérification en local.
- [ ] La CI est bloquante sur les contrôles critiques.
- [ ] Une modification volontairement fautive déclenche un échec attendu.
- [ ] Les rapports indiquent commit/version, scénario, résultat attendu, résultat obtenu et cause d'échec.

### A05 — Mettre le pipeline sous contrôle de preuves

**Fichiers à modifier :** `factory/pipeline.md`, `factory/README.md`, `factory/standards/livrables.md`, `.claude/agents/testeur.md`, `.claude/agents/verificateur-securite.md`, `.claude/agents/ops-factory.md`.

**Travaux :**

- [ ] Définir trois niveaux de contrôle : **léger** (contenu/correction mineure), **standard** (outil local sans IA distante) et **renforcé** (données client, clés, IA distante, effets juridiques substantiels).
- [ ] Faire du niveau renforcé la règle par défaut en cas d'incertitude sur le risque.
- [ ] Exiger des rapports référant à des preuves observables (commande exécutée, statut de CI, sortie de test, version, fichiers inspectés).
- [ ] Interdire à l'agent ayant produit une fonctionnalité d'auto-certifier seul sa conformité.
- [ ] Conserver la validation humaine pour les décisions d'architecture, les arbitrages juridiques et la publication.
- [ ] Prévoir une procédure de dérogation motivée, datée, temporaire et accompagnée de mesures compensatoires.

**Critères de validation :**

- [ ] Le type de pipeline est déterminé et enregistré avant le développement.
- [ ] Les blocages sont traçables et reproductibles.
- [ ] Un défaut bloquant empêche effectivement le passage au statut « publié ».

---

## 5. P0 — Prioriser une première livraison réaliste

### A06 — Faire de P05 Lite le premier outil public candidat

**Constat :** `projets/P05-controle-avant-envoi.md` mentionne `dépend_de: [P04, P10]` alors qu'un contrôle non destructif et sans IA pourrait être autonome.

**Fichiers à modifier :** `projets/P05-controle-avant-envoi.md`, `BACKLOG.md`, `factory/registre.md`, `docs/cahier-des-charges.md` (MVP, sous réserve de validation).

**Proposition de découpage :**

- **P05 Lite / MVP :** lecture et contrôle **non destructifs** d'un `.docx`, sans API ni clé, avec rapport et recommandations ; aucune édition ni « nettoyage automatique » à ce stade.
- **P05 avancé :** édition ou génération de copies, contrôle assisté par modèle et fonctions dépendant éventuellement de P04/P10.

**Travaux :**

- [ ] Modifier la dépendance du MVP : `dépend_de: []` si la preuve technique confirme l'autonomie du lecteur DOCX choisi.
- [ ] Définir la liste exacte des éléments détectés dans les principales parties du paquet OOXML (document, commentaires, propriétés et parties reliées selon besoin), sans promettre une couverture universelle.
- [ ] Contrôler le comportement avec les documents non pris en charge, les fichiers chiffrés/protégés et les erreurs de parsing : **ne pas donner un feu vert trompeur**.
- [ ] Prévoir une sortie « détecté / non détecté dans les contrôles réalisés / non vérifié / erreur », plutôt qu'un simple « document sûr ».
- [ ] Conserver le fichier source intact ; générer un rapport local lisible et exportable.
- [ ] Produire une démo avec fichier fictif et une fiche de limites.

**Critères de validation MVP :**

- [ ] Aucun envoi de document vers un serveur externe pendant les essais.
- [ ] Toutes les anomalies **explicitement plantées dans `F-DOCX-01` et couvertes par le périmètre annoncé** sont détectées, ou les écarts sont documentés avant publication.
- [ ] Aucune modification du DOCX d'entrée.
- [ ] Rapport clair, avec localisation et possibilité de correction manuelle.
- [ ] Le cas d'erreur ne se transforme jamais en conclusion rassurante non fondée.

### A07 — Repositionner P09 et expliciter ses limites

**Fichiers à modifier :** `projets/P09-pseudonymisation-locale.md`, `BACKLOG.md`, `templates/fiche-outil.md`.

**Travaux :**

- [ ] Conserver P09 comme composant majeur, mais le développer après une preuve initiale de capacité de livraison et le banc `F-IDENT-01`.
- [ ] Mesurer **rappel** (entités sensibles réellement détectées) et **précision** (proportion de détections correctes), par catégorie ; documenter les faux négatifs, notamment les identifiants indirects.
- [ ] Vérifier séparément français juridique, noms, adresses, registre national belge, numéros d'entreprise, IBAN et autres motifs retenus.
- [ ] Présenter explicitement la différence entre **pseudonymisation** et **anonymisation**, ainsi que le risque de réidentification par le contexte.
- [ ] Mettre une revue humaine des passages détectés et non détectés avant export.
- [ ] Si la table de correspondance est conservée, documenter chiffrement éventuel, emplacement, durée de conservation et procédure de suppression.
- [ ] Ne jamais considérer P09 comme un blanc-seing pour transmettre des pièces couvertes par le secret professionnel à un service tiers.

**Critères de validation :**

- [ ] Résultats par catégorie publiés avec taille du corpus et limites ; aucun taux global seul n'est utilisé pour suggérer une garantie.
- [ ] Traitement local vérifié sur les scénarios couverts.
- [ ] Avertissements visibles dans l'outil, pas seulement dans le guide.

### A08 — Reporter les composants lourds jusqu'à validation de leurs dépendances

**Fichiers :** `projets/P04-propositions-modifications.md`, `projets/P10-composant-editeur-docx.md`, `projets/P11-composant-conversion-documents.md`, `BACKLOG.md`.

- [ ] Réaliser des prototypes de faisabilité ciblés pour les modifications suivies et la conversion, avec jeux de tests.
- [ ] Ne pas lancer immédiatement un éditeur DOCX complet pour satisfaire un besoin de simple lecture ou inspection.
- [ ] Comparer les options en termes de fidélité documentaire, prise en charge des formats, performance, compatibilité, licences et complexité d'installation.
- [ ] Abandonner ou réduire le périmètre d'un composant dont les garanties ne peuvent pas être démontrées avec les moyens disponibles.

---

## 6. P1 — Produits, expérience utilisateur et confiance

### A09 — Insérer une validation du besoin avant « prêt »

**Fichiers à modifier :** `templates/fiche-projet.md`, `factory/pipeline.md`, `factory/registre.md`, `factory/metriques.md`.

**Champs à ajouter au modèle de fiche :**

- Utilisateurs et tâches concernés.
- Fréquence réelle du problème ; méthode actuelle de résolution.
- Frictions, erreurs et coût de l'approche actuelle.
- Hypothèse de valeur et indicateur observable (temps gagné, incidents détectés, qualité, compréhension).
- Solutions alternatives, y compris l'absence de nouvel outil.
- Complexité, risques, dépendances et coût de maintenance.
- Critère d'abandon ou de réduction du périmètre.
- Hypothèses encore non vérifiées.

**Critères :**

- [ ] Aucun projet n'entre au statut « prêt » sans valeur attendue et critère de succès testable.
- [ ] Au moins cinq tests exploratoires auprès d'avocats aux profils variés sont envisagés pour les premiers outils ; la taille de l'échantillon et ses limites sont déclarées.
- [ ] Les observations réelles sont distinguées des opinions ou projections de l'équipe.

### A10 — Créer un « contrat de confiance » public pour chaque outil

**Fichiers à modifier :** `templates/fiche-outil.md`, `docs/cahier-des-charges.md`, pages de fiches dans `site/` lorsque créées.

**Contenu recommandé :**

- Ce que l'outil fait et **ne fait pas**.
- Où s'exécute le code et où les données sont effectivement traitées.
- Flux sortants possibles ; destinataires et finalités.
- Nécessité ou non d'une clé API ; politique de conservation du fournisseur le cas échéant.
- Version vérifiée, date, code source et dépendances majeures.
- Tests réalisés, périmètre couvert, résultats et limites.
- Éléments qui doivent être contrôlés par l'avocat.
- Procédure de signalement, de correction et de retrait d'une version défectueuse.

**Critères :**

- [ ] Toute affirmation technique vérifiable est associée à une preuve datée lorsque cela est possible.
- [ ] La fiche n'annonce pas « 100 % sûr », « conforme RGPD » ou « aucune donnée transmise » sans périmètre vérifié et justification.

### A11 — Concevoir la supervision humaine comme une propriété de chaque outil

**Fichiers :** `docs/principes-outils.md`, `factory/standards/livrables.md`, `templates/fiche-projet.md`, `templates/fiche-outil.md`.

- [ ] Préférer la proposition à l'action irréversible pour les tâches à conséquence juridique.
- [ ] Afficher, lorsqu'il y a une sortie IA, les sources ou extraits d'origine **vérifiables** et l'incertitude pertinente.
- [ ] Autoriser acceptation/rejet des modifications individuellement lorsqu'il s'agit d'une édition contractuelle.
- [ ] Préserver l'original et permettre comparaison avant/après.
- [ ] Différencier faits extraits, inférences du modèle et appréciations humaines.
- [ ] Prévoir des tests UX de compréhension des limites, et pas uniquement d'ergonomie.

**Critère :**

- [ ] Un avocat peut identifier les éléments nécessitant son jugement et contrôler ce qui sera exporté ou utilisé.

### A12 — Clarifier le positionnement éditorial d'iavocat.be

**Fichiers :** `docs/cahier-des-charges.md`, `docs/charte-editoriale.md`, `templates/fiche-outil.md`, futur `site/`.

**Proposition de positionnement à valider :** « Un laboratoire ouvert d'outils pratiques pour les avocats, testés, documentés et conçus pour préserver la maîtrise professionnelle. »

- [ ] Organiser le catalogue par **tâches** (préparer un document, analyser un dossier, vérifier, comparer, structurer) plutôt que seulement par technologies.
- [ ] Prévoir une démonstration fictive avant installation.
- [ ] Afficher clairement niveau technique, compatibilité et effort de prise en main.
- [ ] Favoriser les guides progressifs et les parcours de premier usage pour les avocats non techniciens.
- [ ] Mesurer la réussite du premier parcours, les difficultés signalées et les corrections publiées sans installer de traçage intrusif par défaut.

---

## 7. P1 — Simplifier et fiabiliser la Factory

### A13 — Actualiser les capacités Claude Code avant d'ajouter des couches internes

**Fichiers :** `factory/README.md`, `.claude/agents/*.md`, `.claude/commands/*.md`, `.claude/skills/memoire-projet/SKILL.md`, `projets/F03-memoire-factory.md`.

- [ ] Vérifier **dans la documentation officielle correspondant à la version installée** les règles de délégation entre sous-agents, les permissions, la mémoire native, les hooks et les commandes/skills.
- [ ] Supprimer ou réécrire les affirmations devenues obsolètes sur l'impossibilité de délégation imbriquée, si la version utilisée la permet.
- [ ] Éviter la duplication avec la mémoire native si ses capacités couvrent les besoins ; conserver la mémoire documentaire du dépôt lorsque cela sert la traçabilité ou la portabilité.
- [ ] Restreindre les outils autorisés aux agents selon leur fonction et limiter les modifications hors de leur périmètre.
- [ ] Définir des seuils de déclenchement : un changement mineur ne mobilise pas obligatoirement tous les agents ; une modification à risque déclenche le parcours renforcé.

**Critère :**

- [ ] Chaque règle d'orchestration est compatible avec la version réellement utilisée et vérifiée sur un projet factice.

### A14 — Unifier les statuts et corriger les dépendances documentaires

**Fichiers :** `factory/pipeline.md`, `factory/registre.md`, `projets/F02-revue-ux.md`, `projets/F03-memoire-factory.md`, `templates/fiche-projet.md`.

- [ ] Décider si « intégré » et « en essai » sont des statuts transversaux, des attributs distincts ou des états propres aux projets Factory.
- [ ] Appliquer une seule nomenclature dans pipeline, registre et métadonnées, ou ajouter explicitement une dimension `état_exploitation` séparée.
- [ ] Décrire les dépendances **du MVP** séparément de celles de la version complète (notamment P05).
- [ ] Distinguer « bloqué par une décision » et « bloqué techniquement ».
- [ ] Automatiser, lorsque utile, la validation des champs obligatoires et des références croisées.

**Critère :**

- [ ] Aucun statut et aucune dépendance utilisée dans le registre n'est hors de la nomenclature publiée.

### A15 — Mesurer l'efficacité de production et la qualité après publication

**Fichiers :** `factory/metriques.md`, `factory/retours/README.md`, `factory/ameliorations.md`.

- [ ] Suivre durée de cycle, retours en arrière, coût API de développement/évaluation, bugs détectés en test et après publication.
- [ ] Mesurer la part des reprises de travail causées par une mauvaise spécification, un mauvais test ou une divergence entre agents.
- [ ] Suivre les incidents utilisateurs, fréquence de mise à jour et délai de correction.
- [ ] Identifier les composants réellement réutilisés et leur coût de maintenance.
- [ ] Utiliser les indicateurs comme support d'amélioration, pas comme justification automatique d'une augmentation de l'autonomie d'un agent.

**Critère :**

- [ ] Après deux livraisons, une rétrospective compare la Factory à un parcours simplifié et propose de supprimer les étapes sans valeur démontrée.

---

## 8. P2 — Écosystème et évolutivité

### A16 — Préparer un socle de composants partagé seulement après besoins réels

**Fichiers :** `factory/composants/README.md`, `factory/standards/code.md`.

- [ ] Mutualiser en priorité les composants déjà employés par deux outils (lecture documentaire, export, visualisation des sources, configuration des fournisseurs, suivi des coûts).
- [ ] Définir des interfaces stables et des tests de non-régression avant mutualisation.
- [ ] Éviter un framework interne générique avant deux cas d'usage concrets.

### A17 — Documenter maintenance, versions et fin de vie

**Fichiers :** `docs/cahier-des-charges.md`, `templates/fiche-outil.md`, `factory/pipeline.md`.

- [ ] Définir versionnement, dates de revue, politique de correctifs et retrait des outils non maintenus.
- [ ] Prévoir une procédure de réponse aux vulnérabilités et une manière de prévenir les utilisateurs lorsque nécessaire et possible.
- [ ] Documenter les versions de fournisseurs et bibliothèques compatibles ; prévoir un mode de dégradation explicite lorsqu'une API change.

### A18 — Établir une stratégie de diffusion et d'apprentissage

**Fichiers :** `docs/cahier-des-charges.md`, `factory/metriques.md`.

- [ ] Tester les outils auprès d'un groupe pilote d'avocats francophones belges avec des scénarios fictifs.
- [ ] Organiser les retours par besoin, incident, incompréhension, friction et proposition d'évolution.
- [ ] Publier des démonstrations et guides reproductibles plutôt que des promesses générales d'efficacité.
- [ ] Mesurer adoption utile et capacité à terminer une tâche, avec respect des choix de confidentialité.

---

## 9. Tableau de pilotage des actions

| ID | Priorité | Objet | Fichiers principalement concernés | Livrable / preuve |
|---|---|---|---|---|
| A01 | P0 | Architecture BYOK | `docs/principes-outils.md`, `docs/decisions.md` | ADR-010 + matrice de compatibilité |
| A02 | P0 | Sécurité exécutable | `docs/securite-confidentialite.md`, CI | Tests de secrets, flux et dépendances |
| A03 | P0 | Responsabilités juridiques | ADR-004, cahier des charges, pages légales | Mentions corrigées et vérifiées |
| A04 | P0 | Banc d'essai P12 | `projets/P12-banc-essai.md`, `factory/jeux-de-test/` | Fixtures + tests automatisés |
| A05 | P0 | Contrôles de passage | `factory/pipeline.md`, agents | Gates fondés sur preuves |
| A06 | P0 | Premier MVP P05 Lite | `projets/P05-controle-avant-envoi.md` | Outil DOCX non destructif testé |
| A07 | P0 | Fiabilité P09 | `projets/P09-pseudonymisation-locale.md` | Mesures de précision/rappel et limites |
| A08 | P0 | Maîtrise de portée | P04, P10, P11, backlog | Prototypes de faisabilité |
| A09 | P1 | Validation des besoins | `templates/fiche-projet.md` | Hypothèses et tests utilisateurs |
| A10 | P1 | Contrat de confiance | `templates/fiche-outil.md` | Fiche avec preuves et limites |
| A11 | P1 | Supervision humaine | principes, standards, fiches | Contrôle des propositions IA |
| A12 | P1 | Positionnement public | cahier des charges, site | Catalogue orienté usages |
| A13 | P1 | Simplification des agents | `factory/README.md`, `.claude/` | Règles adaptées à version vérifiée |
| A14 | P1 | Registre et statuts | `factory/registre.md`, pipeline | Nomenclature cohérente |
| A15 | P1 | Mesures de performance | `factory/metriques.md` | Tableau de bord post-livraison |
| A16 | P2 | Composants partagés | `factory/composants/` | Composants extraits de besoins réels |
| A17 | P2 | Maintenance | cahier des charges, pipeline | Politique de support et fin de vie |
| A18 | P2 | Diffusion | cahier des charges, métriques | Pilote et retours structurés |

---

## 10. Ordre d'exécution conseillé

### Sprint 0 — Arbitrages structurants

- [ ] Valider le positionnement et le premier cas d'usage.
- [ ] Arbitrer ADR-002, ADR-003, ADR-004 (révision), ADR-005, ADR-006 et ADR-010.
- [ ] Choisir le mode d'exécution du MVP P05 Lite.
- [ ] Mettre à jour `BACKLOG.md` et les fiches P05/P09/P12.

**Sortie :** périmètre du MVP défini, architecture approuvée, aucun risque bloquant ignoré.

### Sprint 1 — Base technique et banc d'essai

- [ ] Initialiser uniquement le socle technique nécessaire au premier outil et à son site de présentation.
- [ ] Créer F-DOCX-01 et la CI minimale bloquante.
- [ ] Mettre en place scan des secrets et dépendances.
- [ ] Mettre à jour le pipeline avec les preuves attendues.

**Sortie :** un test fautif échoue volontairement ; la chaîne de validation est reproductible.

### Sprint 2 — P05 Lite utilisable

- [ ] Développer l'inspection DOCX sans IA et sans réécriture.
- [ ] Produire rapport lisible, messages d'erreurs et démonstration fictive.
- [ ] Effectuer tests automatisés + contrôle manuel de non-régression.
- [ ] Produire fiche de confiance et guide d'utilisation.

**Sortie :** première version candidate à la publication, sans preuve de conformité ou de sécurité non étayée.

### Sprint 3 — Pilote et publication

- [ ] Tester l'outil auprès d'avocats sur des cas fictifs.
- [ ] Corriger les erreurs et lacunes bloquantes.
- [ ] Vérifier les pages légales et précautions.
- [ ] Publier après validation humaine, puis recueillir les retours.

**Sortie :** un outil public maintenable et une première rétrospective documentée.

### Sprint 4 — P09 et premier usage d'IA distante

- [ ] Qualifier la bibliothèque de pseudonymisation sur F-IDENT-01.
- [ ] Développer P09 si les résultats justifient sa mise à disposition ; publier les limites.
- [ ] Préparer P01, premier outil génératif, uniquement après validation du modèle de flux et des évaluations.

**Sortie :** composants validés sur la base d'usages réels, pas seulement de projections.

> Les « sprints » sont des **séquences de travail**, sans engagement de délai. La durée dépend de la stack, des décisions d'architecture et des problèmes révélés par les tests.

---

## 11. Définition de « terminé » (Definition of Done)

Une livraison est considérée comme terminée uniquement si :

- [ ] Son besoin et son périmètre sont validés.
- [ ] Les risques et flux de données sont décrits sans ambiguïté.
- [ ] Les décisions structurantes sont consignées et approuvées.
- [ ] Le code s'exécute sur l'environnement annoncé.
- [ ] Les tests pertinents sont automatiques, reproductibles et passants.
- [ ] Les limitations et erreurs non résolues sont identifiées.
- [ ] Aucun secret ni document réel n'a été incorporé au dépôt.
- [ ] L'original de l'utilisateur n'est pas modifié sans action explicite.
- [ ] Les documents exportés peuvent être vérifiés et l'utilisateur garde la main.
- [ ] Les mentions de licence, sécurité, confidentialité et droit applicables ont été examinées.
- [ ] Une fiche publique indique version, compatibilité, limites, tests et signalement.
- [ ] La publication a été validée humainement et inscrite au registre.

## 12. Instructions d'utilisation de ce plan par la Factory

1. **Ne pas appliquer automatiquement les ADR.** Les créer au statut « Proposée » et demander l'arbitrage prévu.
2. Pour chaque action A01 à A18, créer une tâche dans `BACKLOG.md` ou une issue associée, avec un lien vers la présente section.
3. Traiter les P0 avant les P1, sauf dépendances techniques justifiées par écrit.
4. Modifier la documentation **et** les vérifications correspondantes ; une simple réécriture des règles ne vaut pas implémentation.
5. Toute modification aux agents, standards ou commandes doit respecter la règle de validation humaine décrite dans `factory/README.md`.
6. En fin de sprint, renseigner `factory/registre.md`, `factory/metriques.md` et `LOG.md` avec les éléments réellement vérifiés.
7. Toute nouvelle hypothèse technique ou juridique non confirmée doit rester marquée `[À VÉRIFIER]`, avec une méthode et une source de vérification identifiées.

## 13. Décisions humaines ouvertes

- [x] Le premier produit sera-t-il **P05 Lite**, ou souhaite-t-on malgré tout donner la priorité à P09 ? → P05 Lite (ADR-011, 2026-10-31)
- [ ] Pour les outils à API externe, privilégie-t-on une **application locale** plutôt qu'une page navigateur recevant une clé ?
- [ ] Accepte-t-on les trois parcours Factory (léger/standard/renforcé) ?
- [ ] Quel degré d'ouverture du code et des résultats de test souhaite-t-on rendre public ?
- [ ] Quel public pilote et quels premiers critères de valeur retient-on ?
- [x] Qui sera l'éditeur juridique du site et quelle relation exacte est prévue avec Avroy Avocats ? → Florian Ernotte à titre personnel (2026-10-31) ; relation avec le cabinet [À VÉRIFIER]

---

## 14. Résultat attendu après les premières itérations

Le projet doit disposer **d'un outil réellement publié**, d'un socle de tests empêchant les régressions les plus importantes, d'une architecture de confidentialité techniquement justifiée, d'une documentation transparente pour les utilisateurs et d'une Factory dont la complexité a été mesurée puis ajustée. La priorité n'est pas d'augmenter le nombre d'agents ou de composants, mais de rendre la production **utile, vérifiable, reproductible et soutenable**.
