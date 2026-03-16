# Measure the Real Robustness of a Fabric Data Agent in Italian

This repository collects the assets used across a two-part article workflow:

1. designing a Spider2-inspired benchmark for a Microsoft Fabric Data Agent in an Italian business scenario
2. using that benchmark to evaluate the Data Agent on Fabric with ground truth, notebooks, exports, and SDK source-code inspection

The repository currently includes benchmark files, evaluation notebooks, SDK inspection notebooks, helper scripts, and supporting schema material. :contentReference[oaicite:1]{index=1}

## Related article series

### 1. Benchmark design
[Building a Spider2-Inspired Benchmark to Measure the Real Robustness of a Fabric Data Agent in Italian](https://medium.com/data-science-collective/building-a-spider2-inspired-benchmark-to-measure-the-real-robustness-of-a-fabric-data-agent-in-ita-abe6f0781b34)

This first article focuses on:
- extracting realistic business questions
- defining canonical intents
- validating them against the real schema perimeter
- freezing metric definitions
- generating four formulations per intent
- producing the final 72-question benchmark

### 2. Benchmark execution and evaluation on Fabric
[We Built the Benchmark. Now Let's Evaluate the Fabric Data Agent for Real](ADD_ARTICLE_LINK_HERE)

This second article focuses on:
- completing the `expected_answer` column
- preparing the benchmark as an evaluation dataset
- uploading it to a supporting Lakehouse
- running evaluation with `evaluate_data_agent`
- inspecting summaries and row-level details
- auditing the SDK evaluation behavior
- testing stricter custom critic prompts

## Repository contents

### Benchmark assets

- [`final_benchmark.tsv`](./final_benchmark.tsv)  
  Final 72-question benchmark in TSV format.

- [`final_benchmark.xlsx`](./final_benchmark.xlsx)  
  Excel version of the benchmark before ground-truth completion.

- [`final_benchmark_with_expected_answers.xlsx`](./final_benchmark_with_expected_answers.xlsx)  
  Excel version of the benchmark with the `expected_answer` column populated, ready for evaluation on Fabric.

### Schema grounding

- [`zava_db_schema_and_top_20_rows.txt`](./zava_db_schema_and_top_20_rows.txt)  
  Schema and sample-row extract used to define the real perimeter of the Data Agent and to keep benchmark questions grounded in visible entities and available tables.

### Evaluation workflow

- [`zava_agent_evaluation.ipynb`](./zava_agent_evaluation.ipynb)  
  Fabric notebook used to load the benchmark from OneLake, run `evaluate_data_agent`, inspect evaluation summaries and details, and test stricter custom critic prompts.

- [`audit_table.py`](./audit_table.py)  
  Helper script used to rebuild an audit table by merging evaluation exports with benchmark metadata, especially useful when `expected_answer` is missing from exported evaluation details.

### SDK source-code inspection

- [`fabric_evaluation_source_code.ipynb`](./fabric_evaluation_source_code.ipynb)  
  Notebook containing the Python snippets used to inspect the installed `fabric-data-agent-sdk` source code directly, including:
  - default critic prompt extraction
  - model reference inspection
  - evaluation storage behavior
  - placeholder validation such as `{actual_answer}`

### Supporting notes

- [`data_agent_setup_outputs.md`](./data_agent_setup_outputs.md)  
  Supporting notes and outputs related to Data Agent setup and article material.

## Why this repository exists

Fabric Data Agents can look very convincing in guided demos. But moving from a promising demo to a trustworthy analytical interface requires something more structured:

- repeatable evaluation
- explicit ground truth
- intent coverage
- linguistic variability
- schema-bounded questions
- notebook-based execution on Fabric
- a path toward measurable robustness

This repository exists to support that transition.

## What "Spider2-inspired" means here

This project is inspired by the evaluation philosophy behind Spider2, not by a literal reproduction of that benchmark.

Here, "Spider2-inspired" means:
- realistic business questions instead of toy prompts
- canonical intents plus multiple linguistic variants
- robustness to paraphrasing, not just one ideal wording
- schema-aware benchmark construction
- evaluation-oriented assets that can be executed with ground truth

The target scenario is intentionally practical: a Fabric Data Agent over a retail demo schema, with special attention to Italian phrasing and multilingual behavior.

## Suggested reading order

If you are new to the repository, a good order is:

1. start from the benchmark design article
2. inspect [`final_benchmark.tsv`](./final_benchmark.tsv)
3. inspect [`final_benchmark_with_expected_answers.xlsx`](./final_benchmark_with_expected_answers.xlsx)
4. read the evaluation article
5. open [`zava_agent_evaluation.ipynb`](./zava_agent_evaluation.ipynb)
6. inspect [`fabric_evaluation_source_code.ipynb`](./fabric_evaluation_source_code.ipynb)
7. use [`audit_table.py`](./audit_table.py) for deeper post-run analysis

## Practical goal

The goal of this repository is not to showcase another "working demo".

The real goal is to answer a harder question:

**How robust is a Fabric Data Agent when real business users ask realistic questions in Italian, across multiple formulations, and under an explicit evaluation workflow?**

This repository is the working area for that question.
