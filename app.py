# app.py
import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from scraper import scrape_movie_links
from movie_recommender import get_recommendations
from extensions import db  # Import db from extensions.py
from models import User  # Import User from models.py

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize db with the app

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Helper Functions ---
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={os.getenv('TMDB_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={os.getenv('TMDB_API_KEY')}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    trending_movies = get_trending_movies()
    search_results = []

    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        if movie_name:
            search_results = search_movie(movie_name)

    return render_template("index.html", trending=trending_movies, search_results=search_results)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    if not movie:
        return "Movie not found", 404

    # Fetch streaming links
    movie_title = movie.get("title", "")
    streaming_links = scrape_movie_links(movie_title) if movie_title else {}

    # Get AI recommendations (limit to 4 movies)
    trending_movies = get_trending_movies()
    recommended_movies = get_recommendations(movie['title'], trending_movies)[:4]  # Limit to 4 movies

    # Ensure recommended movies have valid poster paths
    for rec_movie in recommended_movies:
        if not rec_movie.get("poster_path"):
            rec_movie["poster_path"] = "/default-poster.jpg"  # Fallback image

    return render_template(
        "movie_details.html",
        movie=movie,
        movie_links=streaming_links,
        recommendations=recommended_movies
    )

@app.route('/recommendations/<int:movie_id>')
@login_required
def recommendations(movie_id):
    movie = get_movie_details(movie_id)
    trending_movies = get_trending_movies()
    recommended_movies = get_recommendations(movie['title'], trending_movies)
    return render_template("recommendations.html", recommendations=recommended_movies)

# --- User Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            if existing_user.email == email:
                flash('Email already exists!', 'error')
            else:
                flash('Username already taken!', 'error')
            return redirect(url_for('register'))

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {str(e)}")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))


# Initialize database
if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()  # Initialize the database
        print("Database tables created successfully!")
    app.run(debug=True)