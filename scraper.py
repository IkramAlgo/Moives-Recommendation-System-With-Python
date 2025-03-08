import requests
from bs4 import BeautifulSoup

def scrape_justwatch(movie_title, country="us"):
    search_url = f"https://www.justwatch.com/{country}/search?q={movie_title.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve data.")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    streaming_links = {}

    # Update the selector to match JustWatch's current structure
    for link in soup.select("a[href^='/us/movie']"):  
        provider_url = "https://www.justwatch.com" + link["href"]
        provider_name = link.find("img")["alt"] if link.find("img") else "Unknown Provider"

        if provider_name not in streaming_links:
            streaming_links[provider_name] = provider_url

    return streaming_links
