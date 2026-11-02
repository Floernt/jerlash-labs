---
titre: Contrôle avant envoi
slug: controle-avant-envoi
version: 0.1.0
mise_a_jour: 2026-10-31
statut: test
mode: local
fournisseurs: []
licence: MIT
code_source: outils/controle-avant-envoi
---

# Contrôle avant envoi

Avant d'envoyer un document Word, l'outil recherche ce qui ne devrait pas partir avec lui : commentaires, modifications suivies, texte masqué, propriétés révélant l'auteur ou le dossier, chemins de vos serveurs, noms d'autres clients. Il produit un rapport qui localise chaque élément et indique comment le corriger dans Word.

Ce qu'il ne fait pas : il ne modifie pas le document, ne vérifie ni le fond, ni l'orthographe, ni les renvois, et n'analyse pas l'intérieur des objets incorporés. Un rapport sans alerte ne dispense pas de relire.

## Cas d'usage

Vous renvoyez au confrère adverse la version révisée d'un contrat de prestation. Le fichier est parti d'un modèle du cabinet, une collaboratrice y a laissé un commentaire sur votre marge de négociation, et le champ « Auteur » contient encore le nom du stagiaire. L'outil liste ces éléments en quelques secondes, avec l'endroit où les corriger.

## Comment il fonctionne

Mode d'exécution : application locale (Python), parce que le document ne doit pas quitter votre ordinateur et qu'aucune IA n'est nécessaire pour ces contrôles.

Fournisseurs compatibles : aucun, l'outil n'utilise pas d'IA.

Éléments recherchés : commentaires ; modifications suivies (corps, en-têtes, pieds de page, notes) ; texte masqué, écrit en blanc ou en taille minuscule ; blancs à compléter (`[●]`, `[à compléter]`, `XXX`…) et texte surligné ; noms d'autres dossiers, à partir d'une liste que vous fournissez ; macros ; propriétés du document (auteur, société, titre, propriétés personnalisées) ; personnes citées comme auteurs ; champs qui affichent le nom ou le chemin du fichier ; liens vers des serveurs internes et modèle attaché ; objets incorporés ; variables de document ; métadonnées EXIF des photos ; notes de bas de page.

## Trajet des données

- Reste sur votre machine : le document, la liste de termes, le rapport.
- Est envoyé à un fournisseur d'IA : rien.
- Est envoyé à jerlash.labs : rien.

Le rapport contient des extraits du document. Il est enregistré dans `Documents\Controle avant envoi`, et non à côté du document, pour éviter de le joindre par erreur.

## Coût estimé

Gratuit : aucun appel à un service payant.

## Précautions

- Faites les corrections dans Word, sur la copie à envoyer, puis relancez le contrôle.
- Un document protégé par mot de passe ou au format .doc ne peut pas être contrôlé : l'outil le dit et ne conclut rien.
- La liste de termes contient des noms de clients : gardez-la hors des dossiers partagés.
- Vérifiez chaque sortie avant de vous y fier ; l'outil couvre des pièges courants, pas tous.

## Installation

1. Installez Python 3.10 ou plus récent depuis python.org, en cochant l'option qui ajoute Python au PATH.
2. Téléchargez l'archive de l'outil sur la fiche jerlash.labs et vérifiez son empreinte SHA-256 (procédure dans le guide « Utiliser un outil en local »).
3. Décompressez l'archive dans un dossier de votre choix.
4. Double-cliquez sur `Controle avant envoi.pyw`.
5. Cliquez sur « Choisir des documents… ».

## Versions

Voir CHANGELOG.md de l'outil.

## Signaler un problème

[À COMPLÉTER : adresse de contact du site]
