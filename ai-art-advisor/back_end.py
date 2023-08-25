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
    dataframe = dataframe[["Artist", "Title", "Price", "Image_URL"]][2:5]
    dataframe.columns = ["title", "text", "price", "img"]
    dataframe["interval"] = None
    
    items = []
    for index, row in dataframe.iterrows():
        items.append(dict(row))
    return items