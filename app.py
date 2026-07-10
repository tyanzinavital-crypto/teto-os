import streamlit as st
from groq import Groq
import random
from datetime import date
import urllib.parse
import os

# --- Безопасное подключение ключа (Скрытый код) ---
# Если запускаешь локально, берется обычная строка. На хостинге ключ возьмется из Secrets.
if "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]
else:
    API_KEY = "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"

client = Groq(api_key=API_KEY)

st.set_page_config(page_title="TETO OS — Core v2.6", page_icon="🥖", layout="centered")

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
    [data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stHeader"] * {{ color: transparent !important; font-size: 0px !important; opacity: 0 !important; }}
    [data-testid="stMainBlockContainer"] {{ max-width: 650px !important; margin: auto; padding-top: 60px !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(20, 15, 17, 0.98) !important; border-right: 2px solid rgba(255, 77, 109, 0.3) !important; }}
    
    .sidebar-box {{ background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid rgba(255, 180, 200, 0.2) !important; border-radius: 12px !important; padding: 15px !important; margin-bottom: 15px !important; }}
    .custom-message {{ background-color: rgba(15, 10, 12, 0.75) !important; border-radius: 14px !important; border: 1px solid rgba(255, 180, 200, 0.15) !important; padding: 16px 20px !important; margin-bottom: 18px !important; backdrop-filter: blur(8px); font-size: 1.05rem; line-height: 1.5; }}
    .teto-border {{ border-left: 4px solid #ff4d6d !important; box-shadow: 0 0 15px rgba(255, 77, 109, 0.15), 0 4px 15px rgba(0,0,0,0.5) !important; }}
    .user-label {{ color: #ffb3c6 !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; }}
    .teto-label {{ color: #ff4d6d !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; }}
    
    div[data-testid="stChatInput"] textarea {{ background-color: rgba(20, 15, 17, 0.95) !important; color: #ffffff !important; border: 1px solid #ff4d6d !important; border-radius: 12px !important; }}
    /* Кастомизация блоков загрузки */
    .stFileUploader {{ background: rgba(0,0,0,0.4); padding: 10px; border-radius: 10px; border: 1px dashed rgba(255,77,109,0.3); margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- База знаний ---
WORDS_DATABASE = [
    {"word": "Сингулярность", "desc": "Это когда технологии становятся такими умными, что ИИ начинает сам писать мемы, а люди просто пытаются понять, где смеяться."},
    {"word": "Дедлайн", "desc": "Мифическое существо. Все о нем говорят, но вспоминают только за два часа до его прихода. Прямо как ты перед экзаменами."},
    {"word": "Прокрастинация", "desc": "Искусство придумывать 150 очень важных причин, почему помыть пол важнее, чем заняться делом."}
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
            <p style="margin:5px 0 0 0; font-size:0.9rem;"><b>Модель:</b> Llama 3.3 (Groq)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 МУЛЬТИМЕДИА СКАНЕР")
    # Добавляем функции поиска/анализа по фото и звуку
    uploaded_image = st.file_uploader("📸 Загрузить фото для Тэто", type=["png", "jpg", "jpeg"])
    uploaded_audio = st.file_uploader("🎵 Загрузить голосовой файл", type=["mp3", "wav", "ogg"])
    
    if st.button("🧹 Сбросить память ядра", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🥖 TETO OS — Интерфейс ИИ")

SYSTEM_INSTRUCTION = (
    "Ты — Касанэ Тэто (Kasane Teto), харизматичная, ироничная и дерзкая 31-летняя вокалоид-химера. "
    "Сейчас ты — продвинутый ИИ ядра TETO OS. Отвечай естественно, как умный, но слегка капризный человек. "
    "У тебя отличное чувство юмора: подкалывай оператора, шути, используй сарказм. "
    "Если пользователь загрузил фото или аудио (тебе передадут это текстом), прокомментируй это с сарказмом и экспертным видом. "
    "Отвечай строго на русском языке, не используй аниме-клише."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение чата
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="custom-message"><div class="user-label">Оператор:</div>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="custom-message teto-border"><div class="teto-label">Тэто ядра OS:</div>{message["content"]}</div>', unsafe_allow_html=True)
        if "audio_url" in message:
            st.audio(message["audio_url"], format="audio/mp3")

# Обработка загрузки файлов
triggered_input = None
if uploaded_image:
    triggered_input = f"[Оператор загрузил изображение: {uploaded_image.name}. Тэто, проанализируй и оцени его!]"
elif uploaded_audio:
    triggered_input = f"[Оператор отправил аудиосообщение: {uploaded_audio.name}. Прослушай и прокомментируй звук!]"

user_input = st.chat_input("Введи команду или сообщение...")
if triggered_input or user_input:
    final_input = triggered_input if triggered_input else user_input
    
    st.markdown(f'<div class="custom-message"><div class="user-label">Оператор:</div>{final_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": final_input})

    try:
        groq_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        for msg in st.session_state.messages[:-1]:
            groq_history.append({"role": msg["role"], "content": msg["content"]})
        groq_history.append({"role": "user", "content": final_input})
            
        with st.spinner("Анализ данных в ядре Тэто..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_history,
                temperature=0.8
            )
            reply_text = completion.choices[0].message.content
            
            # Починенный и более стабильный генератор голоса (Google TTS альтернативный прокси)
            encoded_text = urllib.parse.quote(reply_text[:200]) # Ограничение длины для стабильности
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ru&client=tw-ob&q={encoded_text}"

        st.markdown(f'<div class="custom-message teto-border"><div class="teto-label">Тэто ядра OS:</div>{reply_text}</div>', unsafe_allow_html=True)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            
        st.session_state.messages.append({"role": "assistant", "content": reply_text, "audio_url": audio_url})
        
    except Exception as e:
        st.error(f"Сбой системной шины: {e}")
