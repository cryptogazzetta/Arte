# External Modules
import streamlit as st
# Project Modules
import back_end
import chart

## MAIN
def main():
    ## DATA FROM BACK END
    collection, collection_performance, performance_stats = get_data()

    ## Define CSS
    st.set_option('deprecation.showPyplotGlobalUse', False)
    css = back_end.get_file_from_github('apps/collection_manage/styles.css', format='css')
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    ## PAGE TITLE
    st.markdown('<h>Marte</h>', unsafe_allow_html=True)
    st.markdown(
        '<p>Criamos essa ferramenta para ajudar a gerir coleções com base em análises quantitativas. Fique à vontade para experimentar a ferramenta, compartilhar e propor sugestões ;) </p>',
        unsafe_allow_html=True
    )

    ## CUSTOM COLLECTION
    # collection = st.data_editor(collection)
    
    ## COLLECTION PERFORMANCE
    show_collection_performance(collection, collection_performance, performance_stats)

    ## COLLECTION COMPOSITION
    show_collection_composition(collection)

    ## COLLECTION
    show_collection(collection)

## PAGE CONFIG
st.set_page_config(
    page_title="Marte - Gestão de coleção",
    page_icon=":🎨:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

## DATA FROM BACK END
def get_data():
    collection = back_end.get_collection()
    collection_performance = back_end.get_collection_performance(collection)
    collection = back_end.get_price_prediction(collection, collection_performance)
    performance_stats = back_end.get_performance_stats(collection_performance)
    return collection, collection_performance, performance_stats

def show_collection(collection):
    st.markdown('<h1>Obras da coleção</h1>', unsafe_allow_html=True)
    st.dataframe(back_end.fix_collection_to_show(collection), width=2000)

def show_collection_composition(collection):
    st.markdown('<h1>Composição da coleção</h1>', unsafe_allow_html=True)

    # st.dataframe(collection)


    col1, col2 = st.columns(2)
    with col1:
        artists_options = ['Todos'] + list(collection.index.unique())
        artists_selected = st.selectbox('Filtro por artista', artists_options, index=0)
    with col2:
        mediums_options = ['Todos'] + list(collection['Medium_type'].unique())
        mediums_selected = st.selectbox('Filtro por técnica', mediums_options, index=0)

    # Filter data
    if artists_selected != 'Todos':
        collection = collection.loc[artists_selected]
    if mediums_selected != 'Todos':
        collection = collection.loc[collection['Medium_type'] == mediums_selected]
    
    # get donut charts of value by artist and medium
    artist_value_df = back_end.get_value_by_artist(collection)
    artist_value_donut_fig = chart.get_bar_chart(artist_value_df)
    medium_value_df = back_end.get_value_by_artist(collection)
    medium_value_donut_fig = chart.get_bar_chart(medium_value_df)

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(artist_value_donut_fig)
    with col2:
        st.pyplot(medium_value_donut_fig)

def show_collection_performance(collection, collection_performance, performance_stats):
    st.markdown('<h1>Performance da coleção</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        fig = chart.get_line_chart(collection_performance['Total'])
        st.pyplot(fig)
    with col2:
        st.dataframe(performance_stats, width=300)
