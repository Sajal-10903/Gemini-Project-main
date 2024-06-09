from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("Your Gemini Api code"))  # Your API key here

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini LLM Chat")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Your message:", key="input")
submit = st.button("Send")
clear = st.button("Clear Chat History")

if clear:
    st.session_state['chat_history'] = []
    chat = model.start_chat(history=[])  # Reset chat history on the model as well

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))

    st.subheader("Gemini's Response:")
    response_text = ""
    for chunk in response:
        response_text += chunk.text
        st.markdown(response_text)  # Display in markdown for better formatting
    st.session_state['chat_history'].append(("Gemini", response_text))

st.subheader("Chat History:")
for i, (role, text) in enumerate(st.session_state['chat_history']):
    if role == "You":
        st.write(f"**You:** {text}")
    else:
        st.write(f"**Gemini:** {text}")
