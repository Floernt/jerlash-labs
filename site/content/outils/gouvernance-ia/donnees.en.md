---
draft: false
title: "Data"
description: "Classify information before entrusting it to an AI tool, ask the right questions before processing and document the analysis."
slug: "data"
url: "/en/tools/ai-governance/data/"
aliases: ["/en/tools/governing-ai-in-the-law-firm/data/"]
niveaux:
  - niveau: "Level 1"
    texte: "No data classification. It is enough to be able to recognise classes D0 and D1, the only ones allowed in a tool whose compliance is not established."
  - niveau: "Level 2"
    texte: "[The five classes](#the-five-classes), [the questions before processing](#before-processing) and the tools × data matrix."
  - niveau: "Level 3"
    texte: "The whole module, including the questionnaire attached to the approval file."
weight: 30
traduction:
  source: "302b774cf12b8d39607138be1b8dc259f4088ade"
---

Before passing information to an AI system, or giving the system access to it, you classify it. The class determines which approved tool it may enter and on what conditions. This page proposes a classification, a list of questions to ask before processing and a questionnaire to attach to the [approval](../homologation/) file.

## The five classes

The D0 to D4 classification is an internal policy specific to the toolkit. It is not a legal nomenclature.

| Class | Examples | Basic rule |
| --- | --- | --- |
| D0 Public | Legislation, freely distributable documents | Usable in a system approved for D0, according to its purpose |
| D1 Internal | Firm procedure, non-sensitive draft, unpublished internal budget | System approved for D1, control of access and storage |
| D2 Confidential | Commercial documents, non-public negotiation information, non-public information about third parties | Explicit approval for D2, justified purpose, limited transmission |
| D3 Professional secrecy | Client instructions, correspondence and documents covered by secrecy, defence strategy | Specific legal and professional ethics analysis; provider, access and processing expressly authorised |
| D4 Enhanced protection | Sensitive or criminal data, particularly exposed case files, minors or vulnerable persons | Enhanced measures, specific legal analysis |

D3 and D4 can be combined. D4 does not replace the protection of secrecy. Other constraints (trade secrets, copyright, contractual prohibitions) are added to the class as attributes.

## Before processing

1. What is the minimum data needed for the task?
2. Does the data fall within the scope of the approval, connectors and subcontractors included?
3. Would a fictitious example, a non-identifying summary or another environment be enough?
4. Who has access to the prompts, the answers, the files and the logs, including at the providers?
5. Is the data reused for training, evaluation, security or human support?
6. What are the deletion periods, the transfers and the contractual guarantees?
7. If personal data is involved, is a data processing agreement, an impact assessment, information of the data subjects or another measure required?
8. Does the person responsible for the case file know and control the professional risks?

## Points to watch

Pseudonymising is not anonymising. The context of a document is sometimes enough to re-identify a person.

Hosting in the European Union does not by itself guarantee confidentiality. The contract, the subcontractors, the access and the applicable law must be examined.

A provider that does not train its public models on your data may still process it: it may retain it, consult the logs, have it read by human support staff, monitor it to detect abuse and transfer it.

A freely accessible legal source is not automatically free of copyright or usage restrictions.

Requests, documents and approval decisions that contain protected information are never made public.

## Local authorisation

For each class and each use, the organisation records the class, the data allowed, the minimisation required, the environment, the downstream services, the prohibitions, the validator, the deletion conditions, the duration and the review date. The roles responsible for this classification are set out in [governance](../gouvernance/).

## Processing analysis questionnaire

This questionnaire is completed before approval. It is not a full impact assessment. Where an impact assessment is required, it is carried out in accordance with the applicable requirements and the organisation's method.

```text
DATA PROCESSING QUESTIONNAIRE BEFORE APPROVAL

Organisation and person responsible: [ ]   Tool and use case: [ ]   Date: [ ]

1.  Nature of the information: [D0 / D1 / D2 / D3 / D4; combination and justification]
2.  Personal data: [yes / no / to be clarified]; categories,
    data subjects, any data referred to in Articles 9 or 10
    of the GDPR: [ ]
3.  Purpose and necessity of the processing: [ ]
4.  Roles under the GDPR: controller, processor(s),
    recipients, any joint controllership: [ ]
5.  Legal basis, information and rights of data subjects:
    [analysis to be completed if applicable]
6.  Professional secrecy and other secrets: [qualification and opinion]
7.  Contract and subcontractors: [data processing agreement, security,
    support, reuse, deletion arrangements]
8.  Location and transfers: [infrastructure, support,
    remote access, safeguards]
9.  Security: [multi-factor authentication, encryption,
    isolation, access control, logs, backup, incident response]
10. Retention period and exit: [ ]
11. Minimisation, pseudonymisation, synthetic data: [ ]
12. Impact assessment or possible consultation: [required? reasons and decision]
13. Residual risks and conditions: [ ]
14. Opinion of the DPO if there is one, legal opinion, security opinion: [ ]
15. Decision and duration: [ ]
```
