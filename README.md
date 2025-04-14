# 🎬 Movie Recommendation System with Python

This is a **content-based movie recommendation system** built using Python and the Streamlit framework. It suggests movies based on similarity in genres, keywords, cast, and more.

## 🔍 Features

- Recommend top 5 similar movies based on a selected movie
- Content-based filtering using metadata (cast, crew, genres, keywords)
- Simple and clean **Streamlit UI** for quick interaction
- Uses **cosine similarity** to find related movies
- Works with **TMDB dataset** (5000+ movies)

## 🛠️ Tech Stack

- Python  
- Pandas, Numpy  
- Scikit-learn (Cosine Similarity)  
- Streamlit (for Web UI)  
- Pickle (for model storage)  

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/IkramAlgo/Moives-Recommendation-System-With-Python.git
   cd Moives-Recommendation-System-With-Python

pip install -r requirements.txt

streamlit run app.py

Project Structure

📁 data/                 → contains datasets  
📄 app.py                → main Streamlit application  
📄 similarity.pkl        → precomputed similarity matrix  
📄 movie_list.pkl        → movies metadata  


🧠 Possible Improvements
🔍 Add search functionality to allow users to search instead of dropdown only

🎞️ Display movie posters using the TMDB API

🧠 Integrate hybrid recommendation (combine content-based + popularity)

📈 Show movie ratings, overview, or runtime in the UI

📦 Host app using Streamlit Cloud or HuggingFace Spaces
