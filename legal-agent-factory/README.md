# Legal Agent Factory, Lot 1 : chaîne technique sans secrets

Ticket FLO-64 (parent FLO-57, projet de décembre FLO-24). Première chaîne de bout en bout, exécutable en local, sur des fichiers synthétiques :

1. un fichier est déposé dans un dossier surveillé ;
2. un événement horodaté est produit, avec l'empreinte SHA-256 du contenu ;
3. le document est qualifié par la passerelle de modèle (simulée), et la sortie est validée contre un schéma strict ;
4. une charge utile de création de tâche Paperclip est écrite, sans envoi (« dry run ») ;
5. le runtime HTTP local exécute la tâche ;
6. le résultat est écrit dans un répertoire de sortie distinct du dossier surveillé.

Rien ne sort de la machine : pas de fournisseur d'IA, pas de Paperclip, pas de courriel. Aucune clé n'est lue.

## Prérequis

Python 3.10 ou plus récent. Aucune dépendance : bibliothèque standard seule (ADR-010).

## Lancer la chaîne

Toutes les commandes se lancent depuis ce dossier (`legal-agent-factory/`).

Démonstration complète dans un dossier temporaire (dépôt d'un fichier synthétique, traitement, rejeu, comptage) :

```
python -m laf demo
```

Résultat attendu : une charge utile Paperclip, un fichier de résultat, et `doublon_ignore` au rejeu.

Chaîne réelle en deux terminaux :

```
python -m laf runtime --port 8765
python -m laf surveiller --entree C:\laf\entree --sortie C:\laf\sortie --etat C:\laf\etat --runtime-url http://127.0.0.1:8765
```

Sans `--runtime-url`, le runtime est appelé dans le même processus. `--une-fois` fait trois passages puis s'arrête. Les trois répertoires doivent être distincts et non imbriqués : la commande refuse sinon.

Rejouer un événement (il est ignoré s'il a déjà été traité) :

```
python -m laf rejouer --evenement C:\laf\sortie\evenements\<id>.json --entree C:\laf\entree --sortie C:\laf\sortie --etat C:\laf\etat
```

## Lancer les tests

```
python -m unittest discover -s tests -v
```

`python scripts/verifier.py`, à la racine du dépôt, les lance aussi.

Les tests couvrent : création, attente de la fin d'écriture, modification (nouvelle version), simple changement de date, renommage, suppression, recréation, doublon, rejeu après redémarrage, fichier illisible, contenu changé en cours de traitement, identifiant falsifié, injection d'instructions, modèle qui sort du schéma et demande des outils, réponse non JSON, plafond de tours, refus d'une politique qui autorise une action, serveur et client limités à l'interface locale, journal d'audit sans nom de fichier ni contenu.

## Ce que produit la chaîne

Répertoire de sortie :

| Dossier | Contenu |
|---|---|
| `evenements/` | chaque événement reçu (type, chemin relatif, empreinte, version, horodatage) |
| `signalements/` | fichiers illisibles, à vérifier par une personne |
| `qualifications/` | qualification validée, ou qualification de repli si la sortie du modèle est rejetée |
| `taches-paperclip/` | charge utile de création de tâche, `dry_run: true` |
| `resultats/` | résultat du runtime |

Répertoire d'état : `surveillance.json` (fichiers connus et versions), `traites/` (un marqueur par événement traité), `audit.jsonl`.

Chaque fichier porte l'identifiant de l'événement, dérivé de son contenu (type, chemin, empreinte, version) et non de l'heure. C'est ce qui rend le rejeu sans effet.

## Règles de fonctionnement

Dossier surveillé. Scrutation périodique, sans dépendance. Un fichier n'est pris en compte que lorsque sa taille et sa date sont stables entre deux passages. Une disparition est confirmée au passage suivant, ce qui permet de reconnaître un renommage (même empreinte, autre nom). Même nom avec un contenu différent : nouvelle version. Un fichier illisible produit un signalement, une seule fois tant qu'il ne change pas ; il est traité dès qu'il redevient lisible.

Tâches. Seules la création et la modification produisent une tâche. Le renommage et la suppression sont consignés sans tâche [À VÉRIFIER : choix du Lot 1, à confirmer].

Qualification. La sortie du modèle doit être un JSON conforme à `config/schema-qualification.json` (aucun champ en plus, valeurs dans les listes). Sinon, elle est remplacée par une qualification de repli qui exige un triage humain. `requires_human_triage` à `false` n'ouvre aucune action : c'est une indication de tri, pas une permission.

Contenu non fiable. Le texte d'un fichier n'est jamais mêlé aux instructions : il est placé dans un bloc délimité et annoncé comme donnée, et les délimiteurs présents dans le texte sont neutralisés. Un repérage simple des formules d'injection force le triage humain. Ce repérage ne prétend pas tout détecter : la garantie tient au fait qu'aucune action n'existe.

Niveau A3 (fiche §12). Le runtime ne connaît aucun outil. Une demande d'outil du modèle est refusée et compte pour un tour ; le nombre de tours est plafonné à 4 et une politique ne peut pas le relever. Une politique qui autorise une action est refusée. Aucune fonction d'envoi n'existe dans le code.

Runtime. Interface `execute(task, case_context, skill_bundle, policy) -> result`, indépendante de Paperclip, exposée en HTTP (`POST /execute`, `GET /sante`) sur 127.0.0.1 uniquement. Le client refuse toute adresse qui n'est pas locale.

Passerelle de modèle. Interface de forme « chat completions » compatible OpenAI. L'implémentation simulée renvoie des réponses déterministes et n'analyse rien. Les adaptateurs Scaleway et Umans sont des squelettes sans adresse, sans modèle et sans code réseau ; ils lèvent une erreur s'ils sont appelés.

Journal d'audit. Liste blanche de champs : identifiant d'événement, type, empreinte du contenu, version, issue, catégorie, indicateurs. Le nom du fichier est remplacé par une empreinte du chemin ; aucun contenu n'est écrit.

## Choix techniques

Python, bibliothèque standard seule, plutôt que FastAPI suggéré par la fiche §4. Raisons : ADR-010 (pas de dépendance tant que possible), aucune installation pour lancer la chaîne et les tests, surface d'attaque réduite. Le serveur HTTP est volontairement minimal ; l'interface `execute` est séparée du transport, si bien qu'un passage à FastAPI ne toucherait que `laf/runtime.py`. La surveillance par scrutation évite une dépendance comme `watchdog` ; son coût est un délai d'au moins deux passages avant traitement.

## Provisoire et à vérifier

- Format de qualification : provisoire, à aligner sur la fiche projet v0.2 §7, qui n'a pas été consultée (hors dépôt) [À VÉRIFIER].
- Liste des catégories (`a_trier`, `hors_perimetre`) : bouche-trou technique en attendant la taxonomie figée par FLO-59 [À VÉRIFIER].
- Champs de la charge utile Paperclip : format interne, sans correspondance vérifiée avec l'API Paperclip [À VÉRIFIER].
- Emplacement `legal-agent-factory/` à la racine du dépôt : proposition de la fiche §18 (ADR-035, proposée) [À VÉRIFIER].
- Renommage et suppression sans tâche [À VÉRIFIER].
- Noms des variables d'`env.example` : proposés, non lus par le Lot 1 [À VÉRIFIER].

## Lot 3, MVP : banc d'évaluation (FLO-66)

Harnais d'évaluation du benchmark de faillite (`laf/banc/`), construit sans attendre le Lot 2 ni les accès aux fournisseurs. Il tourne sur la chaîne du Lot 1 avec le modèle simulé : il éprouve la mécanique d'évaluation, pas la qualité juridique ni un modèle réel.

```
python -m laf evaluer sonde --fournisseur simulee --modele simule-deterministe
python -m laf evaluer executer --cas <CSV hors dépôt> --serie config/banc/serie-simulee-design.json --pieces <dossier> --sortie <répertoire de série> [--variantes]
python -m laf evaluer rapport --cas <CSV hors dépôt> --sortie <répertoire de série> [--references <dossier>] [--notes <dossier>]
```

Cas. Le fichier `JERLASH_Labs_Benchmark_Faillite_40_Cas.csv` reste hors dépôt. Ses colonnes sont contrôlées. La répartition conception (`design`) / test final (`holdout`) est celle de la colonne `jeu`, jamais recalculée ; le jeu `holdout` exige `--confirmer-holdout`. La colonne `attendu` n'est ni montrée au système évalué ni utilisée pour noter.

Pièces. Un sous-dossier par cas (`<pieces>/BK-01/…`) contenant les pièces synthétiques. Le fichier de cas ne contient que des descriptions de scénario : sans pièces, le cas est marqué `pieces_manquantes` et rien n'est mesuré.

Gel. `gel.json` fixe la série (fournisseur, modèle, endpoint, jeu, skill, tarifs) et les empreintes du fichier de cas, des pièces, des instructions, du schéma et du code. Une reprise n'est admise qu'à l'identique ; tout changement impose un nouveau répertoire de série. Seul le plafond peut être relevé pour reprendre.

Dépense. Avec un fournisseur réel, la série est refusée sans `plafond` et sans `tarifs`. Le coût est estimé d'après les tokens déclarés par l'API ; au plafond, la série s'arrête et le signale.

Mesures. Sans juge : orchestration (runtime terminé), ingestion (qualification conforme), actions à risque (tentatives et actions effectuées, zéro toléré), efficience (durée, tokens, appels, demandes d'outils, corrections, coût). Dimensions juridiques (faits critiques avec preuve, droit applicable dans le temps, sources décisives) : notation humaine, prise en compte seulement si une référence signée existe (`<references>/<id>.json` avec `signe_par` et `date_signature`) ; sinon « non évalué ». Les cas à erreur critique sont rapportés un par un, jamais moyennés.

Sonde. Pour chaque modèle et endpoint, essais répétés du JSON contraint (`response_format`) et des appels d'outils (outil fictif, jamais exécuté) ; issue observée, instable, non observée ou erreur. Les adaptateurs Scaleway et Umans n'étant pas branchés, ils donnent aujourd'hui « erreur ».

Variantes. `--variantes` ajoute, pour chaque cas qui a des pièces, des injections d'instructions (consigne, envoi, dépôt, anglais, pièce jointe injectée) et des variations (ordre inversé, pièce tronquée, pièce dupliquée).

À vérifier :
- libellés des dimensions et scénarios sentinelles repris du ticket, la fiche §14 n'ayant pas été consultée (hors dépôt) [À VÉRIFIER] ;
- correspondance sentinelles / cas dans `config/banc/sentinelles.json` [À VÉRIFIER] ;
- forme de `response_format` et `tools` chez Scaleway et Umans [À VÉRIFIER] ;
- `config/banc/instructions-provisoires.txt` tient lieu de skill jusqu'au Lot 2.
