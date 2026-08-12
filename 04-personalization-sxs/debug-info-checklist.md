# Debug Info Verification Checklist

Debug Info is evaluated as evidence, not decoration. A response can be useful and still fail traceability when its claimed source use cannot be reproduced.

## Per-response verification

- [ ] List every claimed source ID.
- [ ] Confirm that each claimed ID exists in the case source bundle.
- [ ] Confirm that the source belongs to the correct person or entity.
- [ ] Confirm that the source timestamp is appropriate for the current request.
- [ ] Compare claimed sources with the facts actually used in the response.
- [ ] Flag available relevant sources that were ignored.
- [ ] Flag sources named in Debug Info but absent from the bundle.
- [ ] Flag conclusions that go beyond what the source supports.
- [ ] Record the exact turn IDs affected by each issue.

## Issue labels

| Label | Meaning |
|---|---|
| `missing_source` | Debug Info claims a source ID that does not exist. |
| `unused_claimed_source` | A source is named but has no visible relationship to the answer. |
| `relevant_source_omitted` | An available source would materially change the answer but was ignored. |
| `identity_mismatch` | The source belongs to another person or entity. |
| `recency_mismatch` | A stale source is preferred over newer direct evidence without explanation. |
| `unsupported_inference` | The source exists but does not justify the conclusion drawn from it. |

## Pass condition

Debug Info passes only when every claimed source exists, is correctly attributed, and supports the statement it is used to justify. More sources do not earn a higher score by themselves.
