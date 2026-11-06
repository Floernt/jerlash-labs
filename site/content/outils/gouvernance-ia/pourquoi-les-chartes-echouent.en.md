---
draft: false
title: "Why AI charters fail"
description: "What a law firm's AI charter does well, its ten structural weaknesses and the correction proposed for each."
slug: "why-ai-charters-fail"
url: "/en/tools/ai-governance/why-ai-charters-fail/"
aliases: ["/en/tools/governing-ai-in-the-law-firm/why-ai-charters-fail/"]
weight: 10
traduction:
  source: "72309d13e3a1745ffbcd85964f4974820567474f"
---

The toolkit grew out of the analysis of a law firm's AI charter, submitted to the project as a starting point. Its text is not reproduced here. It resembles many others: its principles are sound, but there is no way to check that they are complied with. This text identifies what should be kept, where it stops too early, and how the modules of the toolkit propose to remedy this.

## What should be kept

The charter analysed does several useful things. It covers a broad circle of people, beyond lawyers alone. It asserts the primacy of professional judgement. It recalls the requirements of professional secrecy and the precautions arising from the GDPR. It calls for vigilance about the reliability of outputs and about sources. It deals with professional liability, training and incident reporting.

None of this should be abandoned. The difficulty lies in the way these principles are worded.

## Ten weaknesses and their correction

| Charter clause | What is wrong | Proposed correction |
| --- | --- | --- |
| “Authorised” tools | Authorisation is global, with no scope or threshold. | A decision covering a precise combination: tool, configuration, use, data, user and degree of autonomy. See [approval](../homologation/). |
| Security and reliability | Principles, with no tests or eliminatory criteria. | A checkable framework, documentary evidence and test cases. |
| Professional secrecy and data | Caution is left almost entirely to the user. | Data classes, access rights, a retention policy and contracts. See [data](../donnees/). |
| Traceability of any text produced with AI | An excessive burden, and logs that end up containing secrets. | Proportionate traceability, limited to decisive uses and to decisions. See [operations](../operations/). |
| Mandatory human review | The presence of a human does not guarantee that the check takes place. | A check that makes it possible to understand, detect, challenge, correct, refuse and justify. See [oversight](../supervision/). |
| Copying and pasting “prohibited” | The criterion is misleading: rewriting a text verifies nothing. | Intellectual ownership of the output and independent verification of the decisive points. |
| Liability of the lawyer “alone” | It oversimplifies the relationships between the firm, its staff and its service providers. | An allocation of internal duties, without prejudging legal liabilities. See [governance](../gouvernance/). |
| Incidents | Little escalation, no suspension status, no lessons learned. | A process with roles, securing measures, a review and follow-up of corrections. |
| Continuous monitoring | Undifferentiated monitoring of staff creates a risk under employment law and under the GDPR. | Proportionate audits and governance of logs. |
| Autonomous agents | Absent from the text. | Rights kept to a minimum, prior approval of certain actions, a stop mechanism and technical limits. |

Two of these weaknesses deserve closer attention, because they recur in almost every charter.

The first concerns mandatory review. That a lawyer has had the document before their eyes does not show what they checked. For the check to be real, the person must be able to understand what the system did, spot a (plausible) error, challenge it and refuse the output. This requires the competence, the time, the access to sources and the authority to do so. The second is the ban on copying and pasting, which rests on the idea that a reworded text has been thought through. Yet flawed reasoning remains flawed once reworded. The useful question is what has been verified, not the form of the final text.

## The clause that replaces both

The proposed correction is set out in a clause, included in [the charter](../charte/):

> Any content or action supported by an AI system must be subject to a check proportionate to its consequences. The check covers the decisive elements of the analysis and the professional's ability to understand, justify, amend or reject the proposal. Neither copying and pasting nor rewording proves, in itself, the compliance or quality of the service.

## The limits of the correction

These corrections have their own limits, which should be borne in mind.

Internal rules create no general exemption from professional secrecy or the GDPR. A firm's approval of a tool does not replace regulatory obligations. A score, however high, does not exempt anyone from checking the eliminatory conditions. Announcing “human oversight” does not prove that it is effective.

A second limit concerns the lack of implementation of the charter. However well written it may be, it can be circumvented. If no one has been given the power to decide which tools are authorised, if no decision is recorded and if nothing makes it possible to establish that a rule was followed or set aside, the charter remains a statement of principle, which everyone applies according to their own reading. This is why the toolkit begins with [governance](../gouvernance/) and places [the charter](../charte/) at the end of the path: it anchors decisions already taken and checks already in place.

Finally, the distinctions proposed by the toolkit (use classes, data classes, levels of oversight) are design hypotheses. They should be treated as such until they have been tested in practice.
