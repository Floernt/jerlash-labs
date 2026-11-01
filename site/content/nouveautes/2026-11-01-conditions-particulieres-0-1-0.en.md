---
draft: true
title: "Special and general conditions 0.1.0"
description: "Fifth tool: identify what is specific to the transaction in a negotiated contract, article by article, without AI."
date: 2026-11-01
slug: "2026-11-01-special-conditions-0-1-0"
traduction:
  source: "f88b93f92d61a1e37f9f127bee3065804e9f8975"
---

First version of [Special and general conditions](/outils/conditions-particulieres/). The tool reads a Word contract and identifies, in each article, the data specific to the transaction: names, addresses, amounts, dates, identifiers. It proposes classifying each article as special or general conditions, and flags the general clauses that still contain a piece of transaction data, to be cleaned up before reusing the contract as a template.

It works by rules, without AI, and does not modify the contract. The tool page publishes the measurement made on fictitious contracts it had not seen before.
