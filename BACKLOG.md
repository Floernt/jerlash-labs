# Backlog

Règle depuis le 2026-11-01 : livrer plutôt que construire. Un seul chantier dans « Maintenant ». Tout le reste attend ici, et rien n'en sort sans décision de Florian. Ce qui est livré passe dans `CHANGELOG.md`.

## Maintenant : site jerlash.labs 0.1.0 (ADR-022)

- [x] Identité jerlash appliquée au site Hugo (polices, couleurs, logo, fonds pixel)
- [x] Rubrique Blog alimentée par `scripts/importer_articles.py` depuis `../articles` (articles « à publier »)
- [x] Sections outils, guides, automatiser, nouveautés et précautions retirées du site publié (brouillons)
- [x] Florian : créer le dépôt GitHub public `jerlash-labs`, donner son URL et le nom du compte
- [ ] URGENT, Florian : mentions légales et confidentialité retirées du site le 2026-11-01 pour publier sans attendre ; à remettre dès que possible (adresse de contact, adresse du cabinet, BCE, TVA, référence déontologique, journaux GitHub), avec la phrase de contact de la page À propos et security.txt
- [x] Vérification complète sur Linux : archives zip reproductibles d'un système à l'autre (système d'origine fixé à Unix) et jeux de test reproductibles sous Linux (PR #2 et #3)
- [ ] Florian : relire la page d'accueil, les 9 articles importés (dont 4 aux en-têtes vides : titre tiré du nom de fichier) et leurs dates (date du fichier)
- [x] Pousser sur GitHub, activer Pages (source : GitHub Actions), publication verte : en ligne sur jerlash.eu le 2026-11-01
- [x] Accueil : nouveau héros et section « Pourquoi jerlash.labs ? »
- [x] Page À propos réécrite (mission, approche, communs, origine du nom) et traduite en anglais
- [ ] Florian : cocher « Enforce HTTPS » dans Settings → Pages dès que le certificat est délivré, puis relancer la publication (liens canoniques en https) ; au 2026-11-01, `https://jerlash.eu` ne répond pas encore

## Maintenant (ajouté le 2026-11-01 à la demande de Florian) : version anglaise du site (ADR-023, proposée)

- [x] Hugo multilingue `/fr/` et `/en/`, libellés i18n, lien FR/EN, hreflang, redirections des anciennes adresses
- [x] `scripts/traductions.py` (état, diff, marquage) et commande `/traduire`
- [x] Traduction initiale des 35 pages
- [ ] Florian : valider ADR-023, relire l'anglais (accueil, À propos, articles), compléter `docs/glossaire-traduction.md`
- [x] PR `dev` → `main` (PR #1, fusionnée)

## Ensuite

- [ ] Réorganiser le répertoire du projet (nom jerlash.labs, dossiers, fichiers hors dépôt)
- [ ] Choisir les outils à publier, un à la fois, et ce qui manque à chacun pour être prêt
- [ ] Domaine : jerlash.eu choisi et DNS en place ; reste HTTPS (voir plus haut), 2FA GitHub et registraire
- [ ] Rubrique Guides : compléter les quatre guides (clé API, facturation, données envoyées, installation locale)
- [ ] Page Outils et fiches, quand un outil est prêt

## Plus tard

Outils (état au 2026-11-01, tous au statut vérification, aucun publié) :
- [ ] P01 Inventaire 0.2.0 : config-ia.json et .env, mesure réelle `evaluer.py --ia --executions 3` (seuils 14/16 et 13/16), essai sur un dossier réel
- [ ] P02 Glossaire, P03 Conditions, P05 Contrôle avant envoi, P09 Pseudonymisation : essai de la fenêtre par Florian ; mode IA selon ADR-019
- [ ] P09 : meilleure détection des noms de personnes (45 % sur le jeu de contrôle), avec un nouveau jeu de contrôle
- [ ] P04, P06, P07, P08, P10, P11, P12, P13 : fiches dans `projets/`, rien de commencé (sauf P12, jeux de test livrés)

Décisions et vérifications :
- [ ] Valider ADR-016, ADR-017, ADR-018
- [ ] Bibliothèque : URL officielles et date des lignes directrices AVOCATS.BE et OVB, URL du guide CNB
- [ ] Mistral : point d'accès UE à confirmer ; matrice des fournisseurs, 22 points [À VÉRIFIER]
- [ ] Règles de communication de l'Ordre applicables au site, mentions obligatoires
- [ ] Rubrique « Automatiser une prestation » (ADR-012) : relire les deux articles
- [ ] Décider si le tutoriel de veille Cowork, les fiches « avocat entrepreneur » et le livre blanc rejoignent le site

Factory et plan d'amélioration :
- [ ] Factory : valider ADR-007 et le circuit ; AM-001, AM-002 ; essai d'un mois de la mémoire (F03) ; F01
- [ ] Plan d'amélioration du 2026-10-31 (PLAN_AMELIORATIONS.md) : A01, A03, A05, A08 à A18 restent ouverts ; A02, A04, A06, A07 livrés
- [ ] Rythme : fréquence de publication réaliste, revue semestrielle des guides
