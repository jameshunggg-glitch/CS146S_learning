import calculator


TOOLS = {
    "add": {
        "description": "Add two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        },
        "function": calculator.add
    },
    "subtract": {
        "description": "Subtract two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        },
        "function": calculator.subtract
    }
}


def list_tools():
    print("[server] listing available tools...")
    return {
        name: {
            "description": info["description"],
            "input_schema": info["input_schema"]
        }
        for name, info in TOOLS.items()
    }


def validate_request(request):
    print("[server] validating request...")

    if "tool" not in request:
        return False, "Missing 'tool' field"

    if "arguments" not in request:
        return False, "Missing 'arguments' field"

    tool_name = request["tool"]
    arguments = request["arguments"]

    if tool_name not in TOOLS:
        return False, f"Unknown tool: {tool_name}"

    schema = TOOLS[tool_name]["input_schema"]
    required_fields = schema["required"]

    for field in required_fields:
        if field not in arguments:
            return False, f"Missing required argument: {field}"

    return True, "OK"


def run_tool(request):
    print(f"[server] received request: {request}")

    is_valid, message = validate_request(request)
    if not is_valid:
        print(f"[server] request validation failed: {message}")
        return f"Request error: {message}"

    tool_name = request["tool"]
    arguments = request["arguments"]

    a = arguments["a"]
    b = arguments["b"]

    print(f"[server] executing tool: {tool_name}")
    tool_function = TOOLS[tool_name]["function"]
    result = tool_function(a, b)
    print(f"[server] tool result: {result}")

    return result


if __name__ == "__main__":
    print("Available tools:")
    print(list_tools())