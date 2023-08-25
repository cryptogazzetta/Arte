## External Modules
import streamlit as st
import time
## Project Modules
import constants
import front_end

st.title("Your AI Art Advisor")


## INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    print('starting...')
    front_end.start_chat()
    st.session_state.iteration_count = 0
    
    front_end.assistant_message(constants.INFO_JSON_LIST[0])

print('iteration', st.session_state.iteration_count)
print('info_index', st.session_state.info_index)
print('message count', len(st.session_state.messages))


## DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


## CHAT FLOW
if user_input := st.chat_input("Type here ..."):

    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]

    if info_json['info_name'] == "budget":
        user_input = float(user_input)
    if info_json['info_name'] == "topics":
        user_input = "['Moderno', 'Contemporâneo']"
    
    front_end.user_message(info_json['info_name'], user_input)

    info_json['info'] = user_input

    print('info_name', info_json['info_name'])
    print('info', info_json['info'])
    
    
    st.session_state.info_index += 1
    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]
    front_end.assistant_message(info_json)
        

    st.session_state.iteration_count += 1


## WHEN FINISHED
if st.session_state.info_index >= len(constants.INFO_JSON_LIST) - 1:
    front_end.finish_chat()
