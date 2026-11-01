Met à jour la version anglaise du site à partir du français (ADR-023). Argument facultatif : un fichier ou un dossier de `site/content` pour limiter le travail ($ARGUMENTS).

Le français est la version maître. On ne corrige jamais l'anglais pour lui-même : si une traduction doit changer sans que le français change, demander à Florian.

1. Lancer `python scripts/traductions.py --etat $ARGUMENTS` et annoncer la liste à traiter.
2. Lire `docs/glossaire-traduction.md` et, pour le ton, `docs/charte-editoriale.md`.
3. Pour chaque page :
   - **à traduire** : créer `x.en.md` à côté de `x.md`. Mêmes clés de front matter, valeurs textuelles traduites (`title`, `description`, `resume`, blocs de l'accueil…), valeurs techniques recopiées telles quelles (`date`, `draft`, `version`, `sha256`, `telechargement`, `statut`, `mode`, `niveau`, booléens). Ajouter `slug:` en anglais (minuscules, tirets, sans article inutile) ; il ne changera plus ensuite. Ne pas recopier `aliases` ni le commentaire d'import du blog. `taches` : traduire les termes en suivant `ordre_taches` de `[languages.en.params]` dans `site/hugo.toml`.
   - **obsolète** : lancer `python scripts/traductions.py --diff <x.md>` et ne répercuter dans `x.en.md` que les passages modifiés, sans retraduire le reste.
   - **non marqué** : comparer le texte entier au français, corriger les écarts.
   - **brouillon divergent** : aligner `draft` sur le français.
   - **orphelin** : signaler à Florian, ne pas supprimer.
4. Règles de traduction : fidélité stricte, rien ajouté ni retiré, même structure de titres et de paragraphes. Garder la première personne et le ton du texte. Liens internes `/x/` inchangés (Hugo les résout). Marqueurs `[À …]` conservés tels quels. Citations de loi et noms d'institutions belges en langue d'origine (voir le glossaire). Guillemets anglais “ ” ; pas d'espace avant `: ; ! ?`. Anglais britannique.
5. Après chaque fichier : `python scripts/traductions.py --marquer <x.en.md>`.
6. Construire et vérifier : `python scripts/verifier.py --site-seul`. Contrôler `/en/` pour les pages traitées (titre, slug, lien FR/EN de l'en-tête).
7. Rendre compte : pages créées, mises à jour, points de traduction incertains à faire relire par Florian.
