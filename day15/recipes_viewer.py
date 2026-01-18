import os

def load_file(path:str):
    recipes = {}
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            recipe_name = None
            for line in lines:
                line = line.lower().strip()
                if line.startswith("ingredients"):
                    new_line = line.replace("ingredients:", '').strip()
                    recipes[recipe_name]["ingredients"] = new_line.split(", ")
                elif line.startswith("instructions"):
                    new_line = line.replace("instructions:", '').strip()
                    recipes[recipe_name]["instructions"] = new_line.lower().strip()
                else:
                    recipe_name = line.lower().strip()
                    recipes[recipe_name] = {}
    except FileNotFoundError:
        print("The file not founded")

    return recipes

def show_recipe(name, recipe:dict):
    print(f"--- {name.title()} ---")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}.")
    print(f"Instructions: {(recipe['instructions'])}")

def get_recipe(recipes:dict, name:str):
    
    if name not in recipes.keys():
        print("Recipe not found.")
        return None
    
    show_recipe(name, recipes[name])
    
    
def menu():
    
        print("1. View a recipe")
        print("2. List all recipes")
        print("3. Exit")
        
def main():
    recipes = load_file("recipes.txt")
    
    while True:
        os.system("cls")
        menu()
        choice = input("Choose an option: ")
        
        if choice == "1":
            name = input("Enter the recipe name: ").lower().strip()
            get_recipe(recipes, name)
            input("Press Enter to continue...")
        elif choice == "2":
            print("Available recipes:")
            for recipe in recipes.keys():
                print(f"- {recipe.title()}")
            input("Press Enter to continue...")
        elif choice == "3":
            break


if __name__ == "__main__":
    main()
    