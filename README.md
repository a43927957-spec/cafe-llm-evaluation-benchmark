# Traditional Chinese LLM Evaluation Portfolio  
# 繁體中文大型語言模型評估作品集

> Source-grounded SxS judgment, Traditional Chinese semantic analysis, and reproducible evaluation artifacts.  
> 以來源為依據的雙回答判斷、繁體中文語意分析，以及可重跑的評估產物。

這份作品集現在分成兩個核心證據層：

1. **Source-Grounded SxS Evaluation（來源導向的雙回答評估）**：四個合成職務模擬案例，Winner 與核心理由由作者本人以繁體中文獨立完成。
2. **Archived Gemini Product Evaluation（保存的 Gemini 產品評估）**：使用咖啡廳專案留下的真實推論產物，分析繁體中文否定、指涉、並列問句、限定詞與回答直接性等失敗。

## Start here（建議閱讀順序）

- **主作品：** [四個作者親自判斷的 Source-Grounded SxS 案例](00-source-grounded-sxs/README.md)
- **機器可讀版：** [Source-Grounded SxS JSON](data/source_grounded_sxs.json)
- **真實產品證據：** [Gemini 繁體中文六個語意案例](05-gemini-zh-semantics/analysis-zh.md)
- **English recruiter summary：** [Gemini English key findings](05-gemini-zh-semantics/key-findings-en.md)
- **評估規則：** [Rubric 與診斷方法](rubric.md)

## Core portfolio map（核心作品地圖）

| Track | Data type | What is human-judged | Main skills demonstrated |
|---|---|---|---|
| Source-Grounded SxS | Synthetic role simulation | Winner and core reasoning for all 4 cases | Current-turn priority, recency, grounding, source weighting, risk calibration, Debug Info, reference challenge |
| Gemini semantic audit | Synthetic prompts + archived real inference artifacts | Evidence boundaries, diagnoses, and case reasoning are inspectable | Negation, discourse reference, schema loss, qualifier coverage, answer directness |
| Reproducible benchmark | Structured JSON + Python validation | Methods and outputs are auditable | Data validation, regression testing, attribution boundaries |

## Source-Grounded SxS highlights（雙回答評估重點）

| Case | Decision | Key judgment |
|---|:---:|---|
| Current request vs stale coffee preference | A | 當前輪與近期直接陳述高於舊偏好；搜尋紀錄不能證明穩定意圖 |
| Discovery before demo | B | 需求尚未收斂時，先問真實事件，避免 Demo 造成錨定 |
| Knee-injury return to running | B | 走路不痛不等於能承受 5 公里；高風險情境提高證據門檻 |
| Demo request with flawed reference answer | B | 客戶有興趣不等於已具購買意圖；參考答案的成本與轉換率假設無依據 |

完整判斷與來源核對見 [00-source-grounded-sxs](00-source-grounded-sxs/README.md)。

## Gemini Traditional Chinese semantic audit（Gemini 繁體中文語意審查）

主分析取自既有咖啡廳產品 Eval 保存結果。測試提示為合成情境，不含真實顧客訊息；其中三案是可確認的 Gemini API 結構化輸出，另外三案是包含抽取、檢索、路由與 deterministic renderer（確定性回覆器）的端到端系統輸出。

原始 artifact 沒有保存精確 Gemini model ID，因此本作品不猜測版本，也不把整個系統的錯誤全部歸咎於模型。

| Case | User meaning | Observed failure | Diagnosis layer |
|---|---|---|---|
| 咖啡不要太搶 | 咖啡感不要主導 | 抽成 `coffee_forward`，偏好方向相反 | Model extraction |
| 那酒精的也算嗎 | 酒精飲品是否適用上一輪折扣 | 被「酒精」拉去 safety domain | Model extraction |
| 沒選焙度會預設哪個 | 問上一輪商品的預設屬性 | 把焙度當成商品實體 | Model extraction |
| 可以換嗎？要加價嗎？ | 更換資格與加價兩題都要回答 | 遺失 surcharge 子問題 | Semantic representation |
| 大型犬可以坐哪裡 | 體型限制與座位區域 | 只回通用寵物規則 | Evidence coverage |
| 是不是一定都很酸 | 先回答「不一定」 | 有知識但沒有回答是或不是 | Answer realization |

### Iteration evidence（迭代證據）

| System stage | Valid output | Exact frame | Core semantics |
|---|---:|---:|---:|
| Initial 30 prompts × 3 runs | 27 / 90 | 15 / 90 | 27 / 90 |
| After canonical prompt revision | 72 / 90 | 45 / 90 | 63 / 90 |
| Query Frame v2, 30 × 3 | 90 / 90 | 90 / 90 | 90 / 90 |
| Query Frame v2, full 96 | 96 / 96 | 86 / 96 | 96 / 96 |

這些數字描述 prompt、schema 與受控上下文一起調整後的系統迭代，不是 Gemini 模型版本比較。

端到端產品 gate 仍為 **NO-GO**：

- 96 題中只有 46 題產生顧客可見回覆，50 題沉默。
- 34 題具備可回答條件，但只有 26 題真的回答。
- 至少 5 題仍有必要限定條件未被證據覆蓋。

核心結論是：**frame exact（結構完全相符）不等於產品可上線。** 還必須檢查可回答性、限定詞覆蓋、回答直接性，以及每個明問子句是否真正有著落。

## Evaluation method（評估方法）

1. **Current-turn priority（當前輪優先）**：目前的明確要求高於歷史偏好。
2. **Recency with relevance（新近性與相關性）**：較新資料通常優先，但必須真的能控制當前結論。
3. **Proposition and polarity（命題與極性）**：保留肯定、否定、程度與條件方向。
4. **Reference and discourse（指涉與語篇）**：確認「那個」「也算嗎」等省略形式綁到正確前文。
5. **Sub-question coverage（子問題覆蓋）**：每個明問子句都有答案、釐清或轉接。
6. **Evidence threshold（證據門檻）**：健康、安全與不可逆決策需要更保守的結論。
7. **Attribution boundary（歸因邊界）**：區分模型抽取、schema、檢索、證據與 renderer。
8. **Reference audit（參考答案審查）**：標準答案本身若加入無依據假設，也應被推翻。

## Repository structure（倉庫結構）

```text
00-source-grounded-sxs/
  README.md

05-gemini-zh-semantics/
  analysis-zh.md
  key-findings-en.md

04-personalization-sxs/            # Legacy synthetic supporting track
03-cafe-llm-benchmark/             # Legacy synthetic supporting track
02-hallucination-analysis/
01-response-comparison/

data/
  source_grounded_sxs.json
  gemini_zh_semantics.json
  personalization_sxs.json
  evaluations.json

src/
  semantic_audit.py
  score.py

tests/
  test_semantic_audit.py
  test_score.py

rubric.md
```

## Reproduce and validate（重跑與驗證）

只需 Python 3.10 以上，不需第三方套件：

```bash
python3 src/semantic_audit.py
python3 src/score.py
python3 -m unittest discover -s tests -v
```

## Data and provenance（資料與來源說明）

- Source-Grounded SxS 的情境、來源、對話與回答全部為合成資料，不是任何公司的專有 assessment。
- 四個新案例的 Winner 與核心理由由作者本人完成；英文摘要與術語標籤只是同一判斷的結構化呈現。
- Gemini 語意主軌使用真實保存的推論輸出，但輸入提示仍是合成測試案例。
- 不含真實顧客訊息、正式環境對話、API key、token 或可辨識店家資料。
- 公開資料只保留診斷所需的最小欄位。
- `04-personalization-sxs` 與早期咖啡廳合成軌暫時保留作為 legacy supporting material（舊版輔助材料），**不計入四個作者親自盲審的核心案例**。
- 本作品不是官方 Gemini benchmark，也不是過往付費標註工作的冒充。

## English summary

This portfolio combines four author-judged, source-grounded pairwise evaluation exercises with archived Gemini product-evaluation evidence. The SxS track demonstrates current-turn priority, recency handling, weak-signal restraint, risk calibration, source auditing, and the ability to reject an unsupported reference answer. The Gemini track analyzes real saved inference artifacts while preserving clear boundaries between direct model outputs and end-to-end system behavior.
