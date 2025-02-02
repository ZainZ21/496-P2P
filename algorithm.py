import pandas as pd


# Example flavor_pairings dictionary
flavor_pairings = {
    'sweet': {'Flavor_profile_similar': ['salty', 'umami', 'sweet'], 'Flavor_profile_contrast': ['sour', 'bitter']},
    'sour': {'Flavor_profile_similar': ['bitter', 'sour'], 'Flavor_profile_contrast': ['sweet', 'salty', 'umami']},
    'salty': {'Flavor_profile_similar': ['umami', 'salty'], 'Flavor_profile_contrast': ['sweet', 'sour']},
    'bitter': {'Flavor_profile_similar': ['sour', 'bitter'], 'Flavor_profile_contrast': ['sweet', 'salty']},
    'umami': {'Flavor_profile_similar': ['salty', 'umami'], 'Flavor_profile_contrast': ['sweet', 'sour']}
}

# Load your data
df = pd.read_csv('test4.csv')


df.rename(columns={'Taste (if app)': 'Taste', 'Function (if app)': 'Function'}, inplace=True)

# Normalize text formatting
df['Ingredient'] = df['Ingredient'].str.lower().str.strip()
df['Taste'] = df['Taste'].str.lower().str.replace('"', '').str.strip()
df['Pairings'] = df['Pairings'].str.lower().str.replace('"', '').str.strip()

# Debugging
print(df.head())


user_choice = input("Pair ingredients choice: 1 for similar, 2 for contrast, 3 for all pairings: ")
user_ingredient = input("Enter ingredient: ").lower().strip()

# Find the row for the user's chosen ingredient
user_row = df.loc[df['Ingredient'] == user_ingredient]

if user_row.empty:
    print(f"No matching ingredient found for '{user_ingredient}'. Please check spelling.")
else:
    if user_choice == '3':
        print(f"Pairings for '{user_ingredient}':")
        print(user_row['Pairings'].values[0])
    else:

        # Get the user's ingredient taste(s)
        user_taste_str = user_row['Taste'].values[0]  
        user_tastes = [t.strip() for t in user_taste_str.split(',')]

        # Determine whether to look up similar or contrast
        flavor_key = 'Flavor_profile_similar' if user_choice == '1' else 'Flavor_profile_contrast'

        # Collect a set of target flavors from flavor_pairings
        target_flavors = set()
        for t in user_tastes:
            if t in flavor_pairings:
                target_flavors.update(flavor_pairings[t][flavor_key])
            else:
                print(f"Warning: taste '{t}' not found in flavor_pairings. Skipping...")

        # Parse the "Pairings" column from the chosen ingredient
        pairings_str = user_row['Pairings'].values[0]

        # Handle case where pairings are missing
        if pd.isna(pairings_str) or not pairings_str.strip():
            print(f"No pairings found for '{user_ingredient}'.")
        else:
            # Turn the pairings into a list of ingredients
            pairing_list = [p.strip() for p in pairings_str.split(',')]

            # Check if the paired ingredients exist in df
            valid_pairings = []
            for p_ing in pairing_list:
                match_row = df.loc[df['Ingredient'] == p_ing]  # find a row with that ingredient
                if not match_row.empty:
                    # Retrieve taste(s) for that paired ingredient
                    paired_taste_str = match_row['Taste'].values[0]
                    paired_tastes = [pt.strip() for pt in paired_taste_str.split(',')]
                    
                    # If any of the paired_tastes intersect with target_flavors, keep it
                    if any(taste in target_flavors for taste in paired_tastes):
                        valid_pairings.append(p_ing)
                else:
                    print(f"Warning: '{p_ing}' from pairings not found in dataset.")

            # Print out the result
            if not valid_pairings:
                print(f"No valid pairings found for '{user_ingredient}' based on your flavor choice.")
            else:
                print(f"Ingredients paired with '{user_ingredient}' that match your flavor criteria:")
                for vp in valid_pairings:
                    print(f" - {vp}")