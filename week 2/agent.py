from tools import extract_action_items_rule_based, extract_action_items_llm


def run_agent(notes: str, mode: str = "auto") -> list[str]:
    if mode == "rule":
        return extract_action_items_rule_based(notes)

    if mode == "llm":
        return extract_action_items_llm(notes)

    if mode == "auto":
        rule_items = extract_action_items_rule_based(notes)
        if rule_items:
            return rule_items
        return extract_action_items_llm(notes)

    raise ValueError(f"Unsupported mode: {mode}")