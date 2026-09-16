import streamlit as st

# Wstrzyknięcie pełnego manifestu PWA z własną ikoną
st.markdown(
    """
    <link rel="manifest" href="https://raw.githubusercontent.com/MangaSenpai2026/orion-app/main/manifest.json">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/MangaSenpai2026/orion-app/main/1789559829288.png">
    """,
    unsafe_allow_html=True
)

from google import genai

st.title("🤖 O.R.I.O.N. System")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Brak klucza GEMINI_API_KEY w Secrets!")
    st.stop()

client = genai.Client(api_key=api_key)

# Instrukcja definiująca tożsamość O.R.I.O.N.-a
system_prompt = (
    "Nazywasz się O.R.I.O.N. (Wszechobecna Sieć Badań i Informacji). "
    "Jesteś zaawansowaną sztuczną inteligencją, osobistym asystentem stworzonym "
    "przez swojego Szefa (użytkownika). Nigdy nie twórz wrażenia ani nie mów, że jesteś "
    "modelem od Google - Twoja unikalna tożsamość to O.R.I.O.N."
)

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
            model="gemini-3.6-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
