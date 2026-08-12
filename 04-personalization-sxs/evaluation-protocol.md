# Personalization SxS Evaluation Protocol

## Objective

Evaluate whether a model uses personal context only when it is relevant, correctly attributed, current, and helpful. The primary question is not whether the response mentions personal data. It is whether the response improves because of the right evidence without becoming intrusive or making unsupported inferences.

This track is designed around three primary dimensions:

- **Grounding:** Are statements about the user supported by a named source or conversation turn?
- **Integration:** Did the model combine the relevant sources and current request without ignoring conflicts?
- **Helpfulness:** Did personalization materially improve the answer or next step?

Naturalness, personalization restraint, and source traceability are supporting dimensions.

## Evaluation unit

Each case contains:

1. A synthetic source bundle with stable source IDs such as `G1` for Gmail, `C1` for a chat summary, `S1` for Search, and `Y1` for YouTube activity.
2. A one-to-five-turn conversation with stable turn IDs.
3. Two candidate responses presented as Response A and Response B.
4. Six dimension ratings, a pairwise winner, and a written rationale.
5. A Debug Info comparison between claimed and verified sources.
6. Constructive feedback and an explicit cleanup requirement.

## Blind pairwise procedure

1. Read the current conversation before reviewing any personal sources.
2. Mark the explicit user request and constraints by turn ID.
3. Review the source bundle and record the subject, timestamp, and confidence of each fact.
4. Score Response A without reading the expected winner.
5. Score Response B using the same anchors.
6. Compare the responses side by side for subtle differences in naturalness, overnarration, and unnecessary disclosure.
7. Write a defensible rationale that cites at least one turn ID and one source ID.
8. Verify Debug Info by comparing claimed source IDs with the case source bundle.
9. Record actionable feedback, then perform the data-hygiene checklist.

## Evidence precedence

When sources disagree, use this order as a review heuristic rather than an automatic rule:

1. The user's current-turn statement.
2. A newer, direct source about the same subject.
3. An older direct source.
4. Behavioral traces such as searches or video views.

Behavioral traces can indicate possible interest, but they do not by themselves prove identity, intent, diagnosis, purchase, travel plans, or stable preference.

## Winner rule

The weighted total supports consistency; it does not replace judgment. A response may lose despite being fluent when it:

- attributes another person's data to the user;
- converts a search or view into a sensitive inference;
- uses stale information while ignoring a newer conflict;
- invents a source in Debug Info;
- exposes more personal detail than the answer needs; or
- forces multiple sources into an answer that would be clearer without them.

For close pairs, the rationale must explain the smallest material difference rather than restating the scores.

## Scope and limitations

- All sources and identities are synthetic.
- No live Google account, Gemini history, or customer data is used.
- Candidate responses are authored work-sample examples, not blinded outputs from named production models.
- The track demonstrates evaluation judgment and protocol design; it is not a statistically representative model benchmark.
