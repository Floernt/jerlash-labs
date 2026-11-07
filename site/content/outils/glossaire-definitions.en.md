---
draft: true
title: "Glossary of definitions"
description: "List the defined terms of a contract and what is wrong with them: repeated or inconsistent definition, term never used, capitalised words without a definition, drifting spelling. On your computer, without AI."
resume: "The tool reads a Word contract and produces its glossary, with the points to examine: repeated or inconsistent definition, defined term never used, term written with capitals but not defined, different spelling."
slug: "definitions-glossary"
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["review a contract", "check"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/glossaire-definitions-0.1.0.zip"
taille: "28 KB"
sha256: "e53f971d3efecbbf57adacba7579440254bf33598586a5a3d75ccd356b57c075"
traduction:
  source: "3e0afa1e8d506978de6edb79ed17465d1a7c6d0f"
---

## What the tool does

You choose a contract. The tool reads it on your computer, without modifying it, and produces a report in Word. The report first contains the contract's glossary: each defined term, its definition, the clause in which it appears and the number of times the term is used.

It then flags the points to examine:

- a term defined twice, stating whether the two definitions differ; the two wordings are quoted side by side;
- a defined term that is used nowhere;
- a term written with capitals like a defined term (“les Spécifications Techniques”), without a definition in the contract;
- a defined term used with a different spelling (“Date d'entrée en vigueur” for “Date d'Entrée en Vigueur”);
- a term used in article 4 when it is only defined, in passing, in article 10.

Each point states the clause concerned.

## What it does not do

The tool does not modify the contract and does not rewrite any definition. It does not tell you whether a definition is correct, complete or appropriate. It reads Word documents (.docx) and text files, but not footnotes, headers or footers. A PDF or an old .doc must first be saved as .docx.

Identification is rule-based, without AI. It recognises the usual ways of defining a term:
- the “Définitions” article or schedule, tables included;
- “(ci-après « le Prestataire »)” and “ci-après dénommée”;
- “on entend par”;
- “(ensemble, les « Parties »)”.

A term defined in another way may escape it.

## Use case

You take over a services agreement negotiated over five rounds. Before sending it for signature, the report tells you that:
- “Informations Confidentielles” is defined twice, in article 1 and in article 9, with different scopes;
- “Période d'Essai” appears three times without a definition;
- “Force Majeure” is defined but never used again since the former article 14 was deleted.

## Data flow

- Stays on your computer: the contract, which is never modified, and the report.
- Sent to an AI provider: nothing. This version does not use AI.
- Sent to jerlash.labs: nothing.

The tool's code imports no module capable of communicating over the network. An automated test checks this, and another runs the full analysis with the network functions disabled. The report is saved in `Documents\Glossaire des definitions`.

## Tests carried out

Version 0.1.0 was measured on 1 November 2026 on two sets of fictitious contracts. The first, of three contracts, was used to write the rules, which process it without error. The second, of four contracts, was drafted separately, without access to the rules. It contains 50 defined terms and 30 defects. On this second set:

| Point raised | Found | Wrongly flagged |
|---|---|---|
| Defined terms | 48 out of 50 | none |
| Repeated definitions | 5 out of 5 | none |
| Terms never used | 5 out of 5 | none |
| Uses before definition | 5 out of 5 | none |
| Different spellings | 5 out of 6 | none |
| Terms without a definition | 5 out of 6 | 3 |

Two repeated definitions whose wordings say the same thing in other words are flagged as inconsistent: the comparison is based on the words, not on the meaning. The false “without a definition” alerts are expressions written with capitals that are not defined terms: they can be recognised at a glance.

Before publication, an independent review of the code found eighteen defects, none of them blocking. Two examples: a text moved under tracked changes was read twice, which produced a false repeated definition; a term used only in the plural ending in “-aux” was reported as “never used”. All have been fixed and each is covered by a test.

Other tests check three things:
- the contract is not modified (content and date);
- booby-trapped Word files are rejected with a message;
- no existing report is overwritten.

## Cost

Free: the tool calls no paid service.

## Precautions

- The report contains the contract's definitions: it is as confidential as the contract.
- A contract with no point flagged is not thereby free of definition defects.
- The general rules of use are on the [Precautions](/en/ethics/precautions/) page.

## Installation

The guide [Using a tool locally](/guides/utiliser-un-outil-en-local/) details each step. In short:

1. Install Python 3.10 or later.
2. Download the archive above and check its SHA-256 fingerprint.
3. Unzip it, then double-click `Glossaire.pyw`.

The tool also works from the command line (`python -m glossaire_definitions "chemin du contrat.docx"`). The `README.md` file in the archive describes the options.

## Versions

0.1.0 (1 November 2026): first version.

## Report a problem

Write to [À COMPLÉTER : adresse de contact] stating the version of the tool and the wording that was mishandled, copied without any client name or data. Do not send a real contract.
