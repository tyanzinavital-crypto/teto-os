import streamlit as st
from groq import Groq
import base64

# Прямой рабочий API-ключ
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Настройка страницы
st.set_page_config(page_title="TETO OS — Core v3.2", page_icon="🥖", layout="wide")

# Инициализация состояния
if "bg_image" not in st.session_state:
    st.session_state.bg_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop"

if "teto_avatar" not in st.session_state:
    st.session_state.teto_avatar = "🥖"

if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "👤"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Боковая панель со всеми настройками (возвращаем и панельку обоев, и новые функции)
with st.sidebar:
    st.markdown("### 🖥️ СТАТУС СИСТЕМЫ")
    st.info("**Ядро OS:** v3.2-FULL\n\n**Мультискан:** Готов")
    
    st.markdown("---")
    st.markdown("### 📧 РЕГИСТРАЦИЯ GMAIL")
    if not st.session_state.user_email:
        email_input = st.text_input("Введите Gmail:")
        if st.button("Зарегистрироваться"):
            if email_input.endswith("@gmail.com"):
                st.session_state.user_email = email_input
                st.success("Успешно авторизован!")
                st.rerun()
            else:
                st.error("Введите корректный Gmail адрес.")
    else:
        st.success(f"Аккаунт: {st.session_state.user_email}")
        if st.button("Выйти"):
            st.session_state.user_email = None
            st.rerun()

    st.markdown("---")
    st.markdown("### 🖼️ НАСТРОЙКА ОБОЕВ")
    bg_choice = st.selectbox("Тема интерфейса:", ["Тёмный киберпанк", "Неон"])
    
    if bg_choice == "Тёмный киберпанк":
        st.session_state.bg_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop"
    elif bg_choice == "Неон":
        st.session_state.bg_image = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1920&auto=format&fit=crop"
    
    uploaded_bg = st.file_uploader("Загрузить свои обои", type=["png", "jpg", "jpeg"], key="bg_up")
    if uploaded_bg is not None:
        b64_encoded = base64.b64encode(uploaded_bg.getvalue()).decode()
        st.session_state.bg_image = f"data:image/jpeg;base64,{b64_encoded}"

    st.markdown("---")
    st.markdown("### 👤 КАСТОМИЗАЦИЯ АВАТАРОК")
    
    teto_av_file = st.file_uploader("Аватар Тэто (картинка)", type=["png", "jpg", "jpeg"], key="teto_av")
    if teto_av_file is not None:
        teto_b64 = base64.b64encode(teto_av_file.getvalue()).decode()
        st.session_state.teto_avatar = f"data:image/jpeg;base64,{teto_b64}"

    user_av_file = st.file_uploader("Ваш аватар (картинка)", type=["png", "jpg", "jpeg"], key="user_av")
    if user_av_file is not None:
        user_b64 = base64.b64encode(user_av_file.getvalue()).decode()
        st.session_state.user_avatar = f"data:image/jpeg;base64,{user_b64}"

    st.markdown("---")
    st.markdown("### 🔍 МУЛЬТИМЕДИА СКАНЕР")
    st.file_uploader("Upload", type=["png", "jpg"], label_visibility="collapsed")
    st.caption("200MB per file • PNG, JPG")

# Динамическая стилизация интерфейса
st.markdown(f"""
    <style>
    #MainMenu, header, footer {{visibility: hidden;}}
    .stApp {{
        background-image: linear-gradient(rgba(13, 8, 10, 0.85), rgba(13, 8, 10, 0.85)), url("{st.session_state.bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stChatMessage {{background: rgba(26, 18, 21, 0.6) !important; border-radius: 10px; border: 1px solid #3d262b !important;}}
    [data-testid="stChatInput"] {{background: rgba(13, 8, 10, 0.8) !important;}}
    .stChatMessageContent {{color: #e0e0e0 !important; font-size: 1.05rem; line-height: 1.5;}}
    img[data-testid="stImage"] {{border-radius: 50%;}}
    </style>
""", unsafe_allow_html=True)

# Основной интерфейс чата
st.markdown("## 🥖 TETO OS — Интерфейс ИИ")

operator_name = st.session_state.user_email if st.session_state.user_email else "КПТ (Гость)"

st.markdown(f"""
    <div style="background-color: rgba(26, 18, 21, 0.8); padding: 12px; border-radius: 8px; border: 1px solid #3d262b; margin-bottom: 20px;">
        <span style="color: #a08085; font-size: 0.85rem; font-weight: bold;">ОПЕРАТОР:</span><br>
        <span style="color: #ffffff; font-size: 1.1rem;">{operator_name}</span>
    </div>
""", unsafe_allow_html=True)

# Инициализация истории
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Система активна. Ожидаю запроса оператора."}]

# Отображение сообщений с кастомными аватарами
for message in st.session_state.messages:
    current_avatar = st.session_state.teto_avatar if message["role"] == "assistant" else st.session_state.user_avatar
    with st.chat_message(message["role"], avatar=current_avatar):
        st.write(message["content"])

# Промпт характера
SYSTEM_PROMPT = "Ты — Касанэ Тэто. Отвечай кратко, саркастично, без лишних слов. Русский язык. Без эмодзи."

# Логика отправки сообщений
if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.write(prompt)

    with st.chat_message("assistant", avatar=st.session_state.teto_avatar):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
