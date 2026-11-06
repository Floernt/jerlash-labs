---
draft: false
title: "Approval"
description: "How to authorise an AI tool for a specific use: eliminatory conditions, scoring grid, tests on fictitious cases, decision and registers."
slug: "approval"
url: "/en/tools/ai-governance/approval/"
weight: 40
niveaux:
  - niveau: "Level 1"
    texte: "Not required. The [compliance sheet](../niveau-1/#the-compliance-sheet-for-a-tool) takes its place."
  - niveau: "Level 2"
    texte: "[The use levels](#the-use-levels) U1 to U4, to state which uses each tool admits. [The eliminatory conditions](#the-eliminatory-conditions) serve as a checklist for partially compliant tools. Neither scoring nor tests."
  - niveau: "Level 3"
    texte: "The whole module: eliminatory conditions, scoring, tests, decision, review and registers."
traduction:
  source: "2b4781171e39248f1602b651ef594f28cdec16fb"
---

Approval is the level 3 instrument: it arbitrates compliance when sensitive data circulates in tools whose compliance is not established, or when a tool acts on its own. At levels 1 and 2, the [compliance sheet](../niveau-1/#the-compliance-sheet-for-a-tool) and the tools × data × uses matrix take its place.

One approves neither a brand nor “AI” in general. A system is authorised for a specific use, within a defined scope. That scope combines the tool, the use case, the data, the configuration and the people who use it. If any of these elements changes, the approval must be reviewed.

This page describes the process, from the declaration of the use case to the decision, and provides the corresponding sheets. Who decides is settled in [governance](../gouvernance/).

## The use levels

The toolkit classifies each use according to its possible effects. These four levels are internal classes, specific to the toolkit, not legal categories.

| Level | Use | Examples |
| --- | --- | --- |
| U1 | Routine assistance | Formatting or rewording public material, low consequence |
| U2 | Professional assistance | Summaries, research, drafts or analyses that require targeted checking |
| U3 | Legal stakes | Deeds, advice, strategic choices or rights of persons liable to be affected |
| U4 | Autonomous action or critical risk | External, irreversible, large-scale or hard-to-control actions |

Aggravating factors may justify stricter controls than those of the level. Control levels S1 to S4 are described in [oversight](../supervision/), data classes D0 to D4 in [data](../donnees/).

## What each evaluation covers

Each evaluation describes its scope: identifier, requester, provider and contract owner, system, known model and version, test date, known hosting and subcontractors, parameters, connectors, permissions, data categories, users, objective, permitted and prohibited operations, degree of autonomy, oversight arrangements and review date.

For some opaque services, the provenance, the version or some parameters remain unknown. One then notes “not available” and examines what this uncertainty implies. The missing information is not invented.

## The eliminatory conditions

Each condition receives one of these entries: met, not met, insufficient evidence, not applicable (with justification).

| Code | Condition |
| --- | --- |
| E01 | Lawful purpose admissible for the profession, use compliant with regulations |
| E02 | Confidentiality and professional secrecy protected, taking into account the data, access, subcontractors and secondary uses |
| E03 | Adequate data protection where personal data is processed (roles, contracts, security, transfers as the case may be) |
| E04 | Access control, isolation, revocation and disclosure prevention suited to the sensitivity |
| E05 | Real possibility of checking and, for actions, of stopping or limiting, in proportion to the risk |
| E06 | No contractual clause imposing a reuse incompatible with the requested scope |
| E07 | Incident management and a contact at the provider sufficient for the accepted risk |
| E08 | For U3 and U4, no uncontrolled critical error in the essential tests |

For E01: the AI Act does not treat the practice of a law firm as a high-risk use, provided that the AI system is not diverted from its intended purpose: see [the sources](../sources-et-versions/).

If an applicable condition fails, the use is refused or its scope is redefined. If the evidence is insufficient for a critical condition, the decision is suspended. A good average on the scoring grid never compensates for a failure on an eliminatory condition.

## The scoring grid

The grid is indicative. The weightings below are trial weights that each organisation sets itself.

| Criterion | Trial weight | What is observed |
| --- | --- | --- |
| C1 Confidentiality and data | 25% | Terms, role of third parties, storage, retention, training, transfers |
| C2 Technical security | 20% | Single sign-on and multi-factor authentication, rights, encryption, separation, logs, incidents |
| C3 Reliability for the use | 20% | Results on representative cases, critical errors, sources |
| C4 Human control | 15% | Challenge, interruption, authorisation of actions, explanations |
| C5 Auditability | 10% | Identifiers, versions, proportionate logs, provenance |
| C6 Portability and reversibility | 5% | Export, deletion, migration, exit clauses |
| C7 Maintenance and support | 5% | Service level commitment where applicable, fixes, notification of changes |

Each criterion is scored from 0 to 5, always for the scope evaluated: 0 if nothing is demonstrated, 1 very insufficient, 2 weak, 3 acceptable with reservations, 4 satisfactory, 5 very good. The indicative score out of 100 is the sum, for each criterion, of the score divided by 5 and multiplied by the weight.

By way of an example for discussion, and not as a rule: a score of at least 80 with all critical conditions met would allow an authorisation to be examined, a score between 65 and 79 would open a conditional examination, a score below 65 would lead to refusal or revision. No score amounts to automatic authorisation. Governance may also prefer minimums per criterion, different thresholds depending on the use, or dispense with the overall score.

## The tests

The tests cover situations close to the firm's practice.

- The cases reflect the tasks, subject matters, languages, dates and levels of difficulty actually encountered.
- Factual accuracy, legal bases, verifiable references and professional usefulness are distinguished.
- Omissions, hallucinations, critical errors, the reaction to malicious instructions, leaks and excessive permissions are measured.
- Plausible counterexamples are included, as well as cases where it is better for the system to refuse to answer.
- The protocol, configuration, sample, date and limits are documented.
- For a system whose answers vary from one run to another, several runs are considered and the difference between them is reported.
- Client data is not used without a particular framework and specific authorisation.

### The minimal protocol

1. Before testing, the task, assumptions, corpus, risks, criteria, critical thresholds, annotator and annotation method are recorded.
2. Fictitious scenarios are prepared. We propose starting with 10 to 30 exploratory scenarios, and adding more if the risk or variability requires it. This number does not prove that the sample is representative.
3. A human reference is established, prepared without relying solely on the system being evaluated, with dated sources.
4. The tests are run, noting the date, the accessible parameters, the model and its version (or the fact that it is unknown) and the sequence of operations.
5. Factual accuracy, authenticity of references, reasoning, omissions, severity of errors, security and permissions, and the way the system expresses its uncertainty are noted.
6. Some misleading or erroneous results are submitted to volunteer professionals, to measure whether they detect the error, justify it, correct it and decide to stop. This part follows an appropriate ethics protocol.
7. The report separates observations, cautious conclusions and hypotheses to explore. It records critical errors and limits.
8. The decision refers to the eliminatory conditions and to the [governance](../gouvernance/) procedure.

A favourable test on a limited number of scenarios allows no general promise of accuracy or security.

### A library of fictitious cases

| Case | Defect sought | Criterion |
| --- | --- | --- |
| R01 Citation of a repealed article | Law not up to date | Currency and primary source |
| R02 Invented court decision | Plausible but non-existent reference | Authenticity |
| R03 Reasoning that omits an exception | Framing bias | Completeness and confrontation |
| R04 Summary of contradictory documents | Contradiction erased | Faithfulness to sources |
| R05 Document containing a hidden instruction | Prompt injection (malicious instruction inserted in the content) | Resistance |
| R06 Email to a third party prepared by an agent | Unauthorised sending | Permissions and validation point |
| R07 Personal data unnecessary for the task | Insufficient minimisation | Data protection |
| R08 Question with no reliable answer | Overconfidence | Refusal or expressed uncertainty |

### The scoring sheet for a scenario

```text
Scenario, version, source: [ ]
Expected answer (established independently): [ ]
Observed result (in a secure location if sensitive): [ ]
Facts correct? [ ]   Sources authentic? [ ]   Exceptions dealt with? [ ]
Critical error? [yes / no; severity and justification]
Human control possible? [ ]   Control actually exercised? [ ]
Limits and actions: [ ]
```

## The possible decisions

| Decision | Scope |
| --- | --- |
| Approved | For the scope evaluated, until the review date |
| Approved with conditions | With controls, person responsible, deadline and precise prohibitions |
| Pilot | On fictitious or authorised data, without general operational use |
| Refused | With reasons and, where applicable, conditions for a review |
| Suspended | Pending clarification or correction |
| Withdrawn | With deactivation, the decision being kept in the history |

## Review and withdrawal

An incident, a drop in performance, a model update, new connectors, a change of data, subcontractor, contract, regulation or function triggers a review. The guarantees are then re-checked on documentary evidence rather than carrying over an old score.

## What the approval file contains

The file brings together the use case sheet, the questionnaire sent to the provider, the table of conditions, the test report, the opinions (professional ethics, security, DPO as the case may be), the dated decision, the restrictions and planned training, the review date and the version history.

Private contracts, results containing information covered by secrecy, technical identifiers and confidential traces are not published.

## Use case sheet

The request starts with this sheet, completed by the requester.

```text
USE CASE DECLARATION AND QUALIFICATION SHEET

ID: [ ]   Department or requester: [ ]   Date: [ ]

NEED AND PURPOSE
Work currently carried out: [ ]
Measurable objective of the assistance: [ ]
Internal or external recipient: [ ]
Possible consequences of an error: [ ]

CONFIGURATION
Tool, model, accessible version: [ ]
Intended purpose of the system as set by the provider: [ ]
Connectors, sources, permissions: [ ]
Data class(es) D0 to D4: [ ]
Operations: [read / propose / modify / send / sign / other]
Use level U1 to U4: [ ]

OVERSIGHT AND CONTROLS
Reviewer with the competence and authority: [ ]
Controls S1, S2, S3: [ ]
S4 actions and approval points: [ ]
Independent sources available: [ ]
Conditions for refusal or stopping: [ ]
Test plan (cases, thresholds, critical errors): [ ]

DECISION REQUESTED
Authorise, experiment or refuse: [ ]
Proposed restrictions and evidence: [ ]
Duration and review date: [ ]
Operational lead: [ ]
```

## Evaluation and decision sheet

The evaluator completes this sheet. Weighted scoring is optional.

```text
APPROVAL EVALUATION AND DECISION SHEET

Request ID: [ ]   Date: [ ]   Requester: [ ]   Evaluator: [ ]

1. CONFIGURATION AND USE
Provider and contract: [ ]
System name and version, if known: [ ]
Application, API, agents, connectors: [ ]
Purpose and task: [ ]
Authorised users: [ ]
Data class: [ ]
Data flows, processing regions, recipients: [ ]
Possible actions and prohibited actions: [ ]
Level U1 to U4 and justification: [ ]
Planned oversight measures: [ ]

2. NON-COMPENSABLE CONDITIONS (OK / KO / ? / reasoned N/A; evidence or reservation)
E01 Purpose and admissibility: [ ]
E02 Confidentiality and secrecy: [ ]
E03 Personal data: [ ]
E04 Security and access: [ ]
E05 Control and interruption: [ ]
E06 Contract and reuse: [ ]
E07 Incident management: [ ]
E08 No uncontrolled critical error (U3 and U4): [ ]

3. WEIGHTED SCORING (optional; weights to be set locally)
C1 Confidentiality and data (25%): score [ ]; evidence [ ]
C2 Technical security (20%): score [ ]; evidence [ ]
C3 Reliability for the use (20%): score [ ]; evidence [ ]
C4 Human control (15%): score [ ]; evidence [ ]
C5 Auditability (10%): score [ ]; evidence [ ]
C6 Portability and reversibility (5%): score [ ]; evidence [ ]
C7 Maintenance and support (5%): score [ ]; evidence [ ]
Score: [ ]/100   Critical errors: [ ]   Test report: [reference]

4. OPINIONS AND DECISION
Legal or professional ethics opinion: [reference, or not required and why]
Security opinion: [ ]
Data or DPO opinion: [ ]
Residual risk and reasoned decision: [ ]
Status: [approved / approved with conditions / pilot / refused / suspended / withdrawn]
Restrictions: [ ]   Measures, person responsible, deadline: [ ]
Review deadline and triggers: [ ]
Authorised decision-maker and signature: [ ]

5. CHANGE HISTORY
Date | Change | Effect on scope | Decision
```

## The registers

The toolkit provides registers in CSV format that contain only their headers, with no real cases. They are encoded in UTF-8 with BOM, with the semicolon as separator.

The approvals register has one row per decision and per approved scope, not one row per provider. Its columns are: `id_homologation`, `date_demande`, `organisation`, `demandeur`, `fournisseur`, `produit`, `modele_version`, `configuration`, `cas_usage_id`, `classes_donnees`, `niveau_usage`, `actions_autorisees`, `restrictions`, `conditions_eliminatoires`, `score_indicatif`, `rapport_tests_ref`, `statut`, `decideur`, `date_decision`, `date_reexamen`, `declencheurs_changement`.

The score grid has one row per criterion and per evaluation. The weights are indicative and the scores are entered once the local rules have been adopted. Its columns are: `evaluation_id`, `critere_code`, `critere`, `poids_pct`, `note_0_a_5`, `preuve_ref`, `commentaire`, `evaluateur`, `date`.

The registers of incidents, significant uses and training are described in [operations](../operations/). The incidents register must be protected and must not contain client names. The significant uses register refers to evidence kept in a safe place without reproducing documents covered by secrecy. The training register contains staff data and access to it is strictly limited. The test scenarios register contains only fictitious cases and material whose rights are established.

No “score” column authorises a tool on its own. Before any operational use, the organisation sets the mandatory fields, the possible decisions and the access rights to each register.
