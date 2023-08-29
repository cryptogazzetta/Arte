## CONSTANTS
import pandas as pd

GOALS_OPTIONS = ["colecionar", "explorar",
                 "decorar", "comprar um presente",
                 "investir", "outro"]

# get list of columns in csv file
columns_to_drop = ['Size', 'Price', 'Artist', 'Title', 'Image_Url', 'Marketplace']
df = pd.read_csv('artsoul_dummies.csv').drop(columns=columns_to_drop)
interests_list = df.columns.tolist()
INTERESTS_OPTIONS = interests_list

INFO_JSON_LIST = [
        {"info_name": "greeting", "question": "Oi! Estou aqui para te ajudar a encontrar o que você ama em arte. Vamos começar?"},
        {"info_name": "name", "question": "Ótimo! Para começar, como posso te chamar?"},
        {"info_name": "goals", "question": "Muito prazer! Qual o seu objetivo aqui? Pode ser colecionar arte, decorar um apartamento ou comprar um presente, por exemplo.", "options": GOALS_OPTIONS},
        {"info_name": "interests", "question": "Você se interessa por algum estilo, técnica ou material? Pode listar os seus favoritos ;)", "options": INTERESTS_OPTIONS},
        {"info_name": "budget", "question": "Maravilha! Última coisa: quanto você se imagina gastando numa obra de arte?"},
        {"info_name": "bye", "question": "Muito obrigado!! Isso é tudo que eu preciso saber agora. Enquanto eu preparo um relatório completo para você, deixo algumas obras de arte que acho que você vai gostar. Até mais!"}
        ]