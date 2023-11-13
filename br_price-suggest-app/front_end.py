import streamlit as st
# project modules
import back_end


st.markdown(
    """
    <link rel="stylesheet" type="text/css" href="styles.css">
    """,
    unsafe_allow_html=True,
)

st.title('Precificação de Pintura')

artists_list = back_end.artists
galleries_list = back_end.galleries

artists_list.sort()
galleries_list.sort()

st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artista', artists_list, label_visibility="collapsed")

# st.markdown('<h2>Galeria</h2>', unsafe_allow_html=True)
# galeria = st.selectbox('Galeria', galleries_list, label_visibility="collapsed")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2>Altura (cm)</h2>', unsafe_allow_html=True)
    altura = st.slider('Altura', 1, 1000, 40, label_visibility="collapsed")

with col2:
    st.markdown('<h2>Largura (cm)</h2>', unsafe_allow_html=True)
    largura = st.slider('Largura', 1, 1000, 40, label_visibility="collapsed")

if st.button('Sugerir preço'):
    characteristics = {'Artist': artist, 'Area': altura*largura}
    price_prediction = back_end.get_price_prediction(characteristics)

    price_prediction_brl = price_prediction * 5
    st.markdown(f'<span class="price-suggested">Preço sugerido: R$ {price_prediction_brl:.2f}</span>', unsafe_allow_html=True)
