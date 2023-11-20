import streamlit as st
from streamlit_carousel import carousel
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
st.markdown('<p>This tool allows you to explore price some artwork and the art market. Feel free to try it and share your thoughts ;)</p>', unsafe_allow_html=True)

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

    # Get suggested price, similar lots, and performance from back_end
    price_prediction = back_end.get_price_prediction(characteristics)
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
    # Show price suggestion if all inputs are filled
    if artist != 'Any artist' and technique != 'Any Technique' and height and width:
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
    selected_years = [2000, 2005, 2010, 2015, 2020]
    ax1.set_xticks(selected_years)
    ax1.set_xticklabels(selected_years)
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