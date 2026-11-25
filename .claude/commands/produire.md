Produire un livrable à partir du dossier otf (ADR-028). Sujet ou identifiant : $ARGUMENTS

1. Lis CLAUDE.md, la fiche du projet dans `projets/` si elle existe, les tâches correspondantes de `BACKLOG.md` et les lignes de `../otf/INDEX.md` rattachées au sujet. Liste à Florian les fichiers otf que tu comptes utiliser avant de commencer ; si le rattachement est ambigu, demande.
2. Construis le livrable à l'endroit prévu par le dépôt (`site/content/...`, `projets/`, `docs/`), selon `docs/politique-publication.md` et `docs/charte-editoriale.md`. Une page du site est toujours en `draft: true`. Nom de fichier (slug) et `description` suivent la section « Référencement » de `docs/charte-editoriale.md` : propose-les à Florian avec le livrable. Ce qui n'est pas vérifié reste en `[À VÉRIFIER]`. Un texte publié sous le nom de Florian attend sa lecture : signale les prises de position qu'il doit faire siennes.
3. À la fin : coche ou mets à jour les tâches de `BACKLOG.md` ; déplace les fichiers otf utilisés vers `../otf/traite/<ID>/` (crée le dossier) ; retire leurs lignes de `../otf/INDEX.md` ; indique le nouveau chemin dans la fiche projet (champ `source`) ou dans la tâche du backlog.
4. Lance `python scripts/verifier.py`.

Ne publie jamais : aucun `draft: false`, aucun push, sans instruction explicite de Florian.
