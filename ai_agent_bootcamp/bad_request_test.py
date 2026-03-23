import tool_runner

bad_request = {
    "tool": "subtract",
    "arguments": {
        "a": 20
    }
}

result = tool_runner.run_tool(bad_request)
print(result)