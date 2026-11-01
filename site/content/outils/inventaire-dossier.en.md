---
draft: true
title: "Case file inventory"
description: "Draw up the register of the documents in a contractual case file: type, status, date, parties, authoritative version, and what should not be there. Rules on your computer, parties and links proposed by an AI model, with your key."
resume: "The tool goes through the case file of a contractual matter and produces a register of the documents in Word, with alerts: unsigned deed, document belonging to another client, illegible scan, registered letter without proof of posting."
slug: "case-file-inventory"
version: "0.2.0"
statut: "test"
mode: "local"
ia: true
cle_api: true
licence: "MIT"
taches: ["take over a case file", "check"]
mise_a_jour: 2026-11-01
telechargement: "/telechargements/inventaire-dossier-0.2.0.zip"
taille: "67 KB"
sha256: "797bd07eaaad589906a3e18432dd5306ee06194f680c3a1ef60e34374d2395ab"
traduction:
  source: "a3414b212a17fbfb3598316edf6446f131f288dd"
---

## What the tool does

You designate the case file of a contractual matter. The tool reads each document on your computer, without modifying it, and produces a register in Word. For each document, the register states:

- its type: contract, amendment, general terms and conditions, letter, email, note, template, precedent;
- its status: signed or draft;
- the date of the deed, not that of the file;
- the companies that are parties;
- the document to which it relates (an amendment to its contract, an email to the amendment it negotiates);
- whether it is authoritative;
- its SHA-256 fingerprint, which makes it possible to prove later that the document has not changed.

At the top of the register, alerts flag what requires attention:

- a document that the tool could not read;
- an unsigned contract or amendment;
- a document with no party in common with the rest of the case file, which may belong to another client;
- a duplicate;
- a letter announced as registered without proof of posting in the case file.

Each conclusion comes with the clue that produced it, for example “mention (signé) sous la signature” (“(signed)” note under the signature) or “référence au contrat du 15 mars 2023” (reference to the contract of 15 March 2023). You can therefore check it quickly.

## What it does not do

The tool does not analyse the clauses and gives no legal opinion. It reads Word documents (.docx), emails (.eml) and text files. PDFs, old .doc files, Outlook emails (.msg) and images are included in the register with their fingerprint, but flagged “non lus” (not read): the tool never guesses the content of a document it has not read.

The type, the status, the date and the authoritative document are rule-based. The parties and the links between documents, weak points of the rules (see the measurements below), are proposed by an AI model. The register indicates what comes from the model and where it disagrees with the rules. It should be reread as a proposal.

The tool does not work without an API key: you need an account with an AI provider.

## Use case

A fellow lawyer hands over to you a supply case file that has been running for three years, stored in a single folder:
- drafts and signed versions;
- two amendments;
- exported emails;
- a scan;
- a contract belonging to another client, kept “as an example”.

In a few seconds, the register identifies the main contract, the authoritative versions and the amendment that remained a draft. It flags the other client's document and the scan that will have to be opened by hand. It also notes that the termination letter is announced as sent by registered post, without proof of posting in the case file.

## Data flow

- Stays on your computer: the documents, which are never modified, the register, and the table linking each marker to the original name.
- Sent to the AI provider you have chosen, with your key: a single text for the whole case file. For each readable document, it contains the heading, the first fifteen and the last fifteen lines, and the email headers. File names are replaced by numbers. Names, companies, addresses and identifiers are replaced by markers on your computer before sending.
- Sent to jerlash.labs: nothing.

Before sending, the tool displays the exact text, the provider, the place of processing and the retention it declares, and the estimated cost. You can correct the text; nothing goes out without your consent. The tool does not verify the provider's declarations.

Automatic pseudonymisation is imperfect: on our control set, it finds a little under half of the names of individuals. Reread the text. A pseudonymised document may still be covered by professional secrecy, and the decision to send it is yours (see the guidelines of AVOCATS.BE and of the OVB on the use of artificial intelligence).

Only the connector built into the tool can communicate over the network; a test checks this, and another runs the full inventory with a fake provider, all other network access being blocked. The register is saved in `Documents\Inventaire dossier`, never in the inventoried folder.

## Tests carried out

Version 0.1.0 was measured on 31 October 2026 on two fictitious case files. The first, of 12 documents, was used to write the rules, which classify it without error. The second, of 16 documents, was drafted separately, without access to the rules. On this second case file:

| Information | Correct for |
|---|---|
| Document type | 14 documents out of 16 |
| Status (signed or draft) | 14 out of 16 |
| Authoritative document | 15 out of 16 |
| Date of the deed | 13 out of 16 |
| Companies that are parties | 11 out of 16 |
| Document to which it relates | 8 out of 16 |

The main contract is correctly identified.

These figures are those of the rules alone. AI mode (version 0.2.0): [À COMPLÉTER : mesure réelle sur le même dossier, plus mauvais résultat de trois exécutions, avec le modèle, la date et le coût].

Before publication, an independent review of the code found thirteen defects, four of them blocking. Two examples: the register could be written into the inventoried folder through a roundabout path, and a file named “NON signé” passed as signed. All have been fixed and each is covered by a test. A document that only its file name describes as signed is never presented as authoritative: the register states “à vérifier” (to be checked).

Other tests check three things:
- the documents are not modified (content and date);
- booby-trapped Word files are flagged as not read without interrupting the inventory;
- the register cannot be written into the inventoried folder.

The Word register was opened in Word to check that it displays without error.

## Cost

The tool is free; the call to the model is billed by your provider, to your account. The tool displays the maximum estimated cost before sending, and the actual cost in the register. As an indication, a case file of sixteen documents represents about 25,000 characters, i.e. a few cents at the rates noted on 31 October 2026.

## Precautions

- The register contains the names of the documents and of the parties: it is as confidential as the case file.
- Use a key dedicated to the tool, with a spending cap set with the provider.
- The alerts do not tell you everything. A document without an alert is still a document to reread.
- The general rules of use are on the [Precautions](/precautions/) page.

## Installation

The guide [Using a tool locally](/guides/utiliser-un-outil-en-local/) details each step. In short:

1. Install Python 3.10 or later.
2. Download the archive above and check its SHA-256 fingerprint.
3. Unzip it. Copy `config-ia.example.json` under the name `config-ia.json` and choose your provider and your model.
4. Create a `.env` file containing your key (for example `MISTRAL_API_KEY=...`), in the same folder.
5. Double-click `Inventaire dossier.pyw`.

The tool also works from the command line (`python -m inventaire_dossier "chemin du dossier"`). The `README.md` file in the archive describes the options.

## Versions

0.2.0 (1 November 2026): parties and links proposed by an AI model, with your key; sending screen.

0.1.0 (31 October 2026): first version, rules only.

## Report a problem

Write to [À COMPLÉTER : adresse de contact] stating the version of the tool and the misclassified document, described without its content. Do not send a real document.
