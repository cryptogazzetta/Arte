import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_similar_lots_performance_chart(similar_lots_performance):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Convert 'Year of sale' to integers
    years = similar_lots_performance['Year of sale'].astype(int)

    # Plot Total Sales on the left y-axis
    color = '#8a8888'
    ax1.set_ylabel('Sales Count', color=color)
    ax1.bar(years, similar_lots_performance['Sales_Count'], color=color, label='Sales Count')
    ax1.axhline(0, color='white', linewidth=1)  # Include the line of the horizontal axis for Total Sales
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for Mean Price
    ax2 = ax1.twinx()
    color = '#7cf28a'
    ax2.set_ylabel('Mean Price (R$)', color=color)
    ax2.plot(years, similar_lots_performance['Mean_Price'], color=color, label='Mean Price')
    ax2.tick_params(axis='y', labelcolor=color)

    # Set y-axis limits for both axes to coincide at zero
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    # Set black background
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')
    ax2.set_facecolor('black')

    # Include 'Year of Sale' on the x-axis for selected years
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')

    # Format y-axes as currency with no decimals
    formatter = ticker.StrMethodFormatter('R${x:,.0f}')
    # ax1.yaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)

    # Remove the legend
    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)

    plt.show()
