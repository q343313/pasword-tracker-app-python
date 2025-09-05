

import base64
import random
import string
import streamlit as st
import streamlit.components.v1 as components
from loguru import logger


def handle_exception(func):
    
    def wrapper(*args,**kwargs):
        try :
            function = func(*args,**kwargs)
            return function
        
        except Exception as e:
            logger.exception(f"Something Wrong :{e}")
    return wrapper


@handle_exception
def check_password_category(password: str):
    """Check strength category of the given password."""
    if len(password) < 8:
        if any(c.isalpha() for c in password):
            return "Weak"
        elif any(c.isdigit() for c in password):
            return "Medium"
    elif len(password) >= 12:
        if (any(c.isalpha() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)):
            return "Strong"
    return "Normal"


@handle_exception
def generate_random_parts():
    ra = "".join(random.choices(string.ascii_lowercase, k=3))
    punc = "".join(random.choices(string.punctuation, k=2))
    digi = "".join(random.choices(string.digits, k=2))
    return ra, punc, digi


@handle_exception
def encode_password(plain_text: str):
    b64 = base64.b64encode(plain_text.encode()).decode()
    ra, punc, digi = generate_random_parts()
    safe_password = f"{ra}{b64}{punc}{digi}"
    return safe_password


@handle_exception
def decode_password(safe_password: str):
    base64_part = safe_password[3:-4]
    return base64.b64decode(base64_part.encode()).decode()




##  Ui Design

st.set_page_config(page_title="Secure Password Tool", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg,#0f172a,#1e293b);
        color: #e6eef8;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .card {
        background: rgba(255,255,255,0.08);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .card h1 {
        font-size: 2.2rem;
        margin: 0;
        color: #f1f5f9;
    }
    .muted {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 8px;
    }
    .stTextInput > div > input, .stTextArea textarea {
        background: rgba(255,255,255,0.07);
        border: 1px solid #334155;
        color: #f1f5f9 !important;
        border-radius: 12px;
        padding: 10px;
    }
    .stRadio > label { font-weight: 600; font-size: 1.1rem; }
    button[kind="secondary"] {
        background: linear-gradient(135deg,#3b82f6,#6366f1) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    button[kind="secondary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    code {
        background: rgba(0,0,0,0.4);
        color: #22d3ee;
        font-size: 1.1rem;
        padding: 8px 12px;
        border-radius: 10px;
    }
    .copy-box {
        margin-top: 12px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .copy-box textarea {
        width: 100%;
        height: 65px;
        border-radius: 10px;
        padding: 8px;
        border: none;
        background: rgba(255,255,255,0.05);
        color: #f8fafc;
        font-size: 1rem;
    }
    .copy-box button {
        background: #10b981;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 8px;
        cursor: pointer;
        transition: 0.3s;
    }
    .copy-box button:hover {
        background: #059669;
    }
    </style>
""", unsafe_allow_html=True)

# Header Card
st.markdown("""
    <div class="card">
        <h1>🔐 Secure Password Tool</h1>
        <p class="muted">Encrypt / Decrypt your password, check its strength, and copy results instantly.</p>
    </div>
""", unsafe_allow_html=True)

mode = st.radio("Choose an option", ["Encrypt", "Decrypt"])

# ---------- Encrypt Mode ----------
if mode == "Encrypt":
    plain = st.text_input("Enter password to encrypt", type="password")
    if st.button("Encrypt"):
        if not plain:
            st.error("⚠️ Please enter a password.")
        else:
            category = check_password_category(plain)
            st.info(f"🔎 Password category: **{category}**")

            # Strength bar
            strength_map = {"Weak": 25, "Medium": 50, "Normal": 70, "Strong": 100}
            st.progress(strength_map.get(category, 10))

            safe = encode_password(plain)
            st.success("✅ Password encrypted successfully")
            st.code(safe)

            copy_html = f"""
            <div class="copy-box">
              <textarea id='toCopy'>{safe}</textarea>
              <button onclick="(async()=>{{ navigator.clipboard.writeText(document.getElementById('toCopy').value); this.innerText='Copied ✅'; }})()">Copy</button>
            </div>
            """
            components.html(copy_html, height=140)

# ---------- Decrypt Mode ----------
elif mode == "Decrypt":
    enc_input = st.text_area("Paste encrypted password here")
    if st.button("Decrypt"):
        if not enc_input:
            st.error("⚠️ Please paste an encrypted password.")
        else:
            try:
                original = decode_password(enc_input.strip())
                category = check_password_category(original)
                st.info(f"🔎 Password category: **{category}**")

                st.progress({"Weak":25,"Medium":50,"Normal":70,"Strong":100}.get(category,10))

                st.success("🔓 Decrypted successfully")
                st.code(original)

                copy_html2 = f"""
                <div class="copy-box">
                  <textarea id='toCopy2'>{original}</textarea>
                  <button onclick="(async()=>{{ navigator.clipboard.writeText(document.getElementById('toCopy2').value); this.innerText='Copied ✅'; }})()">Copy</button>
                </div>
                """
                components.html(copy_html2, height=140)
            except Exception as e:
                st.error(f"❌ Decryption failed: {e}")

st.markdown("---")
st.caption("⚠️ This app uses Base64 + obfuscation. For real-world apps, use strong cryptography (`cryptography` with Fernet).")