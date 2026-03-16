# Measure the Real Robustness of a Fabric Data Agent in Italian

This repository contains the benchmark assets described in the article:

[**"Building a Spider2-Inspired Benchmark to Measure the Real Robustness of a Fabric Data Agent in Italian"**](https://medium.com/data-science-collective/building-a-spider2-inspired-benchmark-to-measure-the-real-robustness-of-a-fabric-data-agent-in-ita-abe6f0781b34)

The goal of this project is not to showcase another "working demo", but to prepare a more rigorous evaluation setup for a **Microsoft Fabric Data Agent** operating on an Italian business scenario.

Instead of testing the agent with a few hand-picked examples, this repository defines a **benchmark of multilingual and business-oriented questions**, inspired by the spirit of **Spider2**: realistic phrasing, multiple formulations of the same intent, schema-aware evaluation, and a structure designed for reproducible testing.

## Why this repository exists

Fabric Data Agents can already look impressive in guided demos. But production readiness requires something different:

- repeatable evaluation
- explicit ground truth
- intent coverage
- linguistic variability
- schema-bounded questions
- a path toward measurable robustness

This repository provides the benchmark foundation needed to move from anecdotal success to structured evaluation.

## What "Spider2-inspired" means here

This project is **inspired by the evaluation philosophy** behind Spider2, not a literal reproduction of that benchmark.

In this repository, "Spider2-inspired" means:

- focusing on **realistic business questions**, not toy prompts
- defining **canonical intents** and **multiple linguistic variants**
- testing **robustness to paraphrasing**, not only one ideal wording
- keeping the benchmark **schema-aware and execution-oriented**
- preparing a dataset that can later be used for **systematic evaluation with ground truth**

The target scenario here is narrower and intentionally practical: a **Fabric Data Agent over a retail demo schema**, with special attention to **Italian phrasing** and multilingual behavior.

## Repository contents

This repository is expected to contain assets such as:

- the master benchmark file
- benchmark documentation
- intent definitions
- question variants
- evaluation notes
- optional helper notebooks or scripts for Fabric-based execution
- article-related examples and supporting material

