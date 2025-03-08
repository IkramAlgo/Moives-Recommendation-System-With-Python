import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from scraper import scrape_movie_links
# Correct function name

# Load API credentials from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Read API credentials
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

if not TMDB_API_KEY:
    raise ValueError("No TMDB API Key found. Please check your .env file.")

if not TMDB_ACCESS_TOKEN:
    raise ValueError("No TMDB Access Token found. Please check your .env file.")

app = Flask(__name__)

# Function to fetch trending movies
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Function to get movie details
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Function to search for a movie
def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route("/", methods=["GET", "POST"])
def home():
    trending_movies = get_trending_movies()
    
    # Define default movie_links for the homepage
    movie_links = {
        "IMDb": "https://www.imdb.com",
        "TMDB": "https://www.themoviedb.org",
        "JustWatch": "https://www.justwatch.com"
    }
    
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        search_results = search_movie(movie_name)
        return render_template("index.html", trending=trending_movies, search_results=search_results, movie_links=movie_links)
    
    return render_template("index.html", trending=trending_movies, movie_links=movie_links)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)  # Fetch movie details

    if not movie:
        return "Movie not found", 404

    # Extract movie title and fetch streaming links dynamically
    movie_title = movie.get("title", "")
    streaming_links = scrape_movie_links(movie_title) if movie_title else {}

    # Construct movie links (Ensure these links are correctly formatted)
    movie_links = {
        "IMDb": f"https://www.imdb.com/title/{movie.get('imdb_id', '')}" if movie.get('imdb_id') else "#",
        "TMDB": f"https://www.themoviedb.org/movie/{movie_id}",
        "JustWatch": f"https://www.justwatch.com/us/movie/{movie_title.replace(' ', '-').lower()}"
    }

    return render_template("movie_details.html", movie=movie, streaming_links=streaming_links, movie_links=movie_links)

if __name__ == "__main__":

    app.run(debug=True)