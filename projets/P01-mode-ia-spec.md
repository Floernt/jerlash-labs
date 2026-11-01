# P01 Inventaire d'un dossier - spécification du mode IA (version 0.2.0)

Date : 2026-11-01. Statut : validée par Florian le 2026-11-01 (parties et rattachement seulement, un envoi par dossier, seuils 14 et 13). Cadre : ADR-019 (connexion API en BYOK, sans clé l'outil ne fonctionne pas), ADR-020 (connecteur IA), ADR-021 (outil autonome), docs/deontologie-ia.md.

## 1. Ce que l'IA doit apporter

Sur le dossier de contrôle F-DOSSIER-01, les règles de la version 0.1.0 trouvent le type (14/16), le statut (14/16), la date (13/16) et le document qui fait foi (15/16). Elles sont faibles sur deux champs : les parties (11/16) et le rattachement d'une pièce au contrat qu'elle concerne (8/16).

Proposition : l'IA ne traite que ces deux champs. Le type, le statut, la date et le document qui fait foi restent calculés par les règles, qui sont reproductibles et gratuites.

## 2. Déroulement

1. Lecture du dossier et passage des règles, comme en 0.1.0, sans rien envoyer.
2. Sans clé API configurée, l'outil s'arrête ici avec un message qui renvoie au guide d'obtention d'une clé (ADR-019, point 2).
3. Construction d'un seul envoi pour tout le dossier : une pièce ne se rattache qu'en la comparant aux autres.
4. Pseudonymisation de cet envoi par la copie de P09 embarquée dans l'outil, avec une table unique : une même société garde le même marqueur ([ORGANISATION_1]) d'une pièce à l'autre.
5. Écran d'envoi du connecteur : informations sur le fournisseur, texte complet modifiable, case à cocher. Sans elle, rien ne part et aucun registre n'est produit.
6. Appel, lecture du JSON, rétablissement des données à partir de la table, qui n'a jamais quitté le poste.
7. Fusion avec le résultat des règles (section 4), puis registre .docx, .md et .json comme en 0.1.0.

## 3. Ce qui part, pièce par pièce

- un numéro (P1, P2…) à la place du nom du fichier, qui contient souvent le nom du client ;
- le type, le statut et la date trouvés par les règles ;
- l'intitulé, les 15 premières et les 15 dernières lignes (fonctions `debut` et `fin` existantes) ;
- pour un courriel : expéditeur, destinataires, objet et date, pseudonymisés.

Plafonds : 2 000 caractères par pièce et 80 000 pour l'envoi. Au-delà, les pièces sont tronquées et le registre le signale. Ne partent jamais : le corps complet des pièces, les fichiers non lus, les empreintes, les métadonnées du .docx (auteur, dernier modificateur).

Ordre de grandeur pour F-DOSSIER-01 (16 pièces) : environ 25 000 caractères, soit environ 6 000 jetons. Avec les tarifs relevés le 2026-10-31 pour claude-sonnet-5-5 (2 et 10 USD par million), le coût maximal d'une exécution est d'environ 0,05 USD, réponse comprise. À mesurer réellement.

## 4. Ce que le modèle renvoie et comment on le fusionne

Le modèle renvoie, pour chaque pièce : les parties (marqueurs ou noms tels qu'ils figurent dans le texte), le numéro de la pièce à laquelle elle se rattache (ou rien), et une justification d'une phrase.

Fusion :
- les règles ont trouvé une valeur et le modèle est d'accord : valeur retenue ;
- les règles n'ont rien trouvé : la valeur du modèle est retenue, marquée « proposée par le modèle » ;
- les règles et le modèle divergent : les deux valeurs figurent au registre, avec une alerte « à vérifier » ;
- un numéro de pièce inconnu, un marqueur absent de la table ou un JSON illisible : la proposition est écartée et signalée.

Le registre gagne une mention en tête (fournisseur, modèle, date de l'envoi, jetons et coût réels) et une marque dans les cellules « Parties » et « Se rapporte à » : « (modèle) » ou « (à vérifier) ». Mise en œuvre (0.2.0) : une marque dans la cellule plutôt qu'une colonne « source », pour garder les largeurs du tableau Word ; le JSON porte un champ `source` par pièce.

## 5. Garanties modifiées

- Le test statique « aucun module réseau » devient : seule la copie de `connecteur_ia` importe `urllib`.
- Le parcours complet est testé avec un faux fournisseur sur 127.0.0.1 et les autres accès réseau neutralisés : ce qui part est exactement le texte validé sur l'écran d'envoi, sans nom de fichier ni donnée de la table.
- Les garanties de lecture seule, de registre hors du dossier et de résistance aux .docx piégés restent inchangées.

## 6. Mesure

- Tests automatiques : faux fournisseur, réponses enregistrées, aucun coût.
- Mesure réelle, lancée à la main avec la clé de Florian, sur le dossier de développement puis sur le dossier de contrôle. Trois exécutions, parce que les réponses varient. On publie le plus mauvais des trois résultats, avec le modèle, la date et le coût.
- Seuil d'acceptation proposé sur le dossier de contrôle : au moins 14/16 pour les parties et 13/16 pour le rattachement, sans régression sur les autres champs.

## 7. Choix validés (2026-11-01)

1. L'IA se limite aux parties et au rattachement.
2. Un seul envoi pour tout le dossier.
3. Seuils sur le dossier de contrôle : 14/16 pour les parties, 13/16 pour le rattachement, sur le plus mauvais de trois exécutions.
