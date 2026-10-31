# Standard : code des outils

Complète `docs/principes-outils.md`.

## Structure

Voir la structure type d'un dossier outil dans `docs/principes-outils.md`, avec en plus :

```
outils/<slug>/
  SPEC.md            spécification (architecte)
  verifications/     rapports de test, sécurité, déontologie, UX
```

## Règles

- Un seul fichier de configuration par outil ; fournisseur et modèle y sont paramétrés.
- Les appels aux fournisseurs passent par le composant commun d'accès aux fournisseurs (voir `composants/README.md`) dès qu'il existe.
- Le coût estimé est calculé par le composant commun de coût.
- Aucune dépendance sans justification écrite dans le README de l'outil.
- Versions de dépendances figées.
- Données de test exclusivement fictives, rangées dans `factory/jeux-de-test/`.
- Messages de commit : `<ID> : <action>` (exemple : `P09 : ajout de la détection IBAN`).
- Tout code repris d'un projet tiers garde sa mention de licence et est listé dans `outils/<slug>/TIERS.md`.

## Vérification réelle

Les tests automatiques ne suffisent pas. Avant de demander le passage en vérification, le développeur exécute l'outil sur le jeu de test et joint la sortie obtenue.
