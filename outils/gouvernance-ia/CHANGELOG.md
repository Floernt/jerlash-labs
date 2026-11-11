# Journal des versions — Gouvernance de l'IA

Ce que chaque version de la boîte à outils (P14) ajoute ou change. Les versions du site et des autres outils sont dans le `CHANGELOG.md` à la racine du dépôt ; la date d'arrêt du droit et les points à vérifier sont sur la page [Sources et versions](../../site/content/outils/gouvernance-ia/sources-et-versions.md).

La version est celle du référentiel (`referentiel/gouvernance-ia.json`, champ `version`). Le tableur et les téléchargements la reprennent dans leur nom de fichier.

## Non publié

- Téléchargements de la version 0.3 : pack complet en zip, charte modèle en .docx et kit « petit cabinet » (les six éléments du niveau 1), en français et en anglais. Ils sont reconstruits à partir des pages du site par `telechargements/generer_telechargements.py`, étape de `scripts/verifier.py`, et ne sont donc pas versionnés dans le dépôt (ADR-034). Reproductibles : même contenu, mêmes octets, même empreinte SHA-256.
- Registres vides (CSV, séparateur point-virgule) produits à partir des colonnes du référentiel : homologations, incidents, usages significatifs, formations. La page « Opérations » les annonçait sans qu'ils soient téléchargeables.
- Contrôles automatiques dans `tests/` : reproductibilité octet par octet, présence des dix pages et des six éléments, formulaires vides, parties et XML du .docx, liens utilisables hors du site.
- Les documents de contexte de `99_SOURCES` (archive Proton v0.1.0, hors dépôt) ne sont pas repris dans le pack : les droits de redistribution n'ont pas été vérifiés (§ 6 de la fiche P14).

## 0.3 — 2026-11-06

- Trois niveaux de gouvernance, déterminés outil par outil ; l'organisation retient le niveau le plus élevé de ses outils (ADR-029).
- Nouvelle page « Le niveau 1 » : les six éléments du minimum opérationnel et la fiche de conformité d'un outil (F01 à F11). Chaque module indique ce qu'il demande à chaque niveau.
- Le toolkit devient « Gouvernance de l'IA » : `/fr/outils/gouvernance-ia/` et `/en/tools/ai-governance/` ; les anciennes adresses redirigent.
- Référentiel unique `referentiel/gouvernance-ia.json` : niveaux, règle de détermination du niveau, codes F, D, U, S, E et C, colonnes des registres. Le tableur et, plus tard, le serveur MCP (P20) le lisent (ADR-030).
- Tableur des niveaux 2 et 3 (`tableur/gouvernance-ia-matrices-0.3.xlsx`), produit par `tableur/generer_tableur.py` avec openpyxl et versionné dans le dépôt.
- Les dix pages sont publiées en français et traduites en anglais.

## 0.1.0 — 2026-11-02 (hors dépôt)

Ensemble documentaire d'origine, rédigé avec l'aide d'une IA et non relu par un tiers : note de cadrage, manifeste, analyse critique d'une charte de cabinet, charte en seize articles, politique de gouvernance et matrice RACI, référentiel d'homologation, protocole de supervision S1 à S4, classification D0 à D4, procédures, protocole de recherche H1 et modèles. Statut : proposition non adoptée. Source dans l'archive Proton du 2026-11-03, hors dépôt.

Aucune version 0.2 n'a été publiée : la première version publique est la 0.3.
