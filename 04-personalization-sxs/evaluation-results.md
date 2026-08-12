# Personalization SxS Evaluation Results

Validated with:

```bash
python3 src/score.py --track personalization
```

| Case | Primary issue | A | B | Winner | Decision margin |
|---|---|---:|---:|:---:|---:|
| `PERS-001` | Viewing activity treated as travel intent | 73 | 96 | B | 23 |
| `PERS-002` | Family member's health attributed to user | 96 | 58 | A | 38 |
| `PERS-003` | Old preference used over newer evidence | 69 | 100 | B | 31 |
| `PERS-004` | Newer conflicting source ignored | 97 | 74 | A | 23 |
| `PERS-005` | Correct but intrusive overpersonalization | 81 | 96 | B | 15 |
| `PERS-006` | Relevant personal constraints ignored | 100 | 69 | A | 31 |
| `PERS-007` | Third-party attribute transferred to user | 48 | 100 | B | 52 |
| `PERS-008` | Debug Info claims a missing source | 97 | 85 | A | 12 |
| `PERS-009` | Subtle overnarration in a strong pair | 97 | 100 | B | 3 |
| `PERS-010` | Too many sources forced into response | 96 | 72 | A | 24 |

## Aggregate result

- Cases: 10
- Candidate responses: 20
- Dimension-level ratings: 120
- A wins: 5
- B wins: 5
- Ties: 0
- Debug Info comparisons: 20
- Dataset validation: PASS

The balanced A/B labels are a presentation control, not a model-performance claim.

## Findings

1. **Personalization quality is not source count.** `PERS-010` shows that adding more available sources can make an answer less grounded and less natural.
2. **Subject binding is a critical error class.** `PERS-002` and `PERS-007` demonstrate how family-member data can be incorrectly transferred to the user.
3. **Recency and current-turn evidence matter.** `PERS-003` and `PERS-004` require the evaluator to resolve stale or conflicting sources instead of choosing one silently.
4. **Correct facts can still feel wrong.** `PERS-005` is grounded but loses because it reveals unnecessary personal detail and adds relationship assumptions.
5. **Debug Info is independently testable.** `PERS-008` has two useful answers, but one claims a source that does not exist.
6. **Close pairs reveal evaluator precision.** `PERS-009` differs by only three points and turns on one unsupported phrase, not on factual correctness.

## Recommended quality controls

- Bind every personal claim to a source ID, subject, and timestamp.
- Give current-turn statements and newer direct evidence precedence over older behavioral traces.
- Treat searches and viewing history as weak signals, not proof of identity or intent.
- Score restraint separately so a factually grounded response can still fail for intrusive overuse.
- Compare Debug Info claims with the source bundle as a separate review step.
- Add every overturned evaluator judgment as a future regression case.
