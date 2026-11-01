---
draft: true
title: "Case file inventory 0.1.0"
description: "Third tool: the register of the documents in a contractual case file, with their status, the authoritative version and the relevant alerts, without AI."
date: 2026-10-31
slug: "2026-10-31-case-file-inventory-0-1-0"
traduction:
  source: "f7b31ba2dc1a67fc3281096e6509f12f170a62ca"
---

First version of [Case file inventory](/outils/inventaire-dossier/). The tool goes through the case file of a contractual matter and produces a register of the documents in Word: type, status, date, parties, authoritative version, hash. It flags at the top what needs attention, such as an unsigned amendment or a document that appears to belong to another client.

It works by rules, without AI, and does not yet read PDFs. The tool page publishes the measurement made on a fictitious case file it had not seen before.
