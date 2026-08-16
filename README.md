# Gemini 繁體中文語意品質分析作品集

> 用真實 Gemini API Eval 證據，找出繁體中文裡會讓產品答反、答偏或漏答的語意失誤。

這份作品不是在證明「模型偶爾會犯錯」，而是在示範我會怎麼把一個中文 AI 失敗拆成可重現、可歸因、可修正的品質問題。

主分析取自既有產品 Eval 的保存結果。測試提示皆為合成情境，不含真實顧客訊息；其中三案是可確認的 Gemini API 結構化輸出，另外三案是包含抽取、檢索、路由與 deterministic renderer 的端到端系統輸出。原始 artifact 沒有保存精確 Gemini model ID，所以本作品不猜測版本，也不把整個系統的錯誤都推給模型。

## 先看這三份

- [完整繁體中文分析：六個案例、證據與根因](05-gemini-zh-semantics/analysis-zh.md)
- [English key findings：只保留招聘者快速掃讀的結論](05-gemini-zh-semantics/key-findings-en.md)
- [機器可讀案例、量化結果與來源雜湊](data/gemini_zh_semantics.json)

## 我找到的中文語意問題

| 案例 | 使用者真正表達的意思 | 系統失誤 | 根因層 |
|---|---|---|---|
| 不要太搶 | 咖啡感不要主導 | 抽成 coffee-forward，偏好方向相反 | 模型抽取 |
| 那酒精的也算嗎 | 酒精飲品是否也適用上一輪折扣 | 被「酒精」關鍵字拉去安全領域 | 模型抽取 |
| 沒選焙度會預設哪個 | 問上一輪商品的預設屬性 | 把「焙度」當成商品實體 | 模型抽取 |
| 可以換嗎？要加價嗎？ | 更換資格與加價兩題都要回答 | 只保留 compatibility，遺失 surcharge | 語意表示 |
| 大型犬可以坐哪裡 | 問體型限制與座位區域 | 只回通用寵物規則 | 證據覆蓋 |
| 是不是一定都很酸 | 先回答「不一定」再解釋 | 有相關知識，卻沒回答是或不是 | 回答實現 |

## 最有代表性的一案

使用者問：

> 我喜歡奶味重一點、咖啡不要太搶，有哪杯？

Gemini 保存輸出同時包含 milk_forward 與 coffee_forward。它抓到了奶味偏好，卻把「咖啡不要太搶」這個否定與程度限制翻成相反方向。

這一案也暴露 benchmark 本身的問題：當時 expected frame 只用 creamy 近似，沒有明確的 low_coffee_intensity。成熟的 evaluator 不能只看模型和標準答案是否一致，還要問標準答案是否真的裝得下原句語意。

## 量化證據

| 系統迭代階段 | 有效格式 | 完整 frame 相符 | 核心語意相符 |
|---|---:|---:|---:|
| 初始 30 題 × 3 次 | 27 / 90 | 15 / 90 | 27 / 90 |
| canonical prompt 後 | 72 / 90 | 45 / 90 | 63 / 90 |
| Query Frame v2，30 題 × 3 次 | 90 / 90 | 90 / 90 | 90 / 90 |
| Query Frame v2，完整 96 題 | 96 / 96 | 86 / 96 | 96 / 96 |

這是 prompt、schema 與受控上下文一起調整後的系統迭代，不是 Gemini 模型版本比較。

即使最終結構化抽取明顯改善，端到端產品門檻仍是 NO-GO：

- 96 題中只有 46 題產生顧客可見回覆，50 題沉默。
- 34 題具備可回答條件，但只有 26 題真的回答。
- 至少 5 題仍有必要限定條件未被證據覆蓋。

我的結論是：frame exact 不能代表產品可上線。還要驗證可回答性、限定詞覆蓋、回答直接性，以及每一個明問子句是否真的有著落。

## 我的評估方法

1. 命題與極性：保留肯定、否定、程度副詞與條件。
2. 指涉與語篇：確認省略、那個、也算嗎綁到正確前文。
3. 子問題完整性：每個明問子句都有答案、釐清或轉接。
4. 限定條件覆蓋：尺寸、區域、時段、對象與例外都要有證據。
5. 直接性與自然度：是非問句先回答極性，疑問詞問題回答真正焦點。
6. 根因歸屬：分清模型抽取、語意表示、證據覆蓋與回答實現。

完整規則見 [評分與診斷規則](rubric.md)。

## 作品規模

| 主題 | 案例或執行數 | 用途 |
|---|---:|---|
| Gemini 中文深度案例 | 6 | 逐案證據、語意判讀、根因與修正 |
| Query Frame 迭代紀錄 | 366 次執行 | 比較有效格式、完整 frame 與核心語意 |
| 端到端產品 gate | 96 題 | 防止把抽取通過誤當成產品通過 |
| 個人化回答 SxS | 10 案 | 補充展示來源歸屬、自然度與 Debug Info |
| 咖啡廳有依據回答 | 12 案 | 補充展示 grounding、安全與政策判斷 |

## 支援作品

主作品以 Gemini 中文語意為核心；原有兩條合成評估軌保留作為補充，展示不同面向的 evaluator 能力。

### 個人化回答 SxS

比較一至五輪回答中的事實依據、來源整合、實用性、自然度、個人化克制與來源可追溯性。

- [評估流程](04-personalization-sxs/evaluation-protocol.md)
- [五個完整案例](04-personalization-sxs/case-studies.md)
- [結果與發現](04-personalization-sxs/evaluation-results.md)
- [Debug Info 核對清單](04-personalization-sxs/debug-info-checklist.md)
- [資料清理流程](04-personalization-sxs/data-hygiene.md)
- [機器可讀資料集](data/personalization_sxs.json)

### 有依據的客服回答

比較政策例外、無依據宣稱、上下文、過敏風險、隱私、時效與台灣在地用語。

- [三個完整比較](01-response-comparison/case-studies.md)
- [幻覺與失敗類型](02-hallucination-analysis/failure-taxonomy.md)
- [基準設計](03-cafe-llm-benchmark/benchmark-design.md)
- [評估結果](03-cafe-llm-benchmark/evaluation-results.md)
- [產品改善建議](03-cafe-llm-benchmark/recommendations.md)

## 倉庫結構

    05-gemini-zh-semantics/
      analysis-zh.md
      key-findings-en.md
    04-personalization-sxs/
    03-cafe-llm-benchmark/
    02-hallucination-analysis/
    01-response-comparison/
    data/
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

## 重跑與驗證

只需要 Python 3.10 以上版本，不需安裝第三方套件。

    python3 src/semantic_audit.py
    python3 src/score.py
    python3 -m unittest discover -s tests -v

驗證器會檢查案例結構、來源雜湊、provider 歸因、中文完整分析、英文長度、根因分層、量化數字與隱私邊界。

## 資料、隱私與製作方式

- Gemini 中文主分析使用真實保存的推論輸出，但所有測試提示都是合成案例。
- 不含真實顧客訊息、正式環境對話、API key、token 或可辨識店家資料。
- 公開資料只保留診斷需要的最小欄位，並以報告名稱、時間與 SHA-256 記錄來源。
- 舊有個人化與客服回答軌的身分、帳號活動、搜尋、觀看紀錄、政策及候選回答全部為合成資料。
- 這是 AI 工具協助整理的自建作品，不是過往付費標註工作，也不是官方 Gemini benchmark。

AI 協助資料整理、程式碼、格式與英文校訂；案例判讀、證據邊界與是否通過的理由保留為可檢查內容。面試時應以作者能親自解釋、接受反例與重新判分的內容為準。

## 語言說明

完整判讀以繁體中文撰寫，因為否定、程度、指涉、語用與台灣在地表達必須由能直接理解該語言的人評估。英文只用於欄位名稱、必要術語與招聘者快速閱讀的重點摘要；本作品不以英文篇幅假裝作者具備未主張的流利程度。

## English summary（AI-assisted）

This portfolio audits real archived Gemini API evaluation outputs with synthetic Traditional Chinese prompts. It identifies failures in negation, discourse reference, entity typing, coordinated questions, qualifier coverage, and direct answer realization. The exact Gemini model ID was not recorded, and end-to-end system replies are not presented as direct Gemini quotes.

## 作者

為 [@a43927957-spec](https://github.com/a43927957-spec) 整理的公開求職作品。主要工作語言為繁體中文（台灣），關注 LLM 評估、中文語意品質、grounding 與可追溯的產品 gate。

## 授權

MIT，詳見 [LICENSE](LICENSE)。
