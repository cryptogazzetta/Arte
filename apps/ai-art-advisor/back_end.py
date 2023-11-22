import pandas as pd
import ast

def get_suggested_artworks(user_json):
    artworks = pd.read_csv('artsoul_dummies.csv').drop(columns=['Size', 'Marketplace'])
    suggested_artworks = artworks[artworks['Price'] <= int(user_json['budget'])]

    suggested_artworks['Score'] = 0
    if 'interests' in user_json.keys():
        for interest in user_json['interests']:
            print(interest)
            suggested_artworks['Score'] += suggested_artworks[interest]
    
    suggested_artworks = suggested_artworks.sort_values(by=['Score'], ascending=False)[:5]
    print(suggested_artworks)

    return suggested_artworks


user_json = {'name': 'Lucas', 'goals': ['Decorar'], 'interests': ['Pop', 'Conceitual'], 'budget': 12000}
get_suggested_artworks(user_json)

def get_test_items(dataframe):
    # Convert artworks to format of test_items
    dataframe = dataframe[["Artist", "Title", "Price", "Image_Url"]][:3]
    dataframe.columns = ["title", "text", "price", "img"]
    dataframe["interval"] = None
    
    items = []
    for index, row in dataframe.iterrows():
        items.append(dict(row))
    return items