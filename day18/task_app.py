import json
import os

path = "task.json"


def add_task(task: str):
    with open(path, "r") as file:
        tasks = json.load(file)

    tasks.append({"task": task, "status": "incomplete"})

    with open(path, "w") as file:
        json.dump(tasks, file, indent=4)


def read_tasks():
    tasks = ""
    with open(path, "r") as file:
        for idx, task in enumerate(json.load(file), start=1):
            tasks += f"{idx}. Task {task['task']} - Status: {task['status'].title()}\n"
    tasks = tasks.strip()
    return tasks


def edit_task_status(idx, new_status):
    with open(path, "r") as file:
        tasks = json.load(file)

    tasks[idx]["status"] = new_status

    with open(path, "w") as file:
        json.dump(tasks, file, indent=4)


def delete_taks(idx: int):
    with open(path, "r") as file:
        tasks = json.load(file)

    tasks.pop(idx)

    with open(path, "w") as file:
        json.dump(tasks, file, indent=4)


def menu():
    print("=== Task Manager ===")
    print("[1] Add Task")
    print("[2] View Tasks")
    print("[3] Edit Task Status")
    print("[4] Delete Task")
    print("[5] Exit")


def main():

    while True:
        os.system("cls")
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            task = input("Enter the task description: ")
            add_task(task)
            print("Task added successfully.")
            input("Press Enter to continue...")
        elif choice == "2":
            print("=== Task List ===")
            print(read_tasks())
            input("Press Enter to continue...")
        elif choice == "3":
            print("=== Task List ===")
            print(read_tasks())
            idx = int(input("Enter the task number to edit: ")) - 1
            new_status = input("Enter new status (complete/incomplete): ").lower()

            if new_status in ["complete", "incomplete"]:
                edit_task_status(idx, new_status)
                print("Task status updated successfully.")
                input("Press Enter to continue...")
            else:
                input("Invalid status. Please enter 'complete' or 'incomplete'.")

        elif choice == "4":
            print("=== Task List ===")
            print(read_tasks())
            idx = int(input("Enter the task number to delete: ")) - 1
            delete_taks(idx)
            print("Task deleted successfully.")
            input("Press Enter to continue...")
        elif choice == "5":
            print("Exiting the application.")
            break


if __name__ == "__main__":
    if not os.path.exists(path):
        with open(path, "w") as file:
            json.dump([], file)
    main()
