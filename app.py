import streamlit as st
from groq import Groq

# Прямой рабочий API-ключ
API_KEY = "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"

client = Groq(api_key=API_KEY)

# Скрываем всё лишнее (заголовок, меню, футер) для минимализма
st.set_page_config(page_title="TETO", page_icon="🥖", layout="centered")

st.markdown("""
    <style>
    /* Убираем стандартные элементы интерфейса Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
    .stApp {background-color: #0d080a !important;}
    
    /* Минималистичный стиль чата */
    .stChatMessage {background: transparent !important; border: none !important;}
    [data-testid="stChatInput"] {background: transparent !important;}
    
    /* Текст сообщений */
    .stChatMessageContent {color: #e0e0e0 !important; font-size: 1.1rem; line-height: 1.6;}
    </style>
""", unsafe_allow_html=True)

# Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Система активна. Жду ввода."}]

# Отображение истории
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🥖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Промпт для характера Тэто
SYSTEM_PROMPT = "Ты — Касанэ Тэто. Отвечай кратко, саркастично, без лишних слов. Русский язык. Без эмодзи."

# Обработка ввода пользователя
if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🥖"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
