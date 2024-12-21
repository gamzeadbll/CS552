import pandas as pd
from scholarly import scholarly
import time


# Replace 'your_api_key' with your actual SerpAPI key
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

def get_author_data(author_name, api_key):
    params = {
        "engine": "google_scholar_profiles",
        "mauthors": author_name,
        "api_key": api_key
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


authors = ["Olcay Taner Yıldız", "Milad Elyasi"]
author_rows = []
all_articles = []

for name in authors:
    time.sleep(5)
    print("waited for 5 seconds...")
    print(name)
    author_row  = get_author_details(name)
    author_rows.append(author_row)

author_df = pd.DataFrame(author_rows)
#article_df = pd.DataFrame(all_articles)

# Write to Excel
with pd.ExcelWriter("scholar_data.xlsx") as writer:
    author_df.to_excel(writer, sheet_name="Authors", index=False)
    #article_df.to_excel(writer, sheet_name="Articles", index=False)

print("Data written to scholar_data.xlsx")
