from fastapi import FastAPI, Query, HTTPException
import pickle
import pandas as pd
import requests

# Load pre-trained data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Initialize FastAPI app
app = FastAPI(title="Movie Recommender API")

# Use a session for requests (faster than calling requests.get each time)
session = requests.Session()

# Fetch poster function
def fetch_poster(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=310d3dcf76bc3cfe347b5ad5a4a8cf71"
    response = session.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return None
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend function
def recommend(movie: str):
    if movie not in movies['title'].values:
        raise HTTPException(status_code=404, detail="Movie not found")
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommendations.append({"title": title, "poster_url": poster})
    return recommendations

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Movie Recommender API"}

# Recommendation endpoint
@app.get("/recommend")
def get_recommendations(movie: str = Query(..., description="Movie title to get recommendations for")):
    recs = recommend(movie)
    return {"recommendations": recs}