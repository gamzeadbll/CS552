import pandas as pd
from scholarly import scholarly
import time


# Replace 'your_api_key' with your actual SerpAPI key - not used in this code
API_KEY = "your_api_key"



def fetch_author_data(author_name):
    try:
        # Set up the search parameters for the author
        params = {
            "engine": "google_scholar_author",
            "q": author_name,  # Author's name
            "api_key": API_KEY  # Your SerpAPI key
        }

        # Perform the search
        search = GoogleSearch(params)
        author_data = search.get_dict()

        # Check if the response contains author information
        if "author" not in author_data:
            print(f"No author found for {author_name}.")
            return None, []

        # Extract author information
        author_info = {
            "Name": author_data["author"]["name"],
            "Affiliation": author_data["author"].get("affiliations", ""),
            "Total Citations": author_data["author"].get("cited_by", {}).get("value", 0),
            "h-index": author_data["author"].get("h_index", 0),
            "i10-index": author_data["author"].get("i10_index", 0),
            "Interests": ", ".join(author_data["author"].get("interests", [])),
            "Profile Link": author_data["author"].get("link", "")
        }

        # Extract publications (articles)
        articles = []
        for pub in author_data["author"].get("articles", []):
            article_info = {
                "Title": pub["title"],
                "Citations": pub.get("cited_by", {}).get("value", 0),
                "Year": pub.get("year", "N/A"),
                "Link": pub.get("link", "")
            }
            articles.append(article_info)

        return author_info, articles

    except Exception as e:
        print(f"Error fetching data for {author_name}: {e}")
        return None, []


def setup_proxy():
    pg = ProxyGenerator()
    # Option 1: Free proxies
    if pg.FreeProxies():
        scholarly.use_proxy(pg)
        print("Using free proxies")
    else:
        print("Failed to set up free proxies")

    # Option 2: Tor (requires Tor to be installed and running)
    # if pg.Tor_Internal(tor_cmd="path/to/tor"):
    #     scholarly.use_proxy(pg)
    #     print("Using Tor proxies")
    # else:
    #     print("Failed to set up Tor proxies")


def setup_paid_proxies():
    pg = ProxyGenerator()
    paid_proxy = {
        "http": "http://username:password@proxy-server.com:port",
        "https": "https://username:password@proxy-server.com:port",
    }
    pg.CustomProxies(proxies=[paid_proxy])
    scholarly.use_proxy(pg)
    print("Using paid proxy")

#setup_paid_proxies()

def get_author_details(author_name):
   # try:

        search_query = scholarly.search_author(author_name)
        author = next(search_query)
        print(author)
        author_data = scholarly.fill(author, sections=["basics", "indices", "publications"])

        # Extract author metadata
        author_row = {
            "Name": author_data.get("name", ""),
            "Affiliation": author_data.get("affiliation", ""),
            "Email Domain": author_data.get("email_domain", ""),
            "Cited By": author_data.get("citedby", 0),
            "h-index": author_data.get("hindex", 0),
            "h-index (5y)": author_data.get("hindex5y", 0),
            "i10-index": author_data.get("i10index", 0),
            "i10-index (5y)": author_data.get("i10index5y", 0),
            "Interests": ", ".join(author_data.get("interests", [])),
            #"Scholar ID": author_data.get("scholar_id", ""),
        }

        return author_row

    #except Exception as e:
        #print(f"Error fetching data for {author_name}: {e}")
        #return None, None

def get_articles(author_name):
    try:

        search_query = scholarly.search_author(author_name)
        author = next(search_query)
        author_data = scholarly.fill(author, sections=["basics", "indices", "publications"])

        # Extract article metadata
        articles = []
        for pub in author_data.get("publications", []):
            filled_pub = scholarly.fill(pub)  # Fill publication details
            article_row = {
                "Author Name": author_row["Name"],
                "Article Title": filled_pub.get("bib", {}).get("title", ""),
                "Publication Year": filled_pub.get("bib", {}).get("pub_year", ""),
                "Venue": filled_pub.get("bib", {}).get("venue", ""),
                "Cited By": filled_pub.get("num_citations", 0),
                "Scholar Link": filled_pub.get("pub_url", ""),
            }
            articles.append(article_row)

        return articles

    except Exception as e:
        print(f"Error fetching data for {author_name}: {e}")
        return None, None

def get_author_data(author_name):
    try:
        params = {
            "engine": "google_scholar_profiles",
            "mauthors": author_name
        }
        search = GoogleSearch(params)
        results = search.get_dict()
    
        # Check if author profiles are found
        if "profiles" in results:
            author_profile = results["profiles"][0]  # Take the first matching profile
            author_info = {
                "Name": author_profile.get("name", ""),
                "Affiliation": author_profile.get("affiliations", ""),
                "Interests": ", ".join(author_profile.get("interests", [])),
                "Cited By": author_profile.get("cited_by", {}).get("value", 0),
                "h-index": author_profile.get("h_index", {}).get("value", 0),
                "h-index (5y)": author_profile.get("h_index", {}).get("five_year_value", 0),
                "i10-index": author_profile.get("i10_index", {}).get("value", 0),
                "i10-index (5y)": author_profile.get("i10_index", {}).get("five_year_value", 0),
                "Email Domain": author_profile.get("email", ""),
                "Scholar ID": author_profile.get("author_id", ""),
                "Profile URL": author_profile.get("link", ""),
                "Thumbnail": author_profile.get("thumbnail", "")
            }
            return author_info
        else:
            print(f"No profiles found for {author_name}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        

authors_file_path = "/Users/gamzeadibelli/OZU DS/CS552/Project/data/authors_final.xlsx"

authors_data = pd.ExcelFile(authors_file_path)
authors_sheet_data = pd.read_excel(authors_file_path, sheet_name='Sheet1')

# Extract unique authors from the "Instructor Name" column
authors_list = authors_sheet_data['Instructor Name'].drop_duplicates().tolist()


authors = ["Olcay Taner Yıldız", "Milad Elyasi","SELAHATTİN KURU"]
author_rows = []
all_articles = []
failed_authors = []  # Track authors with errors

# Define function to handle retries and errors
def get_author_data_safely(author_name):
    try:
        print(f"Fetching data for {author_name}...")
        author_row = get_author_details(author_name)
        if author_row:
            return author_row
        else:
            raise ValueError("No data returned for author")
    except Exception as e:
        print(f"Error processing {author_name}: {e}")
        failed_authors.append({"Author Name": author_name, "Error": str(e)})
        time.sleep(1)
        return None

# Process authors
for name in authors_list:
    print("Waiting for 4 seconds...")
    time.sleep(4)
    print(f"Proceeding with {name}...")
    author_row = get_author_data_safely(name)
    if author_row:
        author_rows.append(author_row)

# Create DataFrames
author_df = pd.DataFrame(author_rows)
failed_df = pd.DataFrame(failed_authors)

# Write to Excel
with pd.ExcelWriter("scholarly_data_istanbul.xlsx") as writer:
    author_df.to_excel(writer, sheet_name="Authors", index=False)
    failed_df.to_excel(writer, sheet_name="Failed Authors", index=False)

print("Data written to scholarly_data_istanbul.xlsx")
