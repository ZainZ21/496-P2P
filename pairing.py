# Dictionary of known ingredient pairings
ingredient_pairings = {
    "chocolate": ["vanilla", "peanut butter", "honey", "strawberry"],
    "vanilla": ["chocolate", "strawberry", "honey"],
    "pickle": ["cheese", "mustard"],
    "cheese": ["pickle", "bread", "tomato"],
    "honey": ["chocolate", "vanilla", "peanut butter"],
    "peanut butter": ["chocolate", "honey", "banana"],
    "strawberry": ["chocolate", "vanilla", "cream"],
}

def get_paired_ingredients(ingredient):
    """Retrieve direct pairings for the given ingredient."""
    return ingredient_pairings.get(ingredient, "No known pairings.")

def compare_similarity(ingredient1, ingredient2):
    if ingredient1 in ingredient_pairings and ingredient2 in ingredient_pairings:
        pairings1 = set(ingredient_pairings[ingredient1])
        pairings2 = set(ingredient_pairings[ingredient2])
        
        intersection = len(pairings1.intersection(pairings2))
        union = len(pairings1.union(pairings2))
        jaccard_similarity = intersection / union if union != 0 else 0
        
        return jaccard_similarity
    else:
        return "One or both ingredients not found in the pairings database."
    

# Test
ingredient_to_check = "chocolate"
paired_ingredients = get_paired_ingredients(ingredient_to_check)


print(compare_similarity("chocolate", "vanilla"))



# Display Results
print(f"Best ingredient pairings for {ingredient_to_check}: {paired_ingredients}")