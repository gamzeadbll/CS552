from scholarly import scholarly
import pandas as pd
import os

# Function to extract university names from file names
def extract_university_names(folder_path):
    university_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            # Replace "ÜNİVERSİTESİ" and "Üniversitesi" with "Universityy"
            name = filename.replace("-kadro.xlsx", "").replace("ÜNİVERSİTESİ", "Universityy").replace("Üniversitesi", "Universityy")
            university_names.append(name)
    return university_names

# Function to get author data from Google Scholar
def fetch_author_data(universities):
    author_data = []
    for university in universities:
        print(f"Searching authors for {university}...")
        search_query = scholarly.search_author(university)

        try:
            while True:
                # Get the next author
                author = next(search_query)
                print(f"Found author: {author['name']}")
                author_data.append({
                    "University": university,
                    "Author Name": author['name'],
                    "Author URL": author['url_picture']  # URL of the author
                })
        except StopIteration:
            pass

        # If there is a next page, continue to fetch authors
        # Note: Scholarly handles paginated results automatically.

    return author_data

# Main script
if __name__ == "__main__":
    folder_path = "/Users/gamzeadibelli/OZU DS/CS552/Project/data/data test"

    # Step 1: Extract university names from the folder
    universities = extract_university_names(folder_path)

    # Step 2: Fetch author data from Google Scholar
    all_author_data = fetch_author_data(universities)

    # Step 3: Save the data to a CSV file
    df = pd.DataFrame(all_author_data)
    output_path = folder_path + "/author_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


