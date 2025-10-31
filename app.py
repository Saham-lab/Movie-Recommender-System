
import pickle
import streamlit as st
import requests
import urllib.parse
import os
import gdown


# ---------------------------
st.markdown("""
<div class="app-footer">
    Developed by |
    <a href="https://www.linkedin.com/in/Sowmallya-gbs" target="_blank">Sowmallya</a> &amp;
    <a href="https://www.linkedin.com/in/saham-gbs" target="_blank">Saham</a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Config / Keys
# ---------------------------
OMDB_API_KEY = "e8dc7f80"  # Replace if needed
st.set_page_config(page_title=" 🎬 Movie Recommender App", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Helpers: fetch poster + details from OMDb
# ---------------------------
def fetch_movie_details(title):
    """Return dict with poster, rating, genre, actors, plot"""
    q = urllib.parse.quote_plus(title)
    url = f"http://www.omdbapi.com/?t={q}&apikey={OMDB_API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
    except Exception:
        data = {}

    if data.get("Response") == "True":
        return {
            "title": data.get("Title", title),
            "poster": data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image"),
            "rating": data.get("imdbRating", "N/A"),
            "genre": data.get("Genre", "N/A"),
            "actors": data.get("Actors", "N/A"),
            "plot": data.get("Plot", "N/A")
        }
    else:
        return {
            "title": title,
            "poster": "https://via.placeholder.com/300x450?text=No+Image",
            "rating": "N/A",
            "genre": "N/A",
            "actors": "N/A",
            "plot": "N/A"
        }

# ---------------------------
# Recommend using similarity matrix
# ---------------------------
def get_recommendations(movie_title, top_n=8):
    idx = movies[movies['title'] == movie_title].index
    if len(idx) == 0:
        return []
    index = idx[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recs = []
    for i in distances[1: top_n + 1]:
        t = movies.iloc[i[0]].title
        recs.append((t, i[1]))
    return recs

# ---------------------------
# Load data
# ---------------------------
# Google Drive URLs for datasets
# (make sure the files are shared as "Anyone with the link → Viewer")
# ---------------------------
MOVIE_LIST_URL = "https://drive.google.com/uc?id=16ks5O4TMVWubeTkjqIAnbPnhvu9_kga-"      # movie_list.pkl
SIMILARITY_URL = "https://drive.google.com/uc?id=17-C8I5b05WKNpe1VbxrEvEei-4Y6-Xfq"    # similarity.pkl

movies = "movie_list.pkl"
similarity= "similarity.pkl"

# ---------------------------
# Download files if not present
# ---------------------------
if not os.path.exists(movies):
    with st.spinner("📥 Downloading movie list..."):
        gdown.download(MOVIE_LIST_URL, movies, quiet=False)

if not os.path.exists(similarity):
    with st.spinner("📥 Downloading similarity data..."):
        gdown.download(SIMILARITY_URL, similarity, quiet=False)


# ---------------------------
movies = pickle.load(open(movies, "rb"))
similarity = pickle.load(open(similarity, "rb"))



col_top_left, col_top_center, col_top_right = st.columns([1,6,1])
with col_top_left:
    pass
with col_top_center:
    st.markdown("<h1 style='margin:0; text-align:center; font-family: Inter, system-ui, -apple-system, Roboto; letter-spacing:1px;'>Movie Recommender</h1>", unsafe_allow_html=True)
with col_top_right:
        pass

# ---------------------------
# CSS Styles (two themes)
# ---------------------------
dark_css = """
<style>
:root {
  --bg: #0b0d10;
  --card: rgba(255,255,255,0.04);
  --text: #e8eef1;
  --accent: #ff3b3b; /* red neon */
  --chip-bg: rgba(255,255,255,0.06);
  --muted: #9aa7b0;
}
body, .css-18e3th9 {
  background: linear-gradient(120deg, #071019 0%, #0d1220 50%, #071019 100%);
  color: var(--text);
}

/* page header alignment */
.stApp > header {background: transparent;}

.container { padding-left: 4%; padding-right: 4%; }

/* Card with tilt + minimal neon red glow */
.movie-card {
  width: 220px;
  margin: 12px auto;
  border-radius: 14px;
  background: var(--card);
  padding: 10px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  transform-style: preserve-3d;
  perspective: 1000px;
  border: 1px solid rgba(255,255,255,0.03);
}

/* 3D tilt effect (subtle) */
.movie-card:hover {
  transform: rotateX(4deg) rotateY(-6deg) translateY(-6px);
  box-shadow: 0 10px 30px rgba(255,59,59,0.08), 0 0 18px rgba(255,59,59,0.10);
  border: 1px solid rgba(255,59,59,0.45);
}

/* poster */
.movie-card img {
  border-radius: 10px;
  width: 100%;
  height: 320px;
  object-fit: cover;
  display: block;
  margin: 0 auto;
  transition: transform 0.3s ease;
}

/* small corner boxes removed: no extra elements */

/* title */
.movie-title {
  font-family: "Inter", sans-serif;
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
  margin-top: 10px;
  text-align: center;
  min-height: 40px;
}

/* rating */
.rating {
  color: #ffd166;
  font-weight: 700;
  margin-top: 6px;
  text-align: center;
}

/* genre chips */
.genre-chip {
  display:inline-block;
  background: rgba(0,0,0,0.35);
  color: var(--text);
  padding: 6px 10px;
  border-radius: 999px;
  margin: 6px 4px 0 4px;
  font-size: 12px;
  border: 1px solid rgba(255,255,255,0.03);
}

/* buttons row below each card */
.card-buttons {
  display:flex;
  gap:8px;
  justify-content:center;
  margin-top:10px;
}

/* primary button style */
.btn {
  background: linear-gradient(90deg, rgba(255,59,59,0.95), rgba(200,30,30,0.95));
  color: white;
  padding: 6px 10px;
  border-radius: 8px;
  font-weight:600;
  font-size:13px;
  border: none;
  cursor: pointer;
}

/* subtle secondary button */
.btn-secondary {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.06);
  color: var(--text);
  padding: 6px 10px;
  border-radius: 8px;
  font-size:13px;
}

/* info box when movie clicked */
.info-box {
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  padding: 14px;
  margin-top: 18px;
  border: 1px solid rgba(255,255,255,0.04);
}

/* footer */
.app-footer {
  margin-top: 32px;
  padding: 18px;
  text-align:center;
  color: #bfcbd3;
  border-top: 1px solid rgba(255,255,255,0.03);
}
.app-footer a { color: var(--accent); font-weight:700; text-decoration:none; }
.app-footer a:hover { color: #ffffff; }

/* responsive columns */
@media (max-width: 900px) {
  .movie-card { width: 48%; margin: 12px; }
  .movie-card img { height: 280px; }
}
@media (max-width: 520px) {
  .movie-card { width: 100%; }
  .movie-card img { height: 360px; }
}
</style>
"""


# Inject selected theme css
st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown(dark_css, unsafe_allow_html=True)

# ---------------------------
# Controls: selection box
# ---------------------------

st.markdown("""
    <style>
        .custom-label {
            font-size: 20px;
            color: #9fb6bf;
            font-weight: 100;
            padding-bottom: 0px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
col1, _ = st.columns([10, 1])

with col1:
    st.markdown("<div class='custom-label'>Search or pick a movie</div>", unsafe_allow_html=True)
    selected = st.selectbox("", movies['title'].values, index=0)  # Empty label to hide default





#st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.03); margin-top:14px; margin-bottom:18px;'/>", unsafe_allow_html=True)

# ---------------------------
# Generate recommendations
# ---------------------------
if st.button("🎥 Get Recommendations"):
    recs = get_recommendations(selected, top_n=8)
    if len(recs) == 0:
        st.warning("Movie not found in dataset.")
    else:
        # Pre-fetch details in a list (to reduce repeated requests)
        rec_details = []
        for (title, score) in recs:
            d = fetch_movie_details(title)
            d['score'] = round(float(score), 3) if isinstance(score, (float, int)) else score
            rec_details.append(d)

        # grid display
        # We'll create 4 columns per row (wide layout)
        cards_per_row = 4
        rows = [rec_details[i:i + cards_per_row] for i in range(0, len(rec_details), cards_per_row)]

        clicked_title = st.session_state.get("selected_details", None)

        for row in rows:
            cols = st.columns(cards_per_row, gap="large")
            for col, movie in zip(cols, row):
                with col:
                    # card HTML
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{movie['poster']}" alt="{movie['title']} poster">
                            <div class="movie-title">{movie['title']}</div>
                            <div class="rating">IMDb: {movie['rating']}</div>
                            <div style="text-align:center; margin-top:8px;">
                                {"".join([f"<span class='genre-chip'>{g.strip()}</span>" for g in (movie['genre'] or "").split(",")[:3]])}
                            </div>
                            <div class="card-buttons">
                                <form action="" method="get">
                                    <!-- Buttons are rendered as links that call Streamlit when clicked via unique keys -->
                                </form>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Buttons (Streamlit controls under the card)
                    btn_col1, btn_col2, btn_col3 = st.columns([1,4,1])

                    with btn_col2:
                        # Trailer opens YouTube search results in new tab
                        yt_query = urllib.parse.quote_plus(f"{movie['title']} official trailer")
                        yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
                        st.markdown(f"""<a href="{yt_link}" target="_blank"><button class="btn">Trailer</button></a>""", unsafe_allow_html=True)


# ---------------------------
# Footer
# ---------------------------
# ---------- Thank You Section ---------- #
st.markdown(
    """
    <style>
    .thank-you {
        text-align: center;
        margin-top: 60px;
        padding: 25px;
        background-color: #111;
        color: #FFD700;
        font-size: 30px;
        font-weight: bold;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }
        to { box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); }
    }
    </style>

    <div class="thank-you">
        🎬 Thank You for Using the Movie Recommender System! 🍿
    </div>
    """,
    unsafe_allow_html=True
)
