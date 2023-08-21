## External Modules
import streamlit as st
import time
## Project Modules
import constants
import front_end

st.title("Your AI Art Advisor")


if "messages" not in st.session_state:
    front_end.start_chat()

## DISPLAYING CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## CHAT FLOWING

input_placeholder = st.empty()

if st.session_state.chat_active:

    info_name = constants.INFO_JSON[st.session_state.info_index]["info_name"]

    st.info(f"info_name: {info_name}")
    st.info(f"info_index: {st.session_state.info_index}")

    ## MULTISELECT QUESTIONS
    if info_name == "goals":
        # hide chat_input
        input_placeholder.empty()
        if user_input := st.multiselect("", constants.GOALS_OPTIONS):
            user_input = str(user_input)
            user_info_ = {"info_name": info_name, "content": user_input}
            st.session_state.user.change_attribute(info_name, user_input)
            user_message = {"role": "user", "content": user_input, "info_name": info_name}
            st.session_state.messages.append(user_message)

            front_end.user_message(info_name, user_input)
            st.info(f"info: {user_input}")
            
            st.session_state.info_index += 1
            question = constants.INFO_JSON[st.session_state.info_index]["question"]
            front_end.assistant_message(question, info_name)

    ## TEXT QUESTIONS
    else:
        if user_input := input_placeholder.chat_input("Type here ..."):
            if info_name == "greeting":
                pass
            if info_name == "budget":
                user_input = float(user_input)
            if info_name == "topics":
                user_input = "['Moderno', 'Contemporâneo']"
            
            front_end.user_message(info_name, user_input)
            st.info(f"info: {user_input}")
            
            st.session_state.info_index += 1
            question = constants.INFO_JSON[st.session_state.info_index]["question"]
            front_end.assistant_message(question, info_name)


## WHEN FINISHED
if st.session_state.info_index >= len(constants.INFO_JSON)-1:
    front_end.finish_chat()
