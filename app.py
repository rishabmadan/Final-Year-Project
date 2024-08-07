import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st

from packages.search_song import search_song
from packages.run_recommender import get_feature_vector, show_similar_songs
# load data
dat = pd.read_csv('data/processed/dat_for_recommender.csv')

song_features_normalized = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
song_features_not_normalized = ['duration_ms', 'key', 'loudness', 'mode', 'tempo']

all_features = song_features_normalized + song_features_not_normalized + ['decade', 'popularity']

st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.markdown("# AI Enabled Music Recommendation System")

    st.sidebar.markdown("### Select Features")
    features = st.sidebar.multiselect('Select the features you care about', all_features, default=all_features)
    st.sidebar.markdown("### Recommendations")
    num_recommendations = st.sidebar.slider('Select the number of recommendations', 10, 30, 10)
    from PIL import Image

    image = Image.open('data/homeimg.jpg')
    st.image(image, caption='Music Recommendation')

    song_name = st.text_input('Enter the name of the song')
    if song_name != '':
        song_name = song_name.upper()
    year = st.text_input('Enter the year')
    if year != '':
        year = int(year)

    if st.button('Search for My Song Related'):
        found_flag, found_song = search_song(song_name, dat)
        if found_flag:
            st.markdown("Perfect, this song is in the dataset:")
            st.markdown(found_song)
        else:
            st.markdown("Sorry, this song is not in the dataset. Please try another song!")

    if st.button('Get Recommendations'):
        if song_name == '':
            st.markdown("Please enter the name of the song!")
        elif year == '':
            st.markdown("Please enter the year of the song!")
        else:

            fig_bar = show_similar_songs(song_name, year, dat, features, top_n=num_recommendations, plot_type='bar')
            st.pyplot(fig_bar)

if __name__ == "__main__":
    main()

    
    


