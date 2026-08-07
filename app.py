import streamlit as st
from groq import Groq

# Прямой рабочий API-ключ
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Настройка страницы
st.set_page_config(page_title="TETO OS — Core v3.2", page_icon="🥖", layout="wide")

# Инициализация состояния обоев
if "bg_image" not in st.session_state:
    st.session_state.bg_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop" # дефолтный темный фон

# Боковая панель (Статус системы и Настройки обоев)
with st.sidebar:
    st.markdown("### 🖥️ СТАТУС СИСТЕМЫ")
    st.info("**Ядро OS:** v3.2-FULL\n\n**Мультискан:** Готов")
    
    st.markdown("---")
    st.markdown("### 🖼️ НАСТРОЙКА ОБОЕВ")
    
    bg_choice = st.selectbox("Выбрать тему:", ["Тёмный киберпанк", "Неон", "Свой вариант (ссылка/файл)"])
    
    if bg_choice == "Тёмный киберпанк":
        st.session_state.bg_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop"
    elif bg_choice == "Неон":
        st.session_state.bg_image = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1920&auto=format&fit=crop"
    
    uploaded_bg = st.file_uploader("Загрузить свои обои", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_bg is not None:
        # Сохранение загруженной картинки в виде data-url
        import base64
        bytes_data = uploaded_bg.getvalue()
        b64_encoded = base64.b64encode(bytes_data).decode()
        st.session_state.bg_image = f"data:image/jpeg;base64,{b64_encoded}"

    st.markdown("---")
    st.markdown("### 🔍 МУЛЬТИМЕДИА СКАНЕР")
    st.markdown("**📸 Загрузить фото для Тэто**")
    st.file_uploader("Upload", type=["png", "jpg"], label_visibility="collapsed")
    st.caption("200MB per file • PNG, JPG")

# Динамическая стилизация с учетом выбранных обоев
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
    </style>
""", unsafe_allow_html=True)

# Основной интерфейс чата
st.markdown("## 🥖 TETO OS — Интерфейс ИИ")

with st.container():
    st.markdown("""
        <div style="background-color: rgba(26, 18, 21, 0.8); padding: 12px; border-radius: 8px; border: 1px solid #3d262b; margin-bottom: 20px;">
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
