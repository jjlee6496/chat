import os
import openai
import streamlit as st
from io import StringIO
import random
import time
from dotenv import load_dotenv

def split_text_file(text, chunk_size):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def chat(chunks):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("무엇이든 물어보세요."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Choose a random chunk as assistant response
        assistant_response = random.choice(chunks)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


class ChatGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def get_response(self, user_input):
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message["content"]
        return None
    

def main():
    load_dotenv()
    OPENAI_KEY = os.environ.get('OPENAI_KEY')
    if OPENAI_KEY:
        chatbot = ChatGPT(api_key=OPENAI_KEY)
    else:
        openai_key = st.text_input('OPEN_AI_API_KEY', type="password")
        chatbot = ChatGPT(api_key=openai_key)
    
    st.title("ChatGPT-like Interface")

    uploaded_file = st.file_uploader("Choose a file")
    spinner_flag = 0
    
    if uploaded_file is not None:
        # # To read file as bytes:
        # bytes_data = uploaded_file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()
        with st.spinner('데이터 처리중...'):
             # Split uploaded file content into chunks of 50 characters
            chunks = split_text_file(string_data, 50)

        chat(chunks)

if __name__ == "__main__":
    main()