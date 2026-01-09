import os


def main():
    contacts = []
    while True:
        os.system("cls")
        menu()
        user_input = input("Choise: ")

        if user_input == "1":
            name = input("Name: ").strip().title()
            phone = input("Phone Number: ").strip().lower()
            email = input("Email: ").strip().lower()
            address = input("Address: ").strip().title()

            contacts.append(create_contact(name, phone, email, address))
            input("Press enter to continue")
        elif user_input == "2":
            name = input("Name to search: ").strip().title()
            print(get_contact(name, contacts))
            input("Press enter to continue")

        elif user_input == "3":
            print(get_contacts_list(contacts))
            input("Press enter to continue")

        elif user_input == "4":

            name = input("Name of contact: ").strip().title()

            if get_contact(name, contacts) == "No contact in list":
                print("Contact not found")
            else:
                new_name = input("New Name: ").strip().title()
                new_phone = input("Phone Number: ").strip().lower()
                new_email = input("Email: ").strip().lower()
                new_address = input("Address: ").strip().title()

                edit_contact(
                    name, contacts, new_name, new_phone, new_email, new_address
                )
            input("Press enter to continue")

        elif user_input == "5":
            name = input("Name of contact: ").strip().title()
            delete_contact(name, contacts)
            input("Press enter to continue")

        elif user_input == "6":
            print("Closing app...")
            break


def menu():
    print("=== Contacts List ===")
    print("[1] Add contact")
    print("[2] Search contact")
    print("[3] View contacts list")
    print("[4] Edit contact")
    print("[5] Delete contact")
    print("[6] Exit")


def create_contact(name, phone_number, email, address):
    contact = {
        "Name": name,
        "Phone Number": phone_number,
        "Email": email,
        "Address": address,
    }
    return contact


def get_contacts_list(contacts_list: list):
    list_str = ""

    for index, info in enumerate(contacts_list):
        list_str += f'{index+1}. {info["Name"]} | Phone: {info["Phone Number"]}\tEmail: {info["Email"]}\tAddress: {info["Address"]}\n'

    return list_str if list_str else "No contacts available"


def get_contact(name, contacts_list: list):

    for contact in contacts_list:
        if name == contact["Name"]:
            return f'{contact["Name"]} | Phone: {contact["Phone Number"]}\tEmail: {contact["Email"]}\tAddress: {contact["Address"]}'

    return "No contact in list"


def edit_contact(
    name: str,
    contacts_list: list,
    new_name=None,
    new_phone_number=None,
    new_email=None,
    new_address=None,
):
    new_info = {
        "Name": new_name,
        "Phone Number": new_phone_number,
        "Email": new_email,
        "Address": new_address,
    }
    founded = False
    for contact in contacts_list:
        if name == contact["Name"]:
            for info, value in new_info.items():
                if value:
                    contact[info] = value
            founded = True
    if not founded:
        print("Contact not found")


def delete_contact(name: str, contacts_list: list):
    for contact in contacts_list:
        if name == contact["Name"]:
            contacts_list.remove(contact)


if __name__ == "__main__":
    main()
