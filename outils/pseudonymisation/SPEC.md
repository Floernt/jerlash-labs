# Spécification - Pseudonymisation (P09 Lite)

Version 0.1.0 - 2026-10-31 - Parcours Factory : renforcé (pièces de dossier, ADR-007)

## Besoin

Avant de soumettre une pièce à une IA, l'avocat veut en retirer les noms, adresses et identifiants. Faire ces remplacements à la main prend du temps et donne des résultats irréguliers : un nom est oublié au troisième paragraphe, ou deux personnes reçoivent le même remplacement. Ensuite, il faut remettre les vrais noms dans la réponse de l'IA.

## Périmètre

Inclus :
- lecture d'un texte collé, d'un .txt, d'un .md ou du corps d'un .docx ;
- détection par règles de douze catégories (`detection.py`, `CATEGORIES`), auxquelles s'ajoute la liste de termes de l'utilisateur ;
- relecture et correction dans la fenêtre : remplacer ou conserver chaque donnée, ajouter un oubli ;
- texte pseudonymisé et table de correspondance ;
- rétablissement des données dans la réponse de l'IA ;
- ligne de commande.

Exclus de la version Lite :
- l'anonymisation au sens du RGPD ;
- la détection par un modèle de langue, qu'il soit local ou distant ;
- la production d'un .docx pseudonymisé qui conserve la mise en forme ;
- les en-têtes, pieds de page, notes et commentaires d'un .docx ;
- les PDF et les images.

## Mode d'exécution (ADR-010, ADR-014)

L'outil est une application locale Python, en mode B, sans aucune IA distante. Il n'envoie rien : c'est l'avocat qui copie le texte pseudonymisé vers l'IA de son choix.

| Option | Avantages | Inconvénients |
|---|---|---|
| Règles en Python, bibliothèque standard seule (retenue) | aucune dépendance, règles lisibles et testables, résultat identique d'une exécution à l'autre | noms sans contexte mal détectés |
| Bibliothèque stella anonymize | détecteurs existants, plusieurs langues | dépendance compilée (Rust) à installer et à figer, couverture belge non vérifiée |
| Modèle de reconnaissance d'entités local (spaCy ou équivalent) | meilleure détection des noms | installation lourde (centaines de Mo), résultats variables, à qualifier sur F-IDENT-01 |

## Règles de détection

- **Identifiants à somme de contrôle** (numéro national, numéro d'entreprise, IBAN, carte de paiement) : retenus seulement si la somme est juste. Un numéro national à la somme fausse n'est retenu que si le texte l'annonce comme tel.
- **Personnes** : nom précédé d'une civilité, ou d'une mention de lien (« épouse de », « représentée par »). Sont aussi retenus le prénom suivi du nom en capitales et le nom en capitales suivi du prénom. Chaque nom trouvé, et son nom de famille, est ensuite recherché dans tout le texte.
- **Sociétés** : le nom accolé à une forme sociale (SRL, SA, ASBL, BV, NV…) ou qui suit la forme en toutes lettres.
- **Adresses** : un type de voie suivi d'un numéro, avec le code postal et la localité s'ils suivent. Sont aussi retenues les rues flamandes reconnues par leur suffixe (-straat, -laan, -steenweg…).
- **Autres catégories** : courriels, téléphones belges et internationaux, date annoncée comme date de naissance, plaque, références introduites par « R.G. » ou « N/Réf. ».
- **Termes de l'utilisateur** : ils passent avant toute autre règle. Une exclusion de l'utilisateur l'emporte sur tout.
- **Chevauchements** : la catégorie la plus prioritaire l'emporte, puis la détection la plus longue.

Une même donnée reçoit toujours le même marqueur. Deux personnes qui portent le même nom de famille gardent des marqueurs distincts. Un nom de famille seul, partagé par plusieurs personnes, reçoit son propre marqueur.

## Garde-fous

- L'enregistrement est impossible tant que la case « J'ai relu » n'est pas cochée. Toute modification décoche la case.
- L'avertissement sur la différence entre pseudonymisation et anonymisation reste affiché en permanence dans la fenêtre. La ligne de commande l'affiche aussi à chaque exécution.
- Aucun fichier existant n'est remplacé, ni le fichier d'origine, ni un texte, ni une table : un numéro est ajouté au nom.
- La table de correspondance porte un avertissement. Elle est enregistrée dans `Documents\Pseudonymisation`, hors du dossier de la pièce.
- Si le texte d'origine contient déjà des marqueurs de la forme `[PERSONNE_1]`, l'outil le signale.

## Trajet des données

Tout reste sur l'ordinateur : le texte d'origine, le texte pseudonymisé, la table et la réponse rétablie. Le code n'importe aucun module réseau, ce qu'un test statique vérifie. Le parcours complet est aussi testé avec les fonctions réseau neutralisées. Seule l'action de l'avocat fait sortir le texte pseudonymisé.

## Sécurité des entrées

- Limites : 50 Mo par fichier, 60 Mo pour la partie XML, 5 000 éléments, taux de compression de 1 000.
- Une déclaration DOCTYPE ou ENTITY est refusée (expat).
- Un fichier illisible produit un message d'erreur, jamais un texte vide présenté comme pseudonymisé.

## Jeu de test et mesure

Le jeu F-IDENT-01 v1.0 comprend deux parties. Le jeu de développement compte 102 entités. Le jeu de contrôle, rédigé à part, en compte 186.

Résultats de la version 0.1.0 sur le jeu de contrôle :
- rappel global de 63 % ;
- précision de 98 % ;
- 100 % pour les identifiants à somme de contrôle et les courriels ;
- 45 % pour les noms de personnes.

Le détail est dans `factory/jeux-de-test/F-IDENT-01/resultats/2026-10-31-P09-v0.1.0.md`. Les tests échouent si le rappel ou la précision descend sous les planchers de `attendu/P09.json`.

## Critères d'acceptation (fiche projet P09, §7)

- [x] Aucun appel réseau : test statique des imports, et parcours complet exécuté avec les fonctions réseau neutralisées. La fiche projet prévoyait une vérification dans les outils de développement du navigateur. L'outil n'étant pas une page web, ce sont ces tests qui la remplacent.
- [x] Taux de détection mesuré sur un jeu de test fictif belge et publié sur la fiche.
- [x] Avertissement sur les limites visible avant l'export.
