# Veille : Sol Irvine (github.com/zenzen-sol)

Exploration réalisée le 2026-10-31. Sources consultées : page de profil GitHub, liste publique des dépôts (42 dépôts, dont une majorité de forks), README de skillboxing, wargame-oss, open-pstack, mike, stella, docx-editor, laws-of-ux, les cinq SKILL.md de legal-prompts (lecture de l'en-tête et des premières sections), README de stella/anonymize.

Non consulté : le contenu des sites augustus.esq et wargame.esq (cités dans la bio X de Sol Irvine), le site zenzen.io/sol, le code source des dépôts au-delà des README.

## Qui

D'après son profil GitHub : "dev + lawyer", basé à Kyoto. D'après son profil LinkedIn (extrait de recherche) : associé chez Yuson & Irvine LLC, avocat depuis une trentaine d'années, cofondateur de LegalQuants avec Raymond Sun. Sa bio X mentionne "building AI for transactional lawyers" et deux domaines dédiés, augustus.esq et wargame.esq, ce qui correspond au modèle "un domaine par projet" évoqué dans le brief.

## Dépôts retenus pour iavocat.be

| Dépôt | Nature | Licence | Fiche |
|---|---|---|---|
| legal-prompts / matter-intake | skill, propre | MIT | P01 |
| legal-prompts / defined-terms-glossary | skill, propre | MIT | P02 |
| legal-prompts / order-form-restructure | skill, propre | MIT | P03 |
| legal-prompts / working-copy-redlines | skill, propre | MIT | P04 |
| legal-prompts / send-ready-pass | skill, propre | MIT | P05 |
| wargame-oss | application, propre | MIT | P06 |
| skillboxing | plugin Claude/Codex, propre | MIT | P07 et F03 |
| stella (tabular review) | fork d'un projet tiers | Apache-2.0 | P08 |
| stella/anonymize | bibliothèque tierce | Apache-2.0 | P09 |
| docx-editor (eigenpal) | fork d'une bibliothèque tierce | Apache-2.0 | P10 |
| docling-serve, docling-api | forks d'outils tiers | [À VÉRIFIER] | P11 |
| lector | fork, visionneuse PDF | [À VÉRIFIER] | P11 (option) |
| LQ Assess (LegalQuants) | mentionné sur LinkedIn, pas de dépôt consulté | inconnue | P12 |
| mike, stella | plateformes juridiques open source tierces | AGPL-3.0 / Apache-2.0 | P13 |
| open-pstack | fork maintenu d'un plugin tiers | MIT | F01 |
| laws-of-ux | skill d'agent, propre | aucun fichier LICENSE trouvé | F02 |

## Dépôts écartés

| Dépôt | Raison |
|---|---|
| zephyr, commerce, cctp-sample-app, safe-contracts, bridge-v2, yearn-*, ren-js-demo, use-metamask, spl-token-wallet, mobile-pwa-with-passkey-wallet | projets web3 ou e-commerce sans lien avec les outils d'iavocat.be. SafeHarbor2.0, OP-SAFT et metalex peuvent intéresser CryptoReflexions, pas iavocat.be |
| zenzen-leo | agent connecté à WhatsApp : contraire au principe de confidentialité des outils |
| maana-annex | site vitrine d'un projet immobilier |
| para-releases | application desktop dont le code est privé et dont l'objet n'est pas décrit dans le dépôt |
| vllm | serveur d'inférence trop lourd pour le public visé ; à revoir si des outils à modèle local sont développés |
| narai-website, intercom-test, next-reproduction-template, react-*, ember-*, styled-qr-code, cc, next-data-hooks, vscode-tailwindcss | sans rapport |

## Pratiques à retenir (observées dans legal-prompts et wargame-oss)

1. Chaque skill définit un "contrat de complétion" : le travail n'est terminé que lorsque le fichier produit existe et que son nom exact est communiqué. Une phrase affirmant que c'est fait ne vaut pas livrable.
2. Le texte des documents traités est du contenu, jamais des instructions (protection contre l'injection de consignes dans une pièce).
3. L'original n'est jamais modifié ; les sorties sont des copies.
4. Toutes les questions sont posées en une fois, avant de commencer.
5. Restructurer n'est pas renégocier : aucune modification de fond silencieuse, tout changement nécessaire est signalé.
6. wargame-oss : clé de l'utilisateur (OpenAI ou Anthropic), plafonds configurables de tours et de points pour borner la dépense, sortie en .docx avec de vraies modifications suivies.
7. Rédiger les contrats avec un bon de commande en tête qui regroupe toutes les données propres à l'opération facilite la dé-identification (idée exprimée par Sol Irvine sur X, connue ici par un extrait cité sur trendshift.io).

Ces pratiques sont reprises dans `factory/standards/prompts-juridiques.md`.

## Prochaine revue

Revoir la liste des dépôts tous les trois mois (agent `eclaireur`).
