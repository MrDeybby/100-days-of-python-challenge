import os


class Inventory:
    total_items = 0
    products = []

    @classmethod
    def add_product(cls, name, price, quantity):
        for product in cls.products:
            if name == product.product_name:
                product.add(quantity)
                break
        else:
            product = Product(name, price, quantity)
            cls.products.append(product)

        cls.total_items += quantity
        print(f"{quantity} {name}(s) added to inventory.")

    @classmethod
    def sell_product(cls, name, amount):
        for product in cls.products:
            if product.product_name == name:
                product.sell(amount)
                print(f"{amount} {name}(s) sold.")
                cls.total_items -= amount
                return
        else:
            print("Product not found in inventory.")

    @staticmethod
    def calculate_discount(price, discount):
        return price * (1 - discount / 100)

    @classmethod
    def total_items_report(cls):
        print(f"Total Items: {cls.total_items}")

    @classmethod
    def view_products(cls):
        if not cls.products:
            print("No products in inventory.")
        else:
            for product in cls.products:
                product.show_product_details()


class Product:

    def __init__(self, name, price, quantity):
        self.product_name = name
        self.price = price
        self.quantity = quantity

    def sell(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount

    def add(self, amount):
        self.quantity += amount

    def show_product_details(self):
        print(f"Product Name: {self.product_name}")
        print(f"Price: {self.price}")
        print(f"Quantity: {self.quantity}")


def add_product():
    new_product = input("Is a new product? (Y/N): ").upper().strip() == "Y"
    product_name = input("Enter product name: ")
    price = 0
    if new_product:
        try:
            price = float(input("Enter price: "))
        except ValueError:
            print("Price must be integer")
            return
    quantity = int(input("Enter quantity: "))
    inventory.add_product(name=product_name, price=price, quantity=quantity)


def sell_product():
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity to sell: "))
    inventory.sell_product(name=product_name, amount=quantity)


def discount_price():

    try:
        price = float(input("Enter price: "))
        discount_percentage = float(input("Enter discount percentage %: "))
    except ValueError:
        print("Price and discount must be integers")
        return
    discounted_price = Inventory.calculate_discount(price, discount_percentage)
    print(f"Discounted Price: {discounted_price}")


def menu():
    print("--- Inventory Management System ---")
    print("1. Add Product")
    print("2. View Products")
    print("3. Sell Product")
    print("4. Calculate Discount")
    print("5. Total Items Report")
    print("6. Exit")


def main():
    while True:
        os.system("cls")
        menu()

        choice = input("Enter your choice(1-6): ")
        os.system("cls")

        if choice == "1":
            add_product()
            input("Press Enter to continue...")

        elif choice == "2":
            inventory.view_products()
            input("Press Enter to continue...")

        elif choice == "3":
            sell_product()
            input("Press Enter to continue...")

        elif choice == "4":
            discount_price()
            input("Press Enter to continue...")

        elif choice == "5":
            Inventory.total_items_report()
            input("Press Enter to continue...")

        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    inventory = Inventory()
    main()
