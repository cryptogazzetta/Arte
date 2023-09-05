import streamlit as st
import pandas as pd


df = pd.read_csv('artsoul_dummies.csv')

# Create a Streamlit app
st.title('Sugestões para você')

# Initialize an index to keep track of the current artwork
if "artwork_index" not in st.session_state:
    st.session_state.artwork_index = 1

artwork_index = st.session_state.artwork_index

image = df['Image_Url'][artwork_index]
artist = df['Artist'][artwork_index].upper()
title = df['Title'][artwork_index]
artwork_url = 'https//www.google.com'

# Custom CSS to limit the image height to 80% and width to 100%
style = f"""
    <style>
        img{{
            max-height: 60%;
            width: 100%;
            object-fit: contain;
        }}
    </style>
"""

col1, col2 = st.columns([0.9, 0.1])

with col1:
    # Display the image with the custom CSS
    st.markdown(style, unsafe_allow_html=True)
    st.markdown(f'<a href="{artwork_url}" target="_blank"><img src="{image}" alt="Artwork Image"></a>', unsafe_allow_html=True)
    st.write(f'**{artist}**')
    st.write(f'**{title}**')

with col2:
    if artwork_index < len(df) - 1:
        if st.button('Next'):
            st.session_state.artwork_index += 1
