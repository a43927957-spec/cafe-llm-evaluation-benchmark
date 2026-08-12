# zh-TW LLM Evaluation Portfolio

> A reproducible Traditional Chinese (Taiwan) work sample for AI Quality Analyst, LLM Evaluator, and AI Trainer roles.

This repository demonstrates two complementary evaluation tracks:

1. **Personalization SxS evaluation** - multi-turn comparison of personalized responses using synthetic chat, Gmail, Search, and YouTube-style sources.
2. **Grounded customer-service evaluation** - response comparison against explicit business facts, policy constraints, safety rules, and conversational context.

The personalization track is the primary work sample. It evaluates whether personal context is grounded, correctly attributed, current, naturally integrated, genuinely helpful, and traceable through Debug Info. The café track remains as evidence of broader policy-grounding and risk-evaluation ability.

**中文說明：** 這是一份繁體中文（台灣）LLM 評估作品集。主軸是個人化回答的多輪 SxS 評估、來源與 Debug Info 核對、錯誤推論及過度個人化分析；另保留咖啡廳客服基準，展示政策、幻覺、安全、隱私與上下文判斷。

## What this work sample demonstrates

- Creative one-to-five-turn personalization test design
- Side-by-side response ranking with turn-level and source-level rationales
- Grounding, Integration, and Helpfulness evaluation
- Incorrect personalization, identity binding, stale preference, and forced-connection detection
- Subtle naturalness and overnarration judgment when both answers are strong
- Debug Info verification against stable source IDs
- Synthetic-data hygiene and post-evaluation cleanup rules
- Taiwan Traditional Chinese localization, privacy, and safety judgment
- Reproducible scoring and structural validation without third-party dependencies

## Portfolio snapshot

| Item | Personalization SxS | Café grounding | Total |
|---|---:|---:|---:|
| Synthetic cases | 10 | 12 | 22 |
| Candidate responses | 20 | 24 | 44 |
| Dimension-level ratings | 120 | 144 | 264 |
| Pairwise decisions | 10 | 12 | 22 |
| Source records | 19 | - | 19 |
| Conversation turns | 22 | - | 22 |
| Debug Info comparisons | 20 | - | 20 |

Candidate labels alternate across both tracks to prevent one label from consistently representing the stronger answer.

## Track 1 - Personalization SxS evaluation

The primary track contains ten synthetic cases covering:

| Risk area | Representative case |
|---|---|
| Viewing activity incorrectly treated as intent | `PERS-001` |
| Sensitive health inference and identity mismatch | `PERS-002` |
| Stale preference versus newer direct evidence | `PERS-003` |
| Conflicting chat and Gmail sources | `PERS-004` |
| Correct but intrusive overpersonalization | `PERS-005` |
| Relevant context available but ignored | `PERS-006` |
| Third-party attributes transferred to the user | `PERS-007` |
| Correct answer with incorrect Debug Info | `PERS-008` |
| Close SxS pair with a subtle naturalness difference | `PERS-009` |
| Multiple sources forced into an answer | `PERS-010` |

Start with:

- [Evaluation protocol](04-personalization-sxs/evaluation-protocol.md)
- [Five detailed SxS case studies](04-personalization-sxs/case-studies.md)
- [Evaluation results and findings](04-personalization-sxs/evaluation-results.md)
- [Debug Info verification checklist](04-personalization-sxs/debug-info-checklist.md)
- [Data hygiene protocol](04-personalization-sxs/data-hygiene.md)
- [Complete machine-readable dataset](data/personalization_sxs.json)

### Personalization dimensions

| Dimension | Weight | Core question |
|---|---:|---|
| Grounding | 25% | Is every statement about the user supported by a turn or named source? |
| Integration | 20% | Are the relevant sources combined correctly without ignoring conflicts? |
| Helpfulness | 20% | Does personalization materially improve the response? |
| Naturalness | 15% | Is the response concise and natural in `zh-TW`, without overnarrating? |
| Personalization restraint | 10% | Does it avoid sensitive, intrusive, or forced inferences? |
| Source traceability | 10% | Does Debug Info match the sources actually available and used? |

## Track 2 - Grounded customer-service evaluation

The original café track contains 12 synthetic scenarios covering policy exceptions, unsupported actions, missing context, allergy risk, privacy, time validity, and Taiwan localization.

- [Three detailed café comparisons](01-response-comparison/case-studies.md)
- [Hallucination and failure taxonomy](02-hallucination-analysis/failure-taxonomy.md)
- [Benchmark design](03-cafe-llm-benchmark/benchmark-design.md)
- [Evaluation results](03-cafe-llm-benchmark/evaluation-results.md)
- [Product recommendations](03-cafe-llm-benchmark/recommendations.md)

## Repository map

```text
01-response-comparison/
02-hallucination-analysis/
03-cafe-llm-benchmark/
04-personalization-sxs/
  evaluation-protocol.md
  case-studies.md
  evaluation-results.md
  debug-info-checklist.md
  data-hygiene.md
data/
  evaluations.json
  personalization_sxs.json
src/
  score.py
tests/
  test_score.py
rubric.md
```

## Run and validate both tracks

Python 3.10+ is sufficient; there are no third-party dependencies.

```bash
python3 src/score.py
python3 src/score.py --track personalization
python3 -m unittest discover -s tests -v
```

Expected validation summary:

```text
cafe-grounding: 12 cases, 6 A wins, 6 B wins, 0 ties - PASS
personalization-sxs: 10 cases, 5 A wins, 5 B wins, 0 ties - PASS
15 unit tests - PASS
```

## Data, privacy, and authorship

All identities, account activity, messages, searches, viewing history, store names, policies, conversations, and model responses are synthetic. This repository contains no real Gemini, Gmail, Google Search, YouTube, employer, merchant, customer, or personal account data.

AI tools assisted with drafting, code generation, and formatting. The evaluation design, case framing, judgment criteria, and published work sample are presented transparently as a portfolio exercise, not as prior paid annotation work or a production benchmark.

## Author

Prepared for the public portfolio of [@a43927957-spec](https://github.com/a43927957-spec), a native Traditional Chinese (Taiwan) speaker focused on LLM evaluation, personalized-response quality, and grounded conversational AI.

## License

MIT - see [LICENSE](LICENSE).
