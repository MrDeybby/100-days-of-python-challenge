import os


def sum_numbers(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


def subtract_numbers(a: int, b: int) -> int:
    """Returns the subtraction of two numbers."""
    return a - b


def multiply_numbers(a: int, b: int) -> int:
    """Returns the multiplication of two numbers."""
    return a * b


def divide_numbers(a: int, b: int) -> int:
    """Returns the division of two numbers."""
    if b == 0:
        raise ZeroDivisionError(f"Divider cannot be 0: {a}/0")
    return a / b


def menu():
    print("Calculator")
    print("[1] Sum")
    print("[2] Subtract")
    print("[3] Multiply")
    print("[4] Divide")
    print("[5] Exit")


def main():
    while True:
        os.system("cls")
        menu()
        choise = input("Choise: ")

        if choise == "5":
            break
        
        if choise not in {"1", "2", "3", "4"}:
            continue

        try:
            number1 = int(input("Number 1: "))
            number2 = int(input("Number 2: "))
        except ValueError:
            print("Values must be numbers")
            input("Press Enter to continue...")
            continue

        if choise == "1":
            print("Result:", sum_numbers(number1, number2))
            input("Press Enter to continue...")
        elif choise == "2":
            print("Result:", subtract_numbers(number1, number2))
            input("Press Enter to continue...")
        elif choise == "3":
            print("Result:", multiply_numbers(number1, number2))
            input("Press Enter to continue...")
        elif choise == "4":
            try:
                print("Result:", divide_numbers(number1, number2))
            except ZeroDivisionError as zde:
                print(zde)
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
