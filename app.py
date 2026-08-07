import streamlit as st
from groq import Groq

# Прямой рабочий API-ключ
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Настройка страницы
st.set_page_config(page_title="TETO OS — Core v3.2", page_icon="🥖", layout="wide")

# Стилизация под тёмный киберпанк/минимализм
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp {background-color: #0d080a !important;}
    .stChatMessage {background: transparent !important; border: none !important;}
    [data-testid="stChatInput"] {background: transparent !important;}
    .stChatMessageContent {color: #e0e0e0 !important; font-size: 1.05rem; line-height: 1.5;}
    </style>
""", unsafe_allow_html=True)

# Боковая панель (Статус системы)
with st.sidebar:
    st.markdown("### 🖥️ СТАТУС СИСТЕМЫ")
    st.info("**Ядро OS:** v3.2-FULL\n\n**Мультискан:** Готов")
    
    st.markdown("---")
    st.markdown("### 🔍 МУЛЬТИМЕДИА СКАНЕР")
    
    with st.container():
        st.markdown("**📸 Загрузить фото для Тэто**")
        st.file_uploader("Upload", type=["png", "jpg"], label_visibility="collapsed")
        st.caption("200MB per file • PNG, JPG")
    
    st.markdown("---")
    with st.container():
        st.markdown("**🎵 Загрузить голосовой файл**")
        st.file_uploader("Upload_audio", type=["mp3", "wav"], label_visibility="collapsed")

# Основной интерфейс чата
st.markdown("## 🥖 TETO OS — Интерфейс ИИ")

with st.container():
    st.markdown("""
        <div style="background-color: #1a1215; padding: 12px; border-radius: 8px; border: 1px solid #3d262b; margin-bottom: 20px;">
            <span style="color: #a08085; font-size: 0.85rem; font-weight: bold;">ОПЕРАТОР:</span><br>
            <span style="color: #ffffff; font-size: 1.1rem;">КПТ</span>
        </div>
    """, unsafe_allow_html=True)

# Инициализация истории
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Система активна. Ожидаю запроса оператора."}]

# Отображение сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🥖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Промпт характера
SYSTEM_PROMPT = "Ты — Касанэ Тэто. Отвечай кратко, саркастично, без лишних слов. Русский язык. Без эмодзи."

# Логика отправки сообщений
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
