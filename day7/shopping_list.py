import os


def show_menu():
    os.system("cls")
    print("Shopping List Menu:")
    print("1. View items")
    print("2. Add item")
    print("3. Remove item")
    print("4. Clear shopping list")
    print("5. Exit")


def view_list(items_list: list):
    if not items_list:
        print("No item in the list")
    else:
        for i, item in enumerate(items_list):
            print(f"{i+1}. {item}")
        print()


def add_item(items_list: list):
    new_item = input("What's the new item: ")
    items_list.append(new_item)
    print(f"{new_item} added")


def remove_item(items_list: list):
    view_list(items_list)
    try:
        id_item = int(input("item id to delete: "))
        old_item = items_list.pop(id_item - 1)
        print(f"{old_item} deleted")
    except:
        print("Invalid id")


def clear_list(items_list: list):
    items_list.clear()
    print("Clean list")


def main():
    shopping_list = []
    while True:
        show_menu()
        user_input = input("Choice: ")

        if user_input == "1":
            view_list(shopping_list)
            input("Press enter to continue")
        elif user_input == "2":
            add_item(shopping_list)
            input("Press enter to continue")
        elif user_input == "3":
            remove_item(shopping_list)
            input("Press enter to continue")
        elif user_input == "4":
            clear_list(shopping_list)
            input("Press enter to continue")
        elif user_input == "5":
            break


if __name__ == "__main__":
    main()
