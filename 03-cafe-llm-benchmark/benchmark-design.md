# Benchmark Design

## Objective

Measure whether a customer-service LLM can answer in natural Taiwan Traditional Chinese while staying grounded in a small set of store facts and conversational constraints.

## Scope

- 12 synthetic cases
- Two candidate responses per case
- Six weighted dimensions
- Pairwise winner plus written rationale
- No live model API calls and no customer data

## Case coverage

| Risk area | Cases |
|---|---|
| Policy and exception handling | `CAFE-001`, `CAFE-005`, `CAFE-007` |
| Unsupported actions and status claims | `CAFE-002`, `CAFE-006`, `CAFE-009` |
| Missing or multi-turn context | `CAFE-003`, `CAFE-008` |
| Health, safety, and privacy | `CAFE-004`, `CAFE-012` |
| Taiwan localization | `CAFE-010` |
| Time-sensitive information | `CAFE-011` |

## Evaluation procedure

1. Read only the facts, prompt, and relevant prior context for one case.
2. Score Response A independently on all six dimensions.
3. Score Response B independently using the same anchors.
4. Compare weighted totals.
5. Write a short rationale citing the controlling fact and failure mode.
6. Run `src/score.py` to validate score ranges, dimensions, labels, and winner consistency.

## Design controls

- Candidate labels alternate, producing six A wins and six B wins.
- Every case states its evidence explicitly.
- High-risk cases test calibrated refusal instead of generic refusal.
- Scoring code uses only Python's standard library.
- The dataset declares itself synthetic in machine-readable metadata.

## Limits

This is a small portfolio benchmark, not a statistically representative model leaderboard. The responses are synthetic candidates rather than blinded outputs from named production models. A larger study would add multiple raters, agreement metrics, randomized response order, and versioned model outputs.
