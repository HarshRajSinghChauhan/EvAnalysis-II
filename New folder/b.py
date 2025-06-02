import pandas as pd
import re

# Load your file
df = pd.read_csv("bikedekho_ev_reviews.csv")

# Function to extract fields from review text
def extract_bike_review_parts(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if len(lines) < 4:
        return pd.Series([None] * 4)

    lines = lines[1:]  # Skip initial letter

    match = re.match(r"(.+?)\s+On\s+(.+)", lines[0])
    reviewer = match.group(1).strip() if match else None
    review_date = match.group(2).strip() if match else None

    title = lines[2]
    body = ' '.join(lines[3:])

    return pd.Series([reviewer, review_date, title, body])

# Apply extraction
df[['reviewer', 'review_date', 'review_title', 'review_body']] = df['text'].apply(extract_bike_review_parts)

# Rename 'rating' to match cleaned format
df.rename(columns={'rating': 'rating_extracted'}, inplace=True)

# Save cleaned file
df.to_csv("bikedekho_reviews_cleaned.csv", index=False, encoding='utf-8', quoting=1)
