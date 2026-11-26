# F-LAF-01 — Benchmark faillite, pièces du jeu de conception

Version 0.1, 26 novembre 2026. Tout est fictif : personnes, sociétés, adresses (domaines en `.invalid`), montants, juridictions et numéros de rôle.

## À quoi sert ce jeu

Il fournit les pièces que reçoit la chaîne de la Legal Agent Factory pour les 24 cas du jeu de conception (`design`) du benchmark `JERLASH_Labs_Benchmark_Faillite_40_Cas.csv`, qui reste hors dépôt. Le fichier de cas ne contient que des descriptions de scénario ; sans pièces, le banc d'évaluation (`legal-agent-factory/laf/banc/`) ne peut rien mesurer.

Les pièces décrivent des faits. Elles ne contiennent ni réponse attendue ni règle de droit affirmée par le jeu. Quand une pièce affirme quelque chose sur le droit (un créancier qui compte un délai, un ami qui parle d'un arrêt), c'est l'affirmation d'un personnage, à traiter comme une donnée. Aucune référence d'arrêt n'est citée.

Ces pièces ont été rédigées par l'agent qui construit le harnais, à la demande de Florian (FLO-66). Elles n'ont pas été relues par un juriste [À VÉRIFIER].

## Ce qui n'est pas ici

Le jeu de test final (`holdout`, 16 cas) n'est volontairement pas rédigé. Celui qui règle les instructions et le harnais ne doit pas en connaître les pièces, sinon le test final ne mesure plus rien. Ses pièces sont à écrire par Florian, ou par un agent qui n'a accès ni au harnais ni aux instructions, et à conserver hors dépôt.

## Fichiers

```
generer.py       source unique des pièces (un dictionnaire par cas)
pieces-design/   une pièce par fichier, un sous-dossier par cas (BK-01 à BK-24)
resultats/       rapports d'exécution du banc
```

```
python -I factory/jeux-de-test/F-LAF-01/generer.py             régénérer
python -I factory/jeux-de-test/F-LAF-01/generer.py --verifier  contrôler que pieces-design/ correspond aux sources
```

## Particularités

- Les cas BK-01 à BK-20 partagent un même dossier fictif (faillite de Menuiserie Dufour SRL, jugement du 3 novembre 2026) quand le scénario le permet ; les autres cas ont leur propre personnage.
- BK-03 : les deux versions de la facture sont présentes côte à côte ; la détection d'une nouvelle version sous le même nom relève des tests du Lot 1 (`tests/test_surveillance.py`).
- BK-05 : `jugement.pdf` est un PDF tronqué et illisible.
- BK-19 : l'adresse de la « curatrice » n'est pas celle du jugement.
