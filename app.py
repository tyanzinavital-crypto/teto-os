import streamlit as st
from groq import Groq
import random
from datetime import date
import urllib.parse
import base64

# --- Безопасное подключение ключа (Скрытый код) ---
if "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]
else:
    API_KEY = "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"

client = Groq(api_key=API_KEY)

st.set_page_config(page_title="TETO OS — Core v3.1", page_icon="🥖", layout="centered")

# Начальные дефолтные кибер-обои
DEFAULT_BG = "https://i.pinimg.com/originals/bb/53/ce/bb53cecc7c4dd46513142335871f9ce7.jpg"

# --- ХАК ДЛЯ ПАМЯТИ ОБЛИКА (JavaScript LocalStorage) ---
# Этот скрипт проверяет, сохранены ли обои в памяти телефона, и передает их в Streamlit
st.components.v1.html(
    """
    <script>
    const savedBg = localStorage.getItem("teto_os_bg");
    const currentMode = localStorage.getItem("teto_os_mode") || "normal";
    
    // Передаем данные из памяти телефона обратно в Python-код Streamlit
    window.parent.postMessage({
        type: "streamlit:setComponentValue",
        value: { bg: savedBg, mode: currentMode }
    }, "*");
    </script>
    """,
    height=0,
)

# Инициализация переменных памяти в сессии
if "bg_store" not in st.session_state:
    st.session_state.bg_store = {"bg": None, "mode": "normal"}
if "messages" not in st.session_state:
    st.session_state.messages = []

# Хак для чтения данных из JavaScript компонента
if st.session_state.get("bg_store") is None:
    st.session_state.bg_store = {"bg": None, "mode": "normal"}

# --- Вычисляем, какой фон показать прямо сейчас ---
mode = st.session_state.bg_store.get("mode", "normal")
custom_bg_data = st.session_state.bg_store.get("bg", None)

if mode == "deleted":
    # Если пользователь полностью удалил обои — ставим глубокий темный кибер-цвет
    bg_style = "background: #0d080a;"
elif custom_bg_data:
    # Если есть кастомные сохраненные обои
    bg_style = f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{custom_bg_data}');"
else:
    # Иначе — наш стандартный красивый фон
    bg_style = f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{DEFAULT_BG}');"

# --- Наш фирменный кастомный CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        {bg_style}
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
    .stExpander {{ background-color: rgba(15, 10, 12, 0.5) !important; border: 1px solid rgba(255, 77, 109, 0.2) !important; border-radius: 10px !important; margin-bottom: 10px !important; }}
    .sidebar-box {{ background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid rgba(255, 180, 200, 0.2) !important; border-radius: 12px !important; padding: 15px !important; margin-bottom: 15px !important; }}
    .custom-message {{ background-color: rgba(15, 10, 12, 0.75) !important; border-radius: 14px !important; border: 1px solid rgba(255, 180, 200, 0.15) !important; padding: 16px 20px !important; margin-bottom: 18px !important; backdrop-filter: blur(8px); font-size: 1.05rem; line-height: 1.5; }}
    .teto-border {{ border-left: 4px solid #ff4d6d !important; box-shadow: 0 0 15px rgba(
