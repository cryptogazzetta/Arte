## External Modules
import streamlit as st
import time
## Project Modules
import constants
import front_end

# change font
st.markdown(
    """
    <style>
    title {
        font-family: 'Playfair Display';
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Marte Art Advisory")


## INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    print('starting...')
    st.session_state.iteration_count = 0
    front_end.start_chat()
    st.session_state.messages.append({"role": "assistant", "content": "Oi! Estou aqui para te ajudar a encontrar o que você ama no mercado de arte. Vamos começar?", "info_name": "greeting"})


## DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


## CHAT FLOW
user_input = st.session_state.chat_input_container.chat_input("Type here ...")
if user_input:
    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]
    # Handle user input
    info_json['info'] = user_input
    front_end.user_message(info_json['info_name'], user_input)
    # Advance to next info_json, display assistant message
    st.session_state.info_index += 1
    info_json = constants.INFO_JSON_LIST[st.session_state.info_index]
    front_end.assistant_message(info_json)

## WHEN FINISHED
if st.session_state.info_index >= len(constants.INFO_JSON_LIST) - 1:
    front_end.finish_chat()
