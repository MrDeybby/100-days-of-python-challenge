
def check_ingredients(ingredients_list: set, recipe_ingredients: set) -> list:
    missing_ingredients = ingredients_list - recipe_ingredients
    return missing_ingredients

def add_ingredient(ingredient: str, ingredients_list: set):
    ingredients_list.add(ingredient)
    
def main():
    ingredients_list = {"sugar", "salt", "flour", "eggs", "milk", "butter", "baking powder"}
    user_list = set()
    while True:
        user_input = input("Enter a recipe ingredient to check (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        add_ingredient(user_input.lower(), user_list)
        
    
    missing = check_ingredients(ingredients_list, user_list)
    extra_ingredients = check_ingredients(user_list, ingredients_list)
    print("=== Ingredients Checker ===")
    
    if missing and extra_ingredients:
        print("Missing ingredients:", ", ".join(missing))
        print("Extra ingredients:", ", ".join(extra_ingredients))
    elif missing:
        print("Missing ingredients:", ", ".join(missing))
        
    elif extra_ingredients:
        print("Extra ingredients:", ", ".join(extra_ingredients))
        print("You have all the necessary ingredients!")
    else:
        print("You have all the necessary ingredients!")

if __name__ == "__main__":
    main()