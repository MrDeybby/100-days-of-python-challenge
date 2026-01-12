import random


def main():
    points = 0

    for _ in range(10):
        number1, operation, number2 = generate_question()
        user_input = int(input(f"{number1} {operation} {number2} = "))

        if validate_answer(number1, operation, number2, user_input):
            points = add_point(points)

    print("Score:", points)


def generate_question():
    number1 = random.randint(0, 10)
    number2 = random.randint(0, 10)
    operation = random.choice(["-", "+", "x"])
    return number1, operation, number2


def validate_answer(number1: int, operation: str, number2: int, answer: int):
    value = {"+": number1 + number2, "-": number1 - number2, "x": number1 * number2}
    return value[operation] == answer


def add_point(counter: int):
    return counter + 1


if __name__ == "__main__":
    main()
