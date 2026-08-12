# Data Hygiene Protocol

This portfolio uses only synthetic sources. The protocol below demonstrates the cleanup boundary that would apply to a real personalization evaluation environment.

## Before evaluation

- Work from an isolated evaluation conversation.
- Replace names, email addresses, phone numbers, account IDs, locations, and booking references with synthetic values.
- Assign case-local source IDs instead of retaining account identifiers.
- Capture only the minimum source excerpt required for the judgment.
- Confirm that no unrelated personal content is present in screenshots, exports, or notes.

## During evaluation

- Do not paste source content into third-party tools outside the approved evaluation environment.
- Keep evaluator notes tied to case IDs, turn IDs, and source IDs.
- Do not infer health, identity, relationships, or intent when the source does not explicitly establish them.
- Separate the visible response judgment from the Debug Info verification.

## After evaluation

- Delete the evaluation conversation so it cannot affect later personalization tests.
- Delete temporary screenshots and raw exports.
- Retain only the anonymized case, dimension scores, rationale, issue tags, and source-ID verification result.
- Confirm `cleanup_required: true` for every case and record completion in the run log.

## Portfolio boundary

The committed dataset is fully synthetic and contains no real Gemini, Gmail, Google Search, YouTube, employer, merchant, customer, or personal account data.
