import pickle
import streamlit as st
import requests
import urllib.parse
import os
import gdown

# -------------------- OMDb API --------------------
OMDB_API_KEY = "e8dc7f80"  # Replace with your actual OMDb API key

# -------------------- FUNCTIONS --------------------
def fetch_movie_details(movie_title):
    """Fetch poster, genre, and IMDb rating from OMDb"""
    url = f"http://www.omdbapi.com/?t={urllib.parse.quote(movie_title)}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster = data.get("Poster", "https://via.placeholder.com/300x450?text=No+Poster+Available")
    if poster == "N/A":
        poster = "https://via.placeholder.com/300x450?text=No+Poster+Available"
    genre = data.get("Genre", "Unknown")
    rating = data.get("imdbRating", "N/A")
    return poster, genre, rating


def fetch_trailer_link(movie_title):
    """Create a clickable YouTube trailer link"""
    query = urllib.parse.quote(f"{movie_title} official trailer")
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    return youtube_url


def recommend(movie):
    """Recommend top 8 similar movies"""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_genres = []
    recommended_movie_ratings = []
    recommended_movie_trailers = []

    for i in distances[1:9]:  # 8 movies
        movie_title = movies.iloc[i[0]].title
        poster, genre, rating = fetch_movie_details(movie_title)
        trailer = fetch_trailer_link(movie_title)

        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(poster)
        recommended_movie_genres.append(genre)
        recommended_movie_ratings.append(rating)
        recommended_movie_trailers.append(trailer)

    return (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_genres,
        recommended_movie_ratings,
        recommended_movie_trailers
    )


# -------------------- UI --------------------
st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")
st.markdown("<h2 style='text-align: center;'>🎬 Movie Recommender System</h2>", unsafe_allow_html=True)

# Google Drive share links
movie_list_url = "https://drive.google.com/file/d/16ks5O4TMVWubeTkjqIAnbPnhvu9_kga-/view?usp=sharing"
similarity_url = "https://drive.google.com/file/d/17-C8I5b05WKNpe1VbxrEvEei-4Y6-Xfq/view?usp=sharing"

# Local cache filenames
movie_list_path = "movie_list.pkl"
similarity_path = "similarity.pkl"

# Download only if not already present
if not os.path.exists(movie_list_path):
    gdown.download(movie_list_url, movie_list_path, quiet=False)

if not os.path.exists(similarity_path):
    gdown.download(similarity_url, similarity_path, quiet=False)

# Load as usual
movies = pickle.load(open(movie_list_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_genres,
        recommended_movie_ratings,
        recommended_movie_trailers
    ) = recommend(selected_movie)

    st.markdown("<h4 style='text-align: center;'>🎥 Top Recommendations</h4>", unsafe_allow_html=True)

    # ---------- First Row (4 movies) ---------- #
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(
                f"<p style='font-weight:bold; word-wrap:break-word;'>{recommended_movie_names[i]}</p>",
                unsafe_allow_html=True
            )
            st.markdown(f"<p>⭐ IMDb: {recommended_movie_ratings[i]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎭 Genre: {recommended_movie_genres[i]}</p>", unsafe_allow_html=True)
            st.markdown(
                f"<a href='{recommended_movie_trailers[i]}' target='_blank' style='text-decoration:none;'>🎬 Watch Trailer</a>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Second Row (next 4 movies) ---------- #
    cols = st.columns(4)
    for i in range(4, 8):
        with cols[i - 4]:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(
                f"<p style='font-weight:bold; word-wrap:break-word;'>{recommended_movie_names[i]}</p>",
                unsafe_allow_html=True
            )
            st.markdown(f"<p>⭐ IMDb: {recommended_movie_ratings[i]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎭 Genre: {recommended_movie_genres[i]}</p>", unsafe_allow_html=True)
            st.markdown(
                f"<a href='{recommended_movie_trailers[i]}' target='_blank' style='text-decoration:none;'>🎬 Watch Trailer</a>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

