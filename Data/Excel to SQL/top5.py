import pandas as pd

df = pd.read_excel(r"C:\Harsh R.S. Chauhan\Projects\EV analysis II\Data\top5maker.xlsx")

# print("Column names:", df.columns.tolist())

unique_brands_with_category = df[['Category', 'Brand']].drop_duplicates()
print(unique_brands_with_category)

# Save to new Excel file
unique_brands_with_category.to_excel(r"C:\Harsh R.S. Chauhan\Projects\EV analysis II\Data\unique_brands.xlsx", index=False)

print("Saved to unique_brands.xlsx")