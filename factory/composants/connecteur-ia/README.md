# Composant connecteur-ia

Appel d'un modèle de langue avec la clé de l'avocat (ADR-019), par un seul format d'appel, Chat Completions (ADR-020). Python 3.10+, bibliothèque standard seule.

## Ce que fait le composant

- `charger_configuration(chemin_ou_dict)` : lit la configuration de l'outil, complétée par un préréglage (`openai`, `anthropic`, `mistral`, `gemini`, `local`, dans `src/connecteur_ia/prereglages.json`). Refuse une clé écrite dans la configuration, une adresse distante en `http`, un champ inconnu.
- `lire_cle(config, dossier_env)` : lit la clé dans la variable d'environnement nommée par `variable_cle`, sinon dans le fichier `.env` de l'outil. Sans clé, erreur explicite : l'outil ne fonctionne pas (ADR-019, point 2). Le préréglage `local` n'exige pas de clé.
- `estimer` et `resume_envoi` : taille, jetons (estimation grossière, 4 caractères par jeton), coût maximal, et les déclarations du fournisseur à afficher avant l'envoi.
- `interface.confirmer_envoi(parent, config, consigne, texte)` : écran d'envoi tkinter. Il affiche les informations, laisse l'avocat corriger le texte, et n'active « Envoyer » qu'après la case à cocher. Renvoie le texte relu, ou `None`.
- `appeler(config, cle, consigne, texte)` : envoie `model`, `messages` et `max_tokens`, rien d'autre. Renvoie le texte, les jetons consommés et le coût calculé. Les erreurs sont traduites en français et ne contiennent jamais la clé.
- `extraire_json(texte)` : retrouve le JSON demandé dans la consigne, même entouré de texte ; erreur explicite sinon.

## Ce qu'il ne fait pas

- Il ne pseudonymise pas. L'outil appelle P09 avant l'écran d'envoi.
- Il ne vérifie pas les déclarations du fournisseur (conservation, ZDR, lieu de traitement) : il les affiche, avec leur source et leur date.
- Il n'utilise ni `temperature`, ni `response_format`, ni outils, ni fonctions avec état : la couche de compatibilité d'Anthropic refuse certains de ces réglages, et les fonctions avec état sortent de l'absence de conservation (docs/fournisseurs-ia.md, section 5.2).

## Ordre d'appel dans un outil

1. `config = charger_configuration(...)` puis `cle = lire_cle(config, dossier_outil)` : sans clé, l'outil s'arrête avec le message d'erreur.
2. Préparation locale de l'extrait, puis pseudonymisation par P09.
3. `texte = confirmer_envoi(...)` : si `None`, rien ne part.
4. `reponse = appeler(config, cle, consigne, texte)`, puis `extraire_json(reponse.texte)`.
5. Chaque élément venant du modèle est marqué comme tel dans le rapport.

## Configuration d'un outil

Voir `config.example.json`. La configuration réelle (`config.json`) et le fichier `.env` ne sont jamais versionnés.

## Tests

```
cd factory/composants/connecteur-ia
python -m unittest discover -s tests -v
```

Les tests tournent contre un faux fournisseur sur 127.0.0.1 ; aucun test n'appelle un vrai fournisseur.

## Intégration dans les outils

Chaque outil est autonome et téléchargeable seul (ADR-021). Il embarque une copie de ce composant dans son `src/`, déclarée dans son `COMPOSANTS.md` et tenue à jour par `python scripts/synchroniser_composants.py`. On ne modifie jamais la copie : on modifie ce dossier, puis on synchronise.
