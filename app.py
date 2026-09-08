import os
import requests
import pickle
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommender",
     initial_sidebar_state="collapsed",
     layout="wide"
)


#  --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------


st.markdown("""
<style>

    /* --------------------------------------------------------
       MAIN APP
    -------------------------------------------------------- */

    .stApp {
        background-color: #0f0f0f;
        color: white;
    }

    .main {
        padding-top: 1rem;
    }


    /* --------------------------------------------------------
       MAIN TITLE
       -------------------------------------------------------- */

    .main-title {
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .main-title span {
        color: #e50914;
    }
      div[data-testid="stTextInput"] label {
        color: white !important;
        font-size: 16px;
        font-weight: 600;
    }

    /* --------------------------------------------------------
       SUBTITLE
       -------------------------------------------------------- */

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #b5b5b5;
        margin-bottom: 35px;
    }


    /* --------------------------------------------------------
       RECOMMENDATION TITLE
       -------------------------------------------------------- */

    .recommend-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 25px;
    }


    /* --------------------------------------------------------
       MOVIE CARD
       -------------------------------------------------------- */

    .movie-card {
        background-color: #1c1c1c;
        padding: 12px;
        border-radius: 12px;
        min-height: 120px;
        margin-top: 10px;
    }


    /* --------------------------------------------------------
       MOVIE TITLE
       -------------------------------------------------------- */

    .movie-title {
        font-size: 17px;
        font-weight: 700;
        margin-top: 10px;
        color: white;
    }


    /* --------------------------------------------------------
       RATING
       -------------------------------------------------------- */

    .rating {
        color: #ffd700;
        font-size: 15px;
        margin-top: 5px;
    }


    /* --------------------------------------------------------
       SEARCH INPUT
       -------------------------------------------------------- */

    div[data-baseweb="input"] {
        background-color: #1c1c1c;
        border-radius: 10px;
    }

    div[data-baseweb="input"] input {
        color: white;
    }


    /* --------------------------------------------------------
       BUTTON
       -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
        height: 45px;
        background-color: #e50914;
        color: white;
        border: none;
    }

    .stButton > button:hover {
        background-color: #b20710;
        color: white;
    }


</style>
""", unsafe_allow_html=True)

# Download movie_data.pkl from Hugging Face if it doesn't exist locally
FILE_URL = "https://huggingface.co/datasets/Amna30/movie-recommender-data/resolve/main/movie_data.pkl"
FILE_NAME = "movie_data.pkl"

if not os.path.exists(FILE_NAME):
    with st.spinner("Loading movie recommender..."):
        response = requests.get(FILE_URL)
        response.raise_for_status()

        with open(FILE_NAME, "wb") as file:
            file.write(response.content)

# Load movie data and similarity matrix
with open(FILE_NAME, "rb") as file:
    df, similarity = pickle.load(file)


def recommend(movie_name):
    movie_name = movie_name.lower().strip()

    if movie_name not in df['title'].str.lower().values:
        return "Movie not found"
    
    idx = df[df['title'].str.lower() == movie_name].index[0]

    scores = list(enumerate(similarity[idx]))

    scores = sorted(
        scores,
        key=lambda x:x[1]
        ,reverse=True
        )[1:6]
    
    recommendations = []

    for i in scores:
        movie = df.iloc[i[0]]
        recommendations.append(
        {
            "title" : movie['title'],
            "rating" : movie['vote_average'],
            "poster_path" : movie['poster_path']
        })
    return recommendations



st.title("Movie Recommmeder System")
st.write("Select a Movie and get similar recommendation")
selected_movie = st.text_input("Enter movie name: ")

if st.button("Recommmend"):
    if selected_movie.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        results = recommend(selected_movie)
        if results == "Movie not found":
            st.error("Movie not found")
        else:
            st.write("### Top 5 Movies")

            # Create 5 columns
            cols = st.columns(5)
            for col, movie in zip(cols,results):
                with col:
                    # get poster
                    poster_path = movie["poster_path"]
                    if poster_path:
                        poster_url = ("https://image.tmdb.org/t/p/w500"+ poster_path)

                        st.image(
                            poster_url,
                            width="stretch"
                        )
                    else:
                        st.write("Poster not available")

                    # Movie title
                    st.markdown(
                        f"**{movie["title"]}**"
                    )

                    #Rating
                    st.write(f"{movie["rating"]:.1f}")












