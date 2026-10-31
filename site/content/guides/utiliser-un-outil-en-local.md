---
title: "Utiliser un outil en local"
description: "Installer Python, télécharger un outil d'iavocat.be, vérifier son empreinte SHA-256 et le lancer sur Windows."
niveau: "debutant"
derniere_verification: 2026-10-31
---

À la fin de ce guide, vous aurez installé un outil d'iavocat.be sur votre ordinateur Windows, vérifié que le fichier téléchargé est bien celui qui a été publié, et lancé l'outil.

## Ce que veut dire « en local »

Un outil local s'exécute sur votre ordinateur. Les documents que vous lui donnez sont lus sur votre machine et n'en sortent pas, sauf si la fiche de l'outil indique qu'il fait appel à un fournisseur d'IA. Dans ce cas, la fiche décrit précisément ce qui part et vers qui.

Les outils d'iavocat.be sont écrits en Python, un langage gratuit et très répandu. Il faut l'installer une fois ; ensuite, chaque outil se lance par un double-clic.

## Prérequis

- Un ordinateur sous Windows 10 ou 11, avec le droit d'installer un programme (sinon, adressez-vous à votre prestataire informatique en lui transmettant ce guide).
- Une dizaine de minutes la première fois.

## Étapes

### Installer Python

1. Ouvrez [python.org/downloads](https://www.python.org/downloads/) et téléchargez la version proposée pour Windows. Toute version 3.10 ou plus récente convient.
2. Lancez le programme d'installation et suivez ses écrans. S'il propose une option pour ajouter Python au PATH, cochez-la. [À VÉRIFIER sur un poste Windows vierge : libellés exacts de l'installateur actuel]
3. Vérifiez l'installation : ouvrez le menu Démarrer, tapez `PowerShell`, ouvrez-le et tapez `python --version` puis Entrée. Une ligne du type `Python 3.12.10` doit s'afficher.

### Télécharger l'outil et vérifier son empreinte

4. Sur la fiche de l'outil, cliquez sur « Télécharger ». Le fichier arrive dans votre dossier `Téléchargements`.
5. Dans PowerShell, tapez la commande suivante, en adaptant le nom du fichier :

   ```
   Get-FileHash "$HOME\Downloads\controle-avant-envoi-0.1.0.zip" -Algorithm SHA256
   ```

6. Comparez la suite de caractères affichée sous `Hash` avec l'empreinte SHA-256 indiquée sur la fiche de l'outil. Les majuscules ne comptent pas. Si les deux diffèrent, n'utilisez pas le fichier : supprimez-le et signalez-le.

L'empreinte est une sorte de signature numérique du fichier : la moindre modification du fichier donne une empreinte complètement différente. Cette vérification garantit que vous avez exactement le fichier publié, et non une version altérée en chemin.

### Décompresser et lancer

7. Faites un clic droit sur le fichier `.zip`, choisissez « Extraire tout… », puis choisissez un dossier stable, par exemple `Documents\Outils`.
8. Ouvrez le dossier extrait et double-cliquez sur le fichier qui se termine par `.pyw` (par exemple `Controle avant envoi.pyw`). La fenêtre de l'outil s'ouvre.
9. Si Windows vous demande avec quel programme ouvrir le fichier, choisissez « Python ». Si le fichier s'ouvre dans un éditeur de texte, faites un clic droit, « Ouvrir avec », puis « Python ».

### Mettre à jour

10. Quand une nouvelle version est publiée (voir [Nouveautés](/nouveautes/)), téléchargez-la, vérifiez son empreinte et remplacez l'ancien dossier par le nouveau.

## Points d'attention

- Ne téléchargez un outil que depuis sa fiche sur iavocat.be, et vérifiez toujours l'empreinte.
- Rangez l'outil hors de vos dossiers clients et hors des dossiers synchronisés avec des tiers.
- Un outil local qui fait appel à une IA demande votre clé API : la fiche de l'outil et le guide dédié expliquent comment la protéger. L'outil Contrôle avant envoi n'en a pas besoin.
- Sur Mac ou Linux, les outils fonctionnent aussi : installez Python 3.10 ou plus récent, puis lancez `python3 "Controle avant envoi.pyw"` depuis le dossier de l'outil.

## Sources

- Python Software Foundation, page de téléchargement : [python.org/downloads](https://www.python.org/downloads/), consultée le 31 octobre 2026.
- Microsoft, documentation de la commande `Get-FileHash` : [learn.microsoft.com](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash), consultée le 31 octobre 2026.
