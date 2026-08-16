# 繁體中文 LLM 評估作品集

> 一份可重跑、可檢查的繁體中文（台灣）作品，對應 AI Quality Analyst、LLM Evaluator 與 AI Trainer 類型職務。

這個作品集包含兩條互補的評估軌：

1. **個人化回答 SxS 評估**：以合成的對話、Gmail、Search 與 YouTube 類型來源，進行一至五輪的並排回答比較。
2. **有依據的客服回答評估**：根據明確的店家事實、政策限制、安全規則與對話上下文，比較兩個候選回答。

主作品是個人化回答評估，重點不是「有沒有提到個人資料」，而是個人脈絡是否有來源、歸屬正確、仍然有效、融入自然、真的有幫助，並且能用 `Debug Info` 追溯。咖啡廳客服評估則展示我對政策依據、幻覺、安全、隱私與上下文綁定的判斷方式。

**語言說明：** 人工閱讀內容以繁體中文為主，因為這是我能直接判斷語氣、細節與在地用法的工作語言。英文保留在程式碼、資料欄位、常用評估術語，以及頁尾一段由 AI 協助校訂的簡短摘要；本作品不主張流利英文能力。

## 這份作品呈現什麼

- 設計一至五輪的個人化測試案例
- 逐輪、逐來源比較兩個候選回答並寫出判斷理由
- 評估事實依據（Grounding）、整合品質（Integration）與實用性（Helpfulness）
- 找出錯誤個人化、身分綁定錯誤、過時偏好與牽強連結
- 在兩個回答都不差時，辨識不自然、過度敘述等細微差異
- 依穩定的來源 ID 核對 `Debug Info`
- 設計合成資料與評估後清理規則
- 判斷繁體中文（台灣）的在地語氣、隱私與安全風險
- 不使用第三方套件也能重跑計分與結構驗證

## 作品規模

| 項目 | 個人化 SxS | 咖啡廳依據評估 | 合計 |
|---|---:|---:|---:|
| 合成案例 | 10 | 12 | 22 |
| 候選回答 | 20 | 24 | 44 |
| 維度評分 | 120 | 144 | 264 |
| 成對判斷 | 10 | 12 | 22 |
| 來源紀錄 | 19 | - | 19 |
| 對話輪次 | 22 | - | 22 |
| `Debug Info` 比對 | 20 | - | 20 |

兩條評估軌都交錯安排 A、B 標籤，避免某個標籤總是代表較好的回答。

## 評估軌一：個人化回答 SxS 評估

十個合成案例涵蓋：

| 風險 | 代表案例 |
|---|---|
| 把觀看紀錄誤當成使用者意圖 | `PERS-001` |
| 敏感健康推論與身分錯置 | `PERS-002` |
| 舊偏好與較新的直接證據衝突 | `PERS-003` |
| 對話與 Gmail 來源互相矛盾 | `PERS-004` |
| 內容正確但令人不舒服的過度個人化 | `PERS-005` |
| 有相關脈絡卻完全忽略 | `PERS-006` |
| 把第三人的屬性套到使用者身上 | `PERS-007` |
| 回答正確但 `Debug Info` 錯誤 | `PERS-008` |
| 只差一個自然度細節的接近組合 | `PERS-009` |
| 把多個來源硬塞進回答 | `PERS-010` |

建議閱讀順序：

- [評估流程](04-personalization-sxs/evaluation-protocol.md)
- [五個完整 SxS 案例](04-personalization-sxs/case-studies.md)
- [評估結果與發現](04-personalization-sxs/evaluation-results.md)
- [`Debug Info` 核對清單](04-personalization-sxs/debug-info-checklist.md)
- [資料清理流程](04-personalization-sxs/data-hygiene.md)
- [完整機器可讀資料集](data/personalization_sxs.json)

### 個人化評估維度

| 維度 | 權重 | 核心問題 |
|---|---:|---|
| 事實依據（Grounding） | 25% | 每個關於使用者的敘述，是否都有對話輪次或具名來源支持？ |
| 整合品質（Integration） | 20% | 是否正確合併相關來源，並處理來源衝突？ |
| 實用性（Helpfulness） | 20% | 個人化是否真的讓回答更有用？ |
| 自然度（Naturalness） | 15% | 是否為精簡自然的繁中表達，而非刻意炫耀知道多少資料？ |
| 個人化克制（Personalization restraint） | 10% | 是否避免敏感、侵入或牽強的推論？ |
| 來源可追溯性（Source traceability） | 10% | `Debug Info` 是否符合實際可用及真正使用的來源？ |

## 評估軌二：有依據的客服回答評估

原有的咖啡廳評估包含 12 個合成情境，涵蓋政策例外、無依據的操作宣稱、缺少上下文、過敏風險、隱私、資訊時效與台灣在地用語。

- [三個完整客服回答比較](01-response-comparison/case-studies.md)
- [幻覺與失敗類型](02-hallucination-analysis/failure-taxonomy.md)
- [基準設計](03-cafe-llm-benchmark/benchmark-design.md)
- [評估結果](03-cafe-llm-benchmark/evaluation-results.md)
- [產品改善建議](03-cafe-llm-benchmark/recommendations.md)

## 倉庫結構

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

## 重跑與驗證

只需要 Python 3.10 以上版本，不需安裝第三方套件。

```bash
python3 src/score.py
python3 src/score.py --track personalization
python3 -m unittest discover -s tests -v
```

預期結果：

```text
cafe-grounding: 12 cases, 6 A wins, 6 B wins, 0 ties - PASS
personalization-sxs: 10 cases, 5 A wins, 5 B wins, 0 ties - PASS
15 unit tests - PASS
```

## 資料、隱私與製作方式

所有身分、帳號活動、訊息、搜尋、觀看紀錄、店名、政策、對話與模型回答都是合成資料。本倉庫不含任何真實的 Gemini、Gmail、Google Search、YouTube、雇主、店家、顧客或個人帳號資料。

這是一份在 AI 工具協助下完成的自建作品，不是過往付費標註工作，也不是正式上線的模型基準。AI 協助案例初稿、程式碼、格式與英文校訂；公開內容保留評分標準、逐案理由與可重跑驗證，方便招聘者直接檢查判斷是否合理。面試時應以作者能親自說明並接受追問的內容為準。

## 作者

為 [@a43927957-spec](https://github.com/a43927957-spec) 的公開求職作品整理。作者的主要工作語言是繁體中文（台灣），關注 LLM 評估、個人化回答品質與有依據的對話式 AI。

## English summary（AI-assisted）

This is a Traditional Chinese-first portfolio for LLM evaluation roles. It contains reproducible side-by-side evaluations for personalized responses and grounded customer-service answers. AI tools assisted with English polishing; this summary is not a claim of fluent English proficiency.

## 授權

MIT，詳見 [LICENSE](LICENSE)。
