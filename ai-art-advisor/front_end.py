## External Modules
import streamlit as st
from streamlit_carousel import carousel
import time
## Project Modules
import back_end
import constants



## FUNCTIONS
def assistant_message(info_json):
    time.sleep(1)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(info_json['question'])
    assistant_message = {"role": "assistant", "content": info_json['question'], "info_name": info_json['info_name']}
    st.session_state.messages.append(assistant_message)

def user_message(info_name, user_input):
        # update messages
        user_message = {"role": "user", "content": user_input, "info_name": info_name}    
        st.session_state.messages.append(user_message)
        # update user info
        st.session_state.user.change_attribute(info_name, user_input)
        # show user message
        with st.chat_message("user"):
            st.markdown(user_input)


def start_chat():
    st.session_state.info_index = 0
    st.session_state.messages = [] 
    st.session_state.user = back_end.User(name=None)
    st.session_state.chat_active = True


def finish_chat():
    user = st.session_state.user
    message_placeholder = st.empty()
    st.session_state.chat_active = False
    
    artworks_info = back_end.retrieve_artworks_info(user)
    if len(artworks_info) == 0:
        st.write("Sorry, we couldn't find any artwork that matches your preferences.")
    else:
        artworks_info = back_end.get_test_items(artworks_info)
        carousel(items=artworks_info, width=1)



def update_info_json(info_json, user_input):
    user_message(info_json['info_name'], user_input)

    info_json['info'] = user_input

    constants.INFO_JSON_LIST[st.session_state.info_index] = info_json
    # increment info_index, update info_json
    st.session_state.info_index += 1
    
    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]

    assistant_message(info_json)
    print('info_index', st.session_state.info_index)
    print('info_name', info_json['info_name'])