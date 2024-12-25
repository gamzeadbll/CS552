from scrapers.uniName_based_search import scrape_google_scholar_authors
import time
import pandas as pd

def main():
    driver_path = "/Users/egeoruc/Downloads/chromedriver-mac-arm64/chromedriver"  # Replace with the correct path
    excel_file = "data/universities.xlsx"  # Path to your Excel file

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file)

    # Start from the second row (index 1)
    for index, row in df.iloc[1:].iterrows():  # Change the starting index here
        university_name = row['University Name']  # Assuming the column name is 'University Name'

        try:
            print(f"Starting to scrape authors for: {university_name}")
            scrape_google_scholar_authors(driver_path, university_name)
            print(f"Finished scraping for {university_name}. Waiting for 10 minutes...")
            time.sleep(600)  # 600 seconds = 10 minutes
        except Exception as e:
            print(f"Error occurred while scraping for {university_name}: {e}")
            # Optionally, log the error to a file
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"Failed to scrape {university_name}: {e}\n")
            continue  # Skip to the next university

    print("Completed scraping for all universities.")


if __name__ == "__main__":
    main()