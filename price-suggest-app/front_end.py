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

artists_mean_price_per_inch = back_end.artists_mean_price_per_inch
artists_list = artists_mean_price_per_inch['Artist'].tolist()
artists_list.insert(0, '')

st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artista', artists_list, label_visibility="collapsed")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2>Largura</h2>', unsafe_allow_html=True)
    width = st.slider('Largura', 1, 1000, 40, label_visibility="collapsed")
with col2:
    st.markdown('<h2>Altura</h2>', unsafe_allow_html=True)
    height = st.slider('Altura', 1, 1000, 40, label_visibility="collapsed")


col1, col2 = st.columns(2)
with col1:
    st.markdown('<h2>Estilos</h2>', unsafe_allow_html=True)
    styles = st.multiselect('Estilos', ['Figurative', 'Fine Art', 'Abstract', 'Illustration', 'Conceptual',
                                        'Modern', 'Portraiture', 'Surrealism', 'Expressionism', 'Impressionism',
                                        'Minimalism', 'Cubism', 'Street Art', 'Pop Art', 'Realism',
                                        'Abstract Expressionism', 'Contemporary', 'Dada', 'Art Deco',
                                        'Documentary', 'Photorealism'], label_visibility="collapsed")
    st.markdown('<h2>Temas</h2>', unsafe_allow_html=True)
    subjects = st.multiselect('Temas', ['Abstract', 'Women', 'Animal', 'Floral',
                            'Landscape', 'People', 'Nude', 'Portrait', 'Still Life', 'Cities',
                            'Nature', 'Geometric', 'Architecture', 'Seascape', 'Men'], label_visibility="collapsed")
with col2:

    st.header('Mídias')
    mediums = st.multiselect('Mídias', ['Acrylic', 'Oil', 'Ink', 'Digital',
                                        'Black & White', 'Paper', 'Photo', 'Paint', 'Pencil', 'Graphite',
                                        'Pastel', 'Watercolor', 'New Media', 'Color', 'Gesso', 'Charcoal',
                                        'C-type', 'Gouache', 'Marker', 'Manipulated', 'Enamel', 'Vector',
                                        'Spray Paint', 'Photogram'], label_visibility="collapsed")
    st.header('Materiais')
    materials = st.multiselect('Materiais', ['Canvas', 'Paper', 'Other', 'Cardboard',
                            'Wood', 'Plastic', 'Aluminium'], label_visibility="collapsed")

if st.button('Sugerir preço'):
    size = width * height / 6.4516
    characteristics = {'Artist': artist, 'Size': size, 'Style': styles, 'Medium': mediums,
                        'Material': materials, 'Subject': subjects}
    price_prediction = back_end.get_price_prediction(characteristics)
    price_prediction_brl = price_prediction * 5
    st.markdown(f'<span class="price-suggested">Preço sugerido: R$ {price_prediction_brl:.2f}</span>', unsafe_allow_html=True)
