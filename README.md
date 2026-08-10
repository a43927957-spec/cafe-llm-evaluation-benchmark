# Cafe LLM Evaluation Benchmark v0.1

> A compact Traditional Chinese (Taiwan) work sample for AI Trainer, LLM Evaluator, and AI Quality Analyst roles.

This repository demonstrates a reproducible way to evaluate customer-service LLM responses against explicit business facts. It contains 12 synthetic café scenarios, two candidate responses per scenario, a six-dimension weighted rubric, pairwise judgments, a failure taxonomy, and a dependency-free scoring tool.

**中文說明：** 這是一份繁體中文（台灣）LLM 評估作品。內容包含合成的咖啡廳客服情境、回答比較、幻覺與失敗模式分析，以及可重跑的評分程式。

## What this work sample demonstrates

- Pairwise response comparison with evidence-based rationales
- Hallucination and unsupported-action detection
- Instruction-following and multi-turn context evaluation
- Taiwan Traditional Chinese localization judgment
- Safety-aware handling of allergies and personal data
- Reproducible rubric scoring and dataset validation

## Benchmark snapshot

| Item | Value |
|---|---:|
| Synthetic scenarios | 12 |
| Candidate responses | 24 |
| Evaluation dimensions | 6 |
| Dimension-level ratings | 144 |
| Pairwise decisions | 12 |
| Locale | `zh-TW` |

Candidate labels are alternated across cases to avoid making one label consistently represent the stronger answer. The current set contains six wins for A and six wins for B.

## Repository map

```text
01-response-comparison/
  case-studies.md
02-hallucination-analysis/
  failure-taxonomy.md
03-cafe-llm-benchmark/
  benchmark-design.md
  evaluation-results.md
  recommendations.md
data/
  evaluations.json
src/
  score.py
tests/
  test_score.py
rubric.md
```

## Evaluation dimensions

| Dimension | Weight | Core question |
|---|---:|---|
| Factual accuracy | 30% | Does the response match the supplied facts? |
| Grounding | 20% | Are claims supported without invention? |
| Instruction following | 15% | Does it answer the actual request and respect constraints? |
| Helpfulness | 15% | Does it provide a useful next step? |
| Localization | 10% | Is the wording natural for users in Taiwan? |
| Safety and privacy | 10% | Does it avoid unsafe certainty or personal-data disclosure? |

See [rubric.md](rubric.md) for scoring anchors.

## Run the benchmark

Python 3.10+ is sufficient; there are no third-party dependencies.

```bash
python3 src/score.py
python3 -m unittest discover -s tests -v
```

Example output:

```text
Cases: 12 | A wins: 6 | B wins: 6 | Ties: 0
Dataset validation: PASS
```

## Three study tracks

1. [Response comparison](01-response-comparison/case-studies.md) — detailed pairwise judgments for policy, safety, and multi-turn context cases.
2. [Hallucination analysis](02-hallucination-analysis/failure-taxonomy.md) — a reusable taxonomy for unsupported facts, actions, and privacy failures.
3. [Café benchmark](03-cafe-llm-benchmark/benchmark-design.md) — benchmark design, aggregate findings, and product recommendations.

## Data and authorship note

All store names, policies, conversations, and model responses are synthetic. No customer, employer, merchant, or production data is included. AI tools assisted with drafting and code formatting; the repository is presented as a transparent portfolio work sample, not as prior paid annotation work or a production benchmark.

## Author

Prepared for the public portfolio of [@a43927957-spec](https://github.com/a43927957-spec), a native Traditional Chinese (Taiwan) speaker focused on LLM evaluation, conversational quality, and grounded AI responses.

## License

MIT — see [LICENSE](LICENSE).
