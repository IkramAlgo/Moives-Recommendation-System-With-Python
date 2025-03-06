from flask import Flask, request, render_template
from data_loader import load_data
from data_preprocessor import preprocess_data
from movie_recommender import recommend_movies
import os

app = Flask(__name__, template_folder='templates')

# Debugging: Print working directory
print("Current Working Directory:", os.getcwd())
print("Templates Path:", os.path.join(os.getcwd(), "templates"))
print("Files in Templates Directory:", os.listdir("templates"))

# Load and preprocess data
movies, ratings = load_data()
data = preprocess_data(movies, ratings)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    recommendations = recommend_movies(movie_name, movies, ratings)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
