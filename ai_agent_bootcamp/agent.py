import re


def choose_tool_from_text(user_input, available_tools):
    for tool_name, tool_info in available_tools.items():
        description = tool_info["description"].lower()

        if "加" in user_input and "add" in tool_name.lower():
            return tool_name

        if "減" in user_input and "subtract" in tool_name.lower():
            return tool_name

        if "add" in user_input.lower() and "add" in description:
            return tool_name

        if "subtract" in user_input.lower() and "subtract" in description:
            return tool_name

    return None


def decide_tool(user_input, available_tools):
    print(f"[debug] user_input: {user_input}")
    print(f"[debug] available_tools: {list(available_tools.keys())}")

    numbers = re.findall(r"-?\d+(?:\.\d+)?", user_input)
    print(f"[debug] numbers found: {numbers}")

    if len(numbers) < 2:
        print("[debug] not enough numbers")
        return None

    selected_tool = choose_tool_from_text(user_input, available_tools)
    print(f"[debug] selected_tool_from_metadata: {selected_tool}")

    if selected_tool is None:
        print("[debug] no matching tool found")
        return None

    a = float(numbers[0])
    b = float(numbers[1])

    request = {
        "tool": selected_tool,
        "arguments": {
            "a": a,
            "b": b
        }
    }

    print(f"[debug] generated request: {request}")
    return request