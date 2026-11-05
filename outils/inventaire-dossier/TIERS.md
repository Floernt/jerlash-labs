# Code et contenus tiers

Aucun code tiers n'est repris dans cet outil.

L'idée d'un registre des pièces d'un dossier contractuel s'inspire de la skill matter-intake du dépôt zenzen-sol/legal-prompts (licence MIT, consultée le 2026-10-31). Ni son texte ni son code ne sont repris : les règles de classement et le registre sont propres à cet outil (ADR-008).

La lecture prudente des .docx reprend la démarche des outils Contrôle avant envoi et Pseudonymisation du même dépôt.

Dépendances d'exécution : aucune hors de la bibliothèque standard de Python (zipfile, xml.etree, email, tkinter, json, hashlib, urllib pour l'appel au fournisseur).

Composants du projet jerlash.labs copiés dans `src/` (ADR-021, même licence) : connecteur-ia et pseudonymisation. Voir `COMPOSANTS.md`.
