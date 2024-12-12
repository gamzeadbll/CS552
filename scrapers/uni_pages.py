from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import os
from scrapers.instructors_page import fetch_instructors
from utils.helpers import save_instructors_to_excel


def normalize_turkish(text):
    mapping = str.maketrans("İıŞşÇçĞğÜüÖö", "IiSsCcGgUuOo")
    return text.translate(mapping).lower().strip()


def fetch_university_pages(base_url, driver_path):
    os.makedirs("data", exist_ok=True)

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(base_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
        )

        wb = Workbook()
        ws = wb.active
        ws.title = "Universities"
        ws.append(["University Name", "Link"])

        processed_universities = set()

        while True:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
            )
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            all_universities_processed = True

            for idx, row in enumerate(rows):
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 2:
                    university_name = cols[0].text.strip()
                    city = cols[1].text.strip()
                    normalized_city = normalize_turkish(city)

                    if university_name in processed_universities:
                        continue

                    if normalized_city == "istanbul":
                        link_element = cols[0].find_element(By.TAG_NAME, "a")
                        link = link_element.get_attribute("href")

                        ws.append([university_name, link])
                        print(f"Added: {university_name} (City: {city})")
                        processed_universities.add(university_name)
                        link_element.click()

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "authorlistTb"))
                        )

                        try:
                            instructors = fetch_instructors(driver)
                            save_instructors_to_excel(university_name, instructors)
                            print(f"Saved instructors for {university_name}.")
                        except Exception as e:
                            print(f"Error fetching instructors for {university_name}: {e}")

                        print(f"Returning to the base page...")
                        driver.get(base_url)

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
                        )

                        all_universities_processed = False
                        break

            if all_universities_processed:
                break

        wb.save("data/universities.xlsx")
        print(f"Saved university list to data/universities.xlsx.")

    finally:
        driver.quit()

    return list(processed_universities)