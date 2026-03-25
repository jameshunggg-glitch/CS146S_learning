from tools import extract_action_items_rule_based, extract_action_items_llm


def run_agent(notes: str, mode: str = "auto"):
    if mode == "rule":
        items = extract_action_items_rule_based(notes)
        return {
            "items": items,
            "requested_mode": "rule",
            "used_mode": "rule",
            "message": "Rule mode was used as requested.",
        }

    elif mode == "llm":
        items = extract_action_items_llm(notes)
        return {
            "items": items,
            "requested_mode": "llm",
            "used_mode": "llm",
            "message": "LLM mode was used as requested.",
        }

    elif mode == "auto":
        rule_items = extract_action_items_rule_based(notes)

        if rule_items:
            return {
                "items": rule_items,
                "requested_mode": "auto",
                "used_mode": "rule",
                "message": "Auto mode used rule directly.",
            }

        llm_items = extract_action_items_llm(notes)
        return {
            "items": llm_items,
            "requested_mode": "auto",
            "used_mode": "llm",
            "message": "Auto mode tried rule first, then fell back to llm.",
        }

    else:
        raise ValueError(f"Unknown mode: {mode}")