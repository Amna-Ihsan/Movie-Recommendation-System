import streamlit as st
import pickle



# load movie data and similarity mstrix
with open("movie_data.pkl","rb") as file:
    df,similarity = pickle.load(file)


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









 # Add styles

# import streamlit as st
# import pickle


# # --------------------------------------------------
# # PAGE CONFIGURATION
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Movie Recommender",
#     page_icon="🎬",
#     layout="wide"
# )


# # --------------------------------------------------
# # CUSTOM CSS
# # --------------------------------------------------

# st.markdown("""
# <style>

#     /* Main background */
#     .stApp {
#         background-color: #0f0f0f;
#         color: white;
#     }

#     /* Main title */
#     .main-title {
#         font-size: 55px;
#         font-weight: 800;
#         text-align: center;
#         margin-top: 20px;
#         margin-bottom: 5px;
#     }

#     /* Subtitle */
#     .subtitle {
#         text-align: center;
#         font-size: 20px;
#         color: #b5b5b5;
#         margin-bottom: 35px;
#     }

#     /* Recommendation heading */
#     .recommend-title {
#         font-size: 30px;
#         font-weight: 700;
#         margin-top: 40px;
#         margin-bottom: 25px;
#     }

#     /* Movie card */
#     .movie-card {
#         background-color: #1c1c1c;
#         padding: 12px;
#         border-radius: 12px;
#         min-height: 120px;
#         margin-top: 10px;
#     }

#     /* Movie title */
#     .movie-title {
#         font-size: 17px;
#         font-weight: 700;
#         margin-top: 10px;
#     }

#     /* Rating */
#     .rating {
#         color: #ffd700;
#         font-size: 15px;
#         margin-top: 5px;
#     }

#     /* Search input */
#     div[data-baseweb="input"] {
#         background-color: #1c1c1c;
#         border-radius: 10px;
#     }

#     /* Button */
#     .stButton > button {
#         width: 100%;
#         border-radius: 10px;
#         font-size: 18px;
#         font-weight: 600;
#         height: 45px;
#     }

# </style>
# """, unsafe_allow_html=True)


# # --------------------------------------------------
# # LOAD DATA
# # --------------------------------------------------

# with open("movie_data.pkl", "rb") as file:
#     df, similarity = pickle.load(file)


# # --------------------------------------------------
# # RECOMMENDATION FUNCTION
# # --------------------------------------------------

# def recommend(movie_name):

#     movie_name = movie_name.lower().strip()

#     if movie_name not in df["title"].str.lower().values:
#         return "Movie not found"

#     idx = df[df["title"].str.lower() == movie_name].index[0]

#     scores = list(enumerate(similarity[idx]))

#     scores = sorted(
#         scores,
#         key=lambda x: x[1],
#         reverse=True
#     )[1:6]

#     recommendations = []

#     for i in scores:

#         movie = df.iloc[i[0]]

#         recommendations.append({
#             "title": movie["title"],
#             "rating": movie["vote_average"],
#             "poster_path": movie["poster_path"]
#         })

#     return recommendations


# # --------------------------------------------------
# # HEADER
# # --------------------------------------------------

# st.markdown(
#     '<div class="main-title">🎬 Movie Recommender</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">'
#     'Discover movies similar to the ones you love'
#     '</div>',
#     unsafe_allow_html=True
# )


# # --------------------------------------------------
# # SEARCH AREA
# # --------------------------------------------------

# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:

#     selected_movie = st.text_input(
#         "Search for a movie",
#         placeholder="e.g. Inception, Avatar, Titanic..."
#     )

#     recommend_button = st.button(
#         "🎥 Recommend Movies"
#     )


# # --------------------------------------------------
# # RECOMMENDATIONS
# # --------------------------------------------------

# if recommend_button:

#     if selected_movie.strip() == "":

#         st.warning("Please enter a movie name.")

#     else:

#         results = recommend(selected_movie)

#         if results == "Movie not found":

#             st.error(
#                 "❌ Movie not found. Please check the movie title."
#             )

#         else:

#             st.markdown(
#                 '<div class="recommend-title">'
#                 '🍿 Recommended For You'
#                 '</div>',
#                 unsafe_allow_html=True
#             )

#             cols = st.columns(5)

#             for col, movie in zip(cols, results):

#                 with col:

#                     poster_path = movie["poster_path"]

#                     if poster_path:

#                         poster_url = (
#                             "https://image.tmdb.org/t/p/w500"
#                             + poster_path
#                         )

#                         st.image(
#                             poster_url,
#                             width="stretch"
#                         )

#                     else:

#                         st.write("Poster unavailable")

#                     st.markdown(
#                         f'<div class="movie-card">'
#                         f'<div class="movie-title">'
#                         f'{movie["title"]}'
#                         f'</div>'
#                         f'<div class="rating">'
#                         f'⭐ {movie["rating"]:.1f}'
#                         f'</div>'
#                         f'</div>',
#                         unsafe_allow_html=True
#                     )


# # --------------------------------------------------
# # FOOTER
# # --------------------------------------------------

# st.markdown("---")

# st.markdown(
#     "<center>Built with Python • Machine Learning • "
#     "TF-IDF • Cosine Similarity • Streamlit</center>",
#     unsafe_allow_html=True
#)