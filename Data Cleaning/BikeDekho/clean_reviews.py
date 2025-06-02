import pandas as pd

# Load the CSV
df = pd.read_csv("bikedekho_ev_reviews.csv")

# Optional: Clean extra periods or malformed text if needed
df['text'] = df['text'].str.strip().str.replace(r'\.{2,}', '.', regex=True)

# Reorder columns: rating before text
df = df[['brand', 'model_slug', 'rating', 'text']]

# Save the updated version
df.to_csv("cleaned_bikedekho_ev_reviews.csv", index=False)
