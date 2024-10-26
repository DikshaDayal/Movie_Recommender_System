# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 01:21:56 2024

@author: CHAHATI DAYAL
"""
import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Function to fetch poster path from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=017696e96e844770756eda22192b4552&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to download files from Google Drive using direct link
def download_file_from_google_drive(file_id, destination_path):
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        st.write(f"Downloaded {destination_path} successfully!")
    else:
        st.error("Failed to download the file. Please check the file ID and permissions.")

# Google Drive file IDs
movies_file_id = '1I50mx1aLgcXn91t5bEAVtnf5t9bhsqzL'  # movies_list.pkl file ID

# Download the movies_list.pkl file
download_file_from_google_drive(movies_file_id, 'movies_list.pkl')

# Load the pickled data with verification
try:
    with open('movies_list.pkl', 'rb') as f:
        movies = pickle.load(f)
        st.write("Loaded movies_list.pkl successfully!")  # Change this to Streamlit write to show in the app
except Exception as e:
    st.error(f"Error loading movies_list.pkl: {e}")
    movies = None  # Set movies to None if loading fails

# Load the similarity.pkl file (assuming it's stored locally)
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("similarity.pkl file not found. Please ensure it is present in the directory.")
    similarity = None  # Set similarity to None if loading fails
except Exception as e:
    st.error(f"Error loading similarity.pkl: {e}")
    similarity = None

# Check if movies and similarity are loaded successfully before proceeding
if movies is not None and similarity is not None:
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
else:
    st.warning("Movie data not loaded. Cannot proceed with the recommendations.")
