import matplotlib.pyplot as plt

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
