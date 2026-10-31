# Journal de bord

Une entrée par session de travail, la plus récente en haut. Format :

```
## AAAA-MM-JJ - Titre court
Fait :
Décisions : (renvoi vers ADR si applicable)
Problèmes / points ouverts :
Prochaine étape :
```

---

## 2026-10-31 - Préparation du projet : premiers arbitrages, rubrique, git
Fait : examen du dossier iavocat et des contenus du dossier parent ; fiche P05 découpée en P05 Lite / P05 avancé (priorité haute, dépendances du MVP séparées) ; rubrique "Automatiser une prestation" ajoutée au cahier des charges (v0.3) avec import des deux articles en Markdown dans contenus/automatiser-une-prestation/ ; backlog, registre, plan §13 et CLAUDE.md mis à jour ; dépôt git local initialisé, sans remote.
Décisions : ADR-011 (premier outil P05 Lite) et ADR-012 (rubrique "Automatiser une prestation"), acceptées par Florian.
Points ouverts : éditeur du site non tranché (Florian ou Avroy Avocats) ; ADR-002, 003, 005, 006, 010 toujours proposées ; articles importés à relire (charte, invitations à prendre contact en fin d'article) ; sort du tutoriel Cowork, des fiches "avocat entrepreneur" et du livre blanc.
Prochaine étape : choisir le mode d'exécution de P05 Lite et le générateur (ADR-002), puis créer F-DOCX-01 (Sprint 1).

## 2026-10-31 - Intégration du plan d'amélioration
Fait : ajout de PLAN_AMELIORATIONS.md à la racine ; 18 tâches A01 à A18 ajoutées au backlog ; ADR-010 créée au statut Proposée ; ADR-004 passée en révision et assertion "pas de responsabilité de traitement" retirée ; mode navigateur avec clé API suspendu dans docs/principes-outils.md et CLAUDE.md en attendant ADR-010.
Non fait volontairement : les autres modifications du plan (changement de priorités, parcours Factory, statuts, champs de fiche) demandent un arbitrage de Florian (plan §12 et §13).
Prochaine étape : Sprint 0 du plan (§10), en commençant par les décisions du §13.

## 2026-10-31 - Exploration zenzen-sol et création de la Factory
Fait : exploration de github.com/zenzen-sol (liste des dépôts, README des projets pertinents, en-têtes des skills legal-prompts) ; note de veille docs/veille/sol-irvine-zenzen-sol.md ; 16 fiches projet (P01 à P13, F01 à F03) ; mise en place de la Factory (pipeline, registre, standards, composants, jeux de test, rétrospectives, mémoire) ; 9 agents dont ops-factory ; commandes /factory, /factory-lancer, /factory-etape, /factory-revue, /factory-retro, /veille ; skill memoire-projet ; mise à jour de CLAUDE.md, du cahier des charges (v0.2) et du backlog.
Décisions : ADR-007, 008 et 009 proposées. AM-001 et AM-002 proposées.
Points ouverts : sites augustus.esq, wargame.esq et zenzen.io/sol non consultés ; objet de l'application Para inconnu (code privé) ; licence de laws-of-ux et des forks Docling non vérifiées ; format exact des agents et hooks Claude Code à vérifier.
Prochaine étape : /factory, puis valider ADR-007 et choisir le premier outil.

## 2026-10-31 - Cadrage initial
Fait : rédaction du cahier des charges v0.1, de CLAUDE.md, des principes outils, de la charte éditoriale, du document sécurité, du registre des décisions, du backlog, des gabarits et des commandes Claude Code.
Décisions : ADR-001 et ADR-004 acceptées (issues du brief). ADR-002, 003, 005 et 006 proposées.
Points ouverts : voir section 16 du cahier des charges. Le site de Sol Irvine cité comme modèle n'a pas été consulté.
Prochaine étape : valider le cahier des charges et trancher ADR-002, ADR-003 et ADR-005.
