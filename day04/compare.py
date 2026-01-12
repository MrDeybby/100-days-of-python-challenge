number1 = int(input("First number: "))
number2 = int(input("Second number: "))

if number1 > number2:
    print(f"Number {number1} is greater than {number2}")
elif number2 > number1:
    print(f"Number {number2} is greater than {number1}")
else:
    print(f"Numbers are equal")

if number1 == 0:
    print(f"First number is 0")
    
if number2 == 0:
    print(f"Second number is 0")
