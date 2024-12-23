from scrapers.uni_pages import fetch_university_pages


def main():
    BASE_URL = "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"
    DRIVER_PATH = "/Users/egeoruc/Downloads/chromedriver-mac-arm64/chromedriver"

    try:
        universities = fetch_university_pages(BASE_URL, DRIVER_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()