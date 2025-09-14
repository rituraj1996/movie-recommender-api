import streamlit as st
import pickle
import pandas as pd
import requests                #to hit the api

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
session = requests.Session()

# try this fetch_poster function if the below does not work
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=310d3dcf76bc3cfe347b5ad5a4a8cf71"
#     try:
#         response = session.get(url)
#         # response.raise_for_status()
#         data = response.json()
#         return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching poster for movie_id {movie_id}: {e}")
#         time.sleep(1)
#         return None
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=310d3dcf76bc3cfe347b5ad5a4a8cf71"
    response = session.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        # time.sleep(0.3)
        recommended_movies_posters.append(poster)
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    "Which movie do you want to recommendations on?",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
