# Circuit de production

Chaque projet passe par les étapes ci-dessous. `ops-factory` contrôle chaque passage à partir des critères de sortie. Un critère non rempli bloque le passage ; l'exception doit être validée par Florian et notée dans le registre.

## 0. Idée

Entrée : une source, un besoin, une suggestion.
Travail : l'éclaireur ou Florian rédige une fiche à partir de `templates/fiche-projet.md`.
Sortie : fiche dans `projets/`, ligne ajoutée au registre au statut "idée".

## 1. Prêt

Entrée : fiche "idée".
Travail : Florian complète l'appétit et la priorité ; relecteur-deontologie liste les points sensibles.
Sortie, tous requis :
- appétit et priorité renseignés ;
- section contraintes complétée ;
- licence de la source identifiée (ou absence de code repris) ;
- critères d'acceptation mesurables ;
- validation de Florian notée dans le registre.

## 2. Cadrage

Travail : architecte rédige `outils/<slug>/SPEC.md`.
Sortie :
- mode d'exécution choisi et justifié ;
- trajet des données décrit ;
- composants Factory utilisés ou nouveaux composants identifiés ;
- jeu de test fictif identifié ou créé (testeur) ;
- estimation de coût par utilisation ;
- au moins deux options comparées si le choix technique est discutable.

## 3. Prototype

Travail : developpeur réalise l'outil par petites étapes ; designer-ux relit l'interface en cours de route.
Sortie :
- l'outil fonctionne sur le jeu de test ;
- configuration dans un seul fichier, aucun nom de modèle en dur ;
- README technique à jour ;
- CHANGELOG de l'outil commencé.

## 4. Vérification

Travail : testeur, verificateur-securite, relecteur-deontologie, designer-ux, chacun produit un rapport dans `outils/<slug>/verifications/`.
Sortie :
- rapport de test avec résultats mesurés ;
- rapport sécurité sans point bloquant ouvert ;
- rapport déontologie dont chaque point est tranché par Florian ;
- rapport UX sans point bloquant ouvert.

## 5. Publication

Travail : redacteur rédige `FICHE.md` (gabarit fiche-outil) ; Florian relit.
Sortie :
- fiche publique complète et datée ;
- liste de contrôle de `docs/principes-outils.md` cochée ;
- entrée dans les nouveautés du site ;
- validation de Florian.

## 6. Suivi

Travail : rétrospective (`/factory-retro`) ; ops-factory reporte les enseignements dans les standards ou les composants (via `ameliorations.md`).
Revue de la fiche publique tous les six mois.

## Statuts

idée, prêt, cadrage, prototype, vérification, publié, archivé, abandonné. Un projet bloqué garde son statut et porte la mention "bloqué" avec la raison.
