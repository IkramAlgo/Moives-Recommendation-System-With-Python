import pandas as pd

def preprocess_data(movies, ratings):
    # Merge datasets and clean data
    data = pd.merge(ratings, movies, on='movieId')
    data = data.dropna()
    return data