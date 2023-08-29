import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

st.title("Cate um felino")

artworks = pd.read_csv('artsoul_dummies.csv').drop(columns=['Size', 'Marketplace'])

# add style: max height of images = 80%, not distorted
st.markdown(
    """
    <style>
    img {
        max-width:60%;
        max-height:60%;
        width: auto;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

artwork = artworks.iloc[3]

st.image(artwork['Image_Url'])
st.header(artwork['Artist'])
st.write(artwork['Title'])


img = image_select(
    label=" ",
    images=[
        artworks['Image_Url'][0],
        artworks['Image_Url'][1]
    ],
    captions=[artworks['Title'][0], artworks['Title'][1]],
)