# Week 2 Progress Update

## 專案定位
這個專案仍然是「模擬 CS146S week2 練習」的 mini app，目標是先用自己熟悉的工具與節奏，理解 week2 想訓練的核心能力，而不是直接被 starter app 或 Cursor 綁住。核心設計順序原本設定為：最小骨架 → rule-based → llm-based → JSON structured output → auto fallback → tests → 最小 FastAPI API → 前後端整合版。

## 今日更新（補上前端整合與 agent flow 可視化）

### 1. 完成 HTML 前端整合
已不再只是透過 CLI 或 `/docs` 測試 API，而是完成了 FastAPI + Jinja2 模板的網頁版互動流程：
- `GET /` 可顯示網頁首頁
- `POST /extract` 可接收表單輸入並回傳結果頁面
- `templates/index.html` 已納入專案結構

### 2. 完成表單提交與結果顯示
目前前端頁面已支援：
- 輸入 meeting notes
- 選擇 mode（rule / llm / auto）
- 按下 Extract 後顯示抽取結果
- 顯示 Count / Status / 錯誤訊息

### 3. 完成 agent decision visibility
這次最大的升級不是只有「抽到 action items」，而是把 agent 的決策流程顯示出來。

目前結果區塊會顯示：
- Selected mode
- Used mode
- Agent message
- Status
- Count

其中最重要的是：
- `Selected mode` = 使用者要求的模式
- `Used mode` = agent 最後實際採用的路徑

例如：
- 使用者選 `Auto`
- 若 rule 抓得到，就會顯示 `Used mode: Rule-based`
- 若 rule 抓不到、fallback 到模型，就會顯示 `Used mode: LLM`

這讓 app 更像 week2 想練習的 agent flow，而不是單純 extraction demo。

### 4. 完成 agent message 說明文字
目前 `agent.py` 已能根據不同模式，回傳結構化資訊：
- `items`
- `requested_mode`
- `used_mode`
- `message`

範例訊息如：
- `Rule-based mode was used as requested.`
- `LLM mode was used as requested.`
- `Auto mode used Rule-based directly.`
- `Auto mode tried Rule-based first, then fell back to LLM.`

### 5. 完成顯示文字一致化
前端已將內部值與顯示值分開處理，例如：
- `auto` → `Auto`
- `llm` → `LLM`
- `rule` → `Rule-based`
- `success` → `Success`
- `no_items` → `No items found`

因此結果頁面現在比先前更接近 demo / 作業展示版本。

### 6. 處理跨環境執行差異
在另一台 Windows 電腦執行時，曾遇到 `TemplateResponse` / Jinja2 相關錯誤。後來透過更明確的 `TemplateResponse` 參數寫法（包含 `request=request`）後成功跑通。這也提醒之後要補上更穩定的環境管理，例如 `requirements.txt`。

## 目前狀態摘要（更新版）
目前已完成一個更完整的迷你版 week2 app，具備：
- rule-based action item extraction
- llm-based action item extraction
- JSON structured output
- hybrid fallback 模式（`auto`）
- CLI 互動入口
- pytest 測試
- FastAPI backend
- HTML frontend
- 表單提交與結果顯示
- agent decision visibility（selected mode / used mode / agent message）

整體上，已經不只完成原先的前半段核心能力，也已經往「更接近原作業型態的前後端整合版」前進一大步。

## 各完成項目對應原作業哪裡（更新版）

### 對應 TODO 1：LLM extractor
已完成：
- `extract_action_items_llm()`
- JSON 結構化輸出版本
- 本地 Ollama 串接

### 對應 TODO 2：Tests
已完成：
- rule-based test
- real LLM integration test
- mock test
- invalid JSON fallback test

### 對應 TODO 3：Backend / app structure 整理
目前進度：
- 已完成輕量版分層（`main.py` / `agent.py` / `tools.py` / `llm.py` / `app.py`）
- 已開始把 agent 執行資訊變成結構化資料，而不是只回傳 items
- 但尚未正式整理 schema、錯誤處理一致性、環境鎖版、程式風格收斂

### 對應 TODO 4：Endpoint / UI 整合
目前進度：
- 已超越「最小 FastAPI endpoint」階段
- 已完成前後端整合版雛形：HTML 表單 + FastAPI + 結果 render
- 已可展示 agent 決策流程，而不只是 API 回傳結果

### 對應 TODO 5：README / writeup
目前進度：
- 尚未正式撰寫最終 README / writeup
- 但 `week2_goal.md` 與本文件已足以作為中間版本的學習紀錄

## 本次學到的重點（新增）

### 1. 前端送資料給後端，不只一種格式
這次實際碰到並理解了：
- form data
- JSON body
- query params
三者在 FastAPI 的接法不同。

### 2. 後端 render HTML 與 API backend 的差別
目前使用的是 FastAPI + Jinja2，屬於後端直接 render HTML 的做法；這很適合原型、作業與學習。未來若要更接近正式產品，則可考慮前後端分離。

### 3. agent 不只是給答案，也可以解釋決策
這次新增的 `Used mode` 與 `Agent message`，讓 app 不只是顯示輸出，而是顯示流程。這比單純抽取結果更接近 week2 想訓練的能力。

### 4. 不同環境的套件差異會影響行為
macOS 能跑、不代表 Windows 一定能直接跑。這次也實際體會到環境一致性與依賴管理的重要性。

## 下一步建議
下一步建議優先做下面兩件事之一：

### 方向 A：先補 backend / app structure 收尾
優先處理：
- 補 `requirements.txt`
- 檢查 `/extract-json` 是否仍與新版 `run_agent()` 回傳格式一致
- 統一錯誤處理與顯示欄位
- 視需要加入更清楚的 request / response schema

### 方向 B：開始整理 writeup / README 對齊 TODO 5
把目前已完成的內容整理成：
- 專案目的
- 架構圖
- 三種 mode 的差異
- auto fallback 的設計理由
- rule vs llm 的觀察
- 如何啟動與測試

## 總結
目前這個 mini week2 app 已經完成從 CLI 到前後端整合版的躍遷，並且成功把 agent flow 顯示在 UI 上。它還不是正式產品，但已經是一個很有代表性的 week2 練習成果，也為後續的 backend structure 與 writeup 整理打好基礎。
