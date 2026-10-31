# Spécification - Inventaire d'un dossier (P01, mode local)

Version 0.1.0 - 2026-10-31 - Parcours Factory : renforcé (pièces de dossier, ADR-007)

## Besoin

Reprendre un dossier contractuel, qu'il s'agisse d'un nouveau client, d'un collaborateur absent ou d'une négociation qui repart, impose de reconstituer :
- quelles pièces existent ;
- lesquelles sont signées ;
- quelle version fait foi ;
- ce qui ne devrait pas se trouver là.

## Périmètre de la version 0.1.0

Inclus :
- lecture des .docx, .eml, .txt et .md ;
- inventaire de tous les autres fichiers avec leur empreinte ;
- classement par règles : type, statut, date, parties, rattachement, document qui fait foi ;
- alertes ;
- registre .docx, .md et .json ;
- fenêtre et ligne de commande.

Exclus :
- le mode avec IA (ADR-015, proposée) ;
- la lecture des PDF, qui demande une dépendance, et la reconnaissance de caractères (P11) ;
- les courriels .msg ;
- l'analyse juridique des clauses ;
- les dossiers contentieux.

## Mode d'exécution

L'outil est une application locale Python, en mode B d'ADR-010, sans IA distante. Le mode local est utile en lui-même :
- le registre et les empreintes ne dépendent d'aucun fournisseur ;
- les alertes de confidentialité (pièce d'un autre client) se calculent sans rien envoyer ;
- il sert de référence pour mesurer ce qu'un mode avec IA apporterait.

## Règles

- **Type** : déduit de l'intitulé, c'est-à-dire des deux premières lignes qui ne sont pas des puces, de l'extension (.eml) et du nom du fichier (« modèle », « précédent », « notes »). Un document qui contient au moins deux champs à compléter (`[●]`, `[NOM]`) est un modèle.
- **Statut** : « projet » si un indice de projet est présent (mention en tête, blancs de signature, « ne pas signer », « soumis à la signature », commentaires de négociation, nom du fichier) ; ces indices l'emportent sur un nom de fichier « signé ». Sinon « signé » si les dernières lignes portent « (signé) », hors texte masqué, ou si le nom du fichier dit « signé » (participe, sans négation). Sinon « à vérifier », avec une alerte.
- **Date** : dans cet ordre, la date du nom du fichier (AAAA-MM-JJ), « Fait à …, le … », lieu et date d'un courrier, « version du … », l'en-tête du courriel, la première ligne. Aucune date n'est inventée.
- **Parties** : les sociétés suivies de leur forme sociale. Pour un courriel, les sociétés reconnues par le domaine des adresses quand elles figurent ailleurs dans le dossier.
- **Rattachement** :
  - la référence à « contrat … du <date> » ;
  - la mention d'un avenant numéroté, pour les courriels et les courriers ;
  - les mêmes parties qu'un contrat signé, pour un projet antérieur ou pour des conditions générales que ce contrat mentionne.
- **Fait foi** : contrat, avenant ou courrier signé d'après son texte. Signé d'après le seul nom du fichier : « à vérifier », avec une alerte.
- **Alertes** :
  - pièce non lue ;
  - acte non signé ;
  - aucune partie commune avec le reste du dossier ;
  - précédent ;
  - statut à vérifier ;
  - doublon (même empreinte) ;
  - envoi recommandé sans preuve de dépôt au dossier ;
  - fichiers techniques ignorés.

## Garanties

- Les pièces sont lues en lecture seule ; un test vérifie que leurs octets et leurs dates sont inchangés.
- Le registre est refusé à l'intérieur du dossier inventorié ; aucun fichier existant n'est remplacé.
- Le code n'importe aucun module réseau, ce qu'un test statique vérifie, et le parcours complet est testé avec les fonctions réseau neutralisées.
- Les .docx piégés (entités XML, bombes de décompression, faux fichiers) sont signalés « non lus » sans interrompre l'inventaire.
- Limites : 50 Mo par pièce, 2 000 pièces par dossier.

## Mesure (F-DOSSIER-01 v1.0)

| Champ | Dossier de développement (12 pièces) | Dossier de contrôle (16 pièces) |
|---|---|---|
| Type | 12 | 14 |
| Statut | 12 | 14 |
| Date | 12 | 13 |
| Parties | 12 | 11 |
| Rattachement | 12 | 8 |
| Fait foi | 12 | 15 |

Le dossier de contrôle a été rédigé par un agent qui n'avait accès ni au code ni au dossier de développement. Les planchers de non-régression sont dans `attendu/P01-planchers.json`.

## Critères d'acceptation (fiche projet P01, §7)

- [~] Chaque document classé et statut exact sur F-DOSSIER-01 : atteint sur le dossier de développement ; 14 types et 14 statuts exacts sur 16 dans le dossier de contrôle.
- [x] Aucun original modifié : vérifié par test (octets et dates).
- [x] Le registre .docx s'ouvre dans Word sans erreur : vérifié le 2026-10-31 par Word, avec un tableau de 13 lignes en mise en page paysage.
- [ ] Coût d'une exécution mesuré : sans objet en mode local (gratuit) ; à mesurer pour le mode avec IA.
