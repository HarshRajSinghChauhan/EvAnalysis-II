import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_bikedekho_url(brand, model_slug):
    return f"https://www.bikedekho.com/{brand}/{model_slug}/reviews"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Set your chromedriver path here
    service = Service(r"C:\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Read your CSV with Brand and Model_Slug columns
    df = pd.read_csv("bikedekho_ev_models.csv")
    output_file = "bikedekho_ev_reviews.csv"

    for idx, row in df.iterrows():
        all_reviews = []
        brand, model_slug = row["Brand"], row["Model_Slug"]
        url = get_bikedekho_url(brand, model_slug)
        print(f"Scraping: {brand} {model_slug} - {url}")

        for page in range(1, 4):  # Scrape first 3 pages
            page_url = url if page == 1 else url + f"-page{page}"
            driver.get(page_url)

            # Wait up to 15 seconds for reviews to load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.readReviewBox.readReviewLazy"))
                )
                reviews = driver.find_elements(By.CSS_SELECTOR, "div.readReviewBox.readReviewLazy")
            except Exception as e:
                print(f"Timeout: No reviews loaded for {brand} {model_slug}")
                reviews = []

            print(f"Found {len(reviews)} reviews on page {page}.")

            if not reviews:
                break  # No more reviews

            for review in reviews:
                try:
                    text = review.find_element(By.CSS_SELECTOR, "div.contentheight > div").text.strip()
                except:
                    text = ""
                try:
                    rating = review.find_element(By.CSS_SELECTOR, "span.ratingStarNew").text.strip()
                except:
                    rating = ""
                if text:
                    all_reviews.append({
                        "brand": brand,
                        "model_slug": model_slug,
                        "text": text,
                        "rating": rating
                    })
            time.sleep(random.uniform(1, 2))

        # Save after each model is done (append mode or write if first time)
        df_temp = pd.DataFrame(all_reviews)
        if not df_temp.empty:
            if os.path.exists(output_file):
                df_temp.to_csv(output_file, mode='a', header=False, index=False)
            else:
                df_temp.to_csv(output_file, mode='w', header=True, index=False)
            print(f"Saved {len(df_temp)} reviews for {brand} {model_slug} to file.\n")
        else:
            print(f"No reviews extracted for {brand} {model_slug}.\n")

    driver.quit()
    print(f"\nAll done! Reviews are saved to {output_file}")

if __name__ == "__main__":
    main()