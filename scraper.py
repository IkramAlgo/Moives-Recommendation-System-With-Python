import requests
from bs4 import BeautifulSoup
import os

def scrape_movie_links(movie_title):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # IMDb Search & Scraping
    imdb_search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt"
    imdb_response = requests.get(imdb_search_url, headers=headers)
    imdb_soup = BeautifulSoup(imdb_response.text, "html.parser")

    imdb_link = "#"
    imdb_result = imdb_soup.find("a", class_="ipc-metadata-list-summary-item__t")
    if imdb_result:
        imdb_link = "https://www.imdb.com" + imdb_result["href"]
    print(f"IMDb Link: {imdb_link}")  # Debug: Print IMDb link

    # JustWatch Scraping
    justwatch_search_url = f"https://www.justwatch.com/us/search?q={movie_title.replace(' ', '%20')}"
    justwatch_response = requests.get(justwatch_search_url, headers=headers)
    justwatch_soup = BeautifulSoup(justwatch_response.text, "html.parser")

    justwatch_link = "#"
    jw_result = justwatch_soup.find("a", class_="title-list-row__column")
    if jw_result:
        justwatch_link = "https://www.justwatch.com" + jw_result["href"]
    else:
        # Fallback: Search for the first movie link using a different class or tag
        jw_fallback = justwatch_soup.find("a", class_="title-list-row__column")
        if jw_fallback:
            justwatch_link = "https://www.justwatch.com" + jw_fallback["href"]
        else:
            # If still not found, try a different approach
            jw_fallback_2 = justwatch_soup.find("a", href=True)
            if jw_fallback_2:
                justwatch_link = "https://www.justwatch.com" + jw_fallback_2["href"]
    print(f"JustWatch Link: {justwatch_link}")  # Debug: Print JustWatch link

    # TMDB Link
    tmdb_api_key = os.getenv("TMDB_API_KEY")
    tmdb_link = "#"
    if tmdb_api_key:
        tmdb_search_url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={tmdb_api_key}"
        tmdb_response = requests.get(tmdb_search_url).json()
        if tmdb_response.get("results"):
            tmdb_id = tmdb_response["results"][0]["id"]
            tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}"
    print(f"TMDB Link: {tmdb_link}")  # Debug: Print TMDB link

    return {
        "IMDb": imdb_link,
        "JustWatch": justwatch_link,
        "TMDB": tmdb_link
    }