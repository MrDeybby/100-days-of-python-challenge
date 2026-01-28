import os

class BankAccount:
    def __init__(self, name:str,initial_balance:int=0):
        self._name = name
        self._balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    @property
    def name(self):
        return self._name

    @property
    def balance(self):
        return self._balance



def login_account(name, existing_accounts:list[BankAccount]):
    for account in existing_accounts:
        if name == account.name:
            print("Login successful.")
            return account
    return None

def access_account():
    name = input("Enter account holder's name: ").strip()
    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount: "))
            if initial_deposit < 0:
                print("Initial deposit cannot be negative. Please try again.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
        else:
            break
    return BankAccount(name, initial_deposit)

def access_menu_option():
    print("=== Bank Account Menu ===")
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    
def menu():
    print("=== Bank Account Menu ===")
    print("1. View Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

def account_info(account:BankAccount):
    print(f"Account Holder: {account.name}")
    print(f"Current Balance: ${account.balance:.2f}")

def access_account_menu(existing_accounts):
        os.system("cls")
        access_menu_option()
        choice = input("Select an option (1-3): ").strip()
        if choice == '1':
            account = login_account(input("Enter account holder's name: ").strip(), existing_accounts)
            if not account:
                print("Account not found. Please create an account first.")
                return
            return account
        elif choice == '2':
            account = access_account()
            existing_accounts.append(account)
            print("Account created successfully.")
            return account
        elif choice == '3':
            print("Exiting the program.")
            exit()
def main():
    existing_accounts = []
    account = None
    
    while True:
        os.system("cls")
        account = access_account_menu(existing_accounts)
        input("Press Enter to continue...")
        if not account:
            continue
    
        while True:
            os.system("cls")
            menu()
            option = input("Select an option (1-4): ").strip()
            if option == '1':
                account_info(account)
                input("Press Enter to continue...")
            elif option == '2':
                try:
                    amount = float(input("Enter deposit amount: "))
                    if account.deposit(amount):
                        print(f"Deposited ${amount:.2f} successfully.")
                    else:
                        print("Deposit amount must be positive.")
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
                input("Press Enter to continue...")
            elif option == '3':
                try:
                    amount = float(input("Enter withdrawal amount: "))
                    if account.withdraw(amount):
                        print(f"Withdrew ${amount:.2f} successfully.")
                    else:
                        print("Insufficient balance or invalid amount.")
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
                input("Press Enter to continue...")
            elif option == '4':
                print("Exiting account")
                input("Press Enter to continue...")
                break
            else:
                print("Invalid option. Please select from 1 to 4.")
        
if __name__ == "__main__":
    main()