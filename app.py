import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="KrishiBondhu AI",
    page_icon="🌾",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f4fff6,#eefaf1 55%,#ffffff);
}
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

/* ---------- Text color (dark) ---------- */
.stApp p, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"] {
    color: #1f2d24;
}

/* ---------- Hero ---------- */
.hero {
    padding: 30px;
    border-radius: 26px;
    background: linear-gradient(135deg,#126b3a,#2e9856);
    box-shadow: 0 15px 40px rgba(18,107,58,.18);
    margin-bottom: 25px;
}
.hero, .hero h1, .hero p {
    color: white !important;
}
.hero h1 {font-size:42px; margin:0;}
.hero p {font-size:16px; opacity:.9; margin-top:8px;}

/* ---------- Chat message card ---------- */
[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid #dce9df;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 6px 20px rgba(0,0,0,.05);
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] span {
    color: #1f2d24 !important;
}
[data-testid="stChatMessage"] [data-testid="stCaptionContainer"] * {
    color: #6c7a72 !important;
}

/* ---------- Text area ---------- */
.stTextArea textarea {
    background: #ffffff;
    color: #1f2d24;
    border: 1px solid #dce9df;
    border-radius: 16px;
}
.stTextArea textarea::placeholder {
    color: #8a9a90;
}

/* ---------- Preview / small text ---------- */
.preview {
    background: #f2f8f3;
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 10px;
}
.preview, .preview b {
    color: #1f2d24 !important;
}
.small {
    color: #6c7a72 !important;
    font-size: 13px;
}

/* ---------- Buttons (quick prompt = shada, Send = shobuj) ---------- */
div.stButton > button {
    background: #ffffff;
    color: #1f2d24;
    border: 1.5px solid #cfe5d6;
    border-radius: 14px;
}
div.stButton > button:hover {
    border-color: #249653;
    color: #249653;
}
div.stButton > button[kind="primary"] {
    background: #249653;
    color: #ffffff;
    border: none;
}
div.stButton > button[kind="primary"]:hover {
    background: #1b7a42;
    color: #ffffff;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 1.5px dashed #9fcfb0 !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #1f2d24 !important;
}
[data-testid="stFileUploader"] button {
    background: #249653 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] button * {
    color: #ffffff !important;
}
[data-testid="stFileUploader"] svg {
    fill: #249653 !important;
}

/* ---------- Audio input (voice) ---------- */
[data-testid="stAudioInput"],
[data-testid="stAudioInput"] > div,
[data-testid="stAudioInput"] > div > div {
    background: #ffffff !important;
    border-radius: 16px !important;
}
[data-testid="stAudioInput"] {
    border: 1.5px solid #9fcfb0 !important;
    padding: 4px !important;
}
[data-testid="stAudioInput"],
[data-testid="stAudioInput"] *,
[data-testid="stAudioInputWaveformTimeCode"] {
    color: #249653 !important;
}
[data-testid="stAudioInput"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #249653 !important;
}
[data-testid="stAudioInput"] button:hover {
    background: #eefaf1 !important;
}
[data-testid="stAudioInput"] svg {
    color: #249653 !important;
    fill: currentColor !important;
    opacity: 1 !important;
    visibility: visible !important;
}
[data-testid="stAudioInput"] svg path {
    fill: currentColor !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- API ----------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY set kora nei. Environment variable e key din.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are KrishiBondhu AI, a Bangladesh-focused agriculture assistant.

Understand Bangla, Banglish and English.
The farmer may provide text, an image, audio, or any combination of them.

Answer mainly in simple Bangla.

For crop images:
- describe visible symptoms first
- give possible causes, not guaranteed diagnosis
- suggest practical next steps
- mention what extra information would help

For fertilizer/pesticide advice:
- do not invent exact doses
- recommend following the product label and local agriculture officer guidance
- never encourage unsafe chemical handling

Use short headings and bullet points.
If information is insufficient, ask a useful follow-up question.
"""

DISCLAIMER = (
    "⚠️ AI-এর পরামর্শ সহায়ক মাত্র। নিশ্চিত রোগ নির্ণয় বা রাসায়নিক ব্যবহারের "
    "জন্য স্থানীয় কৃষি কর্মকর্তা/বিশেষজ্ঞের পরামর্শ নিন।"
)

# True korle quick prompt-e click korlei shathe shathe Send hoye jabe
AUTO_SEND = False

# ---------------- Session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Header ----------------
st.markdown("""
<div class="hero">
    <h1>🌾 KrishiBondhu AI</h1>
    <p>কৃষকের কথা শুনবে • ছবি দেখবে • সমস্যার সমাধানে সাহায্য করবে</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Chat area (INPUT-er UPORE) ----------------
chat_area = st.container()


def render_message(m):
    avatar = "🧑‍🌾" if m["role"] == "user" else "🌾"
    with st.chat_message(m["role"], avatar=avatar):
        if m.get("text"):
            st.markdown(m["text"])
        if m.get("image"):
            st.image(m["image"], width=260)
        if m.get("has_audio"):
            st.caption("🎙️ Voice message")
        if m["role"] == "assistant":
            st.caption(DISCLAIMER)


with chat_area:
    for m in st.session_state.messages:
        render_message(m)

# ---------------- Quick prompts ----------------
st.divider()
st.caption("💡 দ্রুত প্রশ্ন বেছে নিন (ক্লিক করুন)")

QUICK_PROMPTS = [
    ("🌾 ধানের পাতায় বাদামী দাগ", "আমার ধানের পাতায় বাদামী দাগ হয়েছে, কী করব?"),
    ("🍅 টমেটোর পাতা শুকাচ্ছে", "আমার টমেটো গাছের পাতা শুকিয়ে যাচ্ছে, কী করব?"),
    ("🥔 আলুর পাতায় কালো দাগ", "আমার আলুর পাতায় কালো দাগ পড়েছে, কী করব?"),
]


def set_prompt(prompt_text):
    st.session_state["msg_text"] = prompt_text
    if AUTO_SEND:
        st.session_state["auto_send"] = True


q1, q2, q3 = st.columns(3)
for col, (label, full_text) in zip((q1, q2, q3), QUICK_PROMPTS):
    with col:
        st.button(
            label,
            key=f"qp_{label}",
            on_click=set_prompt,
            args=(full_text,),
            use_container_width=True
        )

st.markdown(
    '<p class="small">একই message-এ text + image + voice একসাথে পাঠাতে পারবেন।</p>',
    unsafe_allow_html=True
)

# ---------------- Composer (NICHE) ----------------
text = st.text_area(
    "Message",
    key="msg_text",
    placeholder="আপনার সমস্যাটি লিখুন... যেমন: আমার ধানের পাতায় বাদামী দাগ হয়েছে, কী করব?",
    height=120,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    image = st.file_uploader(
        "📎",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        help="ছবি attach করুন"
    )
with col2:
    audio = st.audio_input("🎙️", label_visibility="collapsed")
with col3:
    ask = st.button(
        "➤  Send to KrishiBondhu",
        type="primary",
        use_container_width=True
    )

if image:
    st.markdown(
        f'<div class="preview">📷 Image attached: <b>{image.name}</b></div>',
        unsafe_allow_html=True
    )
if audio:
    st.markdown(
        '<div class="preview">🎙️ Voice message attached ✓</div>',
        unsafe_allow_html=True
    )

# ---------------- Send ----------------
auto = st.session_state.pop("auto_send", False)

if ask or auto:
    if not text.strip() and not image and not audio:
        st.warning("Message লিখুন, অথবা 📎 ছবি / 🎙️ voice attach করুন।")
        st.stop()

    image_bytes = image.getvalue() if image else None
    audio_bytes = audio.getvalue() if audio else None

    # 1) user message save + upore dekhao
    user_msg = {
        "role": "user",
        "text": text.strip(),
        "image": image_bytes,
        "has_audio": bool(audio_bytes),
    }
    st.session_state.messages.append(user_msg)
    with chat_area:
        render_message(user_msg)

    # 2) Gemini request banao (ager text conversation context hishebe jabe)
    contents = []
    for m in st.session_state.messages[:-1]:
        if m.get("text"):
            contents.append(types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["text"])]
            ))

    parts = [types.Part.from_text(text=f"""
User text:
{text.strip() or "No text provided."}

Analyze ALL available inputs together.
""")]
    if image_bytes:
        parts.append(types.Part.from_bytes(
            data=image_bytes, mime_type=image.type or "image/jpeg"))
    if audio_bytes:
        parts.append(types.Part.from_bytes(
            data=audio_bytes, mime_type=audio.type or "audio/wav"))
    contents.append(types.Content(role="user", parts=parts))

    # 3) answer-o upore (chat_area-te) dekhao
    with chat_area:
        with st.chat_message("assistant", avatar="🌾"):
            with st.spinner("🌱 KrishiBondhu ভাবছে..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3,
                            max_output_tokens=1400
                        )
                    )
                    answer = response.text or "Response khali ashche, abar try korun."
                    st.markdown(answer)
                    st.caption(DISCLAIMER)
                    st.session_state.messages.append(
                        {"role": "assistant", "text": answer})
                except Exception as e:
                    st.error("Response পাওয়া যায়নি।")
                    st.code(str(e))