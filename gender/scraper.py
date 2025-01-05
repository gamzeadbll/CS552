import unicodedata

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def normalize_name(name):
    name = name.split("(")[0].strip()

    translation_table = str.maketrans({
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o",
        "ş": "s", "Ş": "s",
        "ü": "u", "Ü": "u",
    })
    normalized = name.translate(translation_table).lower()
    return ''.join(
        char for char in unicodedata.normalize('NFD', normalized)
        if unicodedata.category(char) != 'Mn'
    )


def scrape_baby_names(url, names=None):
    if names is None:
        names = []

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    baby_names_table = soup.find("div", id="baby-names-table")
    if not baby_names_table:
        print("Could not find the baby names table.")
        return names

    table = baby_names_table.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        name_anchor = cells[0].find("a", class_="baby-name-link")
        name = normalize_name(name_anchor.text.strip()) if name_anchor else "N/A"
        gender_img = cells[2].find("img")
        if gender_img:
            alt_text = gender_img.get("alt", "").lower()
            if "boy" in alt_text:
                gender = "Male"
            elif "girl" in alt_text:
                gender = "Female"
            elif "unisex" in alt_text:
                gender = "Unisex"
            else:
                gender = "N/A"
        else:
            gender = "N/A"

        names.append((name, gender))

    pagination_div = soup.find("div", class_="bottom_pagination")
    next_button = pagination_div.find("a", class_="next page-numbers") if pagination_div else None

    if next_button:
        next_url = next_button.get("href")
        return scrape_baby_names(next_url, names)

    return names


def save_to_excel(data, file_name):
    wb = Workbook()
    ws = wb.active
    ws.title = "Names"
    ws.append(["Name", "Gender"])

    for name, gender in data:
        ws.append([name, gender])

    wb.save(file_name)
    print(f"Data saved to {file_name}")


# Example usage
def main():
    url = "https://www.momjunction.com/baby-names/turkish/#fiter-baby-names-by-alphabet"
    print("Scraping baby names...")
    baby_names = scrape_baby_names(url)
    save_to_excel(baby_names, "turkish_names.xlsx")


if __name__ == "__main__":
    main()