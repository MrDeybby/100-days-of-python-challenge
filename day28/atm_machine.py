import os   
class BankAccount:
    
    def __init__(self, account_number, pin):
        self._account_number = account_number
        self.__pin = pin
        self.__balance = 0
    
    def check_balance(self):
        return self.__balance  
     
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Amount can't be less than 1")
    
    def withdraw(self, amount):
        if amount < self.__balance:
            raise ValueError("Amount not avaible for withdraw")
        
        self.__balance -= amount
    
    def change_pin(self, old_pin, new_pin):
        if self.validate_pin(old_pin) and len(new_pin) == 4 and new_pin.isdigit():
            self.__pin = new_pin
            return True
        else:
            return False
    
    def validate_pin(self, entered_pin):
        return entered_pin == self.__pin
    
    def number(self):
        return self._account_number
    
class ATM:
    accounts = []
    
    @classmethod
    def get_account(cls, account_number):
        for account in cls.accounts:
            if account.number() == account_number:
                return account
        else:
            return None
        
    @staticmethod
    def menu():
        print("--- ATM Machine ---")
        print("1. Check account balance")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Change PIN")
        print("5. Logout")


    def create_account(self):
        account_number = input("Enter account number: ")
        pin = input("Set a 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            self.accounts.append(BankAccount(account_number, pin))
            print("Account created successfully.")
        else:
            print("Invalid PIN. PIN must be 4 digits.")

    def authenticate_account(self):
        account_number = input("Enter account number: ")
        pin = input("Enter PIN: ")

        account = self.get_account(account_number=account_number)
        if account and account.validate_pin(pin):
            print("Authentication Successful.")
            input("Press Enter to continue...")
            ATM.account_menu(account)
        else:
            print("Invalid account number or PIN.")
    
    @staticmethod
    def account_menu(account):
        while True:
            os.system("cls")
            ATM.menu()

            choice = input("Enter your choice(1-5): ")
            os.system("cls")
            if choice == '1':
                print(f"Current Balance: {account.check_balance()}")
                input("Press Enter to continue...")
                
            elif choice == '2':
                
                try:
                    amount = float(input("Enter deposit amount: "))
                    account.deposit(amount)
                    print(f"${amount} deposited")
                except ValueError:
                    print("Amount can't be less than 1 and must be interger")
                input("Press Enter to continue...")
                
                    
            elif choice == '3':
                
                try:
                    amount = float(input("Enter withdrawal amount: "))
                    account.withdraw(amount)
                    print(f"Withdrew ${amount}")
                except ValueError:
                    print("Amount can't be less than 1 and must be interger")
                    
            elif choice == '4':
                old_pin = input("Enter old PIN: ")
                new_pin = input("Enter new PIN: ")
                if account.change_pin(old_pin, new_pin):
                    print("PIN changed successfully.")
                else:
                    print("Failed to change Pin. Ensure the old Pin si correct and the new PIN is 4 digits")
                input("Press Enter to continue...")
                    
            elif choice == '5':
                print("Logging out. Thank you for using out ATM.")
                break


# Main Men
def main():
    atm = ATM()
    while True:
        os.system("cls")
        print("--- Welcome to Mini ATM Machine ---:")
        print("1. Create Account")
        print("2. Access Account")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        os.system("cls")

        if choice == '1':
            atm.create_account()
            input("Press Enter to continue...")
            
        elif choice == '2':
            atm.authenticate_account()
            input("Press Enter to continue...")
            
        elif choice == '3':
            print("Thank you for using Mini ATM Machine. Goodbye!")
            break
    
if __name__ == "__main__":
    main()