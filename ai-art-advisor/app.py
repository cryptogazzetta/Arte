## External Modules
import streamlit as st
from streamlit_carousel import carousel
import time
## Project Modules
import back_end

st.title("Your AI Art Advisor")


## WHEN STARTING
if "messages" not in st.session_state:
    first_message = "Hi! \n I'm here to help you find the perfect art for you. \n Let's get started?"
    st.session_state.messages = [{"role": "assistant", "content": first_message, "info_name": "user_greeting"}]
    st.session_state.info_index = 0
    st.session_state.user = back_end.User(name=None)
    st.session_state.chat_active = True

info_json = [
        {"info_name": "greeting", "question": "user_greeting"},
        {"info_name": "name", "question": "What's your name?"},
        {"info_name": "goals", "question": "Nice to meet you! What brings you here?"},
        {"info_name": "topics", "question": "What kind of art are you interested in?"},
        {"info_name": "budget", "question": "Last thing: how much do you intend to spend?"},
        {"info_name": "bye", "question": "That's great! That's pretty much everything I need to know now."}]

## CHAT FLOW
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.chat_active:
    info_name = info_json[st.session_state.info_index]["info_name"]
    question = info_json[st.session_state.info_index + 1]["question"]

    if user_input := st.chat_input("Type anything to start ..."):
        if info_name == "greeting":
            pass
        if info_name == "budget":
            user_input = float(user_input)

        if info_name == "topics":
            user_input = "['Moderno', 'Contemporâneo']"
        
        user_info_ = {"info_name": info_name, "content": user_input}
        st.session_state.user.change_attribute(info_name, user_input)

        user_message = {"role": "user", "content": user_input, "info_name": info_name}
        st.session_state.messages.append(user_message)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(question)
        st.session_state.messages.append({"role": "assistant", "content": question, "info_name": info_name})
        st.session_state.info_index += 1


## WHEN FINISHED
if st.session_state.info_index >= len(info_json)-1:
    user = st.session_state.user
    message_placeholder = st.empty()
    st.session_state.chat_active = False
    
    artworks_info = back_end.retrieve_artworks_info(user)
    if len(artworks_info) == 0:
        st.write("Sorry, we couldn't find any artwork that matches your preferences.")
    else:
        artworks_info = back_end.get_test_items(artworks_info)
        carousel(items=artworks_info, width=1)