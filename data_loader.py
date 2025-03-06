import pandas as pd
import os

def load_data():
    current_dir = os.path.dirname(__file__)
    # Update the path to point to the correct location of the data folder
    movies = pd.read_csv(os.path.join(current_dir, 'data', 'movies.csv'))
    ratings = pd.read_csv(os.path.join(current_dir, 'data', 'ratings.csv'))
    return movies, ratings