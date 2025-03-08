import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("No TMDB API Key found. Please check your .env file.")

app = Flask(__name__)

# Fetch trending movies
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Fetch movie details
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Search for a movie
def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route("/", methods=["GET", "POST"])
def home():
    trending = get_trending_movies()
    search_results = []
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        search_results = search_movie(movie_name)
    return render_template("index.html", trending=trending, search_results=search_results)

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    if not movie:
        return render_template("error.html", message="Movie not found.")
    
    streaming_links = {
        "Netflix": f"https://www.netflix.com/search?q={movie['title']}",
        "Prime Video": f"https://www.amazon.com/s?k={movie['title']}+movie"
    }
    
    return render_template("movie_details.html", movie=movie, streaming_links=streaming_links)

if __name__ == "__main__":
    app.run(debug=True)
