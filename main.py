import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the dataset
try:
    movies = pd.read_csv('movies.csv')
except FileNotFoundError:
    print("Error: 'movies.csv' file not found. Please ensure it is in the same directory as this script.")
    exit()

# Check if the necessary columns are present
if 'title' not in movies.columns or 'description' not in movies.columns:
    print("Error: 'movies.csv' must contain 'title' and 'description' columns.")
    exit()

# Create a TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Fill NaN values with an empty string
movies['description'] = movies['description'].fillna('')

# Fit and transform the description column
tfidf_matrix = tfidf.fit_transform(movies['description'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    # Check if the title exists in the dataset
    if title not in movies['title'].values:
        return f"Error: '{title}' not found in the dataset."

    # Get the index of the movie that matches the title
    idx = movies.index[movies['title'] == title].tolist()[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 5 most similar movies
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 5 most similar movies
    return movies['title'].iloc[movie_indices].tolist()

# Example usage
if __name__ == "__main__":
    title = input("Enter a movie title: ")
    recommendations = get_recommendations(title)
    
    if isinstance(recommendations, list):
        print("Recommendations:")
        for movie in recommendations:
            print(movie)
    else:
        print(recommendations)