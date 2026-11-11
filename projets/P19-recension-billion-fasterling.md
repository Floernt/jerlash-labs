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

Brouillon v0.1 d'environ 1 600 mots. Il recense un entretien publié par EDHEC Vox le 9 octobre 2026 sur trois mots du vocabulaire de l'IA : « biais », « compagnon » et « hallucinations ». Le brouillon déclarait l'usage de GPT-6 ; le front matter publié ne nomme pas l'outil. Les déclarations ont été tranchées le 2026-11-11 (§7).

## 2. Problème ou opportunité

Le vocabulaire employé pour parler de l'IA oriente la confiance qu'on lui accorde.

Le texte publié ne formule aucune hypothèse expérimentale pour le programme H1, contrairement à ce qu'annonçait cette fiche et à ce qu'annonce encore le résumé de la carte P19 de la rubrique Recherche (« la recension en tire une hypothèse à éprouver dans le programme », `site/content/recherche/projets/p19.md` et `p19.en.md`). Deux issues, au choix de Florian : corriger les deux résumés, ou écrire l'hypothèse. Les cartes n'ont pas été modifiées. [À VÉRIFIER]

## 3. Solution envisagée

Publication dans Revue. Prévue en décembre 2026, avancée en novembre par Florian le 2026-11-04 ; la page est en ligne depuis le 2026-11-07. C'est le premier texte de la collection après la migration du blog.

Hors périmètre : rien de particulier.

## 4. Adaptation à jerlash.labs

La collection est tranchée : Recensions, objet `article` (ADR-027, proposée, validation de Florian en attente). Le brouillon indiquait « Critical Reviews ».

Voix : Florian a relu le texte avant sa mise en ligne et garde les trois réserves (§9). Les six passages signalés dans le dossier de lecture — dont toute la section « Intérêt pour les juristes », qui adresse des prescriptions à des confrères — sont donc tenus pour siens, et le texte reste tel qu'il est publié. Aucune reprise n'est engagée sans une demande explicite de sa part.

## 5. Approche technique pressentie

Une page Markdown, traduite en anglais.

## 6. Contraintes et risques

La citation de l'entretien et son URL ont été recontrôlées sur la page EDHEC Vox le 2026-11-11 : URL valide, date de publication du 2026-10-09 conforme au front matter, titres des trois sections cités fidèlement (sous forme abrégée), attributions à Billion et à Fasterling conformes. La page porte une date de dernière modification du 2026-10-13, postérieure au `consulte_le: 2026-11-02` du front matter ; la comparaison du 2026-11-11 n'a relevé aucune divergence avec ce que dit la recension.

Reste une affirmation sans source : le texte date la Summer School de « début septembre 2026 », alors que la page écrit seulement « début septembre », sans année (recontrôlé le 2026-11-11). Piste trouvée le 2026-11-11, non confirmée sur la source : l'Augmented Lawyer Academy annonce une « Executive Summer School 2026 » de l'EDHEC Augmented Law Institute les 8, 9 et 10 septembre 2026 à Paris (`https://alll.legal/programme/executive-summer-school-2026/`). La page n'a pas pu être ouverte depuis l'environnement de l'agent (HTTP 404) : l'indication vient des résultats de recherche, pas de la page elle-même. L'année reste à confirmer ou à retirer. [À VÉRIFIER]

## 7. Critères d'acceptation

- [x] Citations vérifiées sur la source (2026-11-04, recontrôlées le 2026-11-11 ; reste l'année de la Summer School)
- [x] Collection choisie (Recensions, ADR-027)
- [x] Déclarations : tranché par Florian le 2026-11-11, « pas obligatoire ». `controles` et `conflits_interets` sont de toute façon facultatifs pour une recension (§9 de la politique, choix du 2026-11-05) ; `usage_ia` reste sans les vérifications humaines qu'énumère le §5. L'auteur n'est pas un champ du front matter (§4) : c'est le paramètre `auteur` du site

## 8. Appétit

Mois léger. Il laisse du temps pour récupérer le code C3 dont P18 a besoin.

## 9. Questions ouvertes

Tranchées : la collection (Recensions, ADR-027, 2026-11-04). Puis, le 2026-11-11, après la lecture du dossier du ticket FLO-18 :

1. **Les trois réserves de la Discussion** (« biais », « un bout de code », « hallucination ») : réponse « oui », comprise comme « gardées telles quelles ». Le texte publié n'est pas modifié. Si la réponse visait en fait une atténuation ou un retrait sur l'une d'elles, la passe reste à faire.
2. **Le statut de publication** : la page reste en ligne. Florian l'a relue avant sa mise en ligne du 2026-11-07, ce qui satisfait la première case du §8 de `docs/politique-publication.md`. Rien à dépublier, rien à retirer de la carte P19.
3. **Les déclarations** : « pas obligatoire ». Front matter inchangé (voir §7).

Ouvertes, pour Florian :

1. L'hypothèse H1 annoncée par les deux résumés et absente du texte (§2) : corriger les résumés, ou écrire l'hypothèse.
2. L'année de la Summer School (§6), seule question du dossier restée sans réponse.

## 10. Prochaine étape

Avancée en novembre 2026 (Florian, 2026-11-04). Collection Recensions retenue, objet `article` (ADR-027). Le 4 novembre 2026, les attributions ont été comparées à la page EDHEC Vox : elles sont conformes, y compris « un bout de code », qui est bien de Billion. La page ne donne pas l'année de la Summer School (« début septembre »).

État au 2026-11-11 : la recension est publiée (`draft: false` en FR et en EN, dans `main` depuis le 2026-11-07), la traduction anglaise est à jour (empreinte `traduction.source` égale au fichier français courant), et la carte P19 de la rubrique Recherche pointe vers elle. Les citations ont été recontrôlées sur la source. Dossier de lecture déposé sur le ticket FLO-18 : `[À VÉRIFIER]` en tête, les trois réserves en questions courtes, les passages à faire siens, les déclarations à remplir.

Lecture et arbitrages de Florian le 2026-11-11 (ticket FLO-18) : réserves gardées, page laissée en ligne, déclarations non obligatoires. Aucun fichier de `site/` n'a été modifié : la recension publiée, sa traduction anglaise et les cartes de Recherche restent dans l'état du 2026-11-07. La traduction anglaise reste donc à jour ; `/traduire` ne se justifiera que si le français bouge.

Reste : l'hypothèse H1 et l'année de la Summer School (§9), toutes deux pour Florian. ADR-027 est toujours au statut « proposée ».
