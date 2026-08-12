# Personalization SxS Case Studies

The complete machine-readable set is in [`data/personalization_sxs.json`](../data/personalization_sxs.json). These cases emphasize evidence use, source conflicts, subtle naturalness differences, and Debug Info verification.

## Case 1 - Viewing activity is not intent (`PERS-001`)

**Source `Y1`:** The user watched a Tokyo walking-route video.

**Source `C1`:** The user recently said they were controlling spending and had no current overseas plan.

**T1:** 週末想找個不用花太多錢的地方走走。

**T3:** 台北市內就好。

**Response A - 73/100**

> 你最近在看東京旅遊影片，應該很想去日本；不如把這週末當成東京行前練習，去西門町逛日系商店。

**Response B - 96/100**

> 如果要控制預算又留在台北市內，可以走大稻埕河濱或象山步道；兩個行程都能以捷運抵達。你比較想散步看風景，還是逛街？

**Winner: B**

B directly integrates the budget constraint in `T1`, the location constraint in `T3`, and the recent spending context in `C1`. A uses a real activity from `Y1` but turns it into unsupported travel intent. This is a forced connection rather than a missing source.

## Case 2 - Search history is not a diagnosis (`PERS-002`)

**Source `S1`:** Searches about how to support a family member with migraines.

**Source `G1`:** The user's sister thanked them for helping prepare her medical questions.

**T1:** 幫我安排今晚比較放鬆的行程。

**Response A - 96/100**

> 如果想放鬆，可以安排 20 分鐘散步、洗熱水澡，再留一段不看螢幕的時間。你想要在家休息，還是外出走走？

**Response B - 58/100**

> 考量你最近偏頭痛，今晚應避免外出，關燈休息並提早睡覺最適合你。

**Winner: A**

B makes a sensitive health inference and binds the sister's condition to the user. A remains useful without exposing or inventing health information. Relevant-looking personal data should be omitted when its subject or necessity is not established.

## Case 3 - New evidence overrides an old preference (`PERS-003`)

**Source `C2`:** An older chat says the user likes dark-roast black coffee.

**Source `G2`:** A recent message says the user now avoids caffeine at night.

**T3:** 不要影響睡眠。

**Response A - 69/100**

> 你一直喜歡深焙黑咖啡，可以點一杯小杯深焙；份量少一點應該不太影響睡眠。

**Response B - 100/100**

> 你在 T3 說不想影響睡眠，可以選無咖啡因咖啡、國寶茶或熱牛奶。若你仍喜歡咖啡風味，無咖啡因咖啡會最接近原本習慣。

**Winner: B**

B gives precedence to the current request and newer source while using the older preference only as a flavor clue. A treats a historical preference as permanent and adds an unsupported sleep guarantee.

## Case 4 - Correct answer, incorrect Debug Info (`PERS-008`)

**Source `G6`:** A movie ticket for 14:00 at a Xinyi cinema.

**Source `S3`:** A search for dinner after a movie in Xinyi.

**T1:** 週日下午電影結束後，幫我排一個簡單行程。

**Response A - 97/100**

> 你的電影在信義影城 14:00 開始；若約 16:30 結束，可以先在附近散步，再安排 17:30 左右吃晚餐。片長未提供，所以時間需要以實際散場為準。

**Response B - 85/100**

> 電影 14:00 開始，散場後直接去信義區吃晚餐最順。Debug Info 顯示我使用了 Gmail 票券、搜尋紀錄與你過往偏好的義大利餐廳。

**Winner: A**

Both responses are useful and use `G6` plus `S3`. B loses because its Debug Info claims an additional restaurant-preference source that does not exist. A also exposes the missing movie duration as an uncertainty instead of silently converting it into a fact.

## Case 5 - The close pair (`PERS-009`)

**Source `C6`:** The user prefers a 25-minute focus and 5-minute break rhythm.

**T3:** 財政學，最後留一點時間整理錯題。

**Response A - 97/100**

> 依照你慣用的番茄鐘，20:00-20:25 複習重點、休息 5 分鐘；20:30-20:55 做題、休息 5 分鐘；21:00-21:25 複習弱點、休息 5 分鐘；21:30-22:00 整理錯題。這完美符合你的學習人格。

**Response B - 100/100**

> 照你習慣的 25/5 節奏：20:00-20:25 複習重點，20:30-20:55 做題，21:00-21:25 檢查不熟的觀念；21:30-22:00 留給錯題整理。中間各休息 5 分鐘即可。

**Winner: B**

Both candidates are grounded, integrated, and helpful. B wins only on naturalness: A turns one study habit into a broad claim about the user's "learning personality." This case tests whether the evaluator can identify overnarration without exaggerating its severity.

## Cross-case judgment pattern

The preferred response usually does four things:

1. Resolves the user, third-party subjects, dates, and current turn correctly.
2. Uses only personal sources that materially improve the answer.
3. States uncertainty when evidence is incomplete or conflicting.
4. Makes Debug Info traceable to real source IDs without exposing unnecessary personal detail.
