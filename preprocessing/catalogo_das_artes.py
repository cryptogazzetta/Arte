import pandas as pd

def preprocess(raw_info_path, clean_info_path):
    lots = pd.read_csv(raw_info_path)

    lots = rename_columns(lots)
    lots = fix_artist(lots)
    lots = fix_dimensions(lots)
    lots = fix_price(lots)
    lots = fix_technique(lots)
    lots = define_sold(lots)
    lots = define_year_of_sale(lots)
    lots = lots.drop(columns=['Dimensão', 'Avaliação', 'Data da Pesquisa'])
    lots = drop_rows(lots)

    lots.to_csv(clean_info_path, index=False)

def rename_columns(lots):
    lots = lots.rename(columns={'Artista': 'Artist', 'Técnica': 'Technique', 'Ano': 'Year',
                                'Tipo': 'Type', 'Width': 'Width (cm)', 'Height': 'Height (cm)',
                                'Year of sale': 'Year of sale'})
    return lots

def fix_artist(lots):
    # get everything before the first non-alphabetic character
    lots['Artist'] = lots['Artist'].str.extract(r'(^[a-zA-Z ]*)')
    lots['Artist'] = lots['Artist'].str.strip()
    return lots

def fix_dimensions(lots):
    lots['Height (cm)'] = lots['Dimensão'].str.extract(r'(.*?) x')
    lots['Height (cm)'] = lots['Height (cm)'].str.replace(' cm', '').str.replace(',', '.').astype(float)
    lots['Width (cm)'] = lots['Dimensão'].str.extract(r'x (.*) cm')
    lots['Width (cm)'] = lots['Width (cm)'].str.replace(' cm', '').str.replace(',', '.').astype(float)
    return lots

def fix_price(lots):
    lots['Price (BRL)'] = lots['Avaliação'].str.extract(r'R\$ (.*?) \|')
    lots['Price (BRL)'] = lots['Price (BRL)'].str.replace('.', '').str.replace(',', '').astype(float) / 100
    lots['Price (USD)'] = lots['Avaliação'].str.extract(r'USD (.*)$')
    lots['Price (USD)'] = lots['Price (USD)'].str.replace('.', '').str.replace(',', '').astype(float) / 100
    return lots

def map_technique(technique):
    technique_fix = {'pintura': ['pintad', 'pintura', 'óleo', 'vinil', 'acrílic', 'aquarela', 'guache', 'pastel', 'tinta', 'têmpera'],
                    'desenho': ['desenho', 'caneta', 'lápis', 'lapis', 'carvao', 'carvão', 'grafite', 'nanquim', 'giz'],
                    'reprodução': ['fine art', 'impressão gráfica', 'reprodução gráfica', 'reprodução', 'giclée', 'giclê', 'gliccée', 'glicée', 'serifrafia', 'litografia', 'litogravura', 'lito offset', 'xilogravura', 'gravura', 'gravu', 'serigrafia', 'xilogravura', 'print', 'agua-forte', 'água-forte']}
       
    for key, values in technique_fix.items():
        for value in values:
            if value.lower() in technique.lower():
                return key
    return 'outro'

def fix_technique(lots):

    lots['Technique'] = lots['Technique'].astype(str)
    lots['Technique_fix'] = lots['Technique'].apply(map_technique)

    return lots

def define_sold(lots):
    lots['Sold'] = lots['Avaliação'].str.contains('Valor de venda em leilão:')
    return lots

def define_year_of_sale(lots):
    lots['Year of sale'] = lots['Data da Pesquisa'].str.extract(r'(\d{4})')
    return lots

def drop_rows(lots):
    lots = lots[lots['Error'] == 'False']
    lots = lots[lots['Price (BRL)'] > 0]
    lots = lots.reset_index(drop=True)

    return lots