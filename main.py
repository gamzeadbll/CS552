from scrapers.uniName_based_search import scrape_google_scholar_authors
import time
import pandas as pd

def main():
    driver_path = "/Users/egeoruc/Downloads/chromedriver-mac-arm64/chromedriver"
    excel_file = "data/universities.xlsx"

    df = pd.read_excel(excel_file)


    for index, row in df.iloc[54:].iterrows():
        university_name = row['University Name']

        try:
            print(f"Starting to scrape authors for: {university_name}")
            scrape_google_scholar_authors(driver_path, university_name)
            print(f"Finished scraping for {university_name}. Waiting for 10 minutes...")
            time.sleep(300)
        except Exception as e:
            print(f"Error occurred while scraping for {university_name}: {e}")
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"Failed to scrape {university_name}: {e}\n")
            continue

    print("Completed scraping for all universities.")


if __name__ == "__main__":
    main()