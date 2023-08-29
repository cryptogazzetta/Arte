## External Modules
import streamlit as st
from streamlit_carousel import carousel
import time
## Project Modules
import back_end
import constants
import data_clean


## FUNCTIONS
def assistant_message(info_json):
    time.sleep(1)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(info_json['question'])
    assistant_message = {"role": "assistant", "content": info_json['question'], "info_name": info_json['info_name']}
    st.session_state.messages.append(assistant_message)


def user_message(info_name, user_input):
        user_message = {"role": "user", "content": user_input, "info_name": info_name}    
        st.session_state.messages.append(user_message)
        st.session_state.user_json[info_name] = user_input
        with st.chat_message("user"):
            st.markdown(user_input)


def start_chat():
    st.session_state.info_index = 0
    st.session_state.messages = [] 
    st.session_state.user_json = {}
    st.session_state.chat_input_container = st.empty()


def finish_chat():
    st.session_state.chat_input_container.empty()

    user_json = st.session_state.user_json
    st.session_state.user_json = data_clean.extract_structured_info(user_json)
    
    artworks_info = back_end.get_suggested_artworks(st.session_state.user_json)
    if len(artworks_info) == 0:
        print("couldn't find any artwork that matches your preferences.")
    
    artworks_info = back_end.get_test_items(artworks_info)
    carousel(items=artworks_info, width=1)
    print(constants.INTERESTS_OPTIONS)

    if st.button("Descubra mais obras de arte"):
        url = 'google.com'
        # go to url
        st.markdown(url, unsafe_allow_html=True)


def update_info_json(info_json, user_input):
    user_message(info_json['info_name'], user_input)

    info_json['info'] = user_input
    constants.INFO_JSON_LIST[st.session_state.info_index] = info_json

    st.session_state.info_index += 1
    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]
    assistant_message(info_json)