# Charte éditoriale

## Ligne

Fonctionnel et opérationnel. Chaque page répond à une question pratique : qu'est-ce que c'est, à quoi ça sert dans un cabinet, comment on l'installe, combien ça coûte, à quoi faire attention.

Les mises en garde font partie du contenu. Elles sont concrètes (que peut-il arriver, que faire) et proportionnées. Outils, guides et pages d'Éthique restent sans développement philosophique.

Depuis ADR-024, la réflexion sur le droit, la pratique juridique et la technique a sa place dans Revue › Perspectives, et les research papers suivent `docs/politique-publication.md`. La réflexion généraliste, indépendante de toute matière, reste sur reflexions.florianernotte.be.

## Communication de l'avocat

Décision de Florian du 2026-10-31. Le site ne mentionne pas la notion d'offre et n'annonce aucun service que Florian fournit. Il est joignable : les rubriques « Contact » donnent une adresse pour écrire au sujet du site, de ses outils et de ses guides. Pas d'invitation à confier un dossier, pas d'appel à prendre contact en fin de page.

## Ton

Un avocat qui explique à un confrère ce qu'il a testé. Première personne admise quand elle apporte une information ("j'ai testé avec 40 pièces, le traitement a pris..."). Pas de promesse, pas de superlatif, pas de dramatisation des enjeux.

## Exactitude

- Toute affirmation factuelle sur un fournisseur, un tarif, un modèle ou une règle est sourcée et datée.
- Ce qui n'est pas vérifié n'est pas publié.
- Les captures d'écran et les tarifs vieillissent : chaque guide porte une date de dernière vérification.
- Sources nommées. Jamais "les experts", "de nombreux observateurs" ou "selon plusieurs études".

## Structure d'un guide

1. En une ou deux phrases : ce que le lecteur saura faire à la fin.
2. Prérequis.
3. Étapes numérotées, une action par étape.
4. Points d'attention.
5. Sources et date de vérification.

Pas de résumé en fin de page qui répète ce qui précède.

## Tics d'écriture à proscrire

Ces formules donnent un texte générique. Une occurrence isolée peut passer, leur accumulation non.

- Adverbes d'emphase vides : "profondément", "fondamentalement", "remarquablement", "discrètement".
- Vocabulaire gonflé : "écosystème", "paysage", "paradigme", "synergie", "tirer parti", "robuste", "plonger dans".
- "Sert de", "se présente comme", "marque" à la place de "est".
- "Ce n'est pas X, c'est Y" et "non pas parce que X, mais parce que Y" en série.
- "Pas X. Pas Y. Juste Z."
- Question rhétorique suivie de sa réponse : "Le résultat ? ..."
- Même début de phrase répété ; énumérations par trois en cascade.
- "Il est intéressant de noter", "notamment" en ouverture de phrase, "il convient de souligner".
- Participe présent en fin de phrase qui ajoute une portée vague ("soulignant l'importance de...").
- Fausses fourchettes "de X à Y" sans échelle réelle.
- Fragments courts isolés pour l'effet, listes de gérondifs sans sujet.
- "Le premier... Le deuxième... Le troisième..." pour déguiser une liste.
- "Voici le point clé", "voici ce que personne ne dit".
- "Imaginez un monde où...", "voyez-le comme...".
- Concepts inventés présentés comme établis ("le paradoxe de la supervision").
- "En conclusion", "pour résumer".
- Tirets cadratins à répétition, flèches Unicode, puces commençant toutes par un mot en gras.
- "Malgré ces défis, ..." en fin de paragraphe.

## Référencement : slug et description

Règle de Florian du 2026-11-12, pour tout texte de la Revue et toute page nouvelle. L'adresse ne change plus une fois la page en ligne : le slug se fixe avant la première publication.

Slug :

- il reprend la requête qu'un lecteur taperait, mot-clé principal en tête (« taux-horaire-avocat-ia », pas « taux-horaire-et-intelligence-artificielle-quelle-place ») ;
- trois à six mots, sans article, sans élision (`lia`, `lavocat`) ni mot vide ;
- chaque page vise une requête qu'aucune autre page du site ne vise déjà. Avant de choisir, vérifier les adresses existantes, rubrique Outils comprise (la boîte à outils occupe « gouvernance-ia ») ;
- recension : le nom de l'auteur recensé, et pour un livre les mots de son titre (`impact-ia-juristes-avocats-affaires-chaduteau`) ;
- en français, le slug est le nom du fichier ; en anglais, le champ `slug:`, construit sur la requête anglaise (« billable hour », « law firm »), pas traduit mot à mot.

Description (`description:` du front matter) :

- 155 caractères au plus, la requête visée dans la première moitié ;
- elle dit ce que le texte apporte, au lieu de reprendre sa première phrase ;
- mêmes règles d'écriture que le texte : pas de superlatif, pas de tic de la liste ci-dessus. Elle est publiée sous le nom de Florian, qui la valide.

Un slug changé avant publication ne demande pas de redirection. Après publication, l'ancienne adresse va dans `aliases`.

## Typographie

Français de Belgique. Espaces insécables avant ; : ! ? dans les textes publiés. Dans le code et les blocs techniques, guillemets droits.
