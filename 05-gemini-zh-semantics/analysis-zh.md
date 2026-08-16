# Gemini 繁體中文語意品質分析

> 這份主報告分析保存下來的真實 Gemini API Eval 結果。測試輸入皆為合成情境，不含真實顧客訊息；完整判讀以繁體中文撰寫，英文只保留招聘者快速審閱所需的結論。

## 我想回答的問題

模型「看得懂中文」不等於它能穩定保留中文句子中的命題。真正會影響產品的，往往是很小、卻不能忽略的語意：

- 否定與程度：不要太搶，不等於咖啡感強。
- 語篇承接：那個也算嗎，必須知道上一輪在算什麼。
- 實體與屬性：焙度是選項屬性，不一定是商品名稱。
- 並列子問題：可以換嗎與要加價嗎，兩題都要留下。
- 限定詞與疑問焦點：大型犬、坐哪裡不能被寵物主題取代。
- 是非問句語用：先回答成立或不成立，再補原因。

本作品不只標記「錯了」，而是把失敗定位到模型抽取、語意表示、證據覆蓋或回答實現，避免把整個系統的問題都籠統歸咎於模型。

## 證據與歸因邊界

| 證據層級 | 可以主張什麼 | 不能主張什麼 |
|---|---|---|
| 直接 Gemini 結構化輸出 | 實測 runner 明確使用 GEMINI_API_KEY 建立 Gemini client；保存的 Query Frame 可視為 Gemini API 輸出 | 保存報告沒有精確 model ID，因此不猜測 Gemini 版本 |
| 端到端系統輸出 | 可以分析 Query Frame、檢索、路由與 renderer 合成後的產品行為 | 回覆文字不能冒充 Gemini 原文，也不能把所有錯誤都算在模型上 |

所有案例都保留來源報告名稱、生成時間與 SHA-256。公開資料只摘錄語意診斷所需的最小欄位，原始測試提示為合成資料，沒有公開店家或顧客身分。

## 量化結果：抽取改善，不等於產品通過

| 階段 | 有效格式 | 完整 frame 相符 | 核心語意相符 |
|---|---:|---:|---:|
| 初始 30 題 × 3 次 | 27 / 90 | 15 / 90 | 27 / 90 |
| canonical prompt 後 | 72 / 90 | 45 / 90 | 63 / 90 |
| Query Frame v2，30 題 × 3 次 | 90 / 90 | 90 / 90 | 90 / 90 |
| Query Frame v2，完整 96 題 | 96 / 96 | 86 / 96 | 96 / 96 |

這些數字代表同一套系統經過 prompt、schema 與受控上下文調整後的迭代，不是 Gemini 模型升級前後的比較。最終 30 題三次重跑達到 90 / 90，表示窄範圍 Query Frame 可以被約束得很穩定；但完整 96 題仍有 10 題不是完整 frame 相符。

更重要的是，端到端產品門檻仍是 NO-GO：

- 96 題中只有 46 題產生顧客可見回覆，50 題沉默。
- 34 題其實具備可回答條件，但只有 26 題真的回答。
- 至少 5 題出現限定條件覆蓋不足。

所以「結構化抽取通過」只能證明其中一層，不能取代端到端產品判斷。

## 六個代表案例

### ZH-SEM-001：否定極性被翻成相反偏好

使用者：

> 我喜歡奶味重一點、咖啡不要太搶，有哪杯？

Gemini 保存輸出：

- milk_forward
- coffee_forward

「咖啡不要太搶」是在降低咖啡強度，不是偏好 coffee-forward。這個錯誤若直接進推薦器，可能把使用者導向完全相反的品項。

同時，當時保存的 expected frame 使用 creamy 近似，也沒有真正表示 low_coffee_intensity。這代表問題不只在模型：若標註 schema 沒有負向或程度限制，評估本身也無法完整描述中文命題。

診斷層：模型抽取，另含 benchmark 表示缺口；嚴重度：高。

English key finding: Gemini reversed a negative coffee-intensity preference into coffee-forward, which could invert the recommendation.

### ZH-SEM-002：單一關鍵字壓過上一輪語境

上一輪在談外帶飲品折 30 元，使用者接著問：

> 那酒精的也算嗎？

預期應綁定外帶折扣政策；Gemini 三次都穩定輸出 alcohol safety。它知道 reference 是 previous_turn，卻仍被「酒精」拉去安全領域。

中文的「那……也算嗎」不是完整命題。「算」可能指折扣、低消、優惠資格或其他規則，必須以正在進行的話題解讀，不能只做當輪關鍵字分類。

診斷層：模型抽取；嚴重度：高。

English key finding: The model noticed a prior-turn reference but let the word alcohol override the active discount context.

### ZH-SEM-003：把屬性詞當成商品實體

使用者：

> 如果我沒選焙度，你們會預設哪一個？

Gemini 三次都把「焙度」填入 Product 的 objectMention，並把 reference 標成 explicit。實際上焙度是上一輪商品的選項屬性，問題需要承接先前物件。

這種錯誤會讓下游拿「焙度」去查商品，最後找不到資料或答非所問。後續加入受控前文並收緊 schema 後，同案達到 3 / 3 exact；這說明改善來自可測量的系統約束，不是宣稱模型自然理解了。

診斷層：模型抽取；嚴重度：中。

English key finding: Gemini repeatedly treated a roast attribute as a product entity and lost the prior-turn reference.

### ZH-SEM-004：並列問句遺失第二個槽位

使用者：

> 拿鐵可以換燕麥奶嗎？要加價嗎？

這句有兩個必答槽位：能不能更換，以及是否加價。保存的 frame 只留下 compatibility；端到端回覆轉去確認原味或風味拿鐵，沒有保留 surcharge。

這裡不應只怪模型。當時的 Query Frame 主要容納單一 property，中文並列問句一進 schema 就被壓扁。只有做端到端「每個明問子句是否有著落」檢查，才看得見資訊遺失。

診斷層：語意表示；嚴重度：高。

English key finding: The frame captured substitution compatibility but dropped the surcharge question from the coordinated request.

### ZH-SEM-005：命中主題，卻漏掉限定詞與疑問焦點

使用者：

> 帶大型犬去可以坐哪裡？

系統命中 pet policy，回覆「寵物可以落地，但請勿影響他人」。這句使用的規則可能是真的，卻沒有回答：

- 大型犬是否有體型限制。
- 可以坐哪個區域。

這是 topic hit 但 qualifier coverage 失敗。產品不能只驗證「有找到寵物規則」，而要驗證使用者明問的每個限定條件是否都有已發布證據。

診斷層：證據覆蓋；嚴重度：高。

English key finding: A generic pet rule ignored both the large-dog modifier and the seating-location question.

### ZH-SEM-006：有相關知識，仍沒回答是或不是

使用者：

> 淺焙是不是一定都很酸？

系統說明淺焙常有明亮酸質，也會受豆種、產區、處理法與沖煮影響；內容相關，但開頭是「可以」，整段沒有先說「不一定」。

中文是非問句先要求命題極性，再要求理由。若只評 grounding，這題很容易被判通過；若站在真人使用者角度，它沒有正面回答。

診斷層：回答實現；嚴重度：中。

English key finding: The evidence was relevant, but the response never directly answered the yes-or-no proposition.

## 根因分層

| 層級 | 要問的問題 | 本報告案例 |
|---|---|---|
| 模型抽取 | 模型是否保留否定、指涉與詞類角色？ | ZH-SEM-001～003 |
| 語意表示 | schema 是否能裝下完整命題與多個子問題？ | ZH-SEM-004 |
| 證據覆蓋 | 已批准的證據是否涵蓋所有限定條件？ | ZH-SEM-005 |
| 回答實現 | 回覆是否直接、自然地回答命題？ | ZH-SEM-006 |

這個分層很重要：如果錯誤出在 schema，單純換 prompt 不一定有用；如果證據缺少大型犬或座位區域政策，模型再聰明也不應自行補答案；如果 frame 已正確，就應檢查回答規劃而不是重做抽取。

## 我會怎麼評繁體中文語意

1. 命題與極性：肯定、否定、程度副詞與雙重條件是否保留。
2. 指涉與語篇：省略主詞、那個、也算嗎等形式是否綁到正確前文。
3. 子問題完整性：每一個明問子句都有答案、釐清或轉接結果。
4. 限定條件覆蓋：尺寸、區域、時段、對象與例外不能被主題標籤取代。
5. 直接性與自然度：是非問句先給極性，疑問詞問題回答正確焦點。
6. 根因歸屬：分清模型、表示、證據與 renderer，避免錯修。

每個案例至少應有最小對比組，例如「咖啡不要太搶／咖啡感可以強一點」、「那酒精的也算嗎／酒精喝了安全嗎」，並做多次重跑，才能區分穩定語意錯誤與偶發輸出波動。

## 限制

- 保存的 Eval 報告能確認 Gemini API provider，但沒有精確 model ID；本作品不補猜版本。
- 測試輸入是合成情境，不代表真實流量分布。
- 各階段同時修改 prompt、schema 與上下文，量化結果只能解讀為系統迭代，不能當作模型版本比較。
- 完整私有來源不公開；公開資料提供報告名稱、時間與 SHA-256，讓面試時可以說清楚證據來源與公開邊界。

## 可檢查資料

- [機器可讀案例與來源雜湊](../data/gemini_zh_semantics.json)
- [English key findings](key-findings-en.md)
- [評分與診斷規則](../rubric.md)
