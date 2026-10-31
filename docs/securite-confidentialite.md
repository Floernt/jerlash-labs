# Sécurité et confidentialité

## Ce qu'on protège

1. La clé API de l'utilisateur (elle permet de consommer à ses frais).
2. Les données de dossier que l'utilisateur fait passer dans un outil (couvertes par le secret professionnel, souvent des données personnelles).
3. L'intégrité du site (une page modifiée pourrait voler des clés).

## Risques principaux et réponses

Script malveillant ou compromis dans une page outil : il pourrait lire la clé saisie et les documents chargés. Réponse : aucune dépendance chargée depuis un CDN dans les pages outils, versions figées, Content-Security-Policy qui n'autorise les connexions sortantes que vers les domaines API des fournisseurs supportés, un sous-domaine par outil (ADR-005).

Clé mémorisée dans le navigateur : lisible par toute page du même domaine et par quiconque accède à l'ordinateur. Réponse : clé en mémoire par défaut, mémorisation en option avec avertissement, recommandation d'une clé dédiée plafonnée.

Clé dans un fichier `.env` d'un outil local : risque de partage accidentel du dossier. Réponse : `.env` ignoré par git, fichier `config.example` sans valeur, rappel dans le README.

Dépôt git public contenant un secret : réponse : vérification avant chaque commit, outil de détection de secrets en pré-commit `[À CHOISIR]`.

Compromission du compte d'hébergement ou du DNS : réponse : authentification à deux facteurs sur le registrar, l'hébergeur et GitHub.

## Données de dossier

- Le site et ses outils ne reçoivent jamais de données de dossier.
- Ce que l'utilisateur envoie à un fournisseur d'IA relève de son contrat avec ce fournisseur. Le guide "Ce que devient une donnée envoyée à un fournisseur d'IA" explique les points à vérifier dans ce contrat (conservation, entraînement, localisation, sous-traitants) sans affirmer à la place du fournisseur ce que dit sa politique.
- Les outils proposent, lorsque c'est pertinent, une étape de pseudonymisation locale avant envoi.

## Site

- HTTPS obligatoire (GitHub Pages, "Enforce HTTPS").
- GitHub Pages ne permet pas d'en-têtes HTTP personnalisés (ADR-003) : Content-Security-Policy et Referrer-Policy posées en balises <meta> ; aucun JavaScript, aucun formulaire sur le site.
- Pas de cookie, pas de traceur, pas de police externe.
- Journaux de l'hébergeur : durée de conservation à documenter dans la politique de confidentialité `[À VÉRIFIER auprès de l'hébergeur retenu]`.

## Signalement

Une adresse de contact pour signaler une faille, indiquée sur le site et dans un fichier `/.well-known/security.txt`.
