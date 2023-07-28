import streamlit as st
# project modules
import back_end

st.title('Precificação de obras de arte')

st.write("Selecione as características da obra de arte:")

width = st.slider('Largura (cm)', 1, 1000, 40)
height = st.slider('Altura (cm)', 1, 1000, 40)
size = width * height
# convert cm² to in²
size = size / 6.4516

styles = st.multiselect('Estilos', ['Figurative', 'Fine Art', 'Abstract', 'Illustration', 'Conceptual',
                                    'Modern', 'Portraiture', 'Surrealism', 'Expressionism', 'Impressionism',
                                    'Minimalism', 'Cubism', 'Street Art', 'Pop Art', 'Realism',
                                    'Abstract Expressionism', 'Contemporary', 'Dada', 'Art Deco',
                                    'Documentary', 'Photorealism'])
mediums = st.multiselect('Mídias', ['Acrylic', 'Oil', 'Ink', 'Digital',
                                    'Black & White', 'Paper', 'Photo', 'Paint', 'Pencil', 'Graphite',
                                    'Pastel', 'Watercolor', 'New Media', 'Color', 'Gesso', 'Charcoal',
                                    'C-type', 'Gouache', 'Marker', 'Manipulated', 'Enamel', 'Vector',
                                    'Spray Paint', 'Photogram'])
materials = st.multiselect('Materiais', ['Canvas', 'Paper', 'Other', 'Cardboard',
                           'Wood', 'Plastic', 'Aluminium'])
subjects = st.multiselect('Temas', ['Abstract', 'Women', 'Animal', 'Floral',
                          'Landscape', 'People', 'Nude', 'Portrait', 'Still Life', 'Cities',
                          'Nature', 'Geometric', 'Architecture', 'Seascape', 'Men'])

characteristics = {'Size': size, 'Style': styles,
                  'Medium': mediums, 'Material': materials,
                  'Subject': subjects}


# botão sugerir preço
if st.button('Sugerir preço'):
    price_prediction = back_end.get_price_prediction(characteristics)
    # converter US$ para BRL
    price_prediction = price_prediction * 5
    st.write(f'Preço sugerido: R$ {price_prediction:.2f}')