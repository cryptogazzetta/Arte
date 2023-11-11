import streamlit as st
# project modules
import back_end

# Define a page-wide CSS style for a more authoritative appearance
st.markdown(
    """
    <style>
    body {
        color: #000000;
        font-family: Arial, sans-serif;
        line-height: 1.6;
    }
    
    h1 {
        color: #195921;
    }

    h2 {
        color: #4a4a4a;
        font-size: 20px
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
        font-size: 24px; /* Aumentar o tamanho do texto */
        font-weight: bold; /* Colocar em negrito */
        background-color: #1ca44c; /* Cor de fundo */
        color: white; /* Cor do texto */
        padding: 10px; /* Adicionar um espaçamento interno para destacar */
        border-radius: 5px; /* Adicionar bordas arredondadas */
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

st.title('Precificação de Pintura')


artists_list = back_end.artists
galleries_list = back_end.galleries

artists_list.sort()
galleries_list.sort()

st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artista', artists_list, label_visibility="collapsed")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2>Area (cm²)</h2>', unsafe_allow_html=True)
    area = st.slider('Area', 1, 1000, 40, label_visibility="collapsed")

with col2:
    st.markdown('<h2>Galeria</h2>', unsafe_allow_html=True)
    galeria = st.selectbox('Galeria', galleries_list, label_visibility="collapsed")

if st.button('Sugerir preço'):
    characteristics = {'Artist': artist, 'Area': area, 'Galeria': galeria}
    price_prediction = back_end.get_price_prediction(characteristics)

    price_prediction_brl = price_prediction * 5
    st.markdown(f'<span class="price-suggested">Preço sugerido: R$ {price_prediction_brl:.2f}</span>', unsafe_allow_html=True)
