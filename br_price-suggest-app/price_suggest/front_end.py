import streamlit as st
# from streamlit_carousel import carousel
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
# project modules
import back_end


## IMPORT STYLES FROM .CSS FILE
with open('./styles.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

## PAGE TITLE
st.markdown('<h>Marte</h>', unsafe_allow_html=True)
st.markdown('<p>Criamos essa ferramenta para ajudar a precificar obras de arte. As sugestões de preço são baseadas em modelos de Inteligência Artificial.</p>', unsafe_allow_html=True)
st.markdown('<p>Fique à vontade para experimentar a ferramenta, compartilhar e propor sugestões ;) </p>', unsafe_allow_html=True)

# Get lists of artists and techniques (converting techniques to string)
artists_list = back_end.artists_list
techniques_list = back_end.techniques_list


#### USER INPUTS

# Artist
st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artista', artists_list, label_visibility="collapsed", index=0)

# Technique
st.markdown('<h2>Técnica</h2>', unsafe_allow_html=True)
technique = st.selectbox('Técnica', techniques_list, label_visibility="collapsed")

# Measures
col1, col2 = st.columns(2)
with col1:
    st.markdown('<h2>Altura (cm)</h2>', unsafe_allow_html=True)
    height = st
    height = st.number_input('Altura', 1, 5000, 50, label_visibility="collapsed")
with col2:
    st.markdown('<h2>Largura (cm)</h2>', unsafe_allow_html=True)
    width = st.number_input('Largura', 1, 5000, 50, label_visibility="collapsed")

# E-mail
st.markdown('<h2>Seu e-mail</h2>', unsafe_allow_html=True)
email = st.text_input('E-mail', label_visibility="collapsed")


#### OUTPUTS

if st.button('Gerar relatório'):
    characteristics = {'Artist': artist, 'Height (cm)': height, 'Width (cm)': width, 'Technique': technique}

    artist = characteristics['Artist']
    technique = characteristics['Technique']

    # Get suggested price, similar lots, and performance from back_end
    price_prediction = back_end.get_price_prediction(characteristics)
    similar_lots = back_end.get_similar_lots(characteristics)
    similar_lots_performance = back_end.get_similar_lots_performance(similar_lots)

    if similar_lots.shape[0] == 0:
        no_similar_lots = True
    else:
        no_similar_lots = False

    st.divider()


    # SHOW PRICE SUGGESTION    
    st.markdown(f'<h1>{technique} by {artist}</h1>', unsafe_allow_html=True)
    if no_similar_lots:
        st.markdown(f'<p>No similar artworks were offered at auction</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p>{similar_lots.shape[0]} Similar artworks were offered at auction</p>', unsafe_allow_html=True)
    # Show price suggestion if all inputs are filled
    st.markdown(f'<h1>Suggested Price: R$ {price_prediction:.2f}</h1>', unsafe_allow_html=True)


    # PLOT MARKET PERFORMANCE OF SIMILAR ARTWORKS
    st.markdown('<h2>Similar artworks total sales</h2>', unsafe_allow_html=True)
    # st.line_chart(similar_lots_performance[['Total_Sales', 'Mean_Price']])
    # Plotting
    # Set Lexend font for better readability
    rcParams['font.family'] = 'Lexend'

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot Total Sales and Mean Price on the left y-axis
    color = 'tab:red'
    ax1.set_xlabel('Year of Sale', color='white')
    ax1.set_ylabel('Total Sales (R$)', color=color)
    ax1.plot(similar_lots_performance['Year of sale'], similar_lots_performance['Total_Sales'], color=color, marker='o', label='Total Sales')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for Mean Price
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Mean Price (R$)', color=color)
    ax2.plot(similar_lots_performance['Year of sale'], similar_lots_performance['Mean_Price'], color=color, marker='o', label='Mean Price')
    ax2.tick_params(axis='y', labelcolor=color)

    # Set black background
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')
    ax2.set_facecolor('black')

    # Include 'Year of Sale' on the x-axis for selected years

    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')

    # Format y-axes as currency with no decimals
    formatter = ticker.StrMethodFormatter('R${x:,.0f}')
    ax1.yaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)

    # Display the legend
    ax1.legend(loc='upper left', bbox_to_anchor=(0.75, 1))

    # Display the plot using Streamlit
    st.pyplot(fig)


    # TABLE OF SIMILAR ARTWORKS AUCTIONED
    st.dataframe(similar_lots[['Artist', 'Technique', 'Height (cm)', 'Width (cm)', 'Price (BRL)']], width=1000)


    # CAROUSEL OF SIMILAR ARTWORKS AUCTIONED
    # st.markdown('<h2>Similar artworks auctioned</h2>', unsafe_allow_html=True)
    # lots_to_slideshow = similar_lots.to_dict('records')
    # # rename keys to match carousel component requirements
    # for lot in lots_to_slideshow:
    #     lot['img'] = lot.pop('img_url')
    #     lot['title'] = f"R$ {lot.pop('Price (BRL)'):.2f}"
    #     lot['text'] = f'{lot.pop("Technique")}, {lot.pop("Height (cm)")} x {lot.pop("Width (cm)")} cm'
    # carousel(lots_to_slideshow, height=800)


    # TABLE OF SIMILAR ARTWORKS BEING SOLD AT MARKETPLACES
    # st.markdown('<h2>Marketplace offers</h2>', unsafe_allow_html=True)
    # st.write('Coming soon...')