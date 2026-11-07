---
draft: false
title: "Equipping lawyers: customising rather than standardising"
date: 2026-11-08
description: "Lawyers refuse to standardise their practice, whereas automation requires breaking it down into steps. The way out lies in tools that lawyers adapt themselves, starting from a practice they have first made explicit."
slug: "customising-rather-than-standardising"
statut: "version de travail"
version: "0.2"
programme: "transversal"
date_arret_recherches: 2026-11-06
controles: "Working version, with no external review."
usage_ia: "Claude Opus 5.5 (November 2026) was used to write a first draft from the transcript of an oral interview with the author, following the angle he chose."
licence: "CC BY 4.0"
financement: "none"
traduction:
  source: "e616e9f09ca67b65fc318b9380750d30b75f02b8"
---

We regularly talk with young legaltech companies that are trying to understand the legal market before building their product. One question often comes up at the end of these conversations: which problem is really worth solving for law firms? The difficulty these teams describe is almost always the same: every lawyer they meet wants something different, and the list of requested features keeps growing. This text brings together the answer we give them, because it touches on a tension we also run into every time we build a tool.

## A practice that refuses the mould

There is no shortage of pain points in the profession. The difficulty lies elsewhere, however: lawyers work in a very individual way. Each has their habits, their way of approaching a case file, their own shortcuts. It is therefore hard to build a tool that suits everyone.

In our view, the cause runs deeper. Lawyers do not know how, and often do not want, to standardise their practice. If you ask a lawyer to stop and describe what they do at the first, the second and then the third step of a case file, the exercise fails most of the time. Their practice is intuitive. We think this resistance has a reason: lawyers sell, in a way, a part of themselves. Standardising the way you work means accepting that it is reproducible, and therefore that it no longer quite belongs to you.

The result shows on the market. For years, two categories of tools have followed one another: general-purpose applications that claim to suit everyone, and highly specialised tools that optimise a task so precise that they are rarely used. Neither fits into the real practice of a law firm.

## The workflow is in the head

Lawyers do follow a method, though. Facing a client, they ask questions; the answers lead them to other questions. By practising the same area day after day, they end up with a kind of algorithm in their head, which guides the interview and the rest of the case file. This is what we call a workflow (a sequence of steps).

The challenge is to get this algorithm out of the head, first onto paper, then into a digital tool. Each sequence has to be broken down, each step identified. Whether there are ten, a hundred or a thousand of them matters little. What counts is that each step is small enough, “atomic”, to be automated.

Let us take two examples from our own practice. The first is very simple: a workflow that lets clients book a video call. An email arrives, it is fed into a template, and the rest runs on its own. Anyone at the firm can use it. The second is more elaborate: scheduled tasks entrusted to an AI, which carry out part of the research and whose results are then taken up by the lawyer. In both cases, we apply the same principle: do something once, so that it can be done again a million times. A reply sent to a client by email can often become a template for others.

## The tension

This is where the problem appears. Automation requires precisely what lawyers refuse: making explicit, breaking down, standardising. For a technology to solve a pain point, the solution has to be formalised. Yet most lawyers have neither the wish nor, often, the flexibility of mind needed to think of their practice as processes. Legal training encourages a certain rigidity, and we do not exclude ourselves from this observation.

Let us illustrate this point. A lawyer recently made an MCP server public (Model Context Protocol, a protocol that connects an AI to external tools and sources). We plugged it into our own assistant: it is a way of communicating with his firm. We infer that he has built a system that passes the information received from a client through a series of tools, in order to better prepare his advice. What strikes us in this example is that this lawyer had to think of the way he produces advice as a chain of steps, something most lawyers never do. Many like technology; few ask themselves how to share, build or optimise their knowledge with it.

## One way forward: let lawyers adapt the tool

If standardisation cannot be imposed, another route remains: opening the tool up to customisation.

AI makes this adaptation far more accessible than before, since one can now describe in natural language what one wants to create or change. We think this is how tools will find their place in law firms: through customisation rather than standardisation.

We are not claiming here that customisation solves everything. It shifts the difficulty. To adapt a tool, users must be able to say what they want, and many lawyers have never put their practice into words. They do not have the elements to provide, because they have never thought about them. Customising therefore requires prior extraction work: getting out of the lawyer's head the algorithm they follow without knowing it. This is where the tension is resolved, at least in part. Lawyers do not have to bend to someone else's method; they only need to make their own explicit, and the tool adapts to it.

## What we take from this for those who build tools

To teams designing tools for law firms, we suggest three concrete avenues. Start from a lawyer's explicit practice rather than from a list of features, even if it means devoting the first part of a user's onboarding to helping them describe their own steps. Let lawyers change the tool themselves, in natural language, rather than delivering a fixed solution. Finally, accept that this extraction work is part of the product, and that it requires supporting the user.

This question connects with our work on human oversight of AI. Overseeing an AI other than by clicking “approve” at the end of a process also requires lawyers to be able to describe what they expect at each step. We will come back to this in the work of the [Agency & AI](/recherche/autonomie-ia/) programme.
