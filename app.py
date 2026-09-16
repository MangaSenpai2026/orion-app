import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# Konfiguracja interfejsu
st.set_page_config(page_title="O.R.I.O.N.", page_icon="🤖")
st.title("🤖 O.R.I.O.N. System")

# Odczytanie klucza API z konfiguracji
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Brak klucza GEMINI_API_KEY w Secrets!")
    st.stop()

# Inicjalizacja połączenia i Google Search Grounding
client = genai.Client(api_key=api_key)
google_search_tool = types.Tool(google_search=types.GoogleSearch())

system_prompt = """
Nazywasz się O.R.I.O.N. (Omnipresent Research & Information Network).
Jesteś zaawansowaną sztuczną inteligencją i osobistym asystentem operacyjnym.
Odpowiadasz w sposób profesjonalny, uprzejmy, zwięzły i rzeczowy.
Masz pełny dostęp do sieci w czasie rzeczywistym – korzystaj z wyszukiwarki Google, aby podawać aktualne dane.
"""

# Historia konwersacji
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie czatu
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Pole wprowadzania zapytań
user_input = st.chat_input("Wpisz polecenie dla O.R.I.O.N.-a...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        # Generowanie odpowiedzi ze sprawdzaniem w internecie
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[google_search_tool],
            ),
        )
        
        reply_text = response.text
        st.write(reply_text)
        st.session_state.messages.append({"role": "assistant", "content": reply_text})

        # Skrypt do czytania odpowiedzi na głos (TTS)
        clean_text = reply_text.replace("'", "\\'").replace("\n", " ")
        tts_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.lang = 'pl-PL';
            msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
        </script>
        """
        components.html(tts_code, height=0)
