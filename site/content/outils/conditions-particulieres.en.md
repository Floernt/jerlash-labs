---
draft: true
title: "Special and general conditions"
description: "Identify, clause by clause, what is specific to the transaction in a negotiated contract: names, addresses, amounts, dates, identifiers. To separate special and general conditions, or to reuse the contract as a template. On your computer, without AI."
resume: "The tool reads a Word contract, identifies in each clause the data specific to the transaction and proposes a classification: special conditions, general conditions, or general clause to be cleaned up before reuse."
slug: "special-and-general-conditions"
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["review a contract", "prepare a template"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/conditions-particulieres-0.1.0.zip"
taille: "28 KB"
sha256: "9d796164a3c76befa8bbcd8e123c6228959b91af990563abee7ddb11f6aeae6a"
traduction:
  source: "6496bc8770f5b046b7f2fb12ebe9cfd9c49cabaf"
---

## What the tool does

You choose a negotiated contract. The tool reads it on your computer, without modifying it, and splits it into blocks: the appearance of the parties, each clause, then the place, the date and the signatures. In each block, it identifies the data specific to the transaction:

- the parties and the individuals (representatives, signatories, contacts);
- the addresses;
- the identifiers: enterprise number, IBAN, email address, telephone, order reference;
- the amounts, the dates and the quantities.

For each block, it then proposes a classification:

- **special conditions**: the block is specific to the transaction (parties, subject matter, price, term, contact details);
- **general conditions**: the block contains no data specific to the transaction and could be reused as is;
- **mixed clause**: a clause of a general nature (payment, liability, confidentiality…) that contains a piece of data specific to the transaction. The report quotes the data to be extracted, for example the figure capping liability or the IBAN slipped into the payment clause.

The report also lists internal cross-references (“article 5”), to be checked if clauses are moved.

## What it does not do

The tool does not produce the two separate documents and does not modify the contract. It does not tell you whether a clause can be moved without changing the effect of the contract: the order of precedence between special and general conditions and the enforceability of the general conditions remain your responsibility.

It does not read headers, footers or footnotes. A header bearing the client's name is therefore not flagged.

Identification is rule-based, without AI. Data written in a way the rules do not anticipate may escape it: a clause classified as “general” must still be reread before it is reused.

## Use case

You want to turn a maintenance contract signed last year into the firm's template. The report classifies eight clauses as general conditions and four as special conditions. It flags three mixed clauses:
- the payment clause contains the former client's IBAN;
- the liability clause, a cap of 25,000 euros negotiated for this transaction;
- the call-out clause, the technician's telephone number.

You know where to look before saving the template.

## Data flow

- Stays on your computer: the contract, which is never modified, and the report.
- Sent to an AI provider: nothing. This version does not use AI.
- Sent to jerlash.labs: nothing.

The tool's code imports no module capable of communicating over the network. An automated test checks this, and another runs the full analysis with the network functions disabled. The report is saved in `Documents\Conditions particulieres`.

## Tests carried out

Version 0.1.0 was measured on 1 November 2026 on two sets of fictitious contracts. The first, of two contracts, was used to write the rules, which process it without error. The second, of three contracts, was drafted separately, without access to the rules. It contains 92 pieces of data specific to the transaction and 46 blocks. On this second set:

| Data | Identified |
|---|---|
| Addresses | 12 out of 12 |
| Amounts | 17 out of 17 |
| Dates | 10 out of 10 |
| Parties and individuals | 21 out of 22 |
| Identifiers | 16 out of 18 |
| Quantities | 4 out of 13 |
| **Total** | **80 out of 92**, with no false positives |

Quantities are the weak point: the tool only recognises common units (bottles, man-days, square metres…).

41 blocks out of 46 are correctly classified. Of the 5 errors, 3 mixed clauses are proposed as special conditions, which errs on the side of caution. One mixed clause is proposed as general conditions, even though it contains a piece of data that was not recognised: this is the error that makes rereading necessary. Finally, one block of general conditions is proposed as special conditions.

Before publication, an independent review of the code found twenty defects, five of them blocking. All had the same consequence: a clause that still contained data from the transaction was presented as reusable. For example, “EUR 12.500” was not recognised as an amount, and a company named “Entre Brasserie du Condroz” in the appearance of the parties was no longer found afterwards. All have been fixed and each is covered by a test.

The tool still does not recognise a person's name written without a title, or a company cited without its legal form, if the contract has not introduced them elsewhere.

Other tests check three things:
- the contract is not modified (content and date);
- booby-trapped Word files are rejected with a message;
- no existing report is overwritten.

## Cost

Free: the tool calls no paid service.

## Precautions

- The report contains the transaction data: it is as confidential as the contract.
- Before reusing a contract as a template, reread it in full, including headers and footers. The report tells you where to look first, not where there is no need to look.
- To replace names in a text before entrusting it to an AI, use the [Pseudonymisation](/outils/pseudonymisation/) tool instead.
- The general rules of use are on the [Precautions](/en/ethics/precautions/) page.

## Installation

The guide [Using a tool locally](/guides/utiliser-un-outil-en-local/) details each step. In short:

1. Install Python 3.10 or later.
2. Download the archive above and check its SHA-256 fingerprint.
3. Unzip it, then double-click `Conditions.pyw`.

The tool also works from the command line (`python -m conditions_particulieres "chemin du contrat.docx"`). The `README.md` file in the archive describes the options.

## Versions

0.1.0 (1 November 2026): first version.

## Report a problem

Write to [À COMPLÉTER : adresse de contact] stating the version of the tool and the wording that was mishandled, copied without any client name or data. Do not send a real contract.
