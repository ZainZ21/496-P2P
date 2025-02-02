import requests
from dotenv import load_dotenv
import os
from algorithm import *

# Load .env file
load_dotenv()
API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.spoonacular.com"

def search_recipes_by_query(api_key, query, ingredients=None, number=1):
    """
    Searches for recipes using the 'complexSearch' endpoint.
    
    :param api_key: Your Spoonacular API key
    :param query: The main query (e.g. 'chicken')
    :param ingredients: Additional ingredients to include in the search (comma-separated string). Optional.
    :param number: Number of results to return
    :return: JSON response from the API
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
    response.raise_for_status()  # Raises an HTTPError if the status isn't 200
    return response.json()

def search_recipes_by_ingredients(api_key, ingredients, number=1):
    """
    Searches for recipes that can be made with the specified ingredients
    using the 'findByIngredients' endpoint.

    :param api_key: Your Spoonacular API key
    :param ingredients: A list or comma-separated string of ingredients
    :param number: Number of results to return
    :return: JSON response from the API
    """
    endpoint = f"{BASE_URL}/recipes/findByIngredients"
    
    # The 'ingredients' parameter in findByIngredients expects a comma-separated string.
    # If you already have a list, you'll need to join it with commas.
    if isinstance(ingredients, list):
        ingredients = ",".join(ingredients)
    
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,
        "number": number
    }
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raises an HTTPError if the status isn't 200
    return response.json()

def print_complex_search_result(data):
    
    results = data.get("results", [])
    if results:
        recipe = results[0]  # For simplicity, just show the first result
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

        # Price is often in cents, so convert to dollars
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

    if data:
        # For simplicity, show the top result
        top_recipe = data[0]
        title = top_recipe.get("title", "No title available")
        used_ing = top_recipe.get("usedIngredients", [])
        missed_ing = top_recipe.get("missedIngredients", [])
        image_url = top_recipe.get("image", "No image available")
        id_ = top_recipe.get("id", None)

        print(f"\n--- Recipe Information ---")
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
            try:
                data = search_recipes_by_ingredients(
                    api_key=API_KEY,
                    ingredients=ingredients_input,
                    number=1
                )
                print_findbyingredients_results(data)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()