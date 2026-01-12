import os
# File path: day10/take_notes.py"""
# A simple notes application that allows users to take, read, and delete notes.
# The notes are stored in a text file named 'notes.txt'.

FILENAME = "notes.txt"

def take_notes():
    """Take notes from user input and save them to a file."""
    try:
        with open(FILENAME, 'a') as file:
            while True:
                note = input("Enter your note (or type 'exit' to finish): ")
                if note.lower() == 'exit':
                    break
                file.write(note + '\n')
        print(f"Notes saved to {FILENAME}.")
    except Exception as e:
        print(f"An error occurred while saving notes: {e}")
        
def read_notes():
    """Read and display notes from the file."""
    try:
        with open(FILENAME, 'r') as file:
            notes = file.readlines()
            if notes:
                print("Your notes:")
                for idx, note in enumerate(notes, start=1):
                    print(f"{idx}. {note.strip()}")
            else:
                print("No notes found.")
    except FileNotFoundError:
        print(f"No notes found. The file {FILENAME} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading notes: {e}")
        
def delete_notes():
    """Delete all notes by clearing the file."""
    delete = input("Are you sure you want to delete all notes? (yes/no): ")
    if delete.lower() != 'yes':
        print("Deletion cancelled.")
        return
    try:
        open(FILENAME, 'w').close()
        print(f"All notes deleted from {FILENAME}.")
    except Exception as e:
        print(f"An error occurred while deleting notes: {e}")

def menu():
    print("\n=== Notes Application ===")
    print("1. Take Notes")
    print("2. Read Notes")
    print("3. Delete Notes")
    print("4. Exit")
    
def main():
    while True:
        os.system('cls')
        menu()
        choice = input("Choose an option (1-4): ")
        
        
        if choice == '1':
            os.system('cls')
            take_notes()
            input("Press Enter to continue...")
        elif choice == '2':
            os.system('cls')
            read_notes()
            input("Press Enter to continue...")
        elif choice == '3':
            os.system('cls')
            delete_notes()
            input("Press Enter to continue...")
        elif choice == '4':
            print("Exiting the application.", end='')
            break
        

if __name__ == "__main__":
    main()
    
    