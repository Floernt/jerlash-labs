---
draft: false
title: "AI governance"
description: "A toolkit for deciding which AI tools a legal organisation uses, for what, with which data, and how to prove it, with a depth proportionate to the tools actually in place."
slug: "ai-governance"
url: "/en/tools/ai-governance/"
aliases: ["/en/tools/governing-ai-in-the-law-firm/"]
statut: "version de travail"
version: "0.3"
licence: "CC BY-NC 4.0"
programme: "H1"
usage_ia: "AI was used for drafting and structuring this working version."
controles: "Working version, with no external review or evaluation."
cascade:
  type: "toolkit"
traduction:
  source: "bf7becc5c7cac9c2fc711b7f0e9b1015382bf4bd"
---

AI use charters often repeat the same instructions: “use secure tools”, “have it reviewed”, “do not copy and paste”. These instructions are sound, but they cannot always be checked. They say neither on what conditions a tool was authorised, nor what the person reviewing must be able to do, nor how to show that a check actually took place.

Governance is therefore necessary. Its depth, on the other hand, should not be the same everywhere. A law firm working with a single tool whose contract, confidentiality guarantees and respect for professional secrecy it has checked does not need an approval procedure, a scoring grid and six registers: the tool itself offers the guarantees that these procedures would seek to establish. Conversely, an organisation whose case files circulate through several tools with uneven guarantees must be able to arbitrate, tool by tool and data item by data item.

This toolkit therefore proposes three governance levels. The first decision of the governance is to determine its own. Everything else follows from it.

## Which level for your organisation?

The level is determined tool by tool, and the organisation then retains the highest level among its tools.

For each tool, two questions are enough.

1. **Has its compliance been checked against documentary evidence?** The [compliance sheet](niveau-1/#the-compliance-sheet-for-a-tool) reviews around ten points: contract, professional secrecy, reuse of data, data protection, sub-processors, deletion, incidents. Compliance is *established* if all points are met, *partial* if all have been examined but some are not met, *not established* if points remain to be checked.
2. **What data goes into it?** Only public or non-sensitive internal data (classes D0 and D1 of the [classification](donnees/)), or also confidential data, data covered by secrecy or particularly protected data (D2 to D4)?

| Compliance of the tool | D0 and D1 data only | D2 to D4 data |
| --- | --- | --- |
| Established | Level 1 | Level 1 |
| Partial | Level 1 | Level 2 |
| Not established | Level 1 | Level 3 |

A tool that acts on its own (sending, filing, modifying a register, signing) falls under level 3 for that use, whatever its compliance, because its actions must be authorised one by one ([agents](supervision/#agents-and-external-actions)).

This table is a working proposal. Each organisation may modify it, for example by placing any use of a partially compliant tool at level 2.

## The three levels

| Level | Situation | What must be produced |
| --- | --- | --- |
| 1 | Each tool is compliant, or receives only D0 and D1 data | An AI lead, the inventory of tools, a compliance sheet per tool, a rule for checking outputs, an incident channel, a short training. It all fits on [one page](niveau-1/). |
| 2 | Several tools, with different levels of compliance | Level 1, plus a matrix stating which data classes and which uses are allowed in each tool, identified roles and graduated oversight. |
| 3 | Sensitive data circulates in tools whose compliance is not established, or tools act on their own | Detailed governance and an [approval](homologation/) that arbitrates the compliance of each tool for each use, with its eliminatory conditions, its tests and its registers. |

The level is not acquired once and for all. A new tool, a new contract, a new category of data or an incident can move the organisation up (or down) a level. The AI lead runs the diagnosis again at each of these changes, and at least once a year.

## The path for each level

**Level 1.** Read [the level 1 page](niveau-1/) and apply it. The other modules serve as reference, each stating at the top what it requires at level 1. The [charter](charte/) can be limited to a few articles.

**Level 2.** Do level 1, then classify the data with [the data module](donnees/), allocate roles with [governance](gouvernance/), draw up the tools × data × uses matrix, and graduate [oversight](supervision/) according to the uses.

**Level 3.** Put in place full [governance](gouvernance/), [data](donnees/), [approval](homologation/), [oversight](supervision/) and [operations](operations/), then draft and adopt [the charter](charte/), which records the choices made along the way. Then record incidents, changes and reviews, and revise the charter when these choices change.

At every level, the charter comes last: adopted from the outset, it would remain a declaration of principles that nothing allows to be checked, as described in the page [Why charters fail](pourquoi-les-chartes-echouent/).

## What the toolkit contains

| Module | Contents | From level |
| --- | --- | --- |
| [Why charters fail](pourquoi-les-chartes-echouent/) | The analysis of a typical law firm charter, what should be kept from it and its ten structural weaknesses | Recommended reading |
| [Level 1](niveau-1/) | Minimum governance and the compliance sheet for a tool | 1 |
| [Governance](gouvernance/) | Who decides, who answers for what, how to challenge a decision | 1 (reduced version), 3 (full) |
| [Data](donnees/) | The D0 to D4 classification and the questions to ask before processing | 2 |
| [Approval](homologation/) | Eliminatory conditions, scoring, tests and the decision for a tool and a use | 3 |
| [Oversight](supervision/) | The control of outputs and actions, and its evidence | 1 (checking a deliverable), 2 (control levels) |
| [Operations](operations/) | Incidents, training, traceability and registers | 1 (incidents and training), 3 (registers) |
| [The charter](charte/) | The internal normative document, which records the choices made in the modules | 1 (short version), 3 (sixteen articles) |
| [Sources](sources-et-versions/) | Legal sources and points to be confirmed | Reference |

## Status of this version

This is a working version. The whole is neither an adopted charter, nor a compliance label, nor individual legal advice. The levels, thresholds, weightings, frequencies and roles proposed in the modules are working proposals. Each organisation sets them itself, through its own governance. They are neither legal obligations nor scientifically validated criteria.

The first audience is Belgian law firms of all sizes. Next come in-house legal departments, in the context of continental European law. Adaptation remains necessary for each organisation and each legal system.

Human oversight is at the centre of the whole. It does not consist in waiting for a professional to click “Approve”: it requires competence, access to the relevant material and the power to challenge, amend or refuse. The toolkit seeks to bring together the conditions in which this judgement can be exercised. It does not replace it. It is accompanied by a research protocol designed to measure the ability of those exercising oversight to detect an error, correct it, challenge an output and justify their choice. This protocol has been neither validated nor carried out.

One rule applies at every level: examples and test sets never contain real client data or material covered by professional secrecy. They are based on fictitious scenarios.
