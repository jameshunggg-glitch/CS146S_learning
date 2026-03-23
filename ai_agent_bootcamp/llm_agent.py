import json
import requests
import tool_runner


def build_prompt(user_input, available_tools):
    return f"""
你是一個工具選擇助手。
你的工作是根據使用者需求，從可用工具中選擇最適合的一個工具，並抽取參數。

可用工具如下：
{json.dumps(available_tools, ensure_ascii=False, indent=2)}

使用者需求：
{user_input}

請只回傳工具執行結果就好
"""


def ask_llm(user_input, available_tools):
    url = "http://localhost:11434/api/generate"

    prompt = build_prompt(user_input, available_tools)

    payload = {
        "model": "qwen3:4b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data["response"]


def main():
    available_tools = tool_runner.list_tools()
    user_input = input("請輸入需求：")

    llm_output = ask_llm(user_input, available_tools)

    print("LLM 原始輸出：")
    print(llm_output)


if __name__ == "__main__":
    main()