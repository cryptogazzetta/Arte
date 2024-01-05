# External modules
import streamlit as st
import pandas as pd
# Project modules
import back_end
import github
import chart

def main():

    st.set_option('deprecation.showPyplotGlobalUse', False)

    ## CSS FILE
    if 'css' not in st.session_state:
        st.session_state['css'] = github.get_file_from_github('apps/price_suggest/styles.css', format='css')
    css = st.session_state['css']
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    ## PAGE TITLE
    st.markdown('<h>Marte</h>', unsafe_allow_html=True)
    st.markdown(
        '<p>Esta ferramenta ajuda a precificar obras de arte com base no histórico de vendas semelhantes em leilão. Fique à vontade para experimentar a ferramenta, compartilhar e propor sugestões! </p>',
        unsafe_allow_html=True
    )

    ## Lists of artists and Medium_types
    if 'artists_list' not in st.session_state:
        st.session_state['artists_list'] = back_end.artists_list
    if 'medium_types_list' not in st.session_state:
        st.session_state['medium_types_list'] = back_end.medium_types_list

    artists_list = st.session_state['artists_list']
    medium_types_list = st.session_state['medium_types_list']

    #### USER INPUT
    email, artist, medium_type, year, height, width = get_user_input(artists_list, medium_types_list)

    #### OUTPUTS

    if st.button('Gerar relatório'):
        check_email(email)
        get_report(email, artist, medium_type, year, height, width)


def get_user_input(artists_list, medium_types_list):
    # Artist
    st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
    artist = st.selectbox('Artista', artists_list, label_visibility="collapsed", index=0)

    # Medium_type and Year
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h2>Técnica</h2>', unsafe_allow_html=True)
        medium_type = st.selectbox('Técnica', medium_types_list, label_visibility="collapsed") 
    with col2:
        st.markdown('<h2>Ano</h2>', unsafe_allow_html=True)
        year = st.selectbox('Ano', [''] + list(range(1900, 2023)), label_visibility="collapsed")

    # Measures
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h2>Altura (cm)</h2>', unsafe_allow_html=True)
        height = st.number_input('Altura', 1, 5000, 50, label_visibility="collapsed")
    with col2:
        st.markdown('<h2>Largura (cm)</h2>', unsafe_allow_html=True)
        width = st.number_input('Largura', 1, 5000, 50, label_visibility="collapsed")

    # E-mail
    st.markdown('<h2>Seu e-mail</h2>', unsafe_allow_html=True)
    email = st.text_input('E-mail', label_visibility="collapsed")

    return email, artist, medium_type, year, height, width

def get_report(email, artist, medium_type, year, height, width):

    ## ARWORK CHARACTERISTICS DICT
    characteristics = {'Artist': artist, 'Year': year, 'Height (cm)': height, 'Width (cm)': width, 'Medium_type': medium_type.lower()}
    artist = characteristics['Artist']
    medium_type = characteristics['Medium_type']

    ## INTERACT WITH BACK-END
    price_prediction, similar_lots, similar_lots_performance = get_data(email, characteristics)
    

    st.divider()


    # SHOW PRICE SUGGESTION    
    st.markdown(f'<h1>{medium_type.capitalize()} por {artist} ({height}x{width})</h1>', unsafe_allow_html=True)
    no_similar_lots = check_similar_lots(similar_lots)
    if no_similar_lots:
        st.markdown(f'<p>Não encontramos obras similares no histórico de leilões.</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p>{similar_lots.shape[0]} obras similares foram encontradas no histórico.</p>', unsafe_allow_html=True)

        # SHOW PRICE RANGE
        price_range = back_end.get_price_range(price_prediction, similar_lots)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 30px; margin-top: 30px;">'
                f'    <p style="margin: 0;">Preço mínimo</p>'
                f'    <p style="font-size: 16px; margin-bottom: 5px;">R$ {price_range[0]:,.0f}</p>'  # formatting to separate thousands with comma
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 30px; margin-top: 30px;">'
                f'    <p style="margin: 0; color: white;">Preço sugerido</p>'
                f'    <p style="font-size: 24px; margin-bottom: 5px; color: white;">R$ {price_prediction:,.0f}</p>'  # formatting to separate thousands with comma
                f'</div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 30px; margin-top: 30px;">'
                f'    <p style="margin: 0;">Preço máximo</p>'
                f'    <p style="font-size: 16px; margin-bottom: 5px;">R$ {price_range[1]:,.0f}</p>'  # formatting to separate thousands with comma
                f'</div>',
                unsafe_allow_html=True
            )

        st.empty

        # PLOT MARKET PERFORMANCE OF SIMILAR ARTWORKS
        st.markdown('<h2>Performance em leilão de obras semelhantes</h2>', unsafe_allow_html=True)

        fig = chart.get_similar_lots_performance_chart(similar_lots_performance)
        st.pyplot(fig)

        # TABLE OF SIMILAR ARTWORKS AUCTIONED
        st.dataframe(similar_lots[['Medium', 'Height (cm)', 'Width (cm)', 'Price (BRL)', 'url']], width=1000)

def check_email(email):
    if not ('@' in email and '.' in email):
        st.error('Por favor, insira um e-mail válido')
        st.stop()
    else:
        pass

def check_similar_lots(similar_lots):
        if similar_lots.shape[0] == 0:
            no_similar_lots = True
        else:
            no_similar_lots = False
        return no_similar_lots


def get_data(email, characteristics):
    back_end.save_lead(email, characteristics)
    price_prediction = back_end.get_price_prediction(characteristics)
    similar_lots = back_end.get_similar_lots(characteristics)
    similar_lots_performance = back_end.get_similar_lots_performance(similar_lots)
    return price_prediction, similar_lots, similar_lots_performance

