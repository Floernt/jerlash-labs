---
draft: true
title: "Pseudonymisation"
description: "Replace the names, addresses and Belgian identifiers in a text with markers before submitting it to an AI, then restore the names in the response. On your computer, without network."
resume: "The tool replaces the names, addresses and numbers in a text with markers such as [PERSONNE_1], has you reread the result, then puts the real names back into the AI's response. It does not find everything: rereading is mandatory."
slug: "pseudonymisation"
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["prepare a document", "protect data"]
mise_a_jour: 2026-10-31
telechargement: "/telechargements/pseudonymisation-0.1.0.zip"
taille: "33 KB"
sha256: "985d6610cdcead1f4253e4def184f980ee2b550604cd14bee7cabfcc5d7d327d"
traduction:
  source: "c74be371e6453a00cbfc334d0afab22c51e8bc9f"
---

## What the tool does

You paste a text or open a file (.txt or .docx). The tool identifies:

- names of individuals preceded by a title (M., Mme, Me…) or written with the surname in capitals, then all other occurrences of those names;
- companies followed by their legal form (SRL, SA, ASBL, BV, NV…);
- addresses (street, number, postcode, town);
- national register numbers, enterprise and VAT numbers, IBANs and card numbers, whose checksum it verifies;
- email addresses, telephone numbers, dates of birth, number plates and court roll numbers.

Each piece of data is replaced by a marker: `M. Thomas Wilmotte` becomes `M. [PERSONNE_1]`, and every mention of Wilmotte in the text becomes `[PERSONNE_1]`. The AI can thus follow who does what without knowing the names.

You reread the pseudonymised text next to the original. You can keep a piece of data that the tool replaced wrongly, or add a name that it missed. You can only save the result after confirming this reread.

Once you have the AI's response, the “Rétablir” (Restore) tab puts the real names back in place of the markers.

## What it does not do

The tool pseudonymises; it does not anonymise. The difference matters: a pseudonymised text may still make it possible to recognise a person. The replaced data is kept in the correspondence table, and the context (a position, a town, a date, a notable fact) is sometimes enough to recognise someone. The pseudonymised text therefore remains personal data, and it remains covered by professional secrecy. The tool reduces what goes out; it does not relieve you of deciding whether the document may be submitted to an AI.

The detection rules do not find everything, and the measurements below show it. Names cited without a title, first names on their own, nicknames and initials often slip through.

For a Word document, only the body of the text is taken: headers, footers, notes and comments are not. The result is plain text, without the document's formatting. The tool does not read PDFs: copy their text and paste it into the window.

## Use case

You want an AI to help you structure written submissions in a lease dispute. You paste the statement of facts. The tool replaces the names of the landlord and the tenant, their addresses, the landlord's national number and the bank account. You notice that it missed the neighbour's first name, cited on its own in the last paragraph, and you add it. You send the pseudonymised text to the AI. You paste its response into the “Rétablir” (Restore) tab and get your names back.

If you know the names of the parties, give them to the tool before running the detection. It searches for them throughout the text, including the surname on its own. This is the safest way to catch what the rules do not see.

## Data flow

- Stays on your computer: the original text, the pseudonymised text, the correspondence table, the restored response.
- Sent to an AI provider: nothing by the tool. You are the one who copies the pseudonymised text to the AI of your choice.
- Sent to jerlash.labs: nothing.

The tool's code imports no module capable of communicating over the network. An automated test checks this at every change, and another runs the full process with the network functions disabled.

The correspondence table contains the original data. It is saved in `Documents\Pseudonymisation`. Never send it with the text.

## Tests carried out

Version 0.1.0 was measured on 31 October 2026 on the fictitious test set F-IDENT-01, in two stages. The **development set** was used to write the rules: 6 texts, 102 pieces of data, all found. This figure only says that the rules cover the cases for which they were written.

The **control set** was drafted separately, without access to the rules. It contains 8 documents: a judgment, an exchange of emails between fellow lawyers, a formal notice, a share transfer, a medical expert report, a record of a hearing, meeting minutes, and a note without any personal data. This set measures what the tool finds in texts it does not know:

| Data | Found in full |
|---|---|
| National and enterprise numbers, IBANs, cards | 21 out of 21 |
| Email addresses | 8 out of 8 |
| Telephone numbers | 8 out of 9 |
| Addresses | 18 out of 21 |
| Companies | 18 out of 23 |
| Number plates | 3 out of 4 |
| Dates of birth | 3 out of 7 |
| Names of individuals | 37 out of 83 |
| Case references | 2 out of 10 |
| **Total** | **118 out of 186 (63%)** |

Of 138 replacements, 3 concerned something other than personal data. Only one of these false alerts concerns the note without personal data: the tool took a reference to the European Court of Human Rights for an address.

In other words, the tool is reliable for numbers. It is not reliable for names cited without a title. That is why rereading is mandatory.

Before publication, an independent review of the code found thirteen defects, four of them blocking. The most serious: the window could save a text modified after the reread, with names in clear. All have been fixed, and each is covered by a test.

Other automated tests check that the original file is never modified, that booby-trapped Word files are rejected, that no existing file is overwritten and that restoration finds the markers even when slightly altered by the AI (`[Personne_1]`, `PERSONNE 1`).

## Cost

Free: the tool calls no paid service.

## Precautions

- Always reread the pseudonymised text in full before sending it.
- Also remove what makes it possible to recognise a person without naming them: an unusual position, a described address, a precise date and place.
- Keep the correspondence table out of shared folders, and delete it when you no longer need it.
- The general rules of use are on the [Precautions](/precautions/) page.

## Installation

The guide [Using a tool locally](/guides/utiliser-un-outil-en-local/) details each step. In short:

1. Install Python 3.10 or later.
2. Download the archive above and check its SHA-256 fingerprint.
3. Unzip it, then double-click `Pseudonymisation.pyw`.

The tool also works from the command line (`python -m pseudonymisation pseudonymiser piece.docx`). The `README.md` file in the archive describes the options.

## Versions

0.1.0 (31 October 2026): first version.

## Report a problem

Write to [À COMPLÉTER : adresse de contact] stating the version of the tool and the type of data missed or wrongly replaced. Do not send the text concerned: reproduce the case on a fictitious example. Each case reported is used to enrich the test set.
