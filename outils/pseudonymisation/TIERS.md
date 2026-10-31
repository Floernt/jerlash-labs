# Code et contenus tiers

Aucun code tiers n'est repris dans cet outil.

La fiche projet P09 envisageait la bibliothèque stella anonymize (Apache-2.0). Elle n'est pas utilisée dans cette version : elle ajouterait une dépendance compilée (cœur en Rust), alors que l'outil est volontairement limité à la bibliothèque standard de Python, et sa couverture des identifiants belges restait à vérifier (ADR-014). Sa qualification sur le jeu F-IDENT-01 reste possible pour une version ultérieure.

La lecture prudente des .docx reprend la démarche de l'outil Contrôle avant envoi du même dépôt (limites de taille et de compression, refus des déclarations XML), en version réduite au corps du document.

Dépendances d'exécution : aucune hors de la bibliothèque standard de Python (re, unicodedata, zipfile, xml.etree, tkinter, json, hashlib).
