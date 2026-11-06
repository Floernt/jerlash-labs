---
draft: false
title: "Governance"
description: "Who decides on the use of an AI tool in the firm, under which rules, when the decision is reviewed and how it is recorded."
slug: "governance"
url: "/en/tools/ai-governance/governance/"
weight: 20
niveaux:
  - niveau: "Level 1"
    texte: "An AI lead and another person who validates their sheets: see [the reduced version](#the-reduced-version-levels-1-and-2). Neither a responsibility matrix nor a decision template."
  - niveau: "Level 2"
    texte: "The reduced version, plus the [decision rules](#the-decision-rules) and the [cases for review](#when-to-review-a-decision)."
  - niveau: "Level 3"
    texte: "The whole module, including the responsibility matrix and the decision template."
traduction:
  source: "2e2c1514eeaea8440040d8883eb1f5bba0cebd5a"
---

Governance is the first step of the path. Its first decision is to determine its [level](/outils/gouvernance-ia/#which-level-for-your-organisation), which sets the depth of everything else. The [charter](../charte/) will come at the end of the path, to anchor the choices made by governance. This page proposes a reduced version for levels 1 and 2, then, for level 3, the roles, the rules governing an authorisation, the path of a use from its declaration to its withdrawal, a responsibility matrix and a decision template. It is a model to be adapted.

## The reduced version (levels 1 and 2)

Three roles are enough. One person may hold several of them, provided that no one approves their own request alone.

| Role | What it does |
| --- | --- |
| AI lead | Keeps the inventory of tools and the compliance sheets, and at level 2 the tools × data × uses matrix; repeats the level diagnosis; receives incident reports. |
| Decision-maker | Validates the sheets and the matrix drawn up by the AI lead, decides on a change of level, a new tool or a suspension. In a law firm, in principle a partner or the management body. |
| Case file lead | Checks the outputs used in their case files and assesses their professional consequences. |

At level 2, the decision-maker relies on the [decision rules](#the-decision-rules) below, and the AI lead on the [cases for review](#when-to-review-a-decision).

## The roles (level 3)

The diagram summarises who decides, who gives an opinion and who applies. A small firm may entrust several of these roles to the same person.

![Management or the AI committee delegates to the AI lead, who submits U3 and U4 uses to it. The AI lead seeks the opinion of legal and professional ethics, of security and IT, and of the DPO. The AI lead authorises the users, who declare uses and report incidents. The case file lead supervises the user.](/images/toolkit/gouvernance-acteurs.svg)

Management, or an AI committee, sets the admissible purposes, the tolerated level of risk, the categories of tools and data, the approval policy and the frequency of reviews. It may delegate in writing, but it retains general supervision.

The AI lead receives the requests, keeps the register and the review calendar, and checks that the conditions set by each decision are complied with. The AI lead coordinates the handling of incidents and requalifications.

Legal or professional ethics examines professional secrecy, the law of the profession, the terms of engagement, client information and intellectual property rights.

Security or IT checks access, authentication, isolation, encryption, technical subcontractors, connectors, logs and continuity.

The DPO, if there is one, analyses the risks to personal data and advises on contracts, transfers and the impact assessment where one is required. The DPO performs the function the law assigns to them, without thereby becoming the decision-maker for all processing.

The case file lead sets the limits of the use in their case file, checks the legal elements and assesses the professional consequences.

The user stays within the approved scope, applies the planned measures and reports incidents and overruns.

## The decision rules

- No one approves themselves for a significant use.
- Every authorisation specifies the scope, the level of risk, the admitted data, the controls, the duration and the approver.
- The eliminatory conditions of [approval](../homologation/) prevail over the weighted score. The absence of any known incident does not prove the absence of a critical risk.
- Each member declares their conflicts of interest. The member concerned recuses themselves, or governance records a proportionate compensating measure.
- The AI lead may technically block a tool as a precautionary measure only if that power has been delegated to them. They then refer the matter without delay to the competent body.
- The requester may obtain a review if they bring new facts or guarantees.

## The path of a use

1. The requester declares the use case and inventories the data concerned.
2. The applicable legal obligations are determined.
3. The eliminatory review is carried out, followed by performance, security and real-use tests.
4. The specialised officers give their opinion and the competent body takes a reasoned decision.
5. Users are authorised and informed of the limits.
6. The AI lead follows the versions, incidents and contract changes.
7. The authorisation is renewed, amended, suspended or withdrawn.

For step 2: the AI Act does not treat the practice of a law firm as a high-risk use, provided that the AI system is not diverted from its intended purpose: see [the sources](../sources-et-versions/).

## When to review a decision

A decision is reviewed in the event of a significant change in the model, new functions or permissions, a new service provider or a new transfer, a change in the confidentiality terms, an incident, a drift in performance, a new type of data, a change in purposes or a change in the law.

## Frequency of reviews

We propose a light review every quarter for sensitive uses, a full review every year and an immediate check after a serious incident or an essential change. These frequencies are to be set by each organisation: the law does not impose them uniformly.

## The responsibility matrix

R performs, A decides and is accountable, C is consulted, I is informed. A decision has only one reference A, unless there is a contractual particularity. Use levels U1 to U4 are described on the page on [approval](../homologation/).

| Activity | Management | AI lead | Legal and professional ethics | Security and IT | DPO (if there is one) | Case file lead |
| --- | --- | --- | --- | --- | --- | --- |
| Policy and risk tolerance | A | R | C | C | C | I |
| Approval criteria | A | R | C | C | C | C |
| Evaluation of a tool | I | A/R | C | R | C | C |
| Approval of a U1 or U2 use (by delegation) | I | A | C | C | C | R |
| Approval of a U3 or U4 use | A | R | C | C | C | R |
| Qualification of data and secrecy | I | C | A | C | C | R |
| Legal validation of a deliverable | I | I | C | I | I | A/R |
| Suspension for security reasons | A (1) | R (1) | C | R | C | I |
| Analysis of a data breach | A | R | C | R | C (2) | C |
| Keeping the register | I | A/R | I | C | C | I |

(1) According to the delegations and the emergency measures provided for.

(2) The DPO advises and monitors in accordance with their legal status, without automatically becoming the decision-maker for notifications (Articles 37 to 39 of the GDPR for the DPO, 33 and 34 for breach notification). The local procedure specifies who is the controller and what its obligations are.

This table is a starting point. Before adopting it, check the independence and tasks of the DPO, the powers of the partners and the separation of decisions.

## Keeping the evidence

Decisions, versions and test summaries are kept in a secure location, for the period the organisation sets. Client case files are not copied into audit logs or into documents intended to be shared. Day-to-day traceability is described in [operations](../operations/).

## Governance decision template

The following template is used to record a decision to approve, refuse, suspend or withdraw. It refers to the governance policy (and to the [charter](../charte/) once adopted), to the use case sheet and to the evaluation sheet described in [approval](../homologation/).

```text
AI GOVERNANCE DECISION

Organisation: [ ]
Body: [ ]
Meeting: [date]
Reference: [ ]

CONTEXT
Having regard to the governance policy of [date / version], where applicable
the charter of [date / version], the use case sheet [ID],
the evaluation of the system [ID / version], the opinions [references]
and the test results [ID].

DECLARATION OF INTERESTS
Members present and guests; conflicts or links with a provider;
abstentions and compensating measures: [ ]

GROUNDS
- Use, data, authorised persons and permitted actions: [ ]
- Eliminatory conditions and reservations: [ ]
- Quality checks and residual risks: [ ]
- Arrangements for effective oversight and ability to interrupt: [ ]
- Resources, training, audit and date of re-evaluation: [ ]

OPERATIVE PART
The body [approves / approves with conditions / authorises a pilot /
refuses / suspends / withdraws] the system [identification] for
[use case], exclusively within the scope described, subject
to [conditions]. The authorisation takes effect on [date] and expires or
is reviewed on [date / event]. Any substantial extension
requires a re-evaluation.

Implementation and follow-up: [person responsible]
Internal notification: [channel and date]
Route for review: [ ]
Signatures or approvals: [ ]
```
