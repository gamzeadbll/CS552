from scrapers.google import scrape_google_scholar

if __name__ == "__main__":
    print("Starting Google Scholar scraping...")
    scrape_google_scholar()
    print("Scraping completed. Check 'turkish_papers.csv' for results.")