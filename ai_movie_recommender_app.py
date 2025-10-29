import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# Sample movie dataset
movies = {
    'title': ['Inception', 'Interstellar', 'The Dark Knight', 'Tenet', 'Avatar', 'Titanic', 'Avengers', 'Iron Man'],
    'genre': ['Action Sci-Fi', 'Adventure Sci-Fi', 'Action Crime', 'Action Sci-Fi', 'Adventure Sci-Fi', 'Romance Drama', 'Action Superhero', 'Action Superhero'],
    'director': ['Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'James Cameron', 'James Cameron', 'Russo Brothers', 'Jon Favreau']
}

df = pd.DataFrame(movies)
df['combined'] = df['genre'] + ' ' + df['director']

# Vectorize
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['combined'])
similarity = cosine_similarity(count_matrix)

# Streamlit UI
st.title("🎬 AI Movie Recommender System")
st.write("Get movie suggestions based on your favorite movie.")

movie_name = st.selectbox("Select or type a movie name:", df['title'].tolist())

if st.button("Recommend"):
    list_of_all_titles = df['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if find_close_match:
        close_match = find_close_match[0]
        index = df[df.title == close_match].index[0]
        similarity_scores = list(enumerate(similarity[index]))
        sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        st.subheader(f"Movies similar to '{close_match}':")
        for i in sorted_movies[1:6]:
            st.write(f"🎥 {df.iloc[i[0]].title}")
    else:
        st.warning("Movie not found in the dataset.")

