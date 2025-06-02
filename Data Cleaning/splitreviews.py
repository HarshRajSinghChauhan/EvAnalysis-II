import pandas as pd
import re

# Load CSV
df = pd.read_csv("cardekho_ev_reviews.csv", quoting=1)

# Function to extract components
def split_review_block(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) < 4:
        return pd.Series([None]*5)

    # 1. Extract reviewer
    reviewer = lines[0]

    # 2. Extract date
    date_match = re.search(r'On (.+)', lines[1])
    review_date = date_match.group(1) if date_match else None

    # 3. Extract rating
    try:
        rating = float(lines[2])
    except ValueError:
        rating = None

    # 4. Extract title
    title = lines[3]

    # 5. Combine rest as review body
    review_body = ' '.join(lines[4:]) if len(lines) > 4 else ""

    return pd.Series([reviewer, review_date, rating, title, review_body])

# Apply function to each row
df[['reviewer', 'review_date', 'rating_extracted', 'review_title', 'review_body']] = df['review'].apply(split_review_block)

# Optional: Drop or keep original review column
# df.drop(columns=['review'], inplace=True)

# Save cleaned version
df.to_csv("carDekho_cleaned_reviews.xlsx", index=False, quoting=1, encoding='utf-8')
