# Ask for user input for two numbers
# Add, Subtract, multiply and divide the numbers


number1 = int(input("First number: "))
number2 = int(input("Second number: "))

print("Addition:", number1 + number2)
print("Subtraction:", number1 - number2)
print("Multiplication:", number1 * number2)
if number2 != 0:
    print("Division:", number1 / number2)