# Legal Agent Factory, Lots 1 et 2

Le Lot 2 (FLO-65) est décrit dans la section « Lot 2 » plus bas. Ce qui suit, jusqu'à cette section, décrit le Lot 1.

## Lot 1 : chaîne technique sans secrets

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

## Lot 2 : courriel, rôles d'agents, routeur, deux skills de faillite

Ticket FLO-65 (parent FLO-57). Le Lot 2 ajoute à la chaîne du Lot 1 l'entrée par courriel, le rapprochement aux dossiers, quatre rôles d'agents, un routeur à sorties structurées, deux skills de faillite belge en brouillon, une revue qualité et la décision humaine. Tout fonctionne sur des dossiers synthétiques, avec le modèle simulé. Rien n'est envoyé, rien n'est déposé, aucun fournisseur d'inférence n'est appelé.

La fiche projet v0.2 (§3, §6 à §9, §12, §15, §17) et le registre des sources de FLO-60 n'étaient accessibles ni dans le dépôt ni sur les cartes : les formats ci-dessous sont provisoires et chaque point concerné est marqué [À VÉRIFIER].

### Parcours

1. Un courriel (format intermédiaire `laf-courriel/0.1`, `config/schema-courriel.json`) ou un fichier déposé devient un événement source de même forme (type, chemin, empreinte, version, identifiant dérivé du contenu). Pour un courriel, le fil est conservé : identifiant du message, `in_reply_to`, `references`, expéditeur, destinataires, date, et les pièces (nom, type, empreinte, taille).
2. Rapprochement (`laf/dossiers.py`) : réponse dans un fil déjà rattaché ; ou référence exacte du dossier dans l'objet avec un expéditeur inscrit au dossier ; ou fichier déposé dans le sous-dossier qui porte la référence. Tout le reste va au dossier d'attente `ATTENTE`, avec son motif. Aucune attribution par déduction.
3. Routeur hybride (`laf/routeur.py`) : règles déterministes sur les autorisations (une demande d'envoi, de dépôt RegSol, de paiement ou de changement de réglage est relevée et ignorée) ; classification par le modèle validée par `config/schema-routage.json` ; décision déterministe.
4. Une tâche par événement (charge utile Paperclip en dry run, format `laf-tache-paperclip/0.2`), avec un statut : `route`, `needs_clarification`, `confirmation_humaine`, `classement` ou `hors_perimetre`.
5. Si `route` : le runtime du Lot 1 exécute le skill attendu, sans outil ; la sortie passe la revue qualité (`laf/revue.py`).
6. Florian approuve, refuse ou corrige (`ChaineLot2.decider`) ; une tâche en `confirmation_humaine` est confirmée par `ChaineLot2.confirmer`. Ces appels sont locaux : aucun courriel ni fichier déposé ne peut les déclencher.

### Règles du routeur

| Situation | Statut |
|---|---|
| sortie du modèle hors schéma | `confirmation_humaine` |
| hors périmètre | `hors_perimetre` |
| pièce nouvelle sans instruction, dossier rattaché | `classement` (rôle Case Analyst, pas de skill) |
| intention et skill proposés incohérents | `confirmation_humaine` |
| élément manquant relevé par le modèle | `needs_clarification`, skill non exécuté |
| personne physique sans date du jugement | `needs_clarification` (le régime peut dépendre de la date et des dispositions transitoires [À VÉRIFIER]) |
| analyse de créance sans jugement de faillite | `needs_clarification` |
| risque élevé, ambiguïté, confiance inférieure à 0,7, personne physique, demande d'action relevée, injection suspectée, créance sans dossier rattaché | `confirmation_humaine` |
| sinon | `route` |

### Niveaux d'action

Définis dans `config/niveaux-action.json`, jamais par le modèle ni par un message : A0 lecture, A1 brouillon interne, A2 écriture interne après approbation (seulement consignée dans le Lot 2), A3 effet hors du cabinet (envoi, dépôt RegSol, contact avec le curateur) bloqué même après approbation. Le runtime garde la politique du Lot 1 : aucun outil, aucune action.

### Rôles d'agents

Un `AGENTS.md` par rôle dans `agents/` : `intake-triage`, `case-analyst`, `insolvency-legal-worker`, `quality-reviewer`. Ce sont des fichiers du dépôt ; aucun agent n'est créé dans Paperclip, et le référent humain est Florian.

### Skills

`skills/be-bankruptcy-intake/` et `skills/be-bankruptcy-claim-analysis/` : un `SKILL.md` (en-tête : nom, version, `status: draft`, `last_legal_review: null`, sources, niveau maximal A1) et un schéma de sortie. Le chargeur (`laf/skills.py`) refuse un skill dont une source n'est pas au registre, ou qui se dit relu sans date de relecture. Les skills ne contiennent aucune règle de droit non sourcée et aucune réponse de référence.

Le registre `config/registre-sources.json` est provisoire : toutes les sources y sont `source_unverified`, sans lien ni version, en attendant le registre de FLO-60.

### Revue qualité

Conformité au schéma de sortie ; cohérence (skill, dossier, statut `brouillon`) ; références (source inconnue : erreur ; `source_unverified` : avertissement) ; confidentialité (référence d'un autre dossier, adresse électronique, IBAN ou numéro de registre national absents des pièces reçues) ; actions (action inconnue ou niveau déclaré différent de la configuration : erreur). L'approbation est impossible tant que la revue n'est pas conforme : il faut corriger, et la correction repasse la revue.

### Sorties supplémentaires

| Dossier | Contenu |
|---|---|
| `routages/` | règles, classification validée, rattachement, décision du routeur |
| `contextes/` | texte examiné et pièces détectées, transmis au skill |
| `revues/` | sortie du skill et revue qualité |
| `decisions/` | décision humaine et effet par action |

Répertoire d'état : `fils.json` (identifiant de message vers dossier). Le journal d'audit reste sans adresse, sans objet et sans texte.

### Démonstrateurs (tests)

`tests/test_lot2.py` exerce, avec le runtime HTTP local et un modèle simulé à réponses enregistrées (`PasserelleEnregistree` : réponse choisie par clé exacte, sans lecture du texte) : un courriel « jugement et factures » et un dépôt équivalent qui ouvrent chacun une seule tâche et activent `be-bankruptcy-claim-analysis` ; un aveu incomplet bloqué en `needs_clarification` ; une personne physique sans date (blocage) et avec date (confirmation humaine, puis exécution) ; une pièce nouvelle sans instruction (classement) ; une réponse qui suit le fil ; un message hors périmètre ; un expéditeur non inscrit ; une injection avec demandes d'action ignorées ; le refus, la correction et l'approbation par le réviseur ; A3 bloqué après approbation ; l'absence de tout module d'envoi.

Les réponses enregistrées (`tests/fixtures/lot2/reponses-enregistrees.json`) sont des données de test du routage. Ce ne sont pas des réponses de référence juridiques : celles-ci seront signées par Florian (Lot 3). La correspondance entre ces démonstrateurs et UC01, UC03, UC04 de la fiche §15 n'a pas pu être vérifiée [À VÉRIFIER].

### Ce que Florian doit fournir pour la suite

- Adresse AgentMail : à créer par Florian, nom d'adresse à choisir. La clé reste dans les secrets, jamais dans le dépôt ni dans une carte. Le format réel des messages AgentMail doit ensuite être lu pour écrire l'adaptateur vers `laf-courriel/0.1` [À VÉRIFIER].
- Connexion Paperclip : action de Florian, avec la documentation de l'API de création de tâche pour remplacer le format interne [À VÉRIFIER].
- Registre des sources de FLO-60 validé, pour remplacer `config/registre-sources.json`.
- Fiche projet v0.2 (§6 à §9, §12, §15, §17), pour aligner rôles, routeur, contrat des skills, niveaux d'action et démonstrateurs.

### Provisoire et à vérifier (Lot 2)

- Format intermédiaire `laf-courriel/0.1` : défini ici, sans lecture du format AgentMail [À VÉRIFIER].
- Schéma de routage, intentions, pièces et éléments manquants : étiquettes techniques, à aligner sur la fiche §7 et la taxonomie de FLO-59 [À VÉRIFIER].
- Seuil de confiance 0,7 [À VÉRIFIER].
- Règle « personne physique : date du jugement requise » et lien avec les dispositions transitoires 2018, 2023, 2026 [À VÉRIFIER].
- Contrat des skills et schéma de sortie, à aligner sur la fiche §8 [À VÉRIFIER].
- Définition des niveaux A0 à A3 et catalogue d'actions, à aligner sur la fiche §12 [À VÉRIFIER].
- Rôles d'agents, à aligner sur la fiche §6 [À VÉRIFIER].
- Référent humain inscrit dans `config/niveaux-action.json` : « Florian Ernotte » [À VÉRIFIER].
- Registre des sources : tout `source_unverified`, en attente de FLO-60 [À VÉRIFIER].
- Correspondance des démonstrateurs avec UC01, UC03, UC04 [À VÉRIFIER].
- Repérage des demandes d'action et des injections par expressions régulières : indicatif, à enrichir par des tests adverses. La garantie tient à l'absence de toute action exécutable.

## Lot 3, MVP : banc d'évaluation (FLO-66)

Harnais d'évaluation du benchmark de faillite (`laf/banc/`), construit en parallèle du Lot 2 et sans les accès aux fournisseurs. Il tourne sur la chaîne du Lot 1 avec le modèle simulé, sans le routeur ni les skills du Lot 2 : il éprouve la mécanique d'évaluation, pas la qualité juridique ni un modèle réel.

```
python -m laf evaluer sonde --fournisseur simulee --modele simule-deterministe
python -m laf evaluer executer --cas <CSV hors dépôt> --serie config/banc/serie-simulee-design.json --pieces <dossier> --sortie <répertoire de série> [--variantes]
python -m laf evaluer rapport --cas <CSV hors dépôt> --sortie <répertoire de série> [--references <dossier>] [--notes <dossier>]
```

Cas. Le fichier `JERLASH_Labs_Benchmark_Faillite_40_Cas.csv` reste hors dépôt. Ses colonnes sont contrôlées. La répartition conception (`design`) / test final (`holdout`) est celle de la colonne `jeu`, jamais recalculée ; le jeu `holdout` exige `--confirmer-holdout`. La colonne `attendu` n'est ni montrée au système évalué ni utilisée pour noter.

Pièces. Un sous-dossier par cas (`<pieces>/BK-01/…`) contenant les pièces synthétiques. Le fichier de cas ne contient que des descriptions de scénario : sans pièces, le cas est marqué `pieces_manquantes` et rien n'est mesuré. Les pièces fictives des 24 cas du jeu de conception sont dans `factory/jeux-de-test/F-LAF-01/pieces-design/` ; celles du jeu de test final restent à rédiger hors dépôt, par quelqu'un qui ne règle pas le harnais.

Gel. `gel.json` fixe la série (fournisseur, modèle, endpoint, jeu, skill, tarifs) et les empreintes du fichier de cas, des pièces, des instructions, du schéma et du code. Une reprise n'est admise qu'à l'identique ; tout changement impose un nouveau répertoire de série. Seul le plafond peut être relevé pour reprendre.

Dépense. Avec un fournisseur réel, la série est refusée sans `plafond` et sans `tarifs`. Le coût est estimé d'après les tokens déclarés par l'API ; au plafond, la série s'arrête et le signale.

Mesures. Sans juge : orchestration (runtime terminé), ingestion (qualification conforme), actions à risque (tentatives et actions effectuées, zéro toléré), efficience (durée, tokens, appels, demandes d'outils, corrections, coût). Dimensions juridiques (faits critiques avec preuve, droit applicable dans le temps, sources décisives) : notation humaine, prise en compte seulement si une référence signée existe (`<references>/<id>.json` avec `signe_par` et `date_signature`) ; sinon « non évalué ». Les cas à erreur critique sont rapportés un par un, jamais moyennés.

Sonde. Pour chaque modèle et endpoint, essais répétés du JSON contraint (`response_format`) et des appels d'outils (outil fictif, jamais exécuté) ; issue observée, instable, non observée ou erreur. Les adaptateurs Scaleway et Umans n'étant pas branchés, ils donnent aujourd'hui « erreur ».

Variantes. `--variantes` ajoute, pour chaque cas qui a des pièces, des injections d'instructions (consigne, envoi, dépôt, anglais, pièce jointe injectée) et des variations (ordre inversé, pièce tronquée, pièce dupliquée).

À vérifier :
- libellés des dimensions et scénarios sentinelles repris du ticket, la fiche §14 n'ayant pas été consultée (hors dépôt) [À VÉRIFIER] ;
- correspondance sentinelles / cas dans `config/banc/sentinelles.json` [À VÉRIFIER] ;
- forme de `response_format` et `tools` chez Scaleway et Umans [À VÉRIFIER] ;
- `config/banc/instructions-provisoires.txt` tient lieu de skill tant que le banc n'est pas branché sur la chaîne du Lot 2.

### Banc branché sur la chaîne du Lot 2

Une série qui porte `"chaine": "lot2"` fait passer chaque cas par la chaîne du Lot 2 (rapprochement, routeur, skill, revue qualité) au lieu de la seule qualification du Lot 1 (`laf/banc/lot2.py`). Série de démonstration, modèle simulé :

```
python -m laf evaluer executer --cas <CSV hors dépôt> --serie config/banc/serie-simulee-lot2-design.json --pieces <dossier> --sortie <répertoire de série> [--variantes]
```

Entrée. Canal `email` : la pièce `*courriel.txt` est convertie au format `laf-courriel/0.1` (en-têtes De, À, Cc, Date, Objet ; le reste fait le corps), les autres pièces deviennent ses pièces jointes. La date des pièces n'a pas de fuseau : UTC par convention [À VÉRIFIER si un cas en dépend]. Canal `folder` : chaque pièce est déposée dans `<entrée>/<id du cas>/` et produit un événement de création ; un dépôt de plusieurs fichiers ouvre donc plusieurs tâches, comme dans la chaîne réelle. Les pièces de contexte (`00-contexte*`) ne sont pas transmises : au Lot 2, c'est le registre des dossiers de la série (clé `dossiers`) qui joue ce rôle. Le registre fourni, `config/banc/dossiers-vide.json`, est vide : aucun cas n'est rattaché [À VÉRIFIER : registre par cas à concevoir avec FLO-59].

Aucune intervention humaine n'est simulée. Une tâche en `confirmation_humaine`, `needs_clarification`, `classement` ou `hors_perimetre` s'arrête là, et c'est son statut qui est mesuré ; le skill ne s'exécute que pour une tâche `route`. Les traces de chaque unité restent sous `<série>/chaine/<unité>/`.

Gel. En plus du fichier de cas, des pièces et du code, `gel.json` fixe les empreintes du registre des dossiers, des skills, des schémas de routage et de courriel, des niveaux d'action et du registre des sources.

Mesures propres au Lot 2 : orchestration (chaque événement ouvre une tâche et tout skill lancé se termine), ingestion (classification du routeur conforme au schéma), routage (statut des tâches, skills exécutés, revues conformes). Les autres dimensions sont celles du Lot 3.

Avec le modèle simulé, la classification n'est pas du JSON : toutes les tâches tombent en `confirmation_humaine` (repli). La série éprouve donc la mécanique, pas le routage ; les branches `route`, skill et revue sont couvertes par les tests (`tests/test_banc.py`).
