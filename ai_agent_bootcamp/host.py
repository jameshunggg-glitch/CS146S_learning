import agent
import client


def show_tools(available_tools):
    print("目前可用工具：")
    print("-" * 30)

    for tool_name, tool_info in available_tools.items():
        print(f"工具名稱: {tool_name}")
        print(f"功能描述: {tool_info['description']}")
        print("input schema:")

        schema = tool_info["input_schema"]
        print(f"  type: {schema['type']}")
        print("  properties:")

        for prop_name, prop_info in schema["properties"].items():
            print(f"    - {prop_name}: {prop_info['type']}")

        print(f"  required: {schema['required']}")
        print("-" * 30)


def main():
    available_tools = client.get_available_tools()
    show_tools(available_tools)

    user_input = input("請輸入需求：")

    request = agent.decide_tool(user_input, available_tools)

    if request is None:
        print("我不知道該用哪個工具，或是找不到足夠的數字。")
        return

    result = client.call_tool(request)
    print("工具執行結果：", result)


if __name__ == "__main__":
    main()