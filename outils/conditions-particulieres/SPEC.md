# Spécification - Conditions particulières et générales (P03 Lite, mode local)

Version 0.1.0 - 2026-11-01 - Parcours Factory : standard (contrat isolé, aucune donnée envoyée, ADR-007)

## Besoin

Deux besoins proches :
- séparer un contrat négocié en conditions particulières, propres à l'opération, et conditions générales réutilisables ;
- réutiliser un contrat comme modèle sans y laisser de données de l'ancien client.

Dans les deux cas, il faut savoir quelles clauses contiennent des données de l'opération. Les plus traîtresses sont les clauses de nature générale où une telle donnée s'est glissée : un plafond de responsabilité chiffré, un IBAN dans la clause de paiement, le téléphone d'un technicien.

## Périmètre de la version 0.1.0 (ADR-017, proposée)

Inclus :
- lecture des .docx (corps et tableaux), .txt et .md ;
- découpage en blocs : comparution, articles, signatures ;
- repérage des données propres à l'opération et proposition de classement ;
- liste des renvois internes ;
- rapport .docx, .md et .json ;
- fenêtre et ligne de commande.

Exclus :
- la production des deux documents séparés (dépend de P10) ;
- toute modification du contrat ;
- les en-têtes, pieds de page et notes de bas de page ;
- l'appréciation juridique du déplacement d'une clause (ordre de priorité, opposabilité des conditions générales).

## Règles

**Données propres à l'opération :**
- parties et personnes : société suivie de sa forme sociale (y compris « srl », « S.R.L. »), « la société X », personne précédée d'une civilité ;
- noms propagés dans tout le contrat, sans tenir compte de la casse : noms des sociétés sans leur forme, noms des personnes et noms de famille, noms abrégés « ci-après « BDC » » qui forment un sigle ou reprennent un mot du nom ;
- adresses : voie, numéro et localité, voies néerlandaises (-straat, -laan…), code postal et localité ;
- identifiants : numéro d'entreprise ou de TVA (avec points même si la somme de contrôle est fausse, sans points seulement si elle est juste), IBAN valide (avec espaces, tirets, en minuscules), courriel, téléphone, référence de commande ou de dossier ;
- montants : en chiffres ou en lettres, devise avant ou après (EUR, €, USD…), « 12.500,- EUR », « 1,5 million d'euros », « 12k€ » ;
- dates : « 1er mars 2026 », « le premier mars deux mille vingt-six », « 01.03.2026 », « 1/3/26 », « 2026-03-01 », « mars 2026 ». La date d'un texte de loi (« loi du 2 août 2002 ») est écartée, pas celle d'une convention ou d'un jugement ;
- quantités : nombre suivi d'une unité usuelle (bouteilles, jours-homme, m², palettes…).

**Blocs :**
- un intitulé est un « Article 4bis », un « 5. Intitulé », un « § 5 », un « 7) Intitulé », un style de titre Word, un paragraphe numéroté automatiquement de quatre mots au plus, une ligne brève en capitales ou un préambule ;
- l'intitulé est analysé avec son bloc ;
- après « Fait à », « Établi à » ou « Pour accord », tout appartient aux signatures jusqu'à une annexe.

**Classement :**
- la comparution et les signatures relèvent des conditions particulières ;
- un intitulé de nature générale (confidentialité, responsabilité, paiement…) donne une clause mixte si le bloc contient une donnée propre à l'opération, des conditions générales sinon ;
- un intitulé propre à l'opération (objet, prix, durée, coordonnées…) donne des conditions particulières, même sans donnée repérée ;
- sinon, le bloc relève des conditions particulières si la moitié au moins de ses paragraphes contient une donnée, d'une clause mixte s'il en contient moins, des conditions générales s'il n'en contient pas.

## Garanties

- Le contrat est lu en lecture seule ; un test vérifie que ses octets et sa date sont inchangés.
- Aucun rapport existant n'est remplacé ; un rapport incomplet (disque plein) est effacé.
- Le code n'importe aucun module réseau, ce qu'un test statique vérifie, et le parcours complet est testé avec les fonctions réseau neutralisées.
- Les .docx piégés sont refusés avec un message (lecture reprise de P02, relue).
- Temps borné : expressions à répétition bornée, 20 000 caractères analysés par paragraphe au plus, une seule expression pour tous les noms propagés.

## Limites connues

- Un nom écrit sans civilité ni forme sociale, que le contrat ne présente nulle part ailleurs, n'est pas reconnu (« adressée à Jean Dupont »).
- Les quantités ne sont reconnues qu'avec une unité de la liste (« 12 serveurs » ou « 120 heures » ne le sont pas).
- Le classement compare des mots de l'intitulé : un intitulé inhabituel tombe dans la règle de proportion.

## Mesure (F-CPCG-01 v1.0)

| | Jeu de développement (2 contrats) | Jeu de contrôle (3 contrats) |
|---|---|---|
| Données repérées | 42 sur 42 | 80 sur 92 |
| Signalements exacts | 42 sur 42 | 80 sur 80 |
| Quantités | 3 sur 3 | 4 sur 13 |
| Blocs bien classés | 28 sur 28 | 41 sur 46 |

Le jeu de contrôle a été rédigé par un agent qui n'avait accès ni au code ni au jeu de développement. Les planchers de non-régression sont dans `attendu/P03-planchers.json`.

## Critères d'acceptation (fiche projet P03, §7, adaptés au périmètre « rapport »)

- [x] Chaque clause figure dans le rapport, une seule fois : le découpage couvre tout le contrat, et chaque paragraphe appartient à un seul bloc.
- [~] Les données propres à l'opération sont repérées : 80 sur 92 sur le jeu de contrôle, sans faux signalement.
- [x] Les changements nécessaires sont listés, pas appliqués : clauses mixtes et renvois internes figurent au rapport ; le contrat n'est pas modifié.
