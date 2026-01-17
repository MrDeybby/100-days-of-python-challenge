from random import randint, choices, shuffle
import string, os

def generate_numbers(k:int, total:int) -> list[int]:
    """
    The function generates a list of k random numbers that sum up to a given total.
    
    :param k: The parameter `k` represents the number of integers to generate in the list
    :type k: int
    :param total: The `total` parameter represents the total sum of all the numbers to be generated
    :type total: int
    :return: A list of k integers that add up to the total value, with each integer being randomly
    generated within a certain range.
    """
    numbers = []
    remaining = total
    for i in range(k - 1):
        max_val = remaining - (k - i - 1)
        number = randint(1, max_val)
        numbers.append(number)
        remaining -= number
    
    numbers.append(remaining)    
    shuffle(numbers)
    
    return numbers

def generate_password(length:int = 12) -> str:
    """
    The function `generate_password` creates a random password of a specified length with a mix of
    uppercase letters, lowercase letters, digits, and special characters.
    
    :param length: The `length` parameter in the `generate_password` function specifies the total length
    of the password to be generated.
    :type length: int (optional)
    
    :return: The function `generate_password` returns a randomly generated password with a specified
    length that includes a mix of uppercase letters, lowercase letters, digits, and special characters from the set "$*&%$!@?/_". The password is shuffled for added security before being returned as a string.
    """
    
    quantity = generate_numbers(4, length)
    special_characters = "$*&%$!@?/_"
    
    password = "".join(
        choices(string.ascii_uppercase, k=quantity[0]) +
        choices(string.ascii_lowercase, k=quantity[1]) +
        choices(string.digits, k=quantity[2]) +
        choices(special_characters, k=quantity[3])
        )
    password = list(password)
    shuffle(password)
    
    return "".join(password)

if __name__ == "__main__":
    while True:
        os.system("cls")
        try:
            length = int(input("Enter the desired password length (minimum 4): "))
            if length < 4:
                print("Password length must be at least 4.")
                input("Press Enter to try again...")
            else:
                print("Generated Password:", generate_password(length))
                break
        except ValueError:
            print("Please enter a valid integer for password length.")
            input("Press Enter to try again...")