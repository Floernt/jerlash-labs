---
draft: false
title: "Oversight and validation"
description: "How to check an output produced by an AI before using it, at what level, and how to keep a record of that check."
slug: "oversight"
url: "/en/tools/ai-governance/oversight/"
weight: 50
niveaux:
  - niveau: "Level 1"
    texte: "[Checking a legal deliverable](#checking-a-legal-deliverable) and [when to refuse or escalate](#when-to-refuse-or-escalate)."
  - niveau: "Level 2"
    texte: "Level 1, plus [the four control levels](#the-four-control-levels) assigned per use and [the minimum evidence](#the-minimum-evidence) for uses with stakes."
  - niveau: "Level 3"
    texte: "The whole module, including the validation sheet and the control of agents."
traduction:
  source: "9cddfbc70344aee30550c1f3cf6f9f3f8800907d"
---

By the end of this page, you will be able to choose a control level (S1 to S4) for a given use, check a legal deliverable produced with an AI and document the decision taken. The module treats human oversight as a requirement of professional practice and professional ethics. Levels S1 to S4 are categories internal to the toolkit.

## What oversight means

To oversee is to exercise a judgement one can account for. Being present while the tool works is not enough, nor is rewriting its text. Taking over word for word a proposal one has checked may be acceptable; rewording an error leaves an error. What is expected is that the person validating has made their own the points on which the professional decision rests.

Depending on the risk, this requires six capabilities:

- understanding the task, the facts, the scope, the version of the tool and its known limits;
- checking the decisive propositions using independent sources or methods;
- challenging, that is, looking for plausible objections, exceptions, omissions and competing hypotheses;
- correcting on a sound basis, and not merely rewording an uncertain proposition;
- refusing an output or interrupting an action, with real means of doing so within the organisation;
- justifying, by being able to trace the decisive elements of the final choice.

## The four control levels

The levels are indicative. Each organisation assigns them on the basis of its risk analysis.

| Control | Typical trigger | Minimum requirements |
|---|---|---|
| S1, simple review | Formatting, public content with no significant impact | Compliance with the request, absence of unexpected elements |
| S2, targeted check | Research, summary of texts, non-binding calculation | Decisive sources and facts, date, omissions, relevance |
| S3, in-depth professional validation | Consultation, conclusions, strategy, opinion, binding communication | Check of primary sources, reasoning, facts, alternatives, competence of the reviewer and reasons |
| S4, control of actions | Agent able to modify, send, sign, file | Permissions, validation point, recipient, log, interruption and resumption |

S4 concerns execution. It is added to S2 or S3 and does not replace the control of the intellectual quality of the output. No single rule imposes S3 for every internal draft.

Three examples help to place the levels. A standard administrative form, compliant with the request, is checked at S1; with nothing particular at stake, it leaves no individual record beyond the normal workflow. A memo on limitation periods in Belgian law is checked at S3: texts and case law consulted, alternative hypotheses examined, cut-off date of the law noted. An agent that sends a letter falls under S3 for the content if it is binding, and under S4 for the sending, with a recipient and a version approved before execution.

## Checking a legal deliverable

1. Reconstruct the legal question without looking at the output: facts, jurisdiction, applicable law, date, client's objectives.
2. Identify the decisive statements: rules on which the conclusion depends, citations, time limits, conditions, risks, figures.
3. Consult the primary sources and the documents in the case file, distinguishing what you have checked from what is merely asserted.
4. Look for a serious alternative or objection: exception, contrary fact, counter-argument, competing interpretation.
5. Check that the output responds to the mandate, the instructions and the intended audience.
6. Correct or discard any proposition you cannot justify, and note the limits that remain.
7. Validate the output as an authorised professional. Validation does not erase the uncertainties that remain.

## When to refuse or escalate

An output is refused, or the question referred to the competent person, in the following cases: a reference cannot be found, the facts show a significant inconsistency, a decisive point has no source, a divergence in case law has not been examined, the output contains a stray instruction or prohibited information, an action cannot be interrupted, the person exercising oversight lacks the required competence or time, data has been exposed outside the intended scope.

## The conditions for real oversight

The person exercising oversight needs time, accessible sources, suitable competence, an effective right to refuse and freedom from pressure to approve. A protocol can be well written and remain without effect in an overloaded department. Organisations therefore check these conditions during pilot phases and in post-incident reviews.

## The minimum evidence

For a use with stakes, the evidence comprises:

- an internal identifier of the case file or the work, which exposes no data;
- the tool, its known version and the use made of it;
- the decisive points checked and the sources or method of checking;
- the decision (used, modified, discarded, escalated);
- the reviewer, the date and any reservation.

The evidence is not a copy of all exchanges with the tool. Confidential information remains in the organisation's secure environment. The page on [operations](../operations/) describes the corresponding register.

## Deliverable validation sheet

The sheet is completed with a non-nominative case file reference, the name of the person responsible and the date. It asks the following questions, which are answered with evidence or a reference.

| Question | Answer, evidence or reference |
|---|---|
| Subject, recipient and consequences of the deliverable | |
| Approved tool, configuration and use case | |
| Applicable U level and S controls | |
| Decisive facts compared with the documents | |
| Texts and decisions consulted at the source | |
| Date of the law checked | |
| Hypotheses and objections examined | |
| Citations, third-party rights and personal data | |
| Errors or hallucinations detected | |
| Corrections and residual limits | |
| Competence and real power of the reviewer | |
| External action requiring confirmation | |

The sheet ends with a decision (validated, validated with reservations, to be corrected, discarded, escalated), the reasons for the decisive points, the name of the reviewer and the date. Levels U1 to U4 and the approval of a tool for a use case are defined in [approval](../homologation/).

Neither the mention “text generated by AI” nor the fact of having reworded the text proves the quality of the work.

## Agents and external actions

An agent is a tool that does not merely propose text: it acts on files, registers or third parties. It receives only the access and actions needed for the use case for which it was approved. A distinction is made between reading, proposing, modifying locally, publishing, sending, filing, signing, paying and deleting.

The following matrix is to be adapted by each organisation.

| Action | Potential risk | Proposed controls |
|---|---|---|
| Read a public document | Low | Adequate sources and access rights |
| Read a case file covered by secrecy | High | Approved environment, isolation, logs reduced to what is necessary |
| Propose a draft | Variable | S1 to S3 check depending on the content |
| Modify an internal register | Variable | Limited rights, consistency check, history and restoration |
| Send a binding communication | High | Approval of the content and recipient before execution, proof of sending |
| File submissions | Critical | Legal check, validated procedure, identity, acknowledgement of receipt, authorised intervention |
| Sign or make a payment | Critical | Separation of powers, prohibition or specific reinforced authorisation |
| Mass deletion | Critical | Prohibited by default; if exceptionally allowed, restoration and double validation |

For each agent, the organisation specifies the permissions per service and per resource, quotas and volume limits, admitted recipients, the test or pilot environment, the management of service access keys (API secrets), the log of decisions and actions, the stop mechanism, instruction injection tests (*prompt injection*), double checking of irreversible operations, the recovery and restoration plan, and the prevention of execution loops.

A human approval point has value only if the person sees what is about to be executed, the binding elements and their consequences. They must be able to refuse without traceability being lost and without an unplanned automatic resumption circumventing their refusal. A validation button does not, on its own, establish that the person has understood.

After an incident involving an agent, the permissions, instructions and sources, decisions, actions, data modifications, the system and its version, and the interruption possibilities that existed are reconstructed, with due regard for confidentiality. The permissions concerned are suspended until a new evaluation. The general procedure is set out in [operations](../operations/).
