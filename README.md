# 🎬 Movie Recommender System

A full-stack Movie Recommendation System built with **Machine Learning**, **FastAPI**, and **Streamlit**.  
The project recommends top 5 movies similar to a given movie, displaying their posters using **TMDb API**.

---

## 🚀 Features
- Content-based recommendation using **CountVectorizer** + **Cosine Similarity**.
- **Streamlit frontend** for interactive movie selection and recommendations.
- **FastAPI backend** serving recommendation results as JSON.
- **Dockerized** for easy deployment.
- Uses **TMDb API** for fetching movie posters.

---

## 📂 Project Structure
```
├── training.py        # Data preprocessing & model training
├── main.py            # FastAPI backend
├── app.py             # Streamlit frontend
├── Dockerfile         # Docker setup for FastAPI
├── requirements.txt   # Python dependencies
├── movie_dict.pkl     # Saved movie data (dict)
├── similarity.pkl     # Saved similarity matrix
├── movie_list.pkl     # Saved movie dataframe
```

---

## ⚙️ Installation

### 1️⃣ Clone the repo
```
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

### 2️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Train the Model (optional)
If you want to re-train:
```
python training.py
```
This will generate:
- `movie_dict.pkl`  
- `similarity.pkl`  
- `movie_list.pkl`

---

## 🎮 Usage

### ▶️ Run Streamlit Frontend
```
streamlit run app.py
```

- Select a movie from the dropdown.  
- Click **Recommend** to get top 5 similar movies with posters.  

### ▶️ Run FastAPI Backend
```
uvicorn main:app --reload
```

Then open:  
- API root → http://127.0.0.1:8000/  
- Docs (Swagger UI) → http://127.0.0.1:8000/docs  

Example request:
```
http://127.0.0.1:8000/recommend?movie=Inception
```

---

## 🐳 Docker Deployment
Build and run the API in Docker:
```
docker build -t movie-recommender .
docker run -p 8000:8000 movie-recommender
```

---

## 📌 Requirements
See `requirements.txt` for full details.  
Key libraries:
- scikit-learn
- pandas
- numpy
- streamlit
- fastapi
- uvicorn
- requests

---

## 🌟 Future Improvements
- Hybrid recommendation (content + collaborative filtering).  
- Improved UI for better user experience.  
- Pagination & more detailed movie metadata.  
- Cloud deployment (AWS/GCP/Heroku).  

---

## 🙌 Acknowledgements
- [TMDb API](https://www.themoviedb.org/documentation/api) for movie data & posters.  
- Inspired by common ML recommender system tutorials.
