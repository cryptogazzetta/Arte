import openai
from utils import constants

# create a new classification model in the openai API
openai.api_key = constants.OPENAI_API_KEY

def chat(system_message, info_txt):
    messages = [system_message]
    messages.append({"role": "user", "content": info_txt})
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
        )
    
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return messages