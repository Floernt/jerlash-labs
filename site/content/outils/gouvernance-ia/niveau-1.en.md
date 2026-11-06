---
draft: false
title: "Level 1"
description: "The minimum governance of an organisation in which each AI tool is compliant or receives only non-sensitive data: six elements and a compliance sheet."
slug: "level-1"
url: "/en/tools/ai-governance/level-1/"
weight: 15
traduction:
  source: "9480f17a00d1904528866622c7f038456fd3bb80"
---

Level 1 applies when each AI tool used by the organisation meets one of these two conditions: its compliance with ethical, professional and contractual requirements has been checked against documentary evidence, or it receives only public or non-sensitive internal data (classes D0 and D1). The diagnosis is on [the home page](/outils/gouvernance-ia/#which-level-for-your-organisation).

At this level, detailed data classification and approval make little sense. The compliant tool offers the guarantees that these procedures would seek to establish. The unchecked tool, for its part, receives nothing that deserves protection. Governance therefore focuses on what remains: knowing which tools are in place, checking that they are compliant, controlling what they produce and reacting when something goes wrong.

## The six elements

1. **An AI lead.** An identified person keeps the inventory of tools, retains the compliance sheets and runs the level diagnosis again when the situation changes. In a small firm, this may be a partner. Another person validates the sheets the AI lead draws up: no one approves their own request alone.
2. **The inventory of tools.** For each tool: its name, the provider, the subscribed plan (free, professional, enterprise), the people who use it and the date of the compliance sheet. An AI feature built into software already in place (word processor, email, practice management software) is a tool to be inventoried.
3. **A compliance sheet per tool**, or failing that the D0/D1 rule: a tool without a sheet, or whose sheet is not fully met, receives only D0 and D1 data. The sheet is set out below.
4. **A rule for checking outputs.** Any output used in a service is checked by the person using it, following the method described in [Checking a legal deliverable](../supervision/#checking-a-legal-deliverable). An output is discarded or escalated when it falls into one of the [cases for refusal](../supervision/#when-to-refuse-or-escalate).
5. **An incident channel.** Everyone knows whom to report a data leak, a significant error or unexpected behaviour of the tool to, and the AI lead applies the [incident procedure](../operations/#the-procedure).
6. **A short training**, focused on the limits of the tools, the checking of sources and the refusal of an output (modules F1 to F3 of [operations](../operations/#the-modules)).

The AI lead reviews the inventory and the sheets at least once a year, and immediately when a tool changes its contract, plan or features, or after an incident.

## The compliance sheet for a tool

The sheet is completed against documentary evidence: terms and conditions, contract, data processing agreement, the provider's security documentation. Each point receives one of these answers: *yes* (with the document establishing it), *no*, or *to be checked*. No answer is invented that the documents do not give.

| Code | Point checked |
| --- | --- |
| F01 | A written contract (terms and conditions or specific contract) is identified, dated and kept, for the plan actually subscribed. |
| F02 | The tool is used in accordance with the intended purpose set by its provider. |
| F03 | The provider does not reuse the content to train or improve its models, or this reuse is disabled in a verifiable way. |
| F04 | Access by the provider and its sub-processors to the content (support, abuse monitoring, logs) is limited and framed in a way compatible with professional secrecy. |
| F05 | If personal data is processed, a data processing agreement complying with Article 28 of the GDPR is in place. |
| F06 | The location of processing, transfers outside the European Union and their safeguards are known. |
| F07 | The list of sub-processors is available, and the provider gives notice of changes to it. |
| F08 | The retention periods of content and logs are known, and deletion is possible. |
| F09 | Accounts are protected (multi-factor authentication, access management, revocation), and exchanges and storage are encrypted. |
| F10 | The provider undertakes to notify security incidents, and a contact is identified. |
| F11 | The tool proposes without acting on its own: it sends, files, signs or modifies nothing without human intervention. |

Compliance is **established** when all points are at *yes*. It is **partial** when all points have been examined but one of them is at *no*, and **not established** when one of them remains *to be checked*. Partial or non-established compliance does not prohibit the tool: it restricts it to D0 and D1 data, or moves the organisation to level 2 or 3.

```text
COMPLIANCE SHEET FOR AN AI TOOL

Tool and subscribed plan: [ ]   Provider: [ ]
Drawn up by: [ ]   Validated by: [ ]   Date: [ ]

F01 Contract identified and dated ........ [yes / no / to be checked]  Document: [ ]
F02 Use in line with intended purpose .... [yes / no / to be checked]  Document: [ ]
F03 No reuse of content .................. [yes / no / to be checked]  Document: [ ]
F04 Access compatible with secrecy ....... [yes / no / to be checked]  Document: [ ]
F05 Data processing agreement ............ [yes / no / to be checked / not applicable]  Document: [ ]
F06 Location and transfers ............... [yes / no / to be checked]  Document: [ ]
F07 Sub-processors ....................... [yes / no / to be checked]  Document: [ ]
F08 Retention and deletion ............... [yes / no / to be checked]  Document: [ ]
F09 Account security and encryption ...... [yes / no / to be checked]  Document: [ ]
F10 Incident notification ................ [yes / no / to be checked]  Document: [ ]
F11 No autonomous action ................. [yes / no / to be checked]  Document: [ ]

Compliance: [established / partial / not established]
Data allowed: [D0 to D4 if established; D0 and D1 otherwise]
Review: [date, and at the latest within one year]
```

## When to move to level 2

The organisation moves to level 2 as soon as it wants to entrust confidential data or data covered by secrecy (D2 to D4) to a tool whose compliance is only partial. It moves to level 3 if it wants to entrust such data to a tool whose compliance is not established, or if a tool must act on its own. A change of level is a governance decision, recorded by the AI lead.

## The charter at level 1

A short charter is enough. Articles 1 (purpose), 2 (principles), 3 (bodies), 5 (data and secrecy), 7 (oversight), 8 (validation of outputs), 14 (incidents) and 16 (adoption) of the [model charter](../charte/) cover the essentials. Article 4 may refer to the inventory and the compliance sheets.
