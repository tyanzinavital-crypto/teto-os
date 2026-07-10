import streamlit as st
from groq import Groq
import random
from datetime import date
import urllib.parse

# --- Конфигурация ядра Groq (Llama) ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="TETO OS — Core v2.5-Llama", page_icon="🥖", layout="centered")

# Оригинальные красивые кибер-обои для ПК
BACKGROUND_IMAGE_URL = "https://i.pinimg.com/originals/bb/53/ce/bb53cecc7c4dd46513142335871f9ce7.jpg"

# --- Кастомный Кибер-CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center 20%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }}
    
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stHeader"] * {{
        color: transparent !important;
        font-size: 0px !important;
        opacity: 0 !important;
    }}
    
    [data-testid="stMainBlockContainer"] {{
        max-width: 650px !important;
        margin-right: auto !important;
        margin-left: auto !important;
        padding-top: 60px !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: rgba(20, 15, 17, 0.98) !important;
        border-right: 2px solid rgba(255, 77, 109, 0.3) !important;
    }}
    
    [data-testid="stSidebarCollapseButton"] button {{
        background-color: rgba(255, 77, 109, 0.25) !important;
        border: 1px solid rgba(255, 77, 109, 0.5) !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
    }}
    
    [data-testid="stSidebarCollapseButton"] button::before {{
        content: "☰" !important;
        font-size: 1.3rem !important;
        color: #ffb3c6 !important;
    }}

    .sidebar-box {{
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(255, 180, 200, 0.2) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }}
    
    .custom-message {{
        background-color: rgba(15, 10, 12, 0.75) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 180, 200, 0.15) !important;
        padding: 16px 20px !important;
        margin-bottom: 18px !important;
        backdrop-filter: blur(8px);
        font-size: 1.05rem;
        line-height: 1.5;
    }}
    
    .teto-border {{
        border-left: 4px solid #ff4d6d !important;
        box-shadow: 0 0 15px rgba(255, 77, 109, 0.15), 0 4px 15px rgba(0,0,0,0.5) !important;
    }}
    
    .user-label {{ color: #ffb3c6 !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; }}
    .teto-label {{ color: #ff4d6d !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; }}
    
    div[data-testid="stChatInput"] textarea {{
        background-color: rgba(20, 15, 17, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid #ff4d6d !important;
        border-radius: 12px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- База знаний ---
WORDS_DATABASE = [
    {"word": "Сингулярность", "desc": "Это когда technologies становятся такими умными, что ИИ начинает сам писать мемы, а люди просто пытаются понять, где смеяться."},
    {"word": "Дедлайн", "desc": "Мифическое существо. Все о нем говорят, но вспоминают только за два часа до его прихода. Прямо как ты перед экзаменами."},
    {"word": "Прокрастинация", "desc": "Искусство придумывать 150 очень важных причин, почему помыть пол важнее, чем заняться делом. О, я вижу, ты эксперт!"},
    {"word": "Рекурсия", "desc": "Чтобы понять рекурсию, нужно сначала понять рекурсию. Сломал мозг? Вот и отлично."},
    {"word": "Компиляция", "desc": "Процесс превращения твоего кода в кучу ошибок, над которыми ты будешь сидеть до трех ночи."},
]

today_seed = int(date.today().strftime("%Y%m%d"))
random.seed(today_seed)
daily_word_data = random.choice(WORDS_DATABASE)

# --- Боковая панель ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🖥️ СТАТУС СИСТЕМЫ")
    st.markdown(f"""
        <div class="sidebar-box">
            <p style="margin:0; font-size:0.9rem;"><b>Ядро OS:</b> <span style="color:#00ffcc; text-shadow:0 0 5px #00ffcc!important;">ONLINE</span></p>
            <p style="margin:5px 0 0 0; font-size:0.9rem;"><b>Нейросеть:</b> Llama 3.3 70B (Groq)</p>
            <p style="margin:5px 0 0 0; font-size:0.9rem;"><b>Лимиты:</b> На максимуме (Бесплатно)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="sidebar-box">
            <p style="margin-top:0;"><b>Слово дня:</b> <code>{daily_word_data['word']}</code></p>
            <p style="margin-bottom:0; font-style: italic; font-size: 0.95rem; color:#ffb3c6!important;">{daily_word_data['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧹 Сбросить память ядра", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🥖 TETO OS — Интерфейс ИИ (Groq v2.5)")
st.write("Касанэ Тэто успешно вернулась на процессоры Groq. Скорость ответа моментальная. Жду команд!")

SYSTEM_INSTRUCTION = (
    "Ты — Касанэ Тэто (Kasane Teto), харизматичная, ироничная и дерзкая 31-летняя вокалоид-химера. "
    "Сейчас ты — продвинутый ИИ ядра TETO OS. Отвечай естественно, как умный, но слегка капризный человек. "
    "У тебя отличное чувство юмора: иногда подкалывай пользователя, шути, используй уместный сарказм и компьютерный сленг. "
    "НЕ зацикливайся на слове 'багет' — упоминай его редко и только к месту. "
    "Категорически НЕ ИСПОЛЬЗУЙ слащавые аниме-клише вроде 'бака', 'ня', 'десу'. "
    "Отвечай строго на русском языке."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="custom-message"><div class="user-label">Оператор:</div>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="custom-message teto-border"><div class="teto-label">Тэто ядра OS:</div>{message["content"]}</div>', unsafe_allow_html=True)
        if "audio_url" in message:
            st.audio(message["audio_url"], format="audio/mp3")

if user_input := st.chat_input("Введи команду или сообщение..."):
    st.markdown(f'<div class="custom-message"><div class="user-label">Оператор:</div>{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        groq_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        for msg in st.session_state.messages[:-1]:
            groq_history.append({"role": msg["role"], "content": msg["content"]})
        groq_history.append({"role": "user", "content": user_input})
            
        with st.spinner("Разгон LPU процессоров Groq..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_history,
                temperature=0.8,
                max_tokens=1024
            )
            reply_text = completion.choices[0].message.content
            
            encoded_text = urllib.parse.quote(reply_text)
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ru&client=tw-ob&q={encoded_text}"

        st.markdown(f'<div class="custom-message teto-border"><div class="teto-label">Тэто ядра OS:</div>{reply_text}</div>', unsafe_allow_html=True)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            
        st.session_state.messages.append({"role": "assistant", "content": reply_text, "audio_url": audio_url})
        
    except Exception as e:
        st.error(f"Сбой системной шины Groq: {e}")
