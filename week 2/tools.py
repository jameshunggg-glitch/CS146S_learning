import re
from llm import ask_llm
import json


ACTION_VERBS = {
    "fix",
    "update",
    "write",
    "create",
    "add",
    "remove",
    "check",
    "review",
    "test",
    "refactor",
    "clean",
    "document",
    "implement",
}


def extract_action_items_rule_based(text: str) -> list[str]:
    action_items = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("todo:"):
            item = line[5:].strip()
            if item:
                action_items.append(item)
            continue

        if line.startswith("-"):
            item = line[1:].strip()
            if item:
                action_items.append(item)
            continue

        first_word = re.split(r"\s+", line)[0].lower().strip(".,!?")
        if first_word in ACTION_VERBS:
            action_items.append(line)

    return action_items


def extract_action_items_llm(text: str) -> list[str]:
    prompt = f"""
You are an assistant that extracts action items from meeting notes.

Return a valid JSON object only.
Do not include markdown fences.
Do not include explanations.

Required format:
{{"action_items": ["item 1", "item 2", "item 3"]}}

Rules:
- Extract only concrete action items
- Ignore discussion and background context
- Keep items short and actionable
- If no action items exist, return:
{{"action_items": []}}

Notes:
{text}
""".strip()

    result = ask_llm(prompt)
    print("LLM raw output:", result)

    try:
        data = json.loads(result)
        items = data.get("action_items", [])
        if isinstance(items, list):
            return [str(item).strip() for item in items if str(item).strip()]
        return []
    except json.JSONDecodeError:
        return []