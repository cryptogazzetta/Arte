import streamlit as st
# project modules
import back_end


st.markdown(
    """
    <style>
body {
    color: #000000;
    font-family: 'Lexend';
    line-height: 1.6;
}

h {
    color: #FFFFFF;
    font-family: 'Playfair Display';
    font-size: 48px;
    padding: 0px;
}

h1 {
    color: #FFFFFF;
    font-size: 20px;
    padding: 0px;
}

h2 {
    color: #4a4a4a;
    font-size: 20px;
}

.stButton>button {
    background-color: #195921;
    color: #ffffff;
    height: 60px;
    width: 60%;
    margin-left: 20%;
    margin-top: 40px;
}

/* Estilo para o preço sugerido */
.price-suggested {
    font-size: 24px;
    background-color:
    color: white;
    padding: 10px;
    border-radius: 5px;
}

/* Efeito de hover para o botão */
.stButton button:hover {
    background-color: #27642F;
    color: #D1F2D1;
}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h>Marte</h>', unsafe_allow_html=True)
st.markdown('<h1>Precificação de Pintura</h1>', unsafe_allow_html=True)

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
