# Gemini Traditional Chinese Semantic Evaluation — Key Findings

> AI-assisted English summary. The complete analysis and evaluator reasoning are written in Traditional Chinese.

## Scope

This case study examines archived outputs from a real Gemini API evaluation runner using synthetic Traditional Chinese prompts. The artifacts confirm the provider, but they do not preserve the exact Gemini model ID. Structured Query Frame outputs are attributed to Gemini; end-to-end replies are labeled as system outputs because retrieval, routing, and deterministic rendering also affected them.

## Six findings

1. Negation polarity: Gemini converted “coffee should not be too dominant” into coffee-forward, potentially reversing the recommendation.
2. Discourse binding: The model recognized a prior-turn reference but allowed the word alcohol to override the active takeout-discount context.
3. Entity versus attribute: It repeatedly treated roast level as a product entity and lost the previous-turn product reference.
4. Coordinated questions: The representation preserved substitution compatibility but dropped the separate surcharge question.
5. Qualifier coverage: A generic pet rule ignored both the large-dog modifier and the seating-location focus.
6. Answer directness: Relevant evidence was given, but the system never directly answered the yes-or-no proposition.

## Iteration evidence

| Evaluation stage | Valid output | Exact frame | Core semantics |
|---|---:|---:|---:|
| Initial 30 prompts × 3 runs | 27 / 90 | 15 / 90 | 27 / 90 |
| After canonical prompt revision | 72 / 90 | 45 / 90 | 63 / 90 |
| Final Query Frame v2, 30 × 3 | 90 / 90 | 90 / 90 | 90 / 90 |
| Final Query Frame v2, full 96 | 96 / 96 | 86 / 96 | 96 / 96 |

These numbers describe a system iteration across prompt, schema, and bounded context. They are not a comparison between Gemini model versions.

The final end-to-end product gate remained NO-GO: only 46 of 96 cases produced visible replies; 50 were silent; only 26 of 34 answerable cases replied; and five qualifier-coverage leaks remained.

## Recommended evaluation method

- Test propositions and polarity, not keywords alone.
- Score discourse reference separately from topic classification.
- Require coverage for every explicit sub-question and qualifier.
- Check directness after grounding and retrieval pass.
- Assign failures to model extraction, semantic representation, evidence coverage, or answer realization before proposing a fix.

For the full evidence and reasoning, read [the Traditional Chinese report](analysis-zh.md).
