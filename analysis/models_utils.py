import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SKLEARN
from sklearn.model_selection import train_test_split
# Metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# Models
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

warnings.filterwarnings('ignore')


## DATA PREPARATION
def get_df_to_model(lots):
    lots_to_model = lots[['Artist', 'Width (cm)', 'Height (cm)', 'Year of sale', 'Price (BRL)', 'Medium_type']]#, 'Year']]
    lots_to_model.dropna(subset=['Artist', 'Width (cm)', 'Height (cm)', 'Year of sale', 'Price (BRL)', 'Medium_type'], inplace=True)
    # lots_to_model.fillna(value=1970, inplace=True) # fill NaN year with 1970

    print('shape of lots_to_model (before split):', str(lots_to_model.shape))

    X = lots_to_model.drop(['Price (BRL)'], axis=1)
    y = lots_to_model['Price (BRL)']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    X_train = pd.get_dummies(X_train, columns=['Artist', 'Medium_type'], drop_first=True)
    X_test = pd.get_dummies(X_test, columns=['Artist', 'Medium_type'], drop_first=True)

    print('model features:', len(X_train.columns))

    # add to X_test all columns that are in X_train but not in X_test
    for column in X_train.columns:
        if column not in X_test.columns:
            X_test[column] = 0

    # remove from x_test all columns that are in X_test but not in X_train
    for column in X_test.columns:
        if column not in X_train.columns:
            X_test.drop(column, axis=1, inplace=True)

    # sort columns alphabetically
    X_train = X_train.reindex(sorted(X_train.columns), axis=1)
    X_test = X_test.reindex(sorted(X_test.columns), axis=1)

    return X_train, X_test, y_train, y_test


## MODELS
def fit_models(X_train, y_train, X_test, y_test):
    models = {'Linear Regression': LinearRegression(),
              'Decision Tree': DecisionTreeRegressor(),
              'Random Forest': RandomForestRegressor(),
              'Gradient Boosting': GradientBoostingRegressor()}

    models_df = pd.DataFrame(columns=['Linear Regression', 'Decision Tree', 'Random Forest', 'Gradient Boosting'],
                             index=['R2', 'RMSE', 'MAE'])

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        r2 = r2_score(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        mae = mean_absolute_error(y_test, pred)
        
        models_df[name] = [r2, rmse, mae]

    return models_df, models # returns df with models performance and models dict


## TEST MODELS
def get_predicted_price_and_error(X_test, y_test, model):
    pred = model.predict(X_test)
    lots_copy = X_test.copy()
    lots_copy['Predicted Price'] = pred
    lots_copy['Actual Price'] = y_test
    lots_copy['Error'] = lots_copy['Predicted Price'] - lots_copy['Actual Price']
    lots_copy['Error %'] = lots_copy['Error'] / lots_copy['Actual Price'] - 1
    return lots_copy

def plot_predicted_vs_actual_price(dataframe):
    plt.figure(figsize=(8,4))
    plt.title('Predicted Price vs Actual Price')
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    # format axes: separate thousands with comma and format as currency
    plt.gca().xaxis.set_major_formatter('${x:,.0f}')
    plt.gca().yaxis.set_major_formatter('${x:,.0f}')
    plt.xscale('log')
    plt.yscale('log')
    plt.scatter(dataframe['Actual Price'], dataframe['Predicted Price'])
    # include trend line
    plt.plot(np.unique(dataframe['Actual Price']), np.poly1d(np.polyfit(dataframe['Actual Price'], dataframe['Predicted Price'], 1))(np.unique(dataframe['Actual Price'])), color='red')
    plt.show()

def plot_error_by_columns(dataframe, columns_names, type_of_column):
    plt.figure(figsize=(10, 4))
    plt.title('Error vs ' + type_of_column)
    plt.xlabel(type_of_column)
    plt.ylabel('Error %')
    plt.yscale('log')
    plt.xticks(rotation=90)
    plt.boxplot([dataframe[dataframe[column_name] == 1]['Error %'] for column_name in columns_names], labels=columns_names)
    plt.show()
