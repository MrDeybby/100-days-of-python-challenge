import os

users = []

class UserProfile:
    
    def __init__(self,username, email, password):
        self.username = username
        self._email = email
        self.__password = None
        
        self.set_password(password=password)
    
    def set_password(self, password):
        if len(password) < 8:
            print("Password's length must be more or equal than 8")
            return
        self.__password = password
        print("Passsword updated successfully")
        
    def get_email(self):
        return self._email

    def set_email(self, new_email):
        if "@" in new_email and "." in new_email:
            self._email = new_email
            print("Email updated successfully")
        else:
            print("Invalid email format")

    def display_profile(self):
        print("\n--- User Profile ---")
        print(f"Username: {self.username}")
        print(f"Email: {self._email}")
        print(f"Password: {self.__password}")
        


def create_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = UserProfile(username, email, password)
    users.append(user)
    print("User created successfully")

def view_profiles():
    if not users:
        print("No users found")
    else:
        for user in users:
            user.display_profile()

def update_email():
    username = input("Enter username to update email: ")
    for user in users:
        if user.username == username:
            new_email = input("Enter new email: ")
            user.set_email(new_email)
            return
        print("User not found")

def menu():
    print("--- Secure User Profile App ---")
    print("1. Create User")
    print("2. View All Profiles")
    print("3. Update Email")
    print("4. Exit")

def main():
    while True:
        
        os.system("cls")
        menu()
        choice = input("Enter your choice(1-4): ")
        os.system("cls")

        if choice == "1":
            create_user()
            input("Press Enter to continue...")
        elif choice == "2":
            view_profiles()
            input("Press Enter to continue...")
        elif choice == "3":
            update_email()
            input("Press Enter to continue...")
        elif choice == "4":
            print("Exiting the program")
            break
        else:
            print("Invalid choice. Please try again")
            
if __name__ == "__main__":
    main()