---
draft: true
title: "Pre-send check"
description: "Check a Word document before sending it: comments, tracked changes, hidden text, properties, names from other case files. Without AI, without network."
resume: "Before you send a Word document, the tool looks for what should not go out with it and locates each item. It never modifies the document."
slug: "pre-send-check"
version: "0.1.0"
statut: "test"
mode: "local"
ia: false
cle_api: false
licence: "MIT"
taches: ["check", "prepare a document"]
mise_a_jour: 2026-10-31
telechargement: "/telechargements/controle-avant-envoi-0.1.0.zip"
taille: "33 KB"
sha256: "3a399124fb5dc3ba06a71e18429de8f33163c052a3b060ad7466012071958b0a"
traduction:
  source: "717722965ace96e8a5343d1fc5a4bdbb61102d27"
---

## What the tool does

It reads the .docx file on your computer and looks for:

- comments, with their author;
- tracked changes not yet accepted, including in headers, footers and notes;
- hidden text, written in white or in a tiny font size;
- blanks to be filled in (`[●]`, `[à compléter]`, `XXX`, `TODO`…) and highlighted text;
- names of other clients or other case files, based on a list you give it;
- the document properties: author, last person to have modified it, company, title, custom properties;
- fields that display the file name or path;
- links to your internal servers and the attached template;
- embedded objects, macros, document variables;
- photo metadata (EXIF);
- footnotes, for a final reread.

For each item, the report gives where it is located and how to correct it in Word. Each check has a status: detected, not detected in the checks carried out, not checked, or error.

## What it does not do

It does not modify the document: corrections are made in Word, on the copy to be sent. It checks neither the substance, nor the spelling, nor the numbering, nor the cross-references. It flags an embedded Excel spreadsheet without opening it. It does not analyse .doc, .odt or PDF files, nor a password-protected document: in those cases, it states that the analysis is impossible and draws no conclusion.

A report without any alert means that the items looked for were not found. It does not remove the need to reread.

## Use case

You send the fellow lawyer on the other side the revised version of a services agreement. The file started from one of the firm's templates. An associate left a comment in it about your negotiating margin, the “Author” field contains a trainee's name, and a reference to another case file lingers in a custom property. The report lists these three items in a few seconds.

## Data flow

- Stays on your computer: the document, the list of terms, the report.
- Sent to an AI provider: nothing. The tool does not use AI.
- Sent to jerlash.labs: nothing.

The tool's code imports no module capable of communicating over the network, and an automated test checks this at every change. The report contains extracts from the document. By default it is saved in `Documents\Controle avant envoi`, and not next to the document, to avoid attaching it by mistake.

## Tests carried out

Version 0.1.0 was tested on 31 October 2026 on a set of fictitious documents:

- a contract containing at least one example of each trap looked for, which opens normally in Word;
- the same contract without any trap;
- a document with a macro and an embedded object;
- a password-protected file and a truncated file.

All the planted traps are detected. The contract without traps triggers no alert. The two unreadable files produce “analyse impossible” (analysis impossible). Other tests check that the analysed file is not modified (identical fingerprint before and after), that no network access takes place, and that booby-trapped files (an archive with an oversized decompression, an XML entity declaration) are rejected without being interpreted.

These tests are based on documents produced for the purpose. Real documents, created by other versions of Word or by other software, may contain structures that the tool does not yet know. Report them: they will be used to extend the test set.

## Cost

Free: the tool calls no paid service.

## Precautions

- Run the check again after your corrections: an “Accept All Changes” removes neither the comments nor the properties.
- The list of terms contains client names. Keep it out of shared folders.
- The report is as confidential as the document. Do not attach it when sending.
- The general rules of use are on the [Precautions](/en/ethics/precautions/) page.

## Installation

The guide [Using a tool locally](/guides/utiliser-un-outil-en-local/) details each step. In short:

1. Install Python 3.10 or later.
2. Download the archive above and check its SHA-256 fingerprint.
3. Unzip it, then double-click `Controle avant envoi.pyw`.
4. Click “Choisir des documents…” (Choose documents…).

For users comfortable with a terminal, the tool also works from the command line (`python -m controle_avant_envoi contrat.docx`), with exit codes that can be used in a script. The `README.md` file in the archive describes the options.

## Versions

0.1.0 (31 October 2026): first version.

## Report a problem

Write to [À COMPLÉTER : adresse de contact] stating the version of the tool, your version of Word and the message you received. Do not send the document concerned: describe its structure or reproduce the problem on a fictitious document.
