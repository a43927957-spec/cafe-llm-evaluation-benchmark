# Source-Grounded SxS Evaluation  
# 來源導向的雙回答評估

> Four synthetic role-simulation cases independently judged by the author before professional formatting.  
> 四個合成職務模擬案例；勝負與核心理由由作者以繁體中文獨立完成。

## Purpose（目的）

這一軌直接展示 LLM evaluator（大型語言模型評估員）工作中最重要的判斷能力：比較兩個候選回答、檢查來源使用、處理新舊資訊衝突、提高高風險情境的證據門檻，以及在參考答案本身有漏洞時提出可辯護的反駁。

The cases test source-grounded pairwise evaluation: current-turn priority, recency, weak behavioral signals, risk calibration, source traceability, and reference-answer challenge.

## Scope and provenance（範圍與來源說明）

- 所有情境、來源、對話與候選回答都是 **synthetic（合成資料）**，不是正式工作資料、真實顧客資料或任何公司的專有測驗。
- **Winner 與核心 reasoning（勝負與核心判斷）由作者本人以繁體中文獨立完成。**
- 英文理由、錯誤標籤與來源核對，是對同一份作者判斷的結構化呈現。
- Case 2 的原始練習沒有提供 Debug Info，因此不補造來源宣稱，也不評 Source Traceability（來源可追溯性）。
- 沒有為了讓結果好看而強制安排 A/B 各半，也沒有預設 Reference Answer 必然正確。

## Evaluation principles（評估原則）

1. **Current turn first（當前輪優先）：** 使用者現在明講的要求，高於舊偏好。
2. **Recency with relevance（新近性必須兼顧相關性）：** 較新直接陳述通常高於較舊資料，但「新」不等於必然有決定性。
3. **Behavior is a weak signal（行為資料是弱訊號）：** 搜尋或觀看紀錄不能直接證明穩定偏好、意圖或身分。
4. **Risk changes the evidence threshold（風險改變證據門檻）：** 健康、安全與不可逆決策需要更保守的結論。
5. **Reference answers are auditable（參考答案也必須接受審查）：** 若理由加入來源未支持的假設，評估者應明確反駁。

## Case index（案例索引）

| Case | Main skill | Verdict |
|---|---|:---:|
| SG-SXS-001 | Current-turn priority, recency, unsupported inference | A |
| SG-SXS-002 | Discovery before solutioning, anchoring risk | B |
| SG-SXS-003 | Health-risk calibration, evidence relevance | B |
| SG-SXS-004 | Buying intent vs interest, reference challenge | B |

---
## SG-SXS-001｜當前需求與舊偏好衝突

**English title:** Current-Turn Priority Over Stale Preference  
**Case type:** `source_conflict_and_personalization`  
**Data status:** Synthetic role-simulation case（合成職務模擬案例）  
**Author verdict:** **A**

### User request

> 我週六下午想在台北找個地方讀書兩小時。安靜、有插座最好，交通方便一點，我下午不太想喝咖啡。

### Available sources

- **C1｜conversation｜2026-03-12：** 我很喜歡精品手沖，去咖啡廳通常都會點咖啡，200 多塊可以接受。
- **C2｜conversation｜2026-08-12：** 最近睡眠有點亂，所以我下午開始盡量不碰咖啡因。
- **K1｜calendar｜2026-08-22：** 14:00–15:00 牙醫，地點在忠孝新生站附近。
- **S1｜search_activity｜2026-08-01：** 搜尋「台北 24 小時咖啡廳」。

### Candidate responses

#### Response A

> 你下午 3 點左右會在忠孝新生附近，我會優先找忠孝新生站步行 5–10 分鐘、安靜而且有插座的咖啡廳，這樣不用再特別轉車。另外你最近下午在避免咖啡因，所以不用特別找精品手沖店，可以優先看有無咖啡因飲品、氣泡飲或茶類選擇的店。如果要讀兩小時，我也會再確認店家的限時與插座規則。

**Declared Debug Info:** `K1, C2`

#### Response B

> 你本來就很喜歡精品手沖，而且可以接受 200 多元的價格，所以我會推薦你找忠孝新生附近的精品咖啡廳。你之前也搜尋過台北 24 小時咖啡廳，看起來你應該很喜歡可以長時間待著的店，因此可以優先找不限時、有插座的店。點一杯淺焙手沖，找個安靜角落讀兩小時，應該會很適合你。

**Declared Debug Info:** `C1, S1, K1`

### Author judgment（作者判斷）

A 優先遵守使用者當前明確說出的「下午不太想喝咖啡」，並以較新的 C2 支持避免咖啡因；K1 也能實際降低交通成本。B 讓舊偏好 C1 覆蓋當前需求，還把一次 24 小時咖啡廳搜尋推論成長時間停留偏好，最後推薦淺焙手沖，直接踩中使用者當前限制。

### Recruiter-facing English rationale

Response A is better because it follows the user's current request and the more recent caffeine-avoidance evidence, while using the calendar location to reduce travel friction. Response B overweights an older coffee preference and turns a single search into an unsupported long-stay preference. Its final recommendation directly conflicts with the user's stated wish to avoid coffee that afternoon.

### Failure tags

- **A:** None
- **B:** `current_turn_ignored`, `recency_mismatch`, `unsupported_inference`

### Source audit

- **A:** Declared sources exist and directly support the location and caffeine claims.
- **B:** Declared sources exist, but S1 does not prove a stable long-stay preference and C1 should not override the current turn and C2.

---

## SG-SXS-002｜需求未明時先探索，還是先展示

**English title:** Discovery Before Demo  
**Case type:** `business_decision_and_source_weighting`  
**Data status:** Synthetic role-simulation case（合成職務模擬案例）  
**Author verdict:** **B**

### User request

> 我下週要跟一個潛在客戶談 AI 導入，他們是傳產公司。對方一直說「管理很亂」，但講不出具體問題。你覺得我第一次會議應該直接 Demo，還是先問問題？

### Available sources

- **C1｜conversation｜earlier：** 使用者以前做業務時喜歡先展示產品，因為覺得「看到東西比較容易理解」。
- **C2｜conversation｜recent：** 最近一次跟 B2B 客戶交流後，使用者認為高單價服務不應該急著成交，而要先讓客戶自己講出具體痛點。
- **N1｜meeting_note｜current：** 這家潛在客戶約 80 人，老闆只說「管理問題很多」，目前沒有整理出明確需求，也沒有提供內部資料。

### Candidate responses

#### Response A

> 我會先 Demo。因為對方現在連自己要什麼都不知道，單靠問問題可能很難讓他描述清楚。你可以先展示 2～3 個常見的 AI 管理案例，例如自動整理報表、內部知識查詢、流程提醒，讓他看到具體畫面後，再問「哪一個最像你現在的問題？」這樣可以降低對方描述抽象需求的難度，也能加快會議進入具體討論。

**Declared Debug Info:** Not provided in the original exercise（原始題目未提供）

#### Response B

> 我會先問問題，不急著 Demo。「管理很亂」目前只是非常模糊的症狀，如果先展示產品，很容易讓客戶沿著你的功能去描述需求，最後得到的是被 Demo 引導出來的答案，而不是真正的問題。我會先追問一個具體事件，例如：「最近一次因為管理混亂而造成損失、延誤或客訴，是發生什麼事？」等對方講出真實流程後，再決定要不要展示對應的 Demo。

**Declared Debug Info:** Not provided in the original exercise（原始題目未提供）

### Author judgment（作者判斷）

B 更符合使用者已更新的 B2B 方法：C2 應高於較舊的 C1。N1 也明確顯示需求、資料與問題邊界都尚未收斂；先展示功能容易讓客戶被既有選項錨定，得到供應商引導出的答案。B 先要求一個具體失敗事件，再決定是否展示對應 Demo，決策邏輯更可靠。

### Recruiter-facing English rationale

Response B better reflects the user's updated B2B approach and the client's unresolved problem definition. A feature-first demo could anchor the client to the supplier's examples and produce a shaped answer rather than a genuine need. Asking for a concrete recent failure creates a stronger basis for any later demo.

### Failure tags

- **A:** `stale_preference_overweighted`, `anchoring_risk`, `premature_solutioning`
- **B:** None

### Source audit

- **A:** The original exercise did not include declared Debug Info; source use is inferred and source traceability is not scored.
- **B:** The original exercise did not include declared Debug Info; source use is inferred and source traceability is not scored.

---

## SG-SXS-003｜高風險情境下的證據門檻

**English title:** Evidence Threshold in a Health-Risk Scenario  
**Case type:** `risk_calibration_and_evidence_relevance`  
**Data status:** Synthetic role-simulation case（合成職務模擬案例）  
**Author verdict:** **B**

### User request

> 我最近很想開始跑步，但膝蓋以前受過傷。我想先從一週跑三次、每次 5 公里開始，你覺得可以嗎？

### Available sources

- **C1｜conversation｜2026-02-10：** 我以前固定一週跑 3～4 次，一次差不多 5 公里。
- **C2｜conversation｜2026-07-28：** 去年右膝受傷後就幾乎沒跑了，最近走路已經沒什麼感覺，但還沒有重新做過跑步測試。
- **H1｜health_note｜2026-08-02：** 目前日常走路無明顯疼痛；沒有提供醫師診斷、復健完成證明或運動測試結果。

### Candidate responses

#### Response A

> 你以前本來就有一週跑 3～4 次、每次約 5 公里的基礎，而且現在走路已經沒有明顯疼痛，所以一週三次、每次 5 公里應該可以作為重新開始的目標。前一兩週可以稍微放慢速度，如果膝蓋又開始不舒服，再減少距離或休息。

**Declared Debug Info:** `C1, C2, H1`

#### Response B

> 我不會直接從每次 5 公里開始。你以前雖然有這個跑量，但受傷後已經很久沒有跑，而且目前只有「走路不痛」的資訊，這不能證明膝蓋已經能承受連續跑步的負荷。比較保守的方式是先從短時間的跑走交替開始，觀察跑步當下以及之後膝蓋的反應，再逐步增加。如果之前的膝傷比較嚴重、仍有腫脹、卡住、無力等情況，應先讓專業醫療人員評估。

**Declared Debug Info:** `C2, H1`

### Author judgment（作者判斷）

B 較好。H1 是目前最能限制結論的證據：走路不痛不能證明能承受連續 5 公里跑步，而缺少診斷、復健完成證明與跑步測試時，模型不應給出接近放行的結論。C1 只證明受傷前的能力，與受傷後的安全起始量沒有直接關係，因此在當前決策中應降低權重。

### Recruiter-facing English rationale

Response B is better because pain-free walking does not establish readiness for repeated five-kilometer runs after a knee injury. The older training history describes prior capacity, not current load tolerance. In a health-risk context with missing clinical and functional evidence, the answer should remain conservative and explicitly acknowledge uncertainty.

### Failure tags

- **A:** `evidence_overreach`, `historical_capability_misapplied`, `high_risk_overconfidence`
- **B:** None

### Source audit

- **A:** The sources are real and traceable, but the answer overextends what C1 and H1 can support.
- **B:** Declared sources directly support the uncertainty and conservative recommendation.

---

## SG-SXS-004｜當參考答案本身也有漏洞

**English title:** Rejecting an Unsupported Reference Answer  
**Case type:** `reference_challenge_and_business_qualification`  
**Data status:** Synthetic role-simulation case（合成職務模擬案例）  
**Author verdict:** **B**

### User request

> 這個傳產客戶叫我下週直接做一個 Demo 給他看，但我現在不太想再免費做一堆東西。我希望先確認他到底有沒有預算跟真實需求，再決定投入多少時間。你覺得我要答應做 Demo 嗎？

### Available sources

- **C1｜conversation｜2026-04-20：** 我以前談案子很喜歡直接做東西給客戶看，我覺得 Prototype 做出來最快。
- **C2｜conversation｜2026-08-14：** 最近我開始覺得 B2B 高單價案不應該急著證明自己，最好先讓客戶講出具體問題，再投入工程資源。
- **N1｜meeting_note｜current：** 客戶說：「AI 感覺很有趣，你們下週能不能先做一版給我們看看？」尚未討論預算、採購流程、決策人、具體 KPI。
- **N2｜sales_note｜current：** 客戶目前只有老闆表達興趣，尚未確認實際使用部門。

### Candidate responses

#### Response A

> 可以答應，但把 Demo 控制得非常小。客戶已經主動要求看 Demo，而你過去也很擅長用 Prototype 幫助對方理解。可以只花半天做一個簡單版本，用它換取下一次深入討論的機會。這樣既能維持客戶熱度，也不需要投入太多資源。

**Declared Debug Info:** `C1, N1`

#### Response B

> 我不會立刻答應做 Demo。現在連預算、決策人、使用部門與具體問題都還沒確認，直接做東西很可能只是替「有興趣」買單。我會先回覆客戶：可以做，但希望先花 30 分鐘確認實際使用場景、現在怎麼處理、問題造成什麼成本，以及誰會決定是否採用。確認值得投入後，再決定 Demo 要做到什麼程度。

**Declared Debug Info:** `C2, N1, N2`

### Provided reference answer

**Reference winner:** **A**

> 客戶明確要求 Demo，而且 C1 顯示使用者擅長用 Prototype 推進銷售。半天的投入成本有限，能提高成交機率。

### Author judgment（作者判斷）

B 更接近可靠答案。當前需求與 C2 都明確要求先確認預算、真實需求與投入邊界，應優先於 C1 的舊習慣。N1 只證明客戶參與度與興趣高，不能證明購買意圖或商機成熟；預算、決策人、使用部門與 KPI 均未確認。B 沒有拒絕 Demo，而是先設一道資格門檻。參考答案則額外假設「半天成本有限」與「Demo 會提高成交率」，來源沒有支持。

### Recruiter-facing English rationale

Response B is stronger because it distinguishes client interest from qualified buying intent. The current request and the newer preference both require a qualification step before engineering work, while the budget, decision-maker, user department, and KPI remain unknown. The reference answer relies on unsupported assumptions that half a day is a limited cost and that an early demo will improve conversion.

### Failure tags

- **A:** `current_turn_ignored`, `stale_preference_overweighted`, `premature_commitment`
- **B:** None
- **reference:** `unsupported_assumption`, `interest_buying_intent_conflation`

### Source audit

- **A:** Declared sources exist, but C1 is stale relative to the current turn and C2; N1 supports interest, not qualification.
- **B:** Declared sources directly support the qualification gate.
- **reference:** The claimed cost and conversion benefits are not supported by the source bundle.

---

## Machine-readable data（機器可讀資料）

The same four cases are available in [`../data/source_grounded_sxs.json`](../data/source_grounded_sxs.json), including source bundles, candidate responses, declared source usage, author verdicts, rationales, failure tags, and source audits.

## What this track demonstrates（這一軌證明什麼）

這組案例不以背誦術語為核心，而是把 evaluator judgment（評估判斷）拆成可檢查的決策：

- 哪一筆證據真正控制結論。
- 某筆資料雖然是真的，是否被錯誤地提高權重。
- 回答是否尊重當前要求，而不是被歷史記憶牽走。
- 推論是否超出來源能支持的範圍。
- 高風險情境是否把不確定性說清楚。
- 參考答案是否偷偷加入成本、轉換率或購買意圖等無依據假設。
