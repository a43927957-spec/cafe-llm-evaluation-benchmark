# Recommendations

The benchmark suggests four practical controls for a customer-service LLM.

## 1. Bind claims to evidence

Require every policy, promotion, branch attribute, and operating hour to come from an approved fact record. When the fact is missing, the model should ask a focused question or route to staff rather than fill the gap.

## 2. Separate answers from actions

The model may draft a reservation request or lost-item inquiry, but it must not say the action succeeded without a confirmed tool result. User-visible wording should distinguish:

- `I can help prepare the request.`
- `The request was accepted by the system.`

## 3. Add deterministic risk gates

Allergy, payment, privacy, and identity-related prompts should trigger stricter response rules before generation. These gates should prevent absolute safety claims and third-party data disclosure.

## 4. Evaluate context binding

Tests should include multiple branches, dates, pronouns, and policy exceptions. Retrieval of a true fact is not enough; the system must attach it to the correct entity and time.

## Suggested next version

- Expand from 12 to 50 cases.
- Collect blinded outputs from at least two named models.
- Add a second human rater and report agreement.
- Track critical failures separately from average score.
- Add regression cases whenever a real evaluator overturns an automated judgment.

This turns evaluation from a one-time demo into an error-driven learning loop: failure → corrected judgment → reusable rule → regression case.
