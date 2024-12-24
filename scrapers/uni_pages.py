from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import os
import locale


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
        ws.append(["University Name", "City","Type","Opening Date "])  # Column header

        processed_universities = set()

        while True:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-striped"))
            )
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            all_universities_processed = True

            for idx, row in enumerate(rows):
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    university_name = cols[0].text.strip()
                    formatted_university_name = university_name.replace("ÜNİVERSİTESİ", "University")
                    city = cols[1].text.strip()
                    normalized_city = normalize_turkish(city)
                    type= cols[2].text.strip()
                    opening_date = cols[3].text.strip()

                    if formatted_university_name in processed_universities:
                        continue

                    ws.append([formatted_university_name,city,type,opening_date])
                    print(f"Added: {formatted_university_name} (City: {city})")
                    processed_universities.add(formatted_university_name)

                    all_universities_processed = False
                    break

            if all_universities_processed:
                break

        wb.save("data/universities.xlsx")
        print(f"Saved university list to data/universities.xlsx.")

    finally:
        driver.quit()

    return list(processed_universities)