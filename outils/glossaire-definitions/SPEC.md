# Spécification - Glossaire des définitions (P02 Lite, mode local)

Version 0.1.0 - 2026-11-01 - Parcours Factory : standard (contrat isolé, aucune donnée envoyée, ADR-007)

## Besoin

Un contrat négocié accumule des définitions dispersées : un terme défini à l'article 1 puis redéfini en passant à l'article 12, des définitions que plus rien n'emploie, des termes écrits avec des majuscules sans jamais avoir été définis, des graphies qui dérivent au fil des versions. Ces défauts se repèrent mal à la relecture et créent des ambiguïtés sur le sens du contrat.

## Périmètre de la version 0.1.0 (ADR-016, proposée)

Inclus :
- lecture des .docx (corps et tableaux), .txt et .md ;
- repérage des définitions selon les usages de rédaction francophones ;
- comptage des emplois et défauts listés ci-dessous ;
- rapport .docx, .md et .json ;
- fenêtre et ligne de commande.

Exclus :
- toute modification du contrat, en particulier le regroupement des définitions dans un article ou une annexe (prévu par la fiche P02, il dépend du composant P10) ;
- l'appréciation du contenu d'une définition ;
- les notes de bas de page, en-têtes et pieds de page ;
- les contrats bilingues FR/NL.

## Règles

- **Définition** :
  - dans l'article ou l'annexe dont le titre contient « Définition » : `« Terme » désigne / signifie / vise / s'entend de…`, `« Terme » : …`, `Terme : …` (sans guillemets, chaque mot avec une majuscule), et les tableaux à deux colonnes « Terme | Définition » ;
  - partout : `(ci-après « le Terme »)`, `ci-après dénommée « la Société »`, `ci-après désignée par « les Données »`, `(le « Prix »)`, `(ensemble, les « Parties » et individuellement une « Partie »)`, `on entend par « Terme »`, `par « Terme », il faut entendre`, `il y a lieu d'entendre par « Terme »`, `le terme « Terme »`, `« Terme » désigne…` ; un renvoi `article 7 (« Confidentialité »)` n'est pas une définition.
  Le terme commence par une majuscule. Les guillemets français, droits et doubles courbes sont reconnus, avec ou sans espace insécable ; les guillemets simples courbes ne le sont pas.
- **Titres** : style de titre Word, paragraphe numéroté automatiquement de quatre mots au plus, « Article 3 », « 3. Intitulé », ligne en capitales. Une ligne courte sans point n'est pas un titre.
- **Identité d'un terme** : sans article, casse, accents ni marque du pluriel (-s, -x, -aux). « Partie » et « Parties » sont le même terme ; les définir l'un et l'autre n'est pas une répétition.
- **Emploi** : occurrence du terme avec ses majuscules, au singulier ou au pluriel. L'occurrence la plus longue l'emporte (« Prix de Cession » n'est pas un emploi de « Prix »). Les titres d'articles et les lignes en capitales ne comptent pas.
- **Défauts** :
  - définition répétée : le terme est défini dans deux paragraphes ; « divergente » si les libellés diffèrent, « répétée » s'ils sont identiques ;
  - terme jamais employé ;
  - terme sans définition : un ou plusieurs mots avec majuscule après un déterminant (« les Spécifications Techniques »), hors noms des parties, des personnes, des institutions et des lieux, hors sigles et adresses ;
  - graphie différente : même terme, autre casse ou autres accents, avec au moins une majuscule hors début de phrase ;
  - emploi avant définition : uniquement pour un terme défini en cours de texte, jamais dans l'article des définitions ; un terme de l'article des définitions employé dans le préambule n'est pas un défaut.

## Garanties

- Le contrat est lu en lecture seule ; un test vérifie que ses octets et sa date sont inchangés.
- Aucun rapport existant n'est remplacé.
- Le code n'importe aucun module réseau, ce qu'un test statique vérifie, et le parcours complet est testé avec les fonctions réseau neutralisées.
- Les .docx piégés (entités XML, bombes de décompression, faux fichiers, format strict) sont refusés avec un message, en moins de cinq secondes.
- Limites : 20 Mo par fichier, 15 Mo de texte XML décompressé, 20 000 paragraphes, 2 millions de caractères. Un contrat de 1,7 Mo comptant 250 termes est analysé en moins de six secondes.
- Relecture indépendante du 2026-11-01 : aucun défaut bloquant, 9 à corriger et 9 mineurs, tous corrigés et couverts par un test (`verifications/2026-11-01-revue.md`).

## Mesure (F-DEF-01 v1.0)

| Catégorie | Jeu de développement (3 contrats) | Jeu de contrôle (4 contrats) |
|---|---|---|
| Termes définis reconnus | 35 sur 35 | 48 sur 50, aucun faux terme |
| Définitions répétées | 3 sur 3 | 5 sur 5 |
| Dont divergentes | 3 sur 3 | 3 sur 3, et 2 signalées divergentes à tort |
| Termes jamais employés | 3 sur 3 | 5 sur 5 |
| Termes sans définition | 6 sur 6 | 5 sur 6, et 3 fausses alertes |
| Graphies différentes | 3 sur 3 | 5 sur 6 |
| Emplois avant définition | 2 sur 2 | 5 sur 5 |

Le jeu de contrôle a été rédigé par un agent qui n'avait accès ni au code ni au jeu de développement. Les planchers de non-régression sont dans `attendu/P02-planchers.json`.

## Critères d'acceptation (fiche projet P02, §7, adaptés au périmètre « rapport »)

- [x] Aucune définition perdue ni ajoutée : 48 sur 50 reconnues sur le jeu de contrôle, aucune ajoutée ; le contrat n'est jamais modifié.
- [x] Le rapport liste les termes non définis et les doublons.
- [x] La mise en forme du document source est conservée : sans objet, le contrat n'est pas modifié.
