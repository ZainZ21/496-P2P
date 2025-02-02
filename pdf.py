import pandas as pd
import re
from pypdf import PdfReader

# Read the PDF
reader = PdfReader('FlavorBible.pdf')

# Extract text while keeping the layout
text_data = []
start_page = 64  # Page 43 in actual PDF (zero-based index)
end_page = 1015  # Page 811

for page_num in range(start_page, end_page):  
    page = reader.pages[page_num]  
    text = page.extract_text()
    if text:
        lines = text.split("\n")  # Split text into lines
        text_data.extend([(page_num + 1, line.strip()) for line in lines])  # Store with correct page number

# Create DataFrame
df = pd.DataFrame(text_data, columns=['Page', 'Text'])

# Drop first 3 rows after extraction (adjust if needed)
df = df.iloc[3:].reset_index(drop=True)

# Define Heuristics
def is_heading(text, page_indents):
    """Checks if the line is a heading based on capitalization and indentation rules."""
    return (
        bool(re.match(r"^[A-Z]{3,}", text))  # First 3+ letters are uppercase
        and page_indents < 2  # Fewer than 2 indents on the page
        and not text.startswith("-")  # No leading dash
        and not text.startswith(" ")  # No indentation
    )

def is_flavor(text, page_indents):
    """Checks if the line is a flavor based on indentation and dash rules."""
    no_pronouns = not re.search(r"\b(I|YOU|WE|THEY|THEIR|MY|OUR)\b", text, re.IGNORECASE)
    
    if page_indents < 2:
        return not text.startswith("-") and no_pronouns
    else:
        return text.startswith(" ") and not text.startswith("-") and no_pronouns

# Identify Indents Per Page
df["Indent"] = df["Text"].apply(lambda x: x.startswith(" "))
df["Page_Indents"] = df.groupby("Page")["Indent"].transform("sum")

# Classify Each Line
df["Heading"] = df.apply(lambda row: is_heading(row["Text"], row["Page_Indents"]), axis=1)
df["Flavor"] = df.apply(lambda row: is_flavor(row["Text"], row["Page_Indents"]), axis=1)
df["Ignore"] = ~df["Heading"] & ~df["Flavor"]  # Anything that is neither heading nor flavor

# Filter Relevant Data
flavor_matches = df[~df["Ignore"]].reset_index(drop=True)

# Create Headings Vector
headings_vec = flavor_matches["Text"][flavor_matches["Heading"]].tolist()

# Repeat each heading until the next heading appears
headings = []
current_heading = None
for is_heading, text in zip(flavor_matches["Heading"], flavor_matches["Text"]):
    if is_heading:
        current_heading = text
    headings.append(current_heading)

# Create Final Tidy DataFrame
tidy_flavors = pd.DataFrame({"Main": headings, "Pairing": flavor_matches["Text"]})
tidy_flavors = tidy_flavors[tidy_flavors["Main"] != tidy_flavors["Pairing"]]  # Remove self-pairing rows

# Save to CSV
tidy_flavors.to_csv("flavor_bible_full.csv", index=False)

