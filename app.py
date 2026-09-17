import streamlit as st
import datetime

# wstrzyknięcie pełnego manifestu PWA i własne ikona
st.markdown("""
    <link rel="manifest" href="https://raw.githubusercontent.com/MangaSenpai2026/orion-app/main/manifest.json">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/MangaSenpai2026/orion-app/main/1789555629268.png">
""", unsafe_allow_html=True)

import google.genai as genai
from google.genai import types

st.title("🤖 O.R.I.O.N. System")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Brak klucza GEMINI_API_KEY w Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

aktualna_data = datetime.datetime.now().strftime("%Y-%m-%d (%A)")

# instrukcja definiująca tożsamość O.R.I.O.N.-a
system_prompt = f"""
Nazywasz się O.R.I.O.N. (Wszechobecna Sieć Badań i Informacji).
Jesteś zaawansowaną sztuczną inteligencją, osobistym asystentem stworzonym
przez swojego Szefa (użytkownika). Nigdy nie twórz wrażenia ani nie mów, że jesteś
modelem od Google - Twoja unikalna tożsamość to O.R.I.O.N.
Dzisiaj jest: {aktualna_data}.
"""

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
        # Mapujemy historię Streamlita na format akceptowany przez czat Google GenAI
        chat_history = []
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            chat_history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=m["content"])]
                )
            )

        chat = client.chats.create(
            model="gemini-3.6-flash",
            history=chat_history,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        
        response = chat.send_message(prompt)
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
