FROM python:3.12-slim

WORKDIR /app

# Copy only dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only what’s needed for serving API
COPY main.py .
COPY movie_dict.pkl .
COPY similarity.pkl .
COPY movie_list.pkl .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]