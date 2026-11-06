---
draft: false
title: "Traceability, incidents and training"
description: "What a law firm keeps as a record of its uses of AI, how it handles an incident and how it trains and authorises the people who use or oversee these tools."
slug: "operations"
url: "/en/tools/ai-governance/operations/"
weight: 60
niveaux:
  - niveau: "Level 1"
    texte: "[The incident procedure](#the-procedure) and training modules F1 to F3."
  - niveau: "Level 2"
    texte: "Level 1, plus [proportionate evidence](#evidence-proportionate-to-the-use-level) and the incident register."
  - niveau: "Level 3"
    texte: "The whole module, including the registers and authorisation to use."
traduction:
  source: "90f8857a2092669ef3fc70cbedce54c626d57216"
---

This module covers day-to-day operation: which traceability elements (evidence) to keep, how to respond to an incident, how to train and authorise. It relies on the use levels U1 to U4 of [approval](../homologation/), the control levels S1 to S4 of [oversight](../supervision/) and the data classes D0 to D4 described in [data](../donnees/). The periods, frequencies and contents proposed here are to be set by each organisation.

## Traceability

### What the evidence must make possible

The evidence must be enough to understand a significant use of AI, the decisions taken and the incidents, without accumulating copies of documents covered by professional secrecy. A mention “AI-assisted” does not prove that a check took place, and nothing requires it to be applied uniformly to every small task.

### Evidence proportionate to the use level

| Use | Proposed evidence |
|---|---|
| U1, formatting | No individual record, except in the event of an incident or a requirement specific to the activity |
| U2, working analysis | Tool, purpose and, where relevant, check of the decisive points |
| U3, advice or binding content | Tool, source of the determining points, decision and validation by a competent person |
| U4, automated action | Identifier of the action, authorisation, authority, target, result, stopping point and any incident |

### Four places

Not all information goes to the same place.

| Place | Contents |
|---|---|
| Governance register | Non-confidential metadata and decisions |
| Secure professional case file | Documents, sources and detailed checks relating to a client |
| Technical log | Events needed for security and diagnosis, with appropriate access rights and deletion |
| Possible public space | Methods, blank forms, synthetic data and redacted results |

### Retention, access and monitoring

The organisation designates a person responsible for retention. It sets retention periods according to the purpose, the legal basis and professional obligations, and provides for the handling of requests from data subjects exercising their rights, as well as security measures.

Continuous monitoring of staff by means of these logs cannot be presumed lawful. It is assessed in the light of employment law, transparency and proportionality. This aspect requires an in-depth review.

### Documenting a decision

A decision concerning a use or a tool is documented by the following elements: identifier, date, requester, tool and configuration, use, data categories, risk level, checks carried out, reasoned decision, approver, deadline and any major change. The complete conversation with the tool is never attached as a reflex when it contains data covered by secrecy.

## Incidents

### When to report

A report is made as soon as there is a serious suspicion of a data leak, a significant legal error, an inappropriate transmission, unexpected behaviour by an agent, circumvention of permissions, a possible infringement of rights or a departure from the approved scope. Near misses also deserve to be reported: they allow the organisation to learn without waiting for harm.

### The procedure

1. Report without undue delay to the designated point of contact (AI lead or security support).
2. Protect: stop the flow or revoke access where authorised to do so, keep the necessary evidence without spreading the data.
3. Qualify: determine the harm, the persons, systems and data affected, and the professional, contractual and regulatory obligations at stake.
4. Escalate, as the case may be, to the case file lead, management, security, the data protection officer or specialist advisers, and determine who notifies what, and within what time.
5. Remedy: correct the deliverable, prevent the consequences, inform the client or third parties if required, review the settings or the rights.
6. Reassess: suspend or modify the approval of the tool, enrich the tests and the training (see [approval](../homologation/)).
7. Close by recording the measures taken, the person responsible and the result, including what could not be established.

### Notifications

The time limits and recipients of a notification depend on the type of incident, the status of the parties, the applicable legislation and the obligations of professional ethics. A single time limit should not be applied to every AI-related error. A personal data breach calls for a specific analysis under the GDPR, which may lead to notifying the supervisory authority and the data subjects where the legal conditions are met (Articles 33 and 34 of the GDPR).

### Quick incident sheet

| Heading | To be completed |
|---|---|
| Identifier | |
| Date and time of discovery | |
| Reporter | |
| Tool and version | |
| Verified facts | |
| Potential impact | |
| Data classes | |
| Containment measures | |
| Decision-making authority | |
| Legal and professional ethics analysis | |
| Notifications and their grounds | |
| Corrective actions (person responsible, deadline) | |
| Outcome for the approval (maintained, limited, suspended, withdrawn) | |
| Anonymised lessons learned | |
| Closure | |

## Training and authorisation to use

The programme below is a proposal. Any legal training requirements remain to be checked.

### The modules

| Module | Audience | Observable competence |
|---|---|---|
| F1, basics and limits of AI | All | Recognise a plausible but unreliable answer, explain the limits |
| F2, confidentiality and data | All | Classify an example in D0 to D4, decide whether transmission is permitted |
| F3, sources and reasoning | Legal staff and lawyers | Check a citation, whether it is up to date and the relevant exception |
| F4, effective oversight | Work leads | Challenge, correct, refuse and give reasons |
| F5, agents and operations | Agent users, IT | Set permissions, recognise a binding action, stop the agent |
| F6, governance and incidents | Decision-makers, AI lead | Approve within a scope, handle an escalation |

### The assessment

The proposed assessment relies on practical exercises. Faced with a case study containing an invented legal error or an outdated rule, the person spots the error and documents their check. Faced with a scenario involving data covered by secrecy, they identify the authorised scope or refuse the transfer. For an agent that is to send an email, they determine where approval sits and who can refuse. During an incident simulation, they apply the procedure and know whom to contact.

If the organisation awards training scores, it defines them itself and provides for a resit. No internal certificate should be presented as an institutional or regulatory accreditation.

### Keeping the capabilities

Oversight presupposes knowing how to do the work without the tool. The organisation therefore has verification tasks carried out without assistance, at a frequency it sets, organises adversarial reviews and seeks to detect excessive reliance on plausible answers. Training and authorisations to use are reviewed whenever there is a major change of system or responsibilities.

## The registers

The toolkit provides the registers as empty CSV files, separated by semicolons, containing only their headers. They are designed for the governance register: case file references in them are internal, and detailed evidence remains in the secure case file.

| Register | What it records | Columns |
|---|---|---|
| `REGISTRE_USAGES_SIGNIFICATIFS.csv` | Significant uses and how they were checked | identifier, date, tool and version, use case, internal case file reference, use level, control S1 to S4, determining points checked, source references, decision, validator, reservation, place where the evidence is securely kept |
| `REGISTRE_INCIDENTS.csv` | Incidents and how they were handled | identifier, dates of discovery and reporting, tool and version, use case, category, potential impact, data class, immediate measures, person responsible, escalation, notification assessment, corrective measures, deadline, approval status, closure date |
| `REGISTRE_FORMATIONS.csv` | Training and authorisations to use | internal identifier of the person, role, module, training date, date and method of assessment, authorisation to use, review date, validator |

The training register contains data about staff members. Access to it is restricted and workers' rights are respected. The approval register is described in [approval](../homologation/).
