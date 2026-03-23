import tool_runner


def get_available_tools():
    print("[client] requesting tool list from server...")
    return tool_runner.list_tools()


def call_tool(request):
    print("[client] sending tool request to server...")
    return tool_runner.run_tool(request)