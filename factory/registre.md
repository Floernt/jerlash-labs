# Registre de production

Tenu par `ops-factory`. Une ligne par projet. Mettre à jour à chaque changement d'étape.

Depuis le 2026-11-11, le rôle `ops-factory` est tenu par l'agent jerlash (option A décidée par Florian sur FLO-58 ; pilote d'un mois suivi sur FLO-61).

| ID | Titre | Statut | Bloqué | Prochaine action | Responsable | Mis à jour |
|---|---|---|---|---|---|---|
| P01 | Inventaire d'un dossier (0.2.0, mode IA, ADR-019) | vérification | mesure réelle du mode IA (clé de Florian) | Florian : config-ia.json et .env, puis `evaluer.py --ia --executions 3` ; tester la fenêtre sur un dossier réel | Florian | 2026-11-01 |
| P02 | Glossaire des définitions (P02 Lite 0.1.0, rapport seul, ADR-016) | vérification | marqueurs [À COMPLÉTER] du site | Florian : tester la fenêtre, valider ADR-016 ; la restructuration attend P10 | Florian | 2026-11-01 |
| P03 | Conditions particulières et générales (P03 Lite 0.1.0, rapport seul, ADR-017) | vérification | marqueurs [À COMPLÉTER] du site | Florian : tester la fenêtre, valider ADR-017 ; la séparation en deux documents attend P10 | Florian | 2026-11-01 |
| P04 | Propositions de modifications | idée | | prototype technique modifications suivies | architecte | 2026-10-31 |
| P05 | Contrôle avant envoi (P05 Lite 0.1.0, ADR-011) | vérification | marqueurs [À COMPLÉTER] du site | Florian : tester la fenêtre, lister les incidents vécus (points déontologiques tranchés le 2026-10-31) | Florian | 2026-10-31 |
| P06 | Simulateur de négociation | idée | dépend de P04, P10 | lecture de l'architecture source | architecte | 2026-10-31 |
| P07 | Mémoire de dossier | idée | | test sur dossier fictif | developpeur | 2026-10-31 |
| P08 | Revue tabulaire | idée | | choix outil ou guide | Florian | 2026-10-31 |
| P09 | Pseudonymisation (P09 Lite 0.1.0, ADR-014) | vérification | marqueurs [À COMPLÉTER] du site | Florian : tester la fenêtre, valider ADR-014 et la mesure publiée | Florian | 2026-10-31 |
| P10 | Composant .docx | idée | ADR-002 | prototype d'évaluation | architecte | 2026-10-31 |
| P11 | Composant conversion | idée | | mesure installation et temps | architecte | 2026-10-31 |
| P12 | Banc d'essai | cadrage | | F-DOCX-01, F-IDENT-01, F-DOSSIER-01, F-DEF-01 et F-CPCG-01 v1.0 livrés et branchés sur la CI, chacun avec un jeu de contrôle rédigé à part (sauf F-DOCX-01) | testeur | 2026-10-31 |
| P13 | Guide plateformes open source | idée | après lancement | aucune | redacteur | 2026-10-31 |
| P14 | Gouvernance de l'IA, Toolkit v0.2 (ADR-024, ADR-026, ADR-029) | prototype | ADR-034 et ouverture de la charte .docx dans Word, à confirmer par Florian | étape 4 du circuit : rapports de vérification dans `outils/gouvernance-ia/verifications/` (téléchargements construits le 2026-11-11, FLO-74) | jerlash (ops-factory) | 2026-11-11 |
| P15 | RP « L'humain dans la boucle » | idée | dépend de P14 | aucune avant avril 2027 | Florian | 2026-11-11 |
| P16 | RP « Modèles discriminatifs et pratique juridique » | idée | | aucune avant février 2027 | Florian | 2026-11-11 |
| P17 | RP « Tarification alternative des avocats » | idée | | aucune avant mars 2027 | Florian | 2026-11-11 |
| P18 | Kit expérimental MCP (C0 à C3) | idée | code C3 à récupérer | décembre 2026 : demander le kit v0.2 complet, avec le code C3 | Florian | 2026-11-11 |
| P19 | Recension Billion et Fasterling (ADR-027) | prototype | hypothèse H1 annoncée par les cartes P19 et absente du texte ; année de la Summer School | Florian : corriger les résumés des cartes ou écrire l'hypothèse ; confirmer l'année (réserves gardées le 2026-11-11, FLO-18) | Florian | 2026-11-11 |
| F01 | Méthode d'ingénierie | idée | ADR-009 | test open-pstack sur dépôt jetable | ops-factory | 2026-10-31 |
| F02 | Revue UX | intégré | | aucune | ops-factory | 2026-10-31 |
| F03 | Mémoire Factory | en essai | | utiliser la skill un mois | ops-factory | 2026-10-31 |

## Lignes ajoutées le 2026-11-11

P14 à P19 avaient une fiche dans `projets/` mais aucune ligne au registre. Les lignes ci-dessus sont reprises des fiches et de l'état relevé sur `main` au commit `69c7c29`.

Deux écarts de vocabulaire, tranchés ici faute de mieux, à confirmer par Florian `[À VÉRIFIER]` :

- la fiche P14 porte `statut: cadrage` (mise à jour du 2026-11-06) alors que les dix pages de la boîte à outils sont en ligne et que le tableur 0.3 est produit par un script versionné. Le registre retient `prototype` ;
- la fiche P19 porte `statut: en cours`, qui n'est pas un statut du circuit. Le texte est déposé en brouillon dans `site/content/revue/recensions/` : le registre retient `prototype`.

## Parcours

Le circuit demande que le parcours soit choisi et noté avant le développement (`pipeline.md`, ADR-007, A05). Aucun parcours n'avait été noté jusqu'ici.

| ID | Parcours | Motif |
|---|---|---|
| P14 | standard `[À VÉRIFIER]` | contenu sans IA distante ni donnée de dossier, mais le projet livre un fichier produit par un script versionné (`outils/gouvernance-ia/tableur/generer_tableur.py`) ainsi que le pack zip, la charte .docx et le kit « petit cabinet » (`outils/gouvernance-ia/telechargements/generer_telechargements.py`, FLO-74). Le parcours standard impose un rapport de test et un rapport de sécurité sur ces téléchargements. Le parcours léger suffirait si l'on ne retenait que les pages. Choix d'`ops-factory`, à confirmer par Florian. |
