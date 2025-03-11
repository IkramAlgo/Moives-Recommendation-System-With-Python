from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_recommendations(movie_title, movies):
    # Handle empty genres
    df = pd.DataFrame([{
        'id': m['id'],
        'title': m['title'],
        'poster_path': m.get('poster_path', '/default-poster.jpg'),
        'genres': ' '.join([genre['name'] for genre in m.get('genres', [])]) if m.get('genres') else 'unknown'
    } for m in movies])

    # Avoid empty vocabulary error
    if df['genres'].nunique() == 1 and df['genres'].iloc[0] == 'unknown':
        return df.sample(5).to_dict('records')  # Fallback to random movies

    # Adjust TF-IDF parameters
    tfidf = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')  # Include single-letter words
    tfidf_matrix = tfidf.fit_transform(df['genres'])

    # Rest of the code remains the same
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx = df[df['title'] == movie_title].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices].to_dict('records')