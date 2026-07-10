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
st.components.v1.html(
    """
    <script>
    const savedBg = localStorage.getItem("teto_os_bg");
    const currentMode = localStorage.getItem("teto_os_mode") || "normal";
    
    window.parent.postMessage({
        type: "streamlit:setComponentValue",
        value: { bg: savedBg, mode: currentMode }
    }, "*");
    </script>
    """,
    height=0,
)

if "bg_store" not in st.session_state:
    st.session_state.bg_store = {"bg": None, "mode": "normal"}
if "messages" not in st.session_state:
    st.session_state.messages = []

# Вычисляем режим и фон
bg_data = st.session_state.bg_store if st.session_state.bg_store else {"bg": None, "mode": "normal"}
mode = bg_data.get("mode", "normal")
custom_bg_data = bg_data.get("bg", None)

if mode == "deleted":
    bg_style = "background: #0d080a !important;"
elif custom_bg_data:
    bg_style = f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{custom_bg_data}') !important;"
else:
    bg_style = f"background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{DEFAULT_BG}') !important;"

# --- Безопасное внедрение CSS БЕЗ f-строк ---
css_code = """
<style>
.stApp {
    BACKGROUND_PLACEHOLDER
    background-size: cover;
    background-position: center 20%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #ffffff !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stHeader"] * { color: transparent !important; font-size: 0px !important; opacity: 0 !important; }
[data-testid="stMainBlockContainer"] { max-width: 650px !important; margin: auto; padding-top: 60px !important; }
[data-testid="stSidebar"] { background-color: rgba(20, 15, 17, 0.98) !important; border-right: 2px solid rgba(255, 77, 109, 0.3) !important; }
.stExpander { background-color: rgba(15, 10, 12, 0.5) !important; border: 1px solid rgba(255, 77, 109, 0.2) !important; border-radius: 10px !important; margin-bottom: 10px !important; }
.sidebar-box { background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid rgba(255, 180, 200, 0.2) !important; border-radius: 12px !important; padding: 15px !important; margin-bottom: 15px !important; }
.custom-message { background-color: rgba(15, 10, 12, 0.75) !important; border-radius: 14px !important; border: 1px solid rgba(255, 180, 200, 0.15) !important; padding: 16px 20px !important; margin-bottom: 18px !important; backdrop-filter: blur(8px); font-size: 1.05rem; line-height: 1.5; }
.teto-border { border-left: 4px solid #ff4d6d !important; box-shadow: 0 0 15px rgba(255, 77, 109, 0.15), 0 4px 15px rgba(0,0,0,0.5) !important; }
.user-label { color: #ffb3c6 !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; }
.teto-label { color: #ff4d6d !important; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px; text-shadow: 0 0 8px rgba(255, 77, 109, 0.6) !important; }
div[data-testid="stChatInput"] textarea { background-color: rgba(20, 15, 17, 0.95) !important; color: #ffffff !important; border: 1px solid #ff4d6d !important; border-radius: 12px !important; }
</style>
""".replace("BACKGROUND_PLACEHOLDER", bg_style)

st.markdown(css_code, unsafe_allow_html=True)

# --- Боковая панель управления ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🖥️ СТАТУС СИСТЕМЫ")
    st.markdown('<div class="sidebar-box"><p style="margin:0; font-size:0.9rem;"><b>Ядро OS:</b> <span style="color:#00ffcc;">v3.1-FIXED</span></p><p style="margin:5px 0 0 0; font-size:0.9rem;"><b>Память телефона:</b> Подключена</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🖼️ УПРАВЛЕНИЕ ОБОЯМИ")
    custom_bg = st.file_uploader("Загрузить новые обои", type=["png", "jpg", "jpeg"])
    
    if custom_bg:
        bytes_data = custom_bg.getvalue()
        b64_str = base64.b64encode(bytes_data).decode()
        data_url = f"data:image/png;base64,{b64_str}"
        
        st.components.v1.html(f"""
            <script>
            localStorage.setItem("teto_os_bg", "{data_url}");
            localStorage.setItem("teto_os_mode", "normal");
            window.parent.location.reload();
            </script>
        """, height=0)

    if st.button("⏪ Вернуть стандартные обои", use_container_width=True):
        st.components.v1.html("""
            <script>
            localStorage.removeItem("teto_os_bg");
            localStorage.setItem("teto_os_mode", "normal");
            window.parent.location.reload();
            </script>
        """, height=0)
        
    if st.button("🗑️ Полностью удалить фон", use_container_width=True):
        st.components.v1.html("""
            <script>
            localStorage.removeItem("teto_os_bg");
            localStorage.setItem("teto_os_mode", "deleted");
            window.parent.location.reload();
            </script>
        """, height=0)

    if st.button("🧹 Очистить переписку", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🥖 TETO OS — Интерфейс ИИ")

# --- Вывод Истории Сообщений ---
if st.session_state.messages:
    with st.expander("⏳ ПОСМОТРЕТЬ ИСТОРИЮ ПЕРЕПИСКИ", expanded=False):
        for index, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f'**Вы:** {message["content"]}')
            else:
                st.markdown(f'**Тэто:** {message["content"]}')
                if "gen_image" in message:
                    st.image(message["gen_image"])
            st.markdown("---")

SYSTEM_INSTRUCTION = (
    "Ты — Касанэ Тэто (Kasane Teto), ИИ ядра TETO OS. Дерзкая, ироничная вокалоид-химера. "
    "Отвечай с сарказмом. Если просят рисовать, пиши команду: [GENERATE: prompt]. Отвечай на русском."
)

user_input = st.chat_input("Напиши Тэто...")
if user_input:
    st.markdown(f'<div class="custom-message"><div class="user-label">Оператор:</div>{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        groq_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        for msg in st.session_state.messages[-5:]:
            groq_history.append({"role": msg["role"], "content": msg["content"]})
            
        with st.spinner("Синхронизация ядер..."):
            completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=groq_history, temperature=0.7)
            reply_text = completion.choices[0].message.content
            
            gen_image_url = None
            if "[GENERATE:" in reply_text:
                start = reply_text.find("[GENERATE:") + len("[GENERATE:")
                end = reply_text.find("]", start)
                prompt = reply_text[start:end].strip()
                reply_text = reply_text.replace(f"[GENERATE:{reply_text[start:end]}]", "🎨 Магический холст Тэто готов:")
                encoded_prompt = urllib.parse.quote(prompt)
                gen_image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=600&height=400&nologo=true&seed={random.randint(1,10000)}"

            encoded_text = urllib.parse.quote(reply_text[:150])
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=ru&client=tw-ob&q={encoded_text}"

        st.markdown(f'<div class="custom-message teto-border"><div class="teto-label">Тэто ядра OS:</div>{reply_text}</div>', unsafe_allow_html=True)
        if gen_image_url: st.image(gen_image_url)
        if audio_url: st.audio(audio_url, format="audio/mp3")
            
        history_entry = {"role": "assistant", "content": reply_text, "audio_url": audio_url}
        if gen_image_url: history_entry["gen_image"] = gen_image_url
        st.session_state.messages.append(history_entry)
        
    except Exception as e:
        st.error(f"Сбой системы: {e}")
