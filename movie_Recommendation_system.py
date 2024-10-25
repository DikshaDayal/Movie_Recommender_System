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
    poster_path = data.get('poster_path')  # Use .get() to avoid KeyError
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None  # Return None if no poster path found

# Download function to retrieve files from Google Drive
def download_file_from_google_drive(file_id, destination_path):
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    session = requests.Session()  # Create a session to handle redirection
    
    response = session.get(url, allow_redirects=True)

    if response.status_code == 200:
        # Check if the content type is HTML, indicating an error page
        if 'text/html' in response.headers.get('Content-Type', ''):
            st.error("Downloaded file appears to be an HTML page. Please check the Google Drive link and file ID.")
            return False

        with open(destination_path, 'wb') as f:
            f.write(response.content)
        st.success(f"Downloaded {destination_path} successfully!")
        return True
    else:
        st.error("Failed to download the file. Please check the file ID and permissions.")
        return False

# Google Drive file IDs
movies_file_id = '1I50mx1aLgcXn91t5bEAVtnf5t9bhsqzL'  # Ensure this is the correct ID

# Attempt to download the movies_list.pkl file
if download_file_from_google_drive(movies_file_id, 'movies_list.pkl'):
    try:
        with open('movies_list.pkl', 'rb') as f:
            movies = pickle.load(f)
            st.success("Loaded movies_list.pkl successfully!")
    except Exception as e:
        st.error(f"Error loading movies_list.pkl: {e}")
        movies = None  # Set to None if loading fails
else:
    movies = None  # If download fails, set to None

# Check if movies data is loaded
if movies is not None:
    movies_list = movies['title'].values

    # Streamlit header
    st.header("Movie Recommender System")

    # Define the image carousel component
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
        # Ensure similarity is defined before using it
        if 'similarity' not in globals():
            st.error("Similarity data is not loaded. Recommendations cannot be generated.")
            return [], []
        
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[1:6]:  # Recommend top 5 movies
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movie_id))
        return recommend_movie, recommend_poster

    # Button to show recommendations
    if st.button("Show Recommend"):
        movie_name, movie_poster = recommend(selectvalue)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if movie_name:
                st.text(movie_name[0])
                st.image(movie_poster[0])
        with col2:
            if movie_name:
                st.text(movie_name[1])
                st.image(movie_poster[1])
        with col3:
            if movie_name:
                st.text(movie_name[2])
                st.image(movie_poster[2])
        with col4:
            if movie_name:
                st.text(movie_name[3])
                st.image(movie_poster[3])
        with col5:
            if movie_name:
                st.text(movie_name[4])
                st.image(movie_poster[4])
else:
    st.error("Movie data not loaded. Cannot proceed with the recommendations.")

