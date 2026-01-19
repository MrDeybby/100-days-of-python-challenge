import os


def write_file(path, mensagge: str):
    with open(path, "a") as file:
        file.write(mensagge)


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def search_lines(lines, keyword) -> list:
    lines_searched = []
    for line in lines:
        if keyword in line:
            lines_searched.append(line)
    return lines_searched


def menu():
    print("[1] add a daily log")
    print("[2] View dailys logs")
    print("[3] Search by keyword")
    print("[4] Exit")


def main():
    while True:
        os.system("cls")
        print("=== Daily Log ===")
        menu()
        user_input = input("Choice: ")

        if user_input == "1":
            new_log = input("Enter your daily log: ")
            write_file("daily_log.txt", new_log + "\n")
            print("Daily log added.")
            input("Press Enter to continue...")
        elif user_input == "2":
            logs = read_file("daily_log.txt")
            if not logs:
                print("No daily logs found.")
                input("Press Enter to continue...")
                continue

            print("=== Daily Logs ===")
            for log in logs:
                print("-", log.strip())
            input("Press Enter to continue...")

        elif user_input == "3":
            logs = read_file("daily_log.txt")

            if not logs:
                print("No daily logs found.")
                input("Press Enter to continue...")
                continue
            keyword = input("Enter keyword to search: ")
            searched_logs = search_lines(logs, keyword)

            if not searched_logs:
                print("No logs found with that keyword.")
                input("Press Enter to continue...")
                continue

            print(f"=== Logs containing '{keyword}' ===")
            for log in searched_logs:
                print("-", log.strip())
            input("Press Enter to continue...")
        elif user_input == "4":
            print("Exiting Daily Log. Goodbye!")
            break


if __name__ == "__main__":
    main()
