import os

class Animal:
    def make_sound(self):
        print("Some general animal sound")
        
class Dog(Animal):
    def make_sound(self):
        print("Woof Woof")
        
class Cat(Animal):
    def make_sound(self):
        print("Meaw Meaw")
        
        
class Cow(Animal):
    def make_sound(self):
        print("Moo Moo")

def make_all_sounds(animals):
    for animal in animals:
        animal.make_sound()

def menu():
    print("=== Animal Sound Simulator ===")
    print("1. Add Dog")
    print("2. Add Cat")
    print("3. Add Cow")
    print("4. Make All Sounds")
    print("5. Exit")
    

def main():
    animals = []
    while True:
        os.system("cls")
        menu()
        choice = input("Enter your choice (1-5): ").strip()
        os.system("cls")

        if choice == "1":
            animals.append(Dog())
            input("Dog Added...")
        elif choice == "2":
            animals.append(Cat())
            input("Cat Added...")
        elif choice == "3":
            animals.append(Cow())
            input("Cow Added...")
        elif choice == "4":
            if not animals:
                print("No animals added")
            else:
                make_all_sounds(animals=animals)
            input("Press Enter to continue...")
        elif choice == "5":
            print("Exiting the program.")
            break
            
if __name__ == "__main__":
    main()
        
            
        
        