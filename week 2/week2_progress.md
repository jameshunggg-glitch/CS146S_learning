# Mini Week 2 Progress

## 文件目的
這份文件是 mini week2 練習的每日進度紀錄。  
用途是記錄目前已完成的內容、對應到原作業的哪一部分，以及下一步要做什麼。

## 專案資訊
- 專案名稱：Mini Week 2 Agent App Practice
- 開發環境：macOS + VS Code + Ollama + Python
- 本地模型：`qwen3:4b`
- Repo URL：<https://github.com/jameshunggg-glitch/CS146S_learning>

## 目前狀態摘要
目前已完成一個迷你版 week2 app，具備：

- rule-based action item extraction
- llm-based action item extraction
- JSON structured output
- hybrid fallback 模式（`auto`）
- CLI 互動入口
- pytest 測試
- 最小 FastAPI endpoint

整體上已完成迷你版中對應原作業前半段的核心能力，下一步是升級成更接近原作業型態的前後端整合版本。

## Day 1 / 目前已完成項目

### 1. 建立專案骨架
已建立：
- `main.py`
- `agent.py`
- `tools.py`
- `llm.py`
- `app.py`

### 2. 完成 `llm.py`
已完成：
- 使用 `requests` 呼叫本地 Ollama API
- 使用 endpoint：`http://localhost:11434/api/generate`

### 3. 完成 rule-based extractor
已完成：
- `TODO:` 開頭抽取
- `-` bullet 抽取
- action verb 開頭句子抽取

### 4. 完成 llm-based extractor
已完成：
- 使用 prompt 要求模型抽取 action items
- 已升級為 JSON structured output：
  `{"action_items": [...]}`

### 5. 完成 hybrid / auto 模式
已完成：
- `rule` 模式
- `llm` 模式
- `auto` 模式  
  邏輯：先跑 rule-based，若無結果再 fallback 到 LLM

### 6. 完成 CLI 互動版
已完成：
- 可手動輸入 notes
- 可手動選擇 mode
- 在 terminal 顯示抽取結果

### 7. 完成 pytest 測試
已完成：
- rule-based test
- real LLM integration test
- mock `ask_llm()` test
- invalid JSON fallback test

### 8. 完成 FastAPI 最小版本
已完成：
- `GET /`
- `POST /extract`
- 已透過 `/docs` 成功測試 API

## 各完成項目對應原作業哪裡

### 對應 TODO 1：LLM extractor
已完成：
- `extract_action_items_llm()`
- JSON 結構化輸出版本

### 對應 TODO 2：Tests
已完成：
- rule-based test
- real integration test
- mock test
- invalid JSON 測試

### 對應 TODO 4：Endpoint / interaction（前半）
已完成：
- 最小 FastAPI endpoint：`POST /extract`

### 屬於前置學習、但不直接等於原作業要求的部分
已完成：
- 自建迷你版 app 骨架
- CLI 互動版
- hybrid fallback 設計
- agent / llm / tools 分層練習

## 本次學到的重點

### 1. agent != LLM
- LLM 是推理與生成能力
- agent 是利用 LLM 做判斷，並協調工具與流程的控制層

### 2. rule-based vs llm-based
- rule-based：穩定、可預測、容易 debug，但覆蓋有限
- llm-based：語意理解能力強，但輸出需約束、也可能不穩

### 3. structured output 的重要性
- LLM 不只是拿來聊天
- 也可以透過 prompt 要求回傳可解析的 JSON 結構

### 4. mock vs integration test
- mock test：快、穩，主要測自己程式邏輯
- integration test：慢，但可以驗證整條鏈是否真的可用

### 5. hybrid strategy 的意義
- 能用 rule-based 先處理就先處理
- 抓不到時再 fallback 到 LLM
- 更接近實務上 rule + LLM 的混合設計

### 6. CLI 與 API 只是不同入口
- `main.py` 是 CLI 入口
- `app.py` 是 API 入口
- 核心邏輯可以共用

## 尚未完成項目
目前尚未完成：

- 更接近原作業的前後端整合版本
- 更正式的 backend structure 整理
- 更完整的 schema / error handling
- README / writeup

## 下一步
下一步預定要做的是：

1. 把目前的迷你版升級成包含前後端的版本
2. 朝更接近原 week2 starter app 的型態前進
3. 開始做更完整的前後端整合與結構整理
