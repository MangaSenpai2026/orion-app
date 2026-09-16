import streamlit as st
import google.generativeai as genai

st.title("🤖 O.R.I.O.N. System")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Brak klucza GEMINI_API_KEY w Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Wpisz polecenie dla O.R.I.O.N.-a...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
