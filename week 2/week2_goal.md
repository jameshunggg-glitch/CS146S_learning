# Mini Week 2 Goal

## 文件目的
這份文件是用來記錄「模擬 CS146S week2 練習」的專案目標與設計方向。  
它不是正式交作業文件，而是為了幫助我用自己的節奏，理解 week2 想訓練的核心能力。

## 練習定位
這個 mini app 的定位是：

- 用熟悉的工具練習 week2 的核心概念
- 不先被 Cursor 或 starter app 的複雜度綁住
- 先理解 agent / LLM / tools / API 的角色分工
- 先做最小可跑版本，再逐步升級成更接近原作業型態的版本

目前採用的環境：

- macOS
- VS Code
- Ollama
- 本地模型：`qwen3:4b`
- Python 專案

## Mini App 的核心目標
這個 mini app 的主要目標如下：

1. 從 notes 中抽取 action items
2. 比較 rule-based 與 llm-based 的差異
3. 練習讓 LLM 回傳結構化輸出
4. 練習 testing（包含 mock 與 integration test）
5. 練習將功能 API 化
6. 為下一階段的前後端整合版做準備

## Mini App 架構設計
目前 mini app 的檔案角色如下：

- `main.py`  
  CLI 入口，負責接收使用者輸入並啟動流程

- `agent.py`  
  流程控制層，負責選擇使用 rule / llm / auto 模式

- `tools.py`  
  放置具體功能，例如 rule-based extractor 與 llm-based extractor

- `llm.py`  
  負責呼叫本地 Ollama API

- `app.py`  
  最小 FastAPI 版本，提供 API endpoint

- `test_tools.py`  
  放置 pytest 測試，包含 rule-based、real LLM integration、mock、invalid JSON 測試

## 核心設計思路
這個 mini app 的設計順序如下：

1. 先建立最小骨架（`main.py`, `agent.py`, `tools.py`, `llm.py`）
2. 先做 rule-based baseline
3. 再做 llm-based extractor
4. 再升級成 JSON 結構化輸出
5. 再做 hybrid fallback（`auto` 模式）
6. 再做 pytest 與 mock/integration test
7. 再做最小 FastAPI API
8. 最後再往更接近原 week2 的前後端整合版前進

## 與原作業 TODO 1～5 的對齊

### TODO 1：LLM extractor
對齊方式：
- 已完成 `extract_action_items_llm()`
- 已要求 LLM 回傳 JSON 格式，例如：
  `{"action_items": [...]}`

### TODO 2：Tests
對齊方式：
- 已完成 rule-based test
- 已完成 real LLM integration test
- 已完成 mock `ask_llm()` test
- 已完成 invalid JSON fallback test

### TODO 3：Backend / app structure 整理
目前狀況：
- 已完成輕量版分層（`main.py` / `agent.py` / `tools.py` / `llm.py` / `app.py`）
- 但尚未正式進入更完整的 schema、error handling、資料層整理

### TODO 4：Endpoint / UI 整合
目前狀況：
- 已完成最小 FastAPI endpoint：`POST /extract`
- 尚未完成更接近原作業的前端整合版本

### TODO 5：README / writeup
目前狀況：
- 尚未正式撰寫
- 本文件可視為較穩定的「專案目標說明」

## 為什麼不直接照 starter app 做
這次的學習策略不是直接進入原本 starter app，而是先做迷你版，原因如下：

- 先用熟悉環境降低認知負擔
- 先理解每個元件的角色，而不是只照作業修改
- 先手做一次最小版，之後再回頭看原作業會更容易理解
- 避免同時學新 IDE、新框架、新結構而分散注意力

## 下一階段方向
下一步要做的是：

- 把目前的 mini app 升級成「包含前後端、較接近原 week2 starter app 型態」的版本
- 開始做更接近原作業風格的前後端整合與結構整理
- 逐步靠近 TODO 3～5 的完整型態
