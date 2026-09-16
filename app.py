import streamlit as st
from google import genai

st.title("🤖 O.R.I.O.N. System")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Brak klucza GEMINI_API_KEY w Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        
