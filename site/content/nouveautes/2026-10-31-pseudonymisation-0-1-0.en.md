---
draft: true
title: "Pseudonymisation 0.1.0"
description: "Second tool: replace the names, addresses and Belgian identifiers in a text before submitting it to an AI, then restore the names in the response."
date: 2026-10-31
slug: "2026-10-31-pseudonymisation-0-1-0"
traduction:
  source: "75e65d2b11ed976e38c914fd9bdef3640fdacac7"
---

First version of [Pseudonymisation](/outils/pseudonymisation/). The tool replaces the names, companies, addresses and Belgian identifiers in a text with markers, has the result reviewed, then puts the real names back into the AI's response. Everything happens on your computer, without a network.

The tool page publishes the measurement carried out on fictitious texts the tool had not seen before. It finds all the numbers with a check digit (national register, company, IBAN), but only 45% of personal names. Review therefore remains essential.
