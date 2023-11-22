import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_similar_lots_performance_chart(similar_lots_performance):
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