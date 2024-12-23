from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import random
from selenium_stealth import stealth


def scrape_google_scholar():
    service = Service("/Users/egeoruc/Downloads/chromedriver-mac-arm64/chromedriver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # Enable verbose logging for debugging
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Apply stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )

    search_query = "site:edu.tr"
    driver.get(f"https://scholar.google.com/scholar?q={search_query}")
    time.sleep(2)

    with open("turkish_papers.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "authors", "year_or_details", "source"])

        while True:
            try:
                results = driver.find_elements(By.CLASS_NAME, "gs_ri")
                for result in results:
                    try:
                        title = result.find_element(By.CLASS_NAME, "gs_rt").text
                        gs_a_html = result.find_element(By.CLASS_NAME, "gs_a").get_attribute("outerHTML")
                        soup = BeautifulSoup(gs_a_html, "html.parser")
                        gs_a_text = soup.text
                        # Normalize text
                        gs_a_text = gs_a_text.replace("\xa0", " ").replace("–", "-").replace("—", "-")
                        authors, year_or_details, source = "couldn't find", "couldn't find", "couldn't find"

                        parts = gs_a_text.split(" - ", maxsplit=2)
                        if len(parts) > 0:
                            authors = parts[0].strip()
                        if len(parts) > 1:
                            year_or_details = parts[1].strip()
                        if len(parts) > 2:
                            source = parts[2].strip()

                        writer.writerow([title, authors, year_or_details, source])
                    except Exception as e:
                        print(f"Error processing result: {e}")
                        continue

                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#gs_n .gs_ico_nav_next + b"))
                    )
                    next_button_anchor = next_button.find_element(By.XPATH, "./..")
                    next_button_anchor.click()

                    time.sleep(random.uniform(10, 20))
                except Exception as e:
                    print(f"No more pages or error encountered: {e}")
                    break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

    driver.quit()