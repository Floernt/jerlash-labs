---
draft: true
title: "Conditions particulières et générales"
description: "Séparer conditions particulières et conditions générales d'un contrat : noms, montants, dates et identifiants propres à l'opération, article par article."
resume: "L'outil lit un contrat Word, repère dans chaque article les données propres à l'opération et propose un classement : conditions particulières, conditions générales, ou clause générale à épurer avant réutilisation."
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["relire un contrat", "préparer un modèle"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/conditions-particulieres-0.1.0.zip"
taille: "28 Ko"
sha256: "9d796164a3c76befa8bbcd8e123c6228959b91af990563abee7ddb11f6aeae6a"
---

## Ce que fait l'outil

Vous choisissez un contrat négocié. L'outil le lit sur votre ordinateur, sans le modifier, et le découpe en blocs : la comparution des parties, chaque article, puis le lieu, la date et les signatures. Dans chaque bloc, il repère les données propres à l'opération :

- les parties et les personnes (représentants, signataires, contacts) ;
- les adresses ;
- les identifiants : numéro d'entreprise, IBAN, courriel, téléphone, référence de commande ;
- les montants, les dates et les quantités.

Pour chaque bloc, il propose ensuite un classement :

- **conditions particulières** : le bloc est propre à l'opération (parties, objet, prix, durée, coordonnées) ;
- **conditions générales** : le bloc ne contient aucune donnée propre à l'opération et pourrait être repris tel quel ;
- **clause mixte** : une clause de nature générale (paiement, responsabilité, confidentialité…) qui contient une donnée propre à l'opération. Le rapport cite la donnée à extraire, par exemple le plafond de responsabilité chiffré ou l'IBAN glissé dans la clause de paiement.

Le rapport liste aussi les renvois internes (« article 5 »), à vérifier si les clauses changent de place.

## Ce qu'il ne fait pas

L'outil ne produit pas les deux documents séparés et ne modifie pas le contrat. Il ne dit pas si une clause peut être déplacée sans changer l'effet du contrat : l'ordre de priorité entre conditions particulières et générales et l'opposabilité des conditions générales restent votre affaire.

Il ne lit pas les en-têtes, pieds de page ni notes de bas de page. Un en-tête au nom du client n'est donc pas signalé.

Le repérage repose sur des règles, sans IA. Une donnée écrite d'une manière que les règles ne prévoient pas peut lui échapper : une clause classée « générale » se relit encore avant d'être réutilisée.

## Cas d'usage

Vous voulez faire d'un contrat de maintenance signé l'an dernier le modèle du cabinet. Le rapport classe huit articles en conditions générales et quatre en conditions particulières. Il signale trois clauses mixtes :
- la clause de paiement contient l'IBAN de l'ancien client ;
- la clause de responsabilité, un plafond de 25.000 euros négocié pour cette opération ;
- la clause d'intervention, le téléphone du technicien.

Vous savez où regarder avant d'enregistrer le modèle.

## Trajet des données

- Reste sur votre ordinateur : le contrat, qui n'est jamais modifié, et le rapport.
- Est envoyé à un fournisseur d'IA : rien. Cette version n'utilise pas d'IA.
- Est envoyé à jerlash.labs : rien.

Le code de l'outil n'importe aucun module capable de communiquer sur le réseau. Un test automatique le vérifie, et un autre exécute l'analyse complète avec les fonctions réseau neutralisées. Le rapport est enregistré dans `Documents\Conditions particulieres`.

## Tests réalisés

La version 0.1.0 a été mesurée le 1er novembre 2026 sur deux jeux de contrats fictifs. Le premier, de deux contrats, a servi à écrire les règles, qui le traitent sans erreur. Le second, de trois contrats, a été rédigé à part, sans accès aux règles. Il compte 92 données propres à l'opération et 46 blocs. Sur ce second jeu :

| Donnée | Repérées |
|---|---|
| Adresses | 12 sur 12 |
| Montants | 17 sur 17 |
| Dates | 10 sur 10 |
| Parties et personnes | 21 sur 22 |
| Identifiants | 16 sur 18 |
| Quantités | 4 sur 13 |
| **Total** | **80 sur 92**, sans aucun faux signalement |

Les quantités sont le point faible : l'outil ne reconnaît que des unités usuelles (bouteilles, jours-homme, mètres carrés…).

41 blocs sur 46 sont bien classés. Parmi les 5 erreurs, 3 clauses mixtes sont proposées en conditions particulières, ce qui pèche par prudence. Une clause mixte est proposée en conditions générales, alors qu'elle contient une donnée non reconnue : c'est l'erreur qui justifie la relecture. Enfin, un bloc de conditions générales est proposé en conditions particulières.

Avant publication, une relecture indépendante du code a relevé vingt défauts, dont cinq bloquants. Tous avaient la même conséquence : une clause qui contenait encore une donnée de l'opération était présentée comme réutilisable. Par exemple, « EUR 12.500 » n'était pas reconnu comme un montant, et une société nommée « Entre Brasserie du Condroz » dans la comparution n'était plus retrouvée ensuite. Tous ont été corrigés et chacun est couvert par un test.

L'outil ne reconnaît pas pour autant un nom de personne écrit sans civilité, ni une société citée sans sa forme sociale, si le contrat ne les a pas présentées ailleurs.

D'autres tests vérifient trois choses :
- le contrat n'est pas modifié (contenu et date) ;
- les fichiers Word piégés sont refusés avec un message ;
- aucun rapport existant n'est remplacé.

## Coût

Gratuit : l'outil n'appelle aucun service payant.

## Précautions

- Le rapport reprend les données de l'opération : il est aussi confidentiel que le contrat.
- Avant de réutiliser un contrat comme modèle, relisez-le en entier, en-têtes et pieds de page compris. Le rapport dit où regarder en premier, pas où il est inutile de regarder.
- Pour remplacer les noms dans un texte avant de le confier à une IA, utilisez plutôt l'outil [Pseudonymisation](/outils/pseudonymisation/).
- Les règles générales d'usage sont sur la page [Précautions](/fr/ethique/precautions-outils-ia-avocat/).

## Installation

Le guide [Utiliser un outil en local](/guides/installer-outil-python-windows/) détaille chaque étape. En bref :

1. Installez Python 3.10 ou plus récent.
2. Téléchargez l'archive ci-dessus et vérifiez son empreinte SHA-256.
3. Décompressez-la, puis double-cliquez sur `Conditions.pyw`.

L'outil fonctionne aussi en ligne de commande (`python -m conditions_particulieres "chemin du contrat.docx"`). Le fichier `README.md` de l'archive décrit les options.

## Versions

0.1.0 (1er novembre 2026) : première version.

## Signaler un problème

Écrivez à [À COMPLÉTER : adresse de contact] en indiquant la version de l'outil et la formulation mal traitée, recopiée sans nom ni donnée du client. N'envoyez pas de contrat réel.
