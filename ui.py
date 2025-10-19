import os

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

st.title("Fashion Chatbot")


def get_api_key_input():
    """Ask user to input their Google API key."""
    # Initializes API key in session state
    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

    # Does not display input box if API key is already set
    if st.session_state["GOOGLE_API_KEY"]:
        return

    st.write("Enter your Google API Key")

    # API key input and submit button
    col1, col2 = st.columns((80, 20))
    with col1:
        api_key = st.text_input("", label_visibility="collapsed", type="password")

    with col2:
        is_submit_pressed = st.button("Submit")
        if is_submit_pressed:
            st.session_state["GOOGLE_API_KEY"] = api_key

    # Set key as env variable to be accessed by langchain
    os.environ["GOOGLE_API_KEY"] = st.session_state["GOOGLE_API_KEY"]

    # Does not display before an API key is inserted
    if not st.session_state["GOOGLE_API_KEY"]:
        st.stop()
    st.rerun()


def load_llm():
    """Get LLM from LangChain."""
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return st.session_state["llm"]


def get_chat_history():
    """Get chat history."""
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]


def display_chat_message(message):
    """Display a single message in the chat column."""
    if type(message) is HumanMessage:
        role = "User"
    elif type(message) is AIMessage:
        role = "AI"
    else:
        role = "Unknown"
    with st.chat_message(role):
        st.markdown(message.content)


def display_chat_history(chat_history):
    """Display all chat history when this is in the chat."""
    for chat in chat_history:
        display_chat_message(chat)


def user_query_to_llm(llm, chat_history):
    """Asks for input query from user, and sends request to LLM."""
    prompt = st.chat_input("Chat with AI")
    if not prompt:
        st.stop()
    chat_history.append(HumanMessage(content=prompt))
    display_chat_message(chat_history[-1])

    response = llm.invoke(chat_history)
    chat_history.append(response)
    display_chat_message(chat_history[-1])


def main():
    """Main program."""
    get_api_key_input()
    llm = load_llm()
    chat_history = get_chat_history()
    display_chat_history(chat_history)
    user_query_to_llm(llm, chat_history)


# Jalankan bagian utama.
main()
