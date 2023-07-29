## FUNCTIONS


## DATAFRAME CREATION
def get_artworks_df():
    artworks = pd.read_csv('../temporary-files/saatchi_artworks_info.csv')
    artworks.rename(columns=lambda x: x.title(), inplace=True)
    artworks = calculate_area_and_price_per_area(artworks)
    for column_name in ['Styles', 'Mediums', 'Subjects', 'Materials']:
        artworks[column_name] = artworks[column_name].apply(lambda x: [str(value.strip()) for value in x.split(',')])
    for column_name in ['Title']:
        artworks[column_name] = artworks[column_name].apply(lambda x: [str(value.strip()) for value in x.split(' ')])
    # Remove outliers (artworks with price / in² in the 0.5% and 99.5% percentiles)
    artworks = artworks[artworks['Price / in²'] > artworks['Price / in²'].quantile(0.05)]
    artworks = artworks[artworks['Price / in²'] < artworks['Price / in²'].quantile(0.95)]
    return artworks

def get_artists_df(artworks_df):
    agg_df = artworks_df.dropna(subset=['Price'])
    agg_data = agg_df.groupby('Artist').agg({'Artist': 'count',
                                            'Price': ['mean', lambda x: x.std(skipna=False)],
                                            'Price / in²': ['mean', lambda x: x.std(skipna=False)],
                                            'Size': ['mean', lambda x: x.std(skipna=False)]})
    agg_data = agg_data.reset_index()

    # Flatten the column names
    agg_data.columns = ['Artist', 'NumArtworks', 'MeanPrice', 'StdPrice', 'MeanPricePerInch', 'StdPricePerInch', 'MeanSize', 'StdSize']

    # Create a new DataFrame with the aggregated data from artworks_info
    artists_from_artworks = pd.DataFrame(agg_data)
    artists_from_artworks = artists_from_artworks[artists_from_artworks['NumArtworks'] >= 3]
    # Get artists data from artists_info
    artists_from_artists = pd.read_json('../temporary-files/saatchi_artists_info_clean.json')
    artists_from_artists.rename(columns=lambda x: x.title(), inplace=True)
    artists_from_artists.rename(columns={'Name': 'Artist'}, inplace=True)

    # New dataframe with all artists that are contained in both dataframes
    artists_from_artists = artists_from_artists[artists_from_artists['Artist'].isin(artists_from_artworks['Artist'])]
    artists = pd.merge(artists_from_artworks, artists_from_artists, on='Artist')

    return artists

def calculate_area_and_price_per_area(dataframe):
    # Iterate over the "Size" column
    df = dataframe.copy()
    for i, size in enumerate(dataframe['Size']):
        # Extract the dimensions using regular expression
        dimensions = re.findall(r'\d+(?:\.\d+)?', size)
        if len(dimensions) >= 2:
            # Extract the width and height dimensions
            try:
                width = float(dimensions[0])
                height = float(dimensions[1])
                total_area = width * height
                df.at[i, 'Size'] = total_area
            except:
                df.at[i, 'Size'] = 'NaN'
    df['Price / in²'] = df['Price'] / df['Size']

    return df




def get_unique_values(df, column_name):
    # Extract all unique styles from the column
    unique_values = set()
    for styles in df[column_name]:
        if isinstance(styles, str):
            styles_list = [style.strip() for style in styles.split(',')]
            unique_values.update(styles_list)
    
    return unique_values

def check_columns(df, columns_names):
    for column in columns_names:
        df[column] = df[column].str.title()
        unique_list = get_unique_values(df, column)
        print(column, len(unique_list), 'unique values')

def restart_df(dataframe):
    df = calculate_area_and_price_per_area(dataframe)
    df = df[['Styles', 'Mediums', 'Subjects', 'Artist', 'Size', 'Price']]
    df = df.dropna(subset='Styles')
    columns_names = ['Styles', 'Mediums', 'Subjects']

    # Turn the "Styles" column into a list of strings
    for column in columns_names:
        column_serie = df[column].apply(lambda x: x.split(','))
        df[column] = column_serie
        return df

## CLEAN DATA

def remove_words_from_list(lst, words_to_remove):
    return [word for word in lst if word not in words_to_remove]


## OOOOLD
def fix_column(dataframe, column_name, fix_dict, remove_list, split_list):
    # Remove whitespaces from the beginning and end of each string
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [item.strip() for item in lst])
    # Change '-' to whitespaces in each string
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [item.replace('-', ' ') for item in lst])
    # Capitalize each string
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [item.title() for item in lst])
    # Remove ' Art' and ' Painting' from the end of each string
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [style.replace(' Art', '') for style in lst])
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [style.replace(' Painting', '') for style in lst])
    # Splits items present the split_list into separate items
    dataframe[column_name] = dataframe[column_name].apply(lambda lst: [item for item in lst if item not in split_list] + [item for item in lst for split_item in split_list if split_item in item])
    return dataframe


## NEEEW
def fix_based_on_dict(column, fix_dict):
    column = column.apply(lambda lst: [next((key for key, values in fix_dict.items() if item in values), item) for item in lst])
    return column

def remove_words_from_column(column, remove_list):
    column = column.apply(lambda lst: remove_words_from_list(lst, remove_list))
    return column


def get_occurrence_count_on_col_dict(values):
    # Get all unique values from the column
    occurrences_counts_dict = dict(Counter(values))
    return occurrences_counts_dict


def group_by_segments(artworks_data, column_name, column, occurrences_threshold):

    ## GETTING ONE DF FOR SEGMENT
    segments_dfs = get_dfs_for_segments(filtered_artworks_data, column_name, occurrence_count_on_col_dict, occurrences_threshold)

    # New dataframe with unique segments as index and MeanPrice, MedianPrice, MeanSize, MedianSize as columns
    all_segments_df = pd.DataFrame(index=segments_dfs.keys(), columns=['MeanPrice', 'MedianPrice', 'MeanSize', 'MedianSize', 'MeanPricePerIn²', 'MedianPricePerIn²', 'Count'])
    # Populate dataframe with mean price, median price, mean size and median size for each segment
    for key, value in segments_dfs.items():
        all_segments_df.loc[key, 'MeanPrice'] = value['Price'].mean().round(0)
        all_segments_df.loc[key, 'MedianPrice'] = value['Price'].median().round(0)
        all_segments_df.loc[key, 'MeanSize'] = value['Size'].mean().round(0)
        all_segments_df.loc[key, 'MedianSize'] = value['Size'].median().round(0)
        all_segments_df.loc[key, 'MeanPricePerIn²'] = value['Price / in²'].mean().round(2)
        all_segments_df.loc[key, 'MedianPricePerIn²'] = value['Price / in²'].median().round(2)
        all_segments_df.loc[key, 'Count'] = len(value)

    all_segments_df.sort_values(by='MeanPrice', ascending=False, inplace=True)
    
    # New dataframe for each segment
    segments_dfs = {}
    for key, value in occurrence_count_on_col_dict.items():
        if value > occurrences_threshold:
            segments_dfs[key] = dataframe[dataframe[column_name].apply(lambda x: key in x)]
    return segments_dfs


def analyse_by_column(dataframe, column_name, threshold):
    artworks_count_by_segment = dataframe[column_name].value_counts()
    artworks_count_pct_by_segment = artworks_count_by_segment / dataframe[column_name].value_counts().sum()
    # filter out segments with less than [threshold] artworks
    threshold = 200
    selection = artworks_count_by_segment[artworks_count_by_segment > threshold].index
    dataframe = dataframe[dataframe[column_name].isin(selection)]
    return dataframe

def compare_segments(dataframe, segments_to_compare, x_column_name, y_column_name):
    for segment in segments_to_compare:
        print(segment)

        if segment == 'All':
            segment_df = dataframe
        else:
            segment_df = segments_dfs[segment]

        x = segment_df[[x_column_name]]
        y = segment_df[y_column_name]
        print('stats:', get_stats(segment_df, x, y))
        get_all_models(x, y)

        xlim = (0, 10000)
        ylim = (0, 40000)
        # segment_df.plot.scatter(x=segment_df[[x_column_name]], y=segment_df[y_column_name], title=segment+' artworks', figsize=(5, 3), xlim=xlim, ylim=ylim)


def segment_and_clean_data(artworks_data, column_name, occurrences_threshold):
    column = artworks_data[column_name]
    
    segments_in_column_list = [value for sublist in column for value in sublist]
    occurrence_count_on_col_dict = get_occurrence_count_on_col_dict(segments_in_column_list)
    
    filtered_artworks_data = remove_empty_rows(artworks_data, column)
    filtered_artworks_data = filtered_artworks_data.dropna(subset=['Price', 'Size'])
    filtered_artworks_data[column_name] = column
    
    segments_dfs = get_dataframes_for_segments(filtered_artworks_data, column_name, occurrence_count_on_col_dict, occurrences_threshold)
    all_segments_df = create_segments_dataframe(segments_dfs)
    
    return filtered_artworks_data, all_segments_df, segments_dfs


def remove_empty_rows(dataframe, column):
    return dataframe[column.apply(lambda x: len(x) > 0)]


def get_dataframes_for_segments(dataframe, column_name, occurrence_count_on_col_dict, occurrences_threshold):
    segments_dfs = {}
    for key, value in occurrence_count_on_col_dict.items():
        if value > occurrences_threshold:
            segments_dfs[key] = dataframe[dataframe[column_name].apply(lambda x: key in x)]
    return segments_dfs


def create_segments_dataframe(segments_dfs):
    all_segments_df = pd.DataFrame(index=segments_dfs.keys(),
                                   columns=['MeanPrice', 'MedianPrice', 'MeanSize', 'MedianSize',
                                            'MeanPricePerIn²', 'MedianPricePerIn²', 'Count'])
    for key, value in segments_dfs.items():
        all_segments_df.loc[key, 'MeanPrice'] = value['Price'].mean().round(0)
        all_segments_df.loc[key, 'MedianPrice'] = value['Price'].median().round(0)
        all_segments_df.loc[key, 'MeanSize'] = value['Size'].mean().round(0)
        all_segments_df.loc[key, 'MedianSize'] = value['Size'].median().round(0)
        all_segments_df.loc[key, 'MeanPricePerIn²'] = value['Price / in²'].mean().round(2)
        all_segments_df.loc[key, 'MedianPricePerIn²'] = value['Price / in²'].median().round(2)
        all_segments_df.loc[key, 'Count'] = len(value)
    all_segments_df.sort_values(by='MeanPrice', ascending=False, inplace=True)
    return all_segments_df


def prepare_dataframe_dummies(artworks_data, column_name, segments_dfs):
    dummies_for_segment = artworks_data[['Price', column_name]].dropna(subset=['Price'])
    
    for key, value in segments_dfs.items():
        dummies_for_segment[key] = artworks_data[column_name].apply(lambda x: True if key in x else False)
    
    return dummies_for_segment