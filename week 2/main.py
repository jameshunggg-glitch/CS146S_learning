from agent import run_agent


def main():
    print("=== Action Item Extractor ===")
    print("請選擇模式：")
    print("1. auto")
    print("2. rule")
    print("3. llm")

    mode_input = input("輸入模式（1/2/3 或 auto/rule/llm）: ").strip().lower()

    if mode_input == "1":
        mode = "auto"
    elif mode_input == "2":
        mode = "rule"
    elif mode_input == "3":
        mode = "llm"
    elif mode_input in {"auto", "rule", "llm"}:
        mode = mode_input
    else:
        print("無效模式，預設使用 auto")
        mode = "auto"

    print("\n請輸入 notes（輸入空白行後按 Enter 結束）：")
    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    notes = "\n".join(lines)

    if not notes.strip():
        print("你沒有輸入任何 notes。")
        return

    items = run_agent(notes, mode=mode)

    print(f"\n=== {mode.upper()} 抽取結果 ===")
    if not items:
        print("沒有抽取到 action items。")
        return

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")


if __name__ == "__main__":
    main()