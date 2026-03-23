import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen3:4b",
    "prompt": "請用一句話回答：1加1等於幾？",
    "stream": False
}

response = requests.post(url, json=payload)
data = response.json()

print("模型回應：")
print(data["response"])