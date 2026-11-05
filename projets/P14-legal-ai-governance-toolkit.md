---
id: P14
titre: Legal AI Governance Toolkit
type: contenu (toolkit)
statut: cadrage
priorité: haute
source: archive Proton du 2026-11-03, JERLASH_Labs_Legal_AI_Governance_Toolkit v0.1.0 (hors dépôt : ../sources-proton/2026-11-03/)
licence_source: aucune licence concédée par la v0.1 ; publication sous CC BY-NC 4.0, éditeur jerlash.labs (ADR-026)
dépend_de: [ADR-024]
mise_a_jour: 2026-11-03
---

# Legal AI Governance Toolkit

## 1. Origine

Ensemble documentaire v0.1.0 daté du 2 novembre 2026, rédigé avec l'aide d'une IA et non relu par un tiers. Environ 19 000 mots, au statut « proposition non adoptée ». Il comprend une note de cadrage, un manifeste, une analyse critique de la charte initiale (10 faiblesses), une charte modèle en 16 articles, une politique de gouvernance et une matrice RACI, un référentiel d'homologation (tests, fiche d'évaluation, grille de scores), un protocole de supervision S1 à S4, une classification des données D0 à D4, des procédures de traçabilité, d'incidents et de formation, le protocole de recherche H1 et des modèles (cas d'usage, décision de gouvernance). Les 6 fichiers CSV ne contiennent que leurs en-têtes.

## 2. Problème ou opportunité

Les chartes IA des cabinets énoncent des principes qu'on ne peut pas vérifier (« faire relire », « outil sécurisé »). Elles ne disent ni comment homologuer un outil pour un usage donné, ni ce que doit savoir faire la personne qui supervise, ni comment prouver qu'un contrôle a eu lieu.

## 3. Solution envisagée

Publier sur jerlash.labs une version de travail v0.2 du Toolkit. Elle comprend :
- une page de présentation ;
- une page « Pourquoi les chartes échouent » ;
- une page par module, dans l'ordre du parcours : gouvernance, données, homologation, supervision, opérations, puis la charte, qui vient en dernier et ancre les choix de gouvernance (décision de Florian, 2026-11-03) ;
- une page « Sources et date d'arrêt du droit » ;
- un journal des versions ;
- en téléchargement, un pack complet en zip, la charte en .docx et un kit « petit cabinet » regroupant les 6 éléments du minimum opérationnel.

C'est le projet de novembre 2026, avec la refonte du site (ADR-024).

Hors périmètre : certification, label de conformité, homologation d'un fournisseur pour tout le marché, avis juridique individualisé, offres payantes (décision D10, à instruire séparément).

## 4. Adaptation à jerlash.labs

- Passage par la charte éditoriale et `scripts/typographie.py`.
- Version française maître, traduction anglaise par `/traduire`.
- Bloc de statut sur chaque page : version de travail, date de vérification du droit, licence, déclaration d'usage de l'IA.
- Les classes internes (U1–U4, S1–S4, D0–D4) sont clairement distinguées des catégories de l'AI Act.

## 5. Approche technique pressentie

Pages Hugo dans `site/content/outils/legal-ai-governance-toolkit/`, avec une sous-page par module. Les fichiers à télécharger sont produits de façon reproductible, sur le modèle de `scripts/empaqueter.py`, et la charte .docx par la skill docx. Les CSV sont livrés tels quels, sans aucune donnée.

## 6. Contraintes et risques

Déontologie : le Toolkit ne doit pas promettre une conformité. Secret professionnel : aucun exemple réel.

Réglementation (décision de Florian, 2026-11-03) : le règlement IA occupe une place limitée dans le Toolkit. Dans le domaine de la justice, les systèmes à haut risque visent l'administration de la justice, c'est-à-dire le travail des magistrats ; la pratique d'un cabinet d'avocats ou de juristes n'en relève pas. Le Toolkit se borne à le rappeler et à poser une règle : aucune déviation de la destination du système d'IA utilisé ne doit être envisagée. Les articles 14 et 26 et les obligations du haut risque sortent des modules. Restent à vérifier : les articles du RGPD cités, le secret professionnel en droit belge et le texte consolidé du règlement IA pour le rappel lui-même. [À VÉRIFIER]

Point soulevé le 2026-11-03, à confirmer par Florian : un cabinet peut déployer un système à haut risque hors de la pratique juridique, par exemple pour le recrutement (annexe III, point 4). Le point 8 a) vise aussi les modes alternatifs de règlement des litiges. Faut-il une phrase sur ces deux cas ?

Technique : rien de particulier.

Licence : CC BY-NC 4.0 (ADR-026). Vérifier les droits sur les deux documents de contexte de `99_SOURCES` avant de redistribuer le zip.

## 7. Critères d'acceptation

- [ ] ADR-024 acceptée et rubriques Outils, Éthique et Revue en ligne
- [ ] Toolkit lu en entier par Florian, qui y adhère
- [ ] Points juridiques vérifiés et datés, ou marqués
- [x] D01 (éditeur : jerlash.labs) et D02 (licence : CC BY-NC 4.0) tranchés (ADR-026)
- [ ] Téléchargements reproductibles, sans données
- [ ] `python scripts/verifier.py --publication` vert
- [ ] Version anglaise à jour

## 8. Appétit

Temps que Florian peut y consacrer : [À COMPLÉTER]
Délai souhaité : publication fin novembre 2026.

## 9. Questions ouvertes

1. Nom français : « Gouverner l'IA au cabinet » (`/fr/outils/gouverner-l-ia-au-cabinet/`), retenu provisoirement le 2026-11-03, à confirmer avant publication.
3. Licence : faut-il ajouter à CC BY-NC 4.0 une autorisation expresse d'adoption et d'adaptation internes par les cabinets ? (question soulevée le 2026-11-03)
2. Faut-il des seuils et pondérations par défaut, ou seulement les paramètres locaux à fixer (D05) ?

## 10. Prochaine étape

Rédiger ADR-024, puis convertir les modules en pages.

Versions suivantes :
- v0.3 en mai 2027, avec deux homologations documentées ;
- v1.0 en octobre 2027, si deux relecteurs externes ont été trouvés.
