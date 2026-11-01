# CNB - La déontologie et l'intelligence artificielle (2026)

- Auteur : Conseil national des barreaux (France), commission des règles et usages (Bruno Blanquer, président ; Guillaume Isouard)
- Titre : « La déontologie et l'intelligence artificielle »
- Date : version adoptée par l'assemblée générale du CNB le 13 mars 2026
- URL officielle : `[À VÉRIFIER]`
- Fichier local : `sources/2026-03-13_CNB_deontologie-et-ia.pdf` (27 pages)
- Consulté le : 2026-11-01
- Portée : guide de la profession d'avocat en France (loi du 31 décembre 1971, RIN, décret du 30 juin 2023). Pas contraignant en Belgique, mais plus détaillé que les lignes directrices belges sur la pseudonymisation, la souveraineté et les critères de choix d'un outil. Il cite le guide du CCBE du 2 octobre 2025 et les directives de l'UIA du 30 octobre 2024.

## Résumé

Résumé, pas une citation. Le principe : ne jamais communiquer de données de dossier ou de client à une IA générative. La solution pratique : pseudonymiser ou anonymiser, en limitant le contexte au strict nécessaire et en restant attentif à la réidentification par recoupement. Les engagements contractuels des éditeurs (pas d'entraînement, pas de conservation) ne sont ni prouvables ni vérifiables. Les deux seules façons d'éliminer le risque de souveraineté sont la pseudonymisation préalable et l'installation du modèle sur les systèmes du cabinet. Le guide propose aussi des critères de choix (hébergement et nationalité du prestataire, chiffrement, suppression des requêtes, journalisation, fiabilité, tests sur des jeux de données) et aborde la vérification des résultats, les conflits d'intérêts, l'information du client et les honoraires.

## Passages cités

« Il est impératif pour l'avocat de veiller à ne jamais communiquer des données relatives à ses dossiers ou à ses clients à des intelligences artificielles génératives (IAG). » (p. 8)

« Ces données comprennent, entre autres, les noms, adresses, numéros de téléphone, informations financières et/ou stratégiques sur les clients et les membres du cabinet [...], ainsi que tout détail spécifique d'un dossier qui pourrait permettre d'identifier une personne ou une entreprise. » (p. 8)

Un avocat ne peut pas « joindre à sa requête tout fichier comportant tout ou partie d'un dossier et qui comporte le nom du client ou des informations confidentielles communiquées par lui ou des éléments stratégiques propres au dossier ». (p. 9)

« La solution réside dans la pseudonymisation ou l'anonymisation des données. » (p. 9)

« A noter : il existe des outils d'IA développés par des cabinets qui permettent d'effectuer toutes les tâches dans le respect du secret professionnel : il s'agit de systèmes d'IA fermés. » (p. 10)

« Il convient de rester vigilant à l'identification rendue possible par le croisement de plusieurs données, quand bien même ces données auraient déjà été pseudonymisées ou anonymisées (exemples : montants, noms de projets donnés en interne, façon de rédiger un contrat qui peuvent être caractéristiques de l'identification d'un client). » (p. 13)

Critères de souveraineté, « par ordre de priorité » : le lieu d'hébergement des données des clients, la nationalité de l'entreprise qui détient les serveurs, « excluant toute entreprise soumise à des dispositions extraterritoriales permettant aux autorités de l'état correspondant d'accéder aux données stockées sur des serveurs appartenant aux entreprises de sa nationalité, comme les entreprises américaines en l'état actuel de leur législation », puis les mêmes critères pour le modèle de langue. (p. 15)

« Néanmoins, même si un modèle propriétaire indique que les données téléchargées ne seront pas réutilisées, cette assertion n'est en général ni prouvable ni vérifiable. » (p. 15)

« La seule manière d'éliminer les risques liés à la souveraineté [...] et de garantir l'étanchéité et la confidentialité pour les données du cabinet "injectées" dans l'outil d'IA sont : l'anonymisation ou la pseudonymisation préalable des données, l'installation du LLM sur les propres systèmes d'information du cabinet (par exemple à partir d'un modèle open source comme Llama ou Mistral AI). » (p. 15)

Critères de confidentialité et de sécurité, notamment : chiffrement en transit et au repos « avec une détention et une gestion par le cabinet de la clé de chiffrement », non-réutilisation pour l'entraînement, suppression automatique des requêtes après réponse, impossibilité d'accès par les salariés de l'éditeur, journalisation. Le guide rattache la comparaison des offres à l'article 28.1 du RGPD. (p. 16)

« Il est recommandé aux professionnels de tester les outils avant leur utilisation en conditions réelles et d'évaluer les performances spécifiques des modèles d'IA dans le domaine juridique, sous forme d'études comparatives spécifiques à l'aide de jeux de données du type "LegalBench". » (p. 17)

« L'avocat doit s'assurer que les données transmises à l'outil ne risquent pas d'être réutilisées dans le cadre d'autres dossiers. » (p. 19)

## Usage dans le projet

- Grille de critères pour qualifier un « prestataire conforme » : `docs/deontologie-ia.md`, ADR-015.
- La recommandation de tester les outils sur des jeux de données rejoint la pratique de la Factory (jeux de développement et de contrôle, `factory/jeux-de-test/`).
- Source possible pour un guide du site sur le choix d'un fournisseur, à condition de signaler qu'il s'agit d'un texte français.
