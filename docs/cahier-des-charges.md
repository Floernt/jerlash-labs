# Cahier des charges - jerlash.labs

Version 0.3 - 31 octobre 2026 - Statut : brouillon à valider

Les éléments marqués `[À VÉRIFIER]`, `[À VALIDER]`, `[À DÉCIDER]` ou `[À COMPLÉTER]` n'ont pas été confirmés. Ils doivent l'être avant publication.

## 1. Objet

Ce document décrit le site jerlash.labs : ce qu'il doit faire, pour qui, ce qu'il exclut, et les contraintes techniques, juridiques et éditoriales qui s'appliquent. Il sert de référence pour le développement mené avec Claude Code.

## 2. Contexte

Florian Ernotte est avocat (Avroy Avocats) et membre de comités scientifiques et consultatifs ainsi que d'advisory boards actifs dans la legal tech `[À COMPLÉTER : liste exacte des comités et boards, avec les dates]`. Il conçoit des outils d'IA appliqués à la pratique d'un cabinet.

Le point de départ est le modèle observé chez Sol Irvine, qui publie ses outils pour avocats sous des noms de domaine dédiés (sa bio X cite augustus.esq et wargame.esq ; ces sites n'ont pas été consultés). Ses dépôts GitHub ont été explorés le 2026-10-31 : voir `docs/veille/sol-irvine-zenzen-sol.md`. Le choix retenu ici est différent : un seul domaine, jerlash.labs, qui regroupe tous les projets.

## 3. Objectifs

1. Donner un lieu de publication à des projets concrets, ce qui oblige à les terminer et à les documenter.
2. Tester des outils dans des conditions réelles, avec un retour d'utilisateurs avocats.
3. Partager les connaissances techniques acquises : API, clés, coûts, confidentialité, installation, rédaction de prompts.
4. Rendre visible l'expérience accumulée dans les comités et advisory boards legal tech, par la qualité des outils et des explications plutôt que par des déclarations.

## 4. Publics

Public principal : avocats et juristes, en priorité belges francophones `[À VALIDER]`, curieux de l'IA mais sans formation technique particulière.

Public secondaire : développeurs et acteurs legal tech qui cherchent des exemples d'outils locaux, et organisateurs de formations ou de conférences.

Conséquence pour l'écriture : chaque guide suppose que le lecteur n'a jamais ouvert un terminal, sauf mention contraire explicite en tête de page.

## 5. Périmètre

### Inclus

- Catalogue d'outils, avec une fiche par outil.
- Guides techniques et pratiques.
- Une page de précautions d'usage (confidentialité, vérification des sorties, limites des modèles).
- Une page de présentation de l'auteur et de son parcours.
- Pages légales : mentions légales, politique de confidentialité.
- Une rubrique "Automatiser une prestation" : contenus pratiques pour décider quoi automatiser dans un cabinet et comment le proposer (ADR-012).

- Depuis ADR-024 (proposée, 2026-11-03) : rubriques Recherche (programmes, protocoles), Revue (Perspectives, Research papers, Notes techniques, Recensions, selon `docs/politique-publication.md`), Éthique (principes, précautions, recherche avec participants), et toolkits dans Outils.

### Exclus

- ~~Contenu philosophique ou réflexif sur le droit et la technologie.~~ Levé par ADR-024 : ce contenu est publié dans Revue › Perspectives. reflexions.florianernotte.be garde la réflexion généraliste, indépendante de toute matière.
- Consultation juridique et contenu qui pourrait passer pour un avis sur un dossier.
- Service hébergé (SaaS) qui traiterait des documents d'utilisateurs sur un serveur de jerlash.labs.
- Compte utilisateur, inscription, collecte de données personnelles. Une newsletter éventuelle fera l'objet d'une décision séparée.
- Vente d'outils `[À VALIDER : gratuité de principe ?]`.

## 6. Organisation des projets sous un domaine unique

Deux options pour exposer chaque outil (décision ADR-005) :

Option A, chemins : jerlash.labs/outils/chronologie. Un seul site, un seul déploiement, référencement concentré sur un domaine.

Option B, sous-domaines : chronologie.jerlash.labs. Chaque outil est isolé, ce qui limite l'impact d'une faille d'un outil sur les autres (point utile quand une clé API est saisie dans une page), au prix d'une configuration DNS et de déploiements multiples.

Recommandation provisoire : fiches et guides en chemins sur le site principal, et chaque outil exécutable dans le navigateur sur son propre sous-domaine, pour isoler les clés API. À valider.

## 7. Arborescence

Arborescence cible depuis ADR-024 (proposée, 2026-11-03), chemins français et doublon anglais sous `/en/` :

```
Accueil
Recherche (/fr/recherche/)
  Programme H1 Human Agency & AI
Outils (/fr/outils/)
  Toolkits : Legal AI Governance Toolkit (une page par module, téléchargements)
  Logiciels BYOK : catalogue et fiches
  Guides
Revue (/fr/revue/)
  Perspectives (anciens articles du blog)
  Research papers
  Notes techniques
  Recensions
Éthique (/fr/ethique/)
  Principes et précautions d'usage
  Recherche avec participants
À propos
Mentions légales
Confidentialité
```

Arborescence précédente (v0.3, conservée pour mémoire) :

```
Accueil
Outils
  Catalogue (filtrable par usage : rédaction, analyse de pièces, organisation du dossier, etc.)
  Fiche outil (une par outil)
Guides
  Démarrer
    Obtenir une clé API et la protéger
    Comprendre la facturation à l'usage
    Ce que devient une donnée envoyée à un fournisseur d'IA
    Utiliser un outil en local : les trois façons de faire
  Approfondir (au fil des publications)
Automatiser une prestation
  Une grille en quatre critères
  Quatre cases pour positionner une prestation
Précautions d'usage
À propos
  Parcours, comités, advisory boards, interventions
  Contact
Nouveautés (journal public des versions)
Mentions légales
Confidentialité
```

## 8. Contenu d'une fiche outil

Chaque fiche suit `templates/fiche-outil.md` et contient obligatoirement :

- ce que fait l'outil, en deux phrases, et ce qu'il ne fait pas ;
- un cas d'usage concret dans un dossier ;
- le mode d'exécution (navigateur, script local, modèle local) ;
- les fournisseurs d'IA compatibles ;
- le trajet des données : ce qui part, vers qui, ce qui reste sur la machine ;
- une estimation de coût par utilisation type, datée, avec la méthode de calcul ;
- les précautions spécifiques à l'outil ;
- l'installation pas à pas ;
- la version, la date de mise à jour, la licence, le lien vers le code source ;
- un moyen de signaler un problème.

## 9. Principes techniques des outils

Détaillés dans `docs/principes-outils.md`. Résumé :

- local d'abord : l'outil tourne sur la machine de l'avocat ;
- BYOK : l'avocat utilise sa propre clé et son propre contrat avec le fournisseur ;
- aucun serveur intermédiaire contrôlé par jerlash.labs ;
- modèle et fournisseur configurables, jamais figés dans le code ;
- option "modèle local" (par exemple via Ollama) envisagée pour les outils où la confidentialité prime `[À ÉVALUER au cas par cas]` ;
- code source publié `[À VALIDER : licence, voir ADR-006]`.

## 10. Exigences fonctionnelles du site

- Catalogue d'outils filtrable.
- Recherche dans les guides `[À VALIDER : nécessaire dès le lancement ?]`.
- Chaque guide indique sa date de dernière vérification. Les pages non revues depuis 6 mois affichent un avertissement.
- Liens d'ancrage sur les titres pour pouvoir citer une section précise.
- Flux RSS ou Atom pour les nouveautés.
- Contact : pas de formulaire au lancement, une adresse électronique suffit `[À VALIDER]`.

## 11. Exigences non fonctionnelles

Performance : site statique, pages légères, pas de script inutile sur les pages de contenu.

Accessibilité : objectif WCAG 2.1 niveau AA (contrastes, navigation au clavier, textes alternatifs, hiérarchie des titres).

Affichage : responsive, mode clair et mode sombre selon le réglage du système.

Sécurité : en-têtes HTTP stricts (Content-Security-Policy, HSTS, X-Content-Type-Options, Referrer-Policy), dépendances minimales et figées à une version précise. Détails dans `docs/securite-confidentialite.md`.

Vie privée : pas de cookie non essentiel, pas de traceur tiers. Si une mesure d'audience est souhaitée, solution sans cookie et sans donnée personnelle `[À DÉCIDER]`.

Référencement : titres et descriptions uniques, données structurées, plan du site. Les guides sont structurés pour être cités par les moteurs de réponse IA : une question par section, réponse directe en tête de section, sources nommées.

## 12. Cadre juridique et déontologique

Points à vérifier avant mise en ligne. Ce document ne tranche aucun d'entre eux.

- Publicité et communication de l'avocat : conformité du site avec les règles applicables (avocats.be et règlement du barreau d'inscription) `[À VÉRIFIER]`.
- Mentions obligatoires d'un site professionnel en droit belge (identification, numéro d'entreprise, ordre professionnel, etc.) `[À VÉRIFIER]`.
- Éditeur : Florian Ernotte à titre personnel (décision du 2026-10-31). Mention de son cabinet d'exercice et accord éventuel d'Avroy Avocats `[À VÉRIFIER]`.
- RGPD : le site ne collecte rien, mais la politique de confidentialité doit l'expliquer, ainsi que le traitement réalisé par l'hébergeur (journaux serveur).
- Outils : rappeler que l'avocat reste responsable du respect du secret professionnel et de ses obligations RGPD lorsqu'il envoie des données à un fournisseur d'IA avec sa propre clé. Le site informe, il n'endosse pas cette responsabilité.
- Règlement européen sur l'IA (AI Act) : vérifier si des obligations de transparence s'appliquent aux outils publiés `[À VÉRIFIER]`.
- Clause de non-responsabilité : outils fournis tels quels, sans garantie, sorties à vérifier systématiquement.
- Licences : licence du code des outils, licence des contenus (par exemple Creative Commons) `[À DÉCIDER]`.

## 13. Identité visuelle

Identité propre, sobre (éditeur à titre personnel).

Indications de départ : sobriété, lisibilité, typographie adaptée à la lecture longue, aucune imagerie de robot ou de cerveau lumineux.

## 14. Contenu du lancement (MVP)

- Accueil, À propos, Précautions d'usage, Mentions légales, Confidentialité.
- Les quatre guides "Démarrer" listés au point 7.
- Un ou deux outils publiés et documentés.

Pistes d'outils : voir `projets/README.md` et `BACKLOG.md`. Premier outil retenu : P05 Lite, contrôle non destructif d'un .docx avant envoi, sans IA ni clé API (ADR-011). La pseudonymisation locale (P09) suit, une fois le banc F-IDENT-01 disponible.

Autres pistes non encore détaillées en fiche : extraction d'une chronologie des faits à partir de pièces, comparaison commentée de deux versions d'un contrat.

## 15. Phases

Phase 0, cadrage : validation de ce document, décisions ADR ouvertes, contenu de la page À propos.

Phase 1, socle : site statique, pages fixes, gabarits, déploiement, en-têtes de sécurité.

Phase 2, lancement : guides "Démarrer", premier outil, relecture juridique des pages légales.

Phase 3, rythme : publication régulière d'outils et de guides, journal des nouveautés.

Aucune date n'est fixée. État au 2026-10-31 : phases 0 et 1 réalisées, phase 2 en préparation (voir LOG.md).

## 16. Questions ouvertes

1. Éditeur du site : Florian Ernotte à titre personnel (tranché le 2026-10-31).
2. Public : Belgique francophone seulement, ou francophonie au sens large ?
3. Code source des outils publié ou non, et sous quelle licence ?
4. Gratuité de principe ?
5. Hébergeur et outil de génération du site : GitHub Pages et Hugo (ADR-002, ADR-003).
6. Mesure d'audience : oui ou non ?
7. Place de l'anglais (une partie du public legal tech est anglophone).
8. Liens avec florianernotte.be et reflexions.florianernotte.be : renvois croisés, menu commun ?
