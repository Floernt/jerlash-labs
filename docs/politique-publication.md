# Politique de publication : Revue et Recherche

Version 1.0 - 3 novembre 2026 - Statut : validée par Florian le 2026-11-03 (ADR-024)

Ce document fixe les règles de publication des textes des rubriques Revue et Recherche. Il reprend, en l'adaptant à un site tenu par une seule personne, le Research Papers Guide de l'archive Proton du 2026-11-03 (hors dépôt : `../sources-proton/2026-11-03/JERLASH_Labs_Legal_AI_Governance_Toolkit/99_SOURCES/JERLASH_Labs_Research_Papers_Guide.md`). Les règles de style restent celles de `docs/charte-editoriale.md`.

## 1. Collections de la Revue

Il y a quatre collections :
- **Perspectives** : essais, prises de position, réflexion sur le droit et la technique. Les articles de l'ancien blog y sont rangés.
- **Research papers** : un texte qui pose une question, applique une méthode et en discute les limites.
- **Notes techniques** : architecture, méthode, documentation, retour d'expérience.
- **Recensions** : l'analyse d'un outil, d'un produit, d'une étude ou d'une publication.

Une prise de position sans méthode va dans Perspectives. Une documentation sans question de recherche va dans les Notes techniques.

## 2. Types de research papers et longueur

Longueur indicative, hors bibliographie et annexes :

| Type | Longueur |
|---|---|
| Conceptuel | 5 000 à 9 000 mots |
| Juridique ou comparatif | 6 000 à 10 000 mots |
| Empirique | 5 000 à 9 000 mots |
| Expérimental | 5 000 à 9 000 mots |
| Réplication ou résultat négatif | 3 000 à 6 000 mots |
| Protocole | 2 500 à 5 000 mots |

## 3. Statuts

Un texte a l'un des trois statuts suivants :
- **Brouillon** : jamais publié.
- **Working paper** : publié. Le texte décrit les contrôles réellement faits, par exemple « sources vérifiées par l'auteur le … ; aucune relecture externe ».
- **Évalué** : seulement après deux relectures complémentaires réellement faites (juridique et, si besoin, technique), avec une réponse point par point.

Tant qu'il n'y a pas de relecteurs, tout research paper publié est un working paper (ADR-025). L'auteur ne décide pas seul du statut « évalué » de son propre texte.

## 4. Métadonnées obligatoires

Chaque texte de Revue et chaque ressource d'Outils porte, dans son front matter, les champs suivants : `statut`, `version`, `date`, `auteurs`, `programme` (H1, C1, T1 ou transversal), `type`, `date_arret_recherches`, `controles` (contrôles réellement faits), `usage_ia`, `licence`, `financement`, `conflits_interets`.

Le partiel « bloc de statut » les affiche en tête de page.

Le champ `type` ne s'écrit pas tel quel dans le front matter d'une page du site : Hugo le réserve au choix du gabarit, et la page perdrait celui de sa rubrique. La collection en tient lieu (pour une recension, le champ `objet` le précise, ADR-027).

Identifiant des research papers : `JLL-RP-AAAA-NNN`, attribué à la première publication, dans l'ordre. On n'indique jamais de DOI qui n'a pas réellement été attribué.

Versions : `0.x` pour les versions de travail, `1.0` pour la première version évaluée. Une correction importante n'est jamais faite en silence : elle figure dans l'historique en fin de texte.

## 5. Usage de l'IA

L'IA n'est ni auteur ni relecteur. Chaque texte déclare :
- les usages importants de l'IA (recherche, rédaction, traduction, code) ;
- les vérifications humaines faites ;
- séparément, l'IA comme objet d'étude et l'IA comme outil de rédaction.

Forme de la déclaration : « [Outil, version ou date] a été utilisé pour [tâches]. L'auteur a vérifié [sources, analyses]. »

La phrase « Aucun matériau confidentiel n'a été transmis » n'est ajoutée que si c'est exact.

## 6. Sources

- Toute référence a été consultée et vérifiée.
- Système auteur-date pour les sciences humaines, notes précises pour les sources juridiques (article, date, version consolidée).
- La loi est citée, pas paraphrasée.
- Les citations traduites sont signalées.
- Un fait non vérifié reste en `[À VÉRIFIER]`, ce qui bloque la publication.

## 7. Licences

Éditeur : jerlash.labs, sauf mention contraire sur la ressource (ADR-026).

Textes : CC BY 4.0 (ADR-006), sous réserve des droits de tiers. Exception : le Legal AI Governance Toolkit est sous CC BY-NC 4.0 (ADR-026). Code : licence de l'ADR-006. Données : licence propre, décidée au cas par cas. Les données réservées d'une étude en cours (corrigés, tests adverses) ne sont pas publiées avant la fin de la collecte.

## 8. Avant publication

- [ ] Florian a lu le texte en entier et y adhère.
- [ ] Les références sont vérifiées.
- [ ] Le front matter est complet et le statut est exact.
- [ ] La déclaration d'usage de l'IA est faite.
- [ ] Aucune donnée de client, aucun matériau réservé.
- [ ] `python scripts/verifier.py --publication` passe.

## 9. Recensions (ADR-027)

Une recension porte, en plus des métadonnées du §4, un champ `objet` et un bloc `oeuvre` qui décrit l'œuvre recensée. La manière de citer dépend de l'objet.

| `objet` | Champs du bloc `oeuvre` | Citation précise |
|---|---|---|
| `livre` | `auteurs`, `titre`, `editeur`, `lieu`, `annee`, `edition_lue`, `isbn` | page |
| `article` (article, billet, rapport en ligne) | `auteurs`, `titre`, `publication`, `date`, `url`, `consulte_le`, `doi` s'il existe | section ou paragraphe |
| `podcast` | `auteurs` (intervenants), `titre`, `publication` (émission), `episode`, `date`, `duree`, `url`, `consulte_le` | minutage (12:40) |
| `conference` | `auteurs` (intervenants), `titre`, `publication` (événement), `lieu`, `date`, `url` de l'enregistrement s'il existe | minutage, ou « propos tenus sur place » |

Une citation orale est transcrite par l'auteur de la recension, qui le signale. Un propos entendu sans enregistrement n'est pas mis entre guillemets.

Le texte suit le plan : le propos de l'œuvre, la discussion, l'intérêt pour les juristes ou pour un programme de recherche, la référence. Une recension sans méthode qui devient une prise de position va dans Perspectives.
