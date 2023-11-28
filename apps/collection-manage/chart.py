import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_donut_chart(data):
    # Create a donut chart with a custom color scheme
    fig, ax = plt.subplots()
    colors = ['red', 'green', 'blue', 'purple', 'orange']
    wedges, texts, autotexts = ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=colors)

    # Draw a white circle at the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.7, color='white', fc='white', linewidth=0)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Set the text color to white
    for text in texts + autotexts:
        text.set_color('black')
    
    return fig

def get_line_chart(data):
    fig, ax = plt.subplots(figsize=(10, 5))

    # index as int
    data.index = data.index.astype(int)
    
    ax.set_ylabel('Portfolio Value')
    ax.plot(data, color='white', label='Portfolio Value (USD)', linewidth=2)
    ax.set_title('Performance da carteira')

    ax.set_ylim(bottom=0)

    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    
    # Set the y-axis color to white
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors='white')

    formatter = ticker.StrMethodFormatter('US${x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    # Set black background
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.legend().set_visible(False)

    return fig