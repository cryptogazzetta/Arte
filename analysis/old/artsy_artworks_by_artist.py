import pandas as pd
import requests




# Get filtered list of artists
df = pd.read_csv("artist_list.csv")
print('csv opened')
# Set column name
df.columns = ['name']
df['name'] = df['name'].str.lower()

print(df)

artist_ids = {}

#get link of each author artworks
def get_artworks_ids():
    for artist in artists.find():
        # Check for artist name
        if artist['name'].lower() in df.values or artist['sortable_name'].lower() in df.values:
            print(artist['name'], artist['id'])
            # Defines name of the artist found
            name = artist['name']
            # Defines link to artworks of the artist found
            artist_ids[name] = artist['_links']['artworks']['href']
    print('get artworks ids OK')
    return artist_ids


def get_artworks():
    artist_artworks = get_artworks_ids()
    for id in artist_ids:
        #get artworks
        req = requests.get("https://api.artsy.net/api/artworks?artist_id=" + id, headers=headers)
        reqjson = req.json()
        print(reqjson)
        artworks = reqjson['_links']['_embedded']['artworks']['href']
        print(artworks.json())
    print('get artworks OK')


get_artworks()