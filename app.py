import streamlit as st
from rag_chain import ask_medicine_bot
from langchain.chat_models import ChatOpenAI
import base64

# ========== 🔧 PAGE CONFIG ==========
st.set_page_config(page_title="🧪 Ayurvedic Medicine Bot", page_icon="🌿")

# ========== 🎨 BACKGROUND IMAGE & TEXT STYLING ==========
def set_background(image_path: str):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: black !important;
            }}
            .stTextInput > div > div > input {{
                background-color: #ffffffcc;
                color: black !important;
            }}
            .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, label, div {{
                color: black !important;
            }}
            .stButton > button {{
                background-color: #0f9960;
                color: white;
                font-weight: bold;
            }}
            .stSuccess, .stInfo, .stError {{
                color: black !important;
            }}
        </style>
    """, unsafe_allow_html=True)

set_background("ayruvedic_3.jpg")  # Ensure this image is in your working directory

# ========== 🌿 HEADER ==========
st.markdown("<h1>🌿 MT Ayurvedic Medicine Advisor</h1>", unsafe_allow_html=True)
st.markdown("<h5>Ask anything about Ayurvedic medicines based on a <b>10,000-record</b> knowledge base.</h5>", unsafe_allow_html=True)

# ========== 💬 USER INPUT ==========
st.markdown("<label style='font-size: 1.1rem; font-weight: bold;'>💬 What would you like to know?</label>", unsafe_allow_html=True)
user_input = st.text_input("", placeholder="e.g., What helps with acidity?", key="input")

# ========== 📌 SESSION STATE INIT ==========
if "response" not in st.session_state:
    st.session_state.response = None

# ========== 👇 SIMPLE BUTTON TO GET ANSWER ==========
if st.button("🔍 Get Answer"):
    if user_input:
        with st.spinner("🔍 Thinking..."):
            try:
                st.session_state.response = ask_medicine_bot(user_input)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ========== ✅ DISPLAY RESPONSE ==========
if st.session_state.response:
    st.markdown("### ✅ Answer:")
    st.success(st.session_state.response)
