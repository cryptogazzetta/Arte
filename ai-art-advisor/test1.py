import streamlit as st

st.title("Your AI Art Advisor.")


with st.chat_message("assistant"):
    st.write("Hi!")
    st.write("I'm here to help you find art you love.")
    st.write("To start, how should I address you?")


if st.chat_input("Answer your name here ...", key='user_name'):
    with st.chat_message("user"):
        st.write(st.session_state.get('user_name'))

    with st.chat_message("assistant"):
        st.write(f"Nice to meet you, {st.session_state.user_name}!")
        st.write("Now, tell me, what brings you here?")
    
    if st.chat_input("", key='user_goal'):
    # if st.multiselect(
    #     "",
    #     ['Decorate a place',
    #     'Start an art collection',
    #     'Buy a gift for someone'],
    #     key="user_goal"
    # ):

        with st.chat_message("user"):
            st.write(st.session_state.get('user_goal'))

        with st.chat_message("assistant"):
            st.write("Great! I'll help you with", ', '.join(st.session_state.get('user_goal') + "."))
            st.write("What kind of art do you like?")


        # if st.multiselect(
        #     "",
        #     ["Modern",
        #     "Contemporary",
        #     "Street",
        #     "Photography",
        #     "Illustration",
        #     "Abstract"]):
            
        #     time.sleep(2)
        #     st.chat_message("assistant", "How much do you intend to spend on a piece?")

        #     if st.slider("", 10, 10000):
        #         st.chat_message("user", st.session_state['user_budget'])

        #     user_input = st.chat_input("Type 'Exit' to quit").lower()
        #     if user_input == 'exit':
        #         message("Fuck OFF")