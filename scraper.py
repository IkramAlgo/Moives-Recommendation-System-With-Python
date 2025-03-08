import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import os

def scrape_movie_links(movie_title):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # IMDb Search & Scraping
    imdb_search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt"
    imdb_response = requests.get(imdb_search_url, headers=headers)
    imdb_soup = BeautifulSoup(imdb_response.text, "html.parser")
    
    imdb_link = "#"
    imdb_result = imdb_soup.find("td", class_="result_text")
    if imdb_result and imdb_result.a:
        imdb_link = "https://www.imdb.com" + imdb_result.a["href"]

    # TMDB Search & Scraping
    tmdb_api_key = os.getenv("TMDB_API_KEY")  # Use environment variable
    tmdb_link = "#"
    
    if tmdb_api_key:
        tmdb_search_url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={tmdb_api_key}"
        tmdb_response = requests.get(tmdb_search_url).json()
        if tmdb_response.get("results"):
            tmdb_id = tmdb_response["results"][0]["id"]
            tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}"

    # JustWatch Scraping (Better Method)
    justwatch_search_url = f"https://www.justwatch.com/us/search?q={movie_title.replace(' ', '%20')}"
    justwatch_response = requests.get(justwatch_search_url, headers=headers)
    justwatch_soup = BeautifulSoup(justwatch_response.text, "html.parser")
    
    justwatch_link = "#"
    jw_result = justwatch_soup.find("a", class_="title-list-row__column")
    if jw_result:
        justwatch_link = "https://www.justwatch.com" + jw_result["href"]

    return {
        "IMDb": imdb_link,
        "TMDB": tmdb_link,
        "JustWatch": justwatch_link
    }

# Flask App
app = Flask(__name__)

@app.route("/movie/<title>")
def movie_details(title):
    movie_links = scrape_movie_links(title)
    
    movie = {
        "title": title,
        "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",  # Example image (Replace with actual API data if needed)
        "release_date": "2010-07-16",
        "overview": "A thief who enters the dreams of others to steal secrets..."
    }
    
    return render_template("movie_details.html", movie=movie, movie_links=movie_links)

if __name__ == "__main__":
    app.run(debug=True)
