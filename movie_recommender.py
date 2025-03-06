from sklearn.neighbors import NearestNeighbors
import numpy as np

def recommend_movies(movie_name, movies, ratings, k=5):
    # Create user-item matrix
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    
    # Fit KNN model
    knn = NearestNeighbors(n_neighbors=k, metric='cosine')
    knn.fit(user_item_matrix.T)

    # Find movie index
    movie_idx = movies[movies['title'].str.contains(movie_name, case=False)].index[0]
    
    # Get recommendations
    distances, indices = knn.kneighbors(user_item_matrix.T[movie_idx].reshape(1, -1), n_neighbors=k+1)
    recommended_movies = [movies.iloc[i]['title'] for i in indices.flatten()[1:]]
    
    return recommended_movies