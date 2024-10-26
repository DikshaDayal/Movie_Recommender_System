# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 01:21:56 2024

@author: CHAHATI DAYAL
"""

import streamlit as st
import pickle
import requests
import gdown
import streamlit.components.v1 as components
import os

# Set your TMDb API key in an environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Make sure this is set before running

# Function to fetch poster path from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500?text=No+Image+Available"
    return full_path

# Function to download files from Google Drive
def download_file_from_google_drive(file_id, destination_path):
    gdown.download(f'https://drive.google.com/uc?id={file_id}&export=download', destination_path, quiet=False)

# Google Drive file IDs
movies_file_id = '1abcdEFGhijkLmnoPQ'  # Replace with your actual movies_list.pkl ID
similarity_file_id = '1I50mx1aLgcXn91t5bEAVtnf5t9bhsqzL'  # Replace with your actual similarity.pkl ID

# Download the pickled data
download_file_from_google_drive(movies_file_id, 'movies_list.pkl')
download_file_from_google_drive(similarity_file_id, 'similarity.pkl')

# Load the pickled data with error handling
try:
    movies = pickle.load(open('movies_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# Extract movie titles for dropdown
movies_list = movies['title'].values

# Streamlit header
st.header("Movie Recommender System")

# Correct path for the frontend component directory
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Pre-fetch some posters
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

# Display the carousel component
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Selectbox to choose a movie
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# Button to show recommendations
if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
