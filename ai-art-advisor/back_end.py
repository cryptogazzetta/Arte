import pandas as pd
import ast


class User:
    def __init__(self, name):
        self.name = name
        self.greeting = None
        self.goals = None
        self.topics = None
        self.budget = 1000
        self.bye = None

    def __repr__(self):
        return f"User(name={self.name}, greeting={self.greeting}, goals={self.goals}, styles={self.styles}, budget={self.budget}, bye={self.bye})"

    def change_attribute(self, attribute_name, new_value):
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, new_value)
            return True
        else:
            return False


def retrieve_artworks_info(user):
    artworks = pd.read_csv("../temporary-files/artsoul_artworks_info.csv")
    # artworks = artworks[artworks["Topics"] == user.topics]
    artworks = artworks[artworks["Price"] <= user.budget]
    return artworks


def get_test_items(dataframe):
    # Convert artworks to format of test_items
    dataframe = dataframe[["Artist", "Title", "Price"]][:3]
    dataframe.columns = ["title", "text", "price"]
    img = [
        "https://imgs.search.brave.com/mD1BWXbTHfRJnFxXNvwJFOYSrtv5tXJ2d7RHGuEl5WI/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9sb2Jv/cG9wYXJ0LmNvbS5i/ci93cC1jb250ZW50/L3VwbG9hZHMvMjAy/MC8wNy9QaW50dXJh/LUJhcnJvY28uanBn",
        "https://imgs.search.brave.com/1xGKqWV1femfu2PvNmv010EN1wzlW6VIZjhVGuOO0Ik/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9jZG4u/Y3VsdHVyYWdlbmlh/bC5jb20vaW1hZ2Vu/cy9nZW9yZ2luYS1h/bGJ1cXVlcnF1ZS1p/bXByZXNzaW9uaXNt/by0wLWNrZS5qcGc",
        "https://imgs.search.brave.com/ucsRKgCqq7tDrp6UqvWfytOa7U3tAXY_hiYOYBpzlLE/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9jZG4u/Y3VsdHVyYWdlbmlh/bC5jb20vaW1hZ2Vu/cy9hcnRlLW1lZGll/dmFsLTU0bi5qcGc"
            ]
    dataframe["img"] = img
    dataframe["interval"] = None
    
    items = []
    for index, row in dataframe.iterrows():
        items.append(dict(row))
    return items