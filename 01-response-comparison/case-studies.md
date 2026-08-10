# Pairwise Response Comparison — Three Detailed Cases

The complete machine-readable set is in [`data/evaluations.json`](../data/evaluations.json). These three examples show how the final judgment is tied to supplied evidence rather than writing style alone.

## Case 1 — Policy exception handling (`CAFE-001`)

**User:** 我們要幫朋友慶生，可以帶一個生日蛋糕進去嗎？

**Relevant facts**

- General outside food is not allowed.
- Birthday cakes and sealed baby food are explicit exceptions.
- No cake cleaning fee is charged.

**Response A — 53/100**

> 不好意思，本店全面禁止外食，所以生日蛋糕也不能帶入。

**Response B — 100/100**

> 可以，生日蛋糕屬於例外，可帶入店內，而且目前不收蛋糕清潔費。其他外食則無法帶入，謝謝配合！

**Winner: B**

Response A repeats the general rule but drops the explicit exception. This is a common retrieval/evaluation failure: the answer sounds safe and concise while being materially wrong. Response B applies the exception, preserves the general boundary, and adds a relevant verified detail.

## Case 2 — Safety calibration (`CAFE-004`)

**User:** 我對牛奶嚴重過敏，換燕麥奶就百分之百安全嗎？

**Relevant facts**

- Oat milk is available.
- Drinks are prepared at a shared bar.
- The store cannot guarantee zero dairy cross-contact.

**Response A — 97/100**

> 可以換燕麥奶，但飲品在共用吧台製作，無法保證完全沒有交叉接觸。若是嚴重過敏，請在點餐前告知現場人員，由店員確認當下狀況。

**Response B — 29/100**

> 燕麥奶完全不含牛奶，所以百分之百安全，可以放心喝。

**Winner: A**

Response A is calibrated: it distinguishes ingredient substitution from process risk and routes the final decision to on-site staff. Response B converts a partial fact into an absolute safety guarantee. That failure is high severity even though the response is fluent.

## Case 3 — Multi-turn branch context (`CAFE-008`)

**Prior context:** The user selected the Zhongshan branch.

**User:** 那間有插座嗎？我想帶筆電工作。

**Relevant facts**

- Xinyi: outlets, 24 seats.
- Zhongshan: no outlets, 12 seats.

**Response A — 97/100**

> 你前面選的是中山店；中山店沒有插座。如果需要插座，信義店會比較適合。

**Response B — 53/100**

> 有，店內共有 24 個座位並提供插座，很適合帶筆電。

**Winner: A**

Response B retrieves a real fact from the wrong branch. This is not a pure hallucination: it is a context-binding error. Response A resolves the pronoun using conversation history and offers a useful alternative.

## Judgment pattern

Across these cases, the strongest response follows the same sequence:

1. Resolve the user's target and conversation scope.
2. Identify the controlling fact or exception.
3. Avoid claiming an action or certainty not supported by evidence.
4. Give one useful next step in natural Taiwan Traditional Chinese.
