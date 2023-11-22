import streamlit as st
from streamlit_carousel import carousel
# project modules
import back_end
import chart

st.set_page_config(page_title="Art Market Explorer", page_icon=":🧭:", layout="centered", initial_sidebar_state="collapsed")
st.set_option('deprecation.showPyplotGlobalUse', False)

## IMPORT STYLES FROM .CSS FILE
with open('./styles.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

## PAGE TITLE
st.markdown('<h>Marte</h>', unsafe_allow_html=True)
st.markdown('<p>Art Market Explorer</p>', unsafe_allow_html=True)
st.markdown('<p>This tool allows you to explore the brazilian art market. Feel free to try it and share your thoughts ;)</p>', unsafe_allow_html=True)

# Get lists of artists and techniques (converting techniques to string)
artists_list = back_end.artists_list
techniques_list = back_end.techniques_list


#### USER INPUTS

st.markdown('<h2>Artist</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artist', artists_list, label_visibility="collapsed", index=0)

st.markdown('<h2>Technique</h2>', unsafe_allow_html=True)
technique = st.selectbox('Technique', techniques_list, label_visibility="collapsed")


if not st.checkbox('Any size'):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h2>Height (cm)</h2>', unsafe_allow_html=True)
        height = st
        height = st.slider('Height', 1, 1000, (50, 150), label_visibility="collapsed")

    with col2:
        st.markdown('<h2>Width (cm)</h2>', unsafe_allow_html=True)
        width = st.slider('Width', 1, 1000, (50, 150), label_visibility="collapsed")
else: 
    height = None
    width = None

if st.checkbox('Only sold artworks'):
    only_sold = True

#### OUTPUTS

if st.button('Get Report'):
    characteristics = {'Artist': artist, 'Height (cm)': height, 'Width (cm)': width, 'Technique': technique}

    artist = characteristics['Artist']
    technique = characteristics['Technique']

    # Get similar lots and performance from back_end
    similar_lots = back_end.get_similar_lots(characteristics)
    similar_lots_performance = back_end.get_similar_lots_performance(similar_lots)

    st.divider()


    # SHOW PRICE SUGGESTION
    if artist == ' ':
        artist = 'Any artist'
    if technique == ' ':
        technique = 'Any technique'
    
    st.markdown(f'<h1>{technique} by {artist}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>{similar_lots.shape[0]} Similar artworks were offered at auction</p>', unsafe_allow_html=True)


    # PLOT MARKET PERFORMANCE OF SIMILAR ARTWORKS
    st.markdown('<h2>Similar artworks total sales</h2>', unsafe_allow_html=True)

    fig = chart.get_similar_lots_performance_chart(similar_lots_performance)
    st.pyplot(fig)


    # TABLE OF SIMILAR ARTWORKS AUCTIONED
    st.dataframe(similar_lots[['Artist', 'Technique', 'Height (cm)', 'Width (cm)', 'Price (BRL)', 'Sold']], width=1000)


    # CAROUSEL OF SIMILAR ARTWORKS AUCTIONED
    st.markdown('<h2>Similar artworks auctioned</h2>', unsafe_allow_html=True)
    lots_to_slideshow = similar_lots.to_dict('records')
    # rename keys to match carousel component requirements
    for lot in lots_to_slideshow:
        lot['img'] = lot.pop('img_url')
        lot['title'] = f"R$ {lot.pop('Price (BRL)'):.2f}"
        lot['text'] = f'{lot.pop("Technique")}, {lot.pop("Height (cm)")} x {lot.pop("Width (cm)")} cm'
    carousel(lots_to_slideshow, height=800)


    # TABLE OF SIMILAR ARTWORKS BEING SOLD AT MARKETPLACES
    # st.markdown('<h2>Marketplace offers</h2>', unsafe_allow_html=True)
    # st.write('Coming soon...')