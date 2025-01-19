import requests
from dotenv import load_dotenv
import os



# Load .env file
load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.spoonacular.com"

endpoint = f"{BASE_URL}/recipes/complexSearch"

user_query = input("Enter a food item: ")

params = {
    "apiKey": API_KEY,
    "query": user_query,
    "number": 1,
    "instructionsRequired": True,
    "includeIngredients": "tomato,cheese",
    "addRecipeInformation": True
}

# Make a GET request
response = requests.get(endpoint, params=params)

# Check the status code
if response.status_code == 200:
    data = response.json()
    results = data.get("results", [])
    
    if results:
        recipe = results[0]
        title = recipe.get("title", "No title available")
        source = recipe.get("sourceName", "Unknown source")
        url = recipe.get("sourceUrl", "No URL available")
        image_url = recipe.get("image", "No image available")
        instructions = recipe.get("analyzedInstructions", [])
        price_per_serving = recipe.get("pricePerServing", "Not provided")
        servings = recipe.get("servings", "Unknown")
        ready_in_minutes = recipe.get("readyInMinutes", "Unknown")

        print(f"\n--- Recipe Information ---")
        print(f"Title: {title}")
        print(f"Source: {source}")
        print(f"URL: {url}")
        print(f"Image: {image_url}")
        print(f"Servings: {servings}")
        print(f"Ready in: {ready_in_minutes} minutes")
        print(f"Price per serving: ${price_per_serving / 100:.2f}")  # Convert cents to dollars
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

else:
    print(f"Error: {response.status_code}, {response.text}")