import requests
from dotenv import load_dotenv
import os
import pandas as pd


# flavor_pairings dictionary
flavor_pairings = {
    'sweet': {'Flavor_profile_similar': ['salty', 'umami', 'sweet'], 'Flavor_profile_contrast': ['sour', 'bitter']},
    'sour': {'Flavor_profile_similar': ['bitter', 'sour'], 'Flavor_profile_contrast': ['sweet', 'salty', 'umami']},
    'salty': {'Flavor_profile_similar': ['umami', 'salty'], 'Flavor_profile_contrast': ['sweet', 'sour']},
    'bitter': {'Flavor_profile_similar': ['sour', 'bitter'], 'Flavor_profile_contrast': ['sweet', 'salty']},
    'umami': {'Flavor_profile_similar': ['salty', 'umami'], 'Flavor_profile_contrast': ['sweet', 'sour']}
}


df = pd.read_csv('test4.csv')


df.rename(columns={'Taste (if app)': 'Taste', 'Function (if app)': 'Function'}, inplace=True)


df['Ingredient'] = df['Ingredient'].str.lower().str.strip()
df['Taste'] = df['Taste'].str.lower().str.replace('"', '').str.strip()
df['Pairings'] = df['Pairings'].str.lower().str.replace('"', '').str.strip()

def show_all_pairings_for_ingredient(ingredient: str, df: pd.DataFrame):
    """
    Prints all pairings for a given ingredient from the local CSV.
    If the ingredient isn't found or doesn't have pairings, it prints a notice.
    """
    ingredient = ingredient.lower().strip()
    row = df.loc[df['Ingredient'] == ingredient]
    
    if row.empty:
        print(f"No matching ingredient found for '{ingredient}'.")
        return
    
    pairings_str = row['Pairings'].values[0]
    
    if pd.isna(pairings_str) or not pairings_str.strip():
        print(f"No pairings found for '{ingredient}'.")
    else:
        print(f"Pairings for '{ingredient}':")
        print(pairings_str)

load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.spoonacular.com"

def search_recipes_by_query(api_key, query, ingredients=None, number=1):
    """
    Searches for recipes using the 'complexSearch' endpoint.
    """
    endpoint = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "apiKey": api_key,
        "query": query,
        "number": number,
        "instructionsRequired": True,
        "addRecipeInformation": True
    }
    
    # If ingredients are provided, add them to the request
    if ingredients:
        params["includeIngredients"] = ingredients
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status() 
    return response.json()

def search_recipes_by_ingredients(api_key, ingredients, number=1):
    """
    Searches for recipes that can be made with the specified ingredients
    using the 'findByIngredients' endpoint.
    """
    endpoint = f"{BASE_URL}/recipes/findByIngredients"
    
    # Ensure 'ingredients' is a comma-separated string
    if isinstance(ingredients, list):
        ingredients = ",".join(ingredients)
    
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,
        "number": number
    }
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  

def print_complex_search_result(data):
    """
    Utility to print the first result from the 'complexSearch' data.
    """
    results = data.get("results", [])
    if results:
        recipe = results[0]  #just show the first result for now
        title = recipe.get("title", "No title available")
        source = recipe.get("sourceName", "Unknown source")
        url = recipe.get("sourceUrl", "No URL available")
        image_url = recipe.get("image", "No image available")
        price_per_serving = recipe.get("pricePerServing", "Not provided")
        servings = recipe.get("servings", "Unknown")
        ready_in_minutes = recipe.get("readyInMinutes", "Unknown")
        instructions = recipe.get("analyzedInstructions", [])

        print(f"\n--- Recipe Information ---")
        print(f"Title: {title}")
        print(f"Source: {source}")
        print(f"URL: {url}")
        print(f"Image: {image_url}")
        print(f"Servings: {servings}")
        print(f"Ready in: {ready_in_minutes} minutes")

        # convert to dollars
        if isinstance(price_per_serving, (int, float)):
            print(f"Price per serving: ${price_per_serving / 100:.2f}")
        else:
            print(f"Price per serving: {price_per_serving}")

        print("\n--- Instructions ---")
        if instructions:
            for i, instruction_set in enumerate(instructions, start=1):
                steps = instruction_set.get("steps", [])
                print(f"\nStep Set {i}:")
                for step in steps:
                    step_number = step.get("number")
                    step_text = step.get("step")
                    print(f"  Step {step_number}: {step_text}")
        else:
            print("No detailed instructions available.")
    else:
        print("No recipes found for the given query.")

def print_findbyingredients_results(data):
    """
    Utility to print the first result from the 'findByIngredients' data.
    """
    if data:
        # just show the top result
        top_recipe = data[0]
        title = top_recipe.get("title", "No title available")
        used_ing = top_recipe.get("usedIngredients", [])
        missed_ing = top_recipe.get("missedIngredients", [])
        image_url = top_recipe.get("image", "No image available")
        id_ = top_recipe.get("id", None)

        print(f"\n--- Top Recipe Information ---")
        print(f"Title: {title}")
        print(f"Image: {image_url}")

        print("\n--- Used Ingredients ---")
        for ing in used_ing:
            print(f" - {ing.get('original')}")

        print("\n--- Missed Ingredients ---")
        for ing in missed_ing:
            print(f" - {ing.get('original')}")

    else:
        print("No recipes found with the given ingredients.")


def main():
    while True:
        print("\n=== Spoonacular Recipe Search ===")
        print("1) Search recipes by query (complexSearch)")
        print("2) Search recipes by ingredients (findByIngredients)")
        print("3) Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user_query = input("Enter a recipe name or keyword: ")
            include_ingredients_choice = input("Include specific ingredients? (y/n): ").lower()
            user_query_ingredients = ""
            if include_ingredients_choice == "y":
                user_query_ingredients = input("Enter ingredients (comma-separated): ")

            try:
                data = search_recipes_by_query(
                    api_key=API_KEY,
                    query=user_query,
                    ingredients=user_query_ingredients,
                    number=1
                )
                print_complex_search_result(data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            ingredients_input = input("Enter ingredients (comma-separated): ")
            
            # Show Spoonacular results first
            try:
                data = search_recipes_by_ingredients(
                    api_key=API_KEY,
                    ingredients=ingredients_input,
                    number=1
                )
                print_findbyingredients_results(data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                continue
            
            # Now also show local pairings (up to the first two ingredients)
            ingredients_list = [ing.strip() for ing in ingredients_input.split(',')]
            print(" pairings ")
            for ingredient in ingredients_list[:2]:
                show_all_pairings_for_ingredient(ingredient, df)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()