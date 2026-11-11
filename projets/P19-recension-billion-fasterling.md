---
id: P19
titre: Recension « Biais, compagnon, hallucinations » (Billion et Fasterling)
type: contenu (recension)
statut: en cours
priorité: moyenne
source: archive Proton du 2026-11-03, recension-billion-fasterling-langage-ia.md (hors dépôt)
licence_source: CC BY 4.0 proposée
dépend_de: [ADR-024, ADR-027]
mise_a_jour: 2026-11-11
---

# Recension « Biais, compagnon, hallucinations »

## 1. Origine

Brouillon v0.1 d'environ 1 600 mots. Il recense un entretien publié par EDHEC Vox le 9 octobre 2026 sur trois mots du vocabulaire de l'IA : « biais », « compagnon » et « hallucinations ». Le texte déclare l'usage de GPT-6 et n'a pas été relu par une seconde personne. L'identifiant, l'auteur et la déclaration de conflits d'intérêts sont à remplir.

## 2. Problème ou opportunité

Le vocabulaire employé pour parler de l'IA oriente la confiance qu'on lui accorde. Le texte en tire une hypothèse expérimentale pour le programme H1.

## 3. Solution envisagée

Publication dans Revue. Prévue en décembre 2026, avancée en novembre par Florian le 2026-11-04 ; la page est en ligne depuis le 2026-11-07. C'est le premier texte de la collection après la migration du blog.

Hors périmètre : rien de particulier.

## 4. Adaptation à jerlash.labs

La collection est tranchée : Recensions, objet `article` (ADR-027, proposée, validation de Florian en attente). Le brouillon indiquait « Critical Reviews ». Reste à passer le texte dans la voix de Florian.

## 5. Approche technique pressentie

Une page Markdown, traduite en anglais.

## 6. Contraintes et risques

La citation de l'entretien et son URL ont été recontrôlées sur la page EDHEC Vox le 2026-11-11 : URL valide, date de publication du 2026-10-09 conforme au front matter, titres des trois sections cités fidèlement (sous forme abrégée), attributions à Billion et à Fasterling conformes. La page porte une date de dernière modification du 2026-10-13, postérieure au `consulte_le: 2026-11-02` du front matter ; la comparaison du 2026-11-11 n'a relevé aucune divergence avec ce que dit la recension.

Reste une affirmation sans source : le texte date la Summer School de « début septembre 2026 », alors que la page écrit seulement « début septembre », sans année (recontrôlé le 2026-11-11). [À VÉRIFIER]

## 7. Critères d'acceptation

- [x] Citations vérifiées sur la source (2026-11-04, recontrôlées le 2026-11-11 ; reste l'année de la Summer School)
- [x] Collection choisie (Recensions, ADR-027)
- [ ] Auteur et déclarations remplis

## 8. Appétit

Mois léger. Il laisse du temps pour récupérer le code C3 dont P18 a besoin.

## 9. Questions ouvertes

Tranchées : la collection (Recensions, ADR-027, 2026-11-04). Ouvertes, toutes pour Florian :

1. Les trois réserves de la Discussion, à trancher avant la reprise dans sa voix (questions détaillées dans le dossier de lecture du ticket FLO-18).
2. Les déclarations : `conflits_interets` et `controles` sont absents du front matter ; `usage_ia` ne dit pas quelles vérifications humaines ont été faites, contrairement au §5 de `docs/politique-publication.md`.
3. La page est en `draft: false` et dans `main` depuis le 2026-11-07, donc déjà en ligne, avant la lecture prévue par le §8 de la politique de publication. La garder en ligne pendant la lecture, ou la repasser en brouillon ?

## 10. Prochaine étape

Avancée en novembre 2026 (Florian, 2026-11-04). Collection Recensions retenue, objet `article` (ADR-027). Le 4 novembre 2026, les attributions ont été comparées à la page EDHEC Vox : elles sont conformes, y compris « un bout de code », qui est bien de Billion. La page ne donne pas l'année de la Summer School (« début septembre »).

État au 2026-11-11 : la recension est publiée (`draft: false` en FR et en EN, dans `main` depuis le 2026-11-07), la traduction anglaise est à jour (empreinte `traduction.source` égale au fichier français courant), et la carte P19 de la rubrique Recherche pointe vers elle. Les citations ont été recontrôlées sur la source. Dossier de lecture déposé sur le ticket FLO-18 : `[À VÉRIFIER]` en tête, les trois réserves en questions courtes, les passages à faire siens, les déclarations à remplir.

Reste : lecture et prise de position de Florian sur les trois réserves, reprise dans sa voix, déclarations, et décision sur le statut de publication pendant la lecture.
