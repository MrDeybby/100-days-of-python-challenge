import os


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)


main_conversions = {
    "C to F": celsius_to_fahrenheit,
    "C to K": celsius_to_kelvin,
    "F to C": fahrenheit_to_celsius,
    "F to K": fahrenheit_to_kelvin,
    "K to C": kelvin_to_celsius,
    "K to F": kelvin_to_fahrenheit,
}


def convert_temperature(value, conversion_type):
    """Convert temperature based on the conversion type."""
    if conversion_type not in main_conversions:
        raise ValueError(f"Unsupported conversion type: {conversion_type}")
    return main_conversions[conversion_type](value)


def menu():
    print("Temperature Converter")
    print("[1] Celsius to Fahrenheit")
    print("[2] Celsius to Kelvin")
    print("[3] Fahrenheit to Celsius")
    print("[4] Fahrenheit to Kelvin")
    print("[5] Kelvin to Celsius")
    print("[6] Kelvin to Fahrenheit")
    print("[7] Exit")


def main():
    while True:
        os.system("cls")
        menu()
        choice = input("Choice: ")

        if choice == "7":
            break

        if choice in conversion_map:
            

            try:
                value = float(input("Enter temperature value: "))
            except ValueError:
                print("Value must be a number")
                input("Press Enter to continue...")
                continue
        
            conversion_type = conversion_map[choice]
            result = convert_temperature(value, conversion_type)
            print(f"Converted temperature: {result}")
            input("Press Enter to continue...")
        else:
            print("Invalid choice")
            input("Press Enter to continue...")


        conversion_map = {
            "1": "C to F",
            "2": "C to K",
            "3": "F to C",
            "4": "F to K",
            "5": "K to C",
            "6": "K to F",
        }



if __name__ == "__main__":
    main()
