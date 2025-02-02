chocolate = ['nutty', 'sweet', 'creamy']
vanilla = ['sweet', 'creamy', 'cold']
pickle = ['sour', 'salty', 'cold']

def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(list2))
    union = len(set(list1).union(list2))
    return intersection / union

def contrast_score(list1, list2):
    intersection = len(set(list1).intersection(list2))
    union = len(set(list1).union(list2))
    if intersection == 0:  # To avoid division by zero
        return float('inf')
    return union / intersection

def normalize_contrast_score(list1, list2):
    contrast = contrast_score(list1, list2)
    max_possible_contrast = len(set(list1).union(list2))  # Union size as the maximum
    return contrast / max_possible_contrast

# Calculate scores for chocolate and vanilla
jaccard = jaccard_similarity(chocolate, pickle)
normalized_contrast = normalize_contrast_score(chocolate, pickle)

# Weights
jaccard_weight = 0.5
contrast_weight = 0.5

# Total score
total_score = jaccard_weight * jaccard + contrast_weight * normalized_contrast

# Print results
print("Jaccard Similarity:", jaccard)
print("Normalized Contrast Score:", normalized_contrast)
print("Total Score:", total_score)

# Interpretation
if jaccard > 0.5:
    print("Chocolate and vanilla are similar.")
elif jaccard >= 0.4:
    print("Chocolate and vanilla are somewhat similar.")
else:
    print("Chocolate and vanilla are not similar.")
