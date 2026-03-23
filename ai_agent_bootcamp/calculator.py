import sys


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def main():
    if len(sys.argv) != 4:
        print("Usage: python calculator.py <add|subtract> <num1> <num2>")
        return

    operation = sys.argv[1]
    a = float(sys.argv[2])
    b = float(sys.argv[3])

    if operation == "add":
        result = add(a, b)
    elif operation == "subtract":
        result = subtract(a, b)
    else:
        print("Unknown operation. Use 'add' or 'subtract'.")
        return

    print(result)


if __name__ == "__main__":
    main()