import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# -------------------------------
# 1. Load Data
# -------------------------------
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge datasets on title
movies = movies.merge(credits, on='title')

# Keep only required columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Drop rows with missing values
movies.dropna(inplace=True)

# -------------------------------
# 2. Data Preprocessing
# -------------------------------

# Convert stringified JSON into lists
movies["genres"] = movies["genres"].apply(lambda s: [d["name"] for d in json.loads(s)])
movies['keywords'] = movies['keywords'].apply(lambda s: [d['name'] for d in json.loads(s)])
movies['cast'] = movies['cast'].apply(lambda s: [d['name'] for d in json.loads(s)][:3])  # top 3 actors
movies['crew'] = movies['crew'].apply(lambda s: [d['name'] for d in json.loads(s) if d['job'] == 'Director'])

# Split overview into list of words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces within multi-word names
movies['cast'] = movies['cast'].apply(lambda x: [s.replace(" ", "") for s in x])
movies['crew'] = movies['crew'].apply(lambda x: [s.replace(" ", "") for s in x])
movies['genres'] = movies['genres'].apply(lambda x: [s.replace(" ", "") for s in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [s.replace(" ", "") for s in x])

# Create a new column combining everything
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# -------------------------------
# 3. New DataFrame with tags
# -------------------------------
new_df = movies[['movie_id', 'title', 'tags']].copy()

# Convert list of tags into a single string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# -------------------------------
# 4. Feature Extraction (Bag of Words)
# -------------------------------
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()

# Compute cosine similarity
similarity = cosine_similarity(vector)

# -------------------------------
# 5. Recommendation Function
# -------------------------------
def recommend(movie):
    """Print top 5 similar movies for a given title."""
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

# -------------------------------
# 6. Save Artifacts with Pickle
# -------------------------------
pickle.dump(new_df, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))

print("✅ Training complete. Pickle files saved: movie_list.pkl, similarity.pkl, movie_dict.pkl")
