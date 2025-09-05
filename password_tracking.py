

import base64
import random
import string
# import streamlit as st
from loguru import logger
# import streamlit.components.v1 as components

def handle_exception(func):
    
    def wrapper(*args,**kwargs):
        try :
        
            function = func(*args,**kwargs)
            return function
        
        except Exception as e:
            logger.exception(f"Something Wrong :{e}")
    return wrapper


@handle_exception
def generate_random_parts():
    # """Generate random prefix (3 letters), 2 punctuation, and 2 digits."""
    ra = "".join(random.choices(string.ascii_lowercase, k=3))
    punc = "".join(random.choices(string.punctuation, k=2))
    digi = "".join(random.choices(string.digits, k=2))
    return ra, punc, digi


@handle_exception
def encode_password(plain_text: str) -> str:
    b64 = base64.b64encode(plain_text.encode()).decode()
    ra, punc, digi = generate_random_parts()
    safe_password = f"{ra}{b64}{punc}{digi}"
    return safe_password


@handle_exception
def decode_password(safe_password: str) -> str:
    if len(safe_password) < 3 + 1 + 4: 
        raise ValueError("Encrypted string is too short to be valid.")
    base64_part = safe_password[3:-4]
    if not base64_part:
        raise ValueError("No base64 data found in encrypted string.")

    decrypted = base64.b64decode(base64_part.encode()).decode()
    return decrypted
   

encdode= encode_password("kpk009988")
print(encdode)
decodepas = decode_password(encdode)
print(decodepas)

# # ------------------ Streamlit UI ------------------

# st.set_page_config(page_title="SecurePassword — Encrypt & Decrypt", layout="centered")

# st.markdown(
#     """
#     <style>
#     .stApp { background: linear-gradient(180deg,#0f172a 0%, #1e293b 100%); color: #e6eef8; }
#     .card { background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02)); padding: 18px; border-radius: 12px; box-shadow: 0 6px 18px rgba(2,6,23,0.6); }
#     .muted { color: #a8b3c7; font-size: 0.9rem }
#     </style>
#     <div class="card">
#       <h1 style="margin:0;">🔒 SecurePassword</h1>
#       <p class="muted">Encrypt and decrypt small secrets using Base64 with a reversible safe wrapper. Includes copy/download UI.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# st.write("")

# col1, col2 = st.columns([2, 1])

# with col1:
#     st.header("Encrypt")
#     plain = st.text_input("Enter password to encrypt", type="default")
#     if st.button("Encrypt", key="enc"):
#         if not plain:
#             st.error("Please enter a password to encrypt.")
#         else:
#             try:
#                 safe = encode_password(plain)
#                 st.success("Password encrypted successfully")
#                 st.code(safe, language=None)

#                 # copy button using simple HTML + JS
#                 copy_html = f"""
#                 <div>
#                   <textarea id='toCopy' style='width:100%;height:60px'>{safe}</textarea>
#                   <button onclick="(async()=>{{ navigator.clipboard.writeText(document.getElementById('toCopy').value); this.innerText='Copied'; }})()">Copy</button>
#                 </div>
#                 """
#                 components.html(copy_html, height=120)

#                 st.download_button("Download encrypted text", safe, file_name="encrypted.txt")
#             except Exception as e:
#                 st.error(f"Encryption failed: {e}")

# with col2:
#     st.header("Decrypt")
#     enc_input = st.text_area("Paste encrypted password here")
#     if st.button("Decrypt", key="dec"):
#         if not enc_input:
#             st.error("Please paste an encrypted password.")
#         else:
#             try:
#                 original = decode_password(enc_input.strip())
#                 st.success("Decrypted successfully")
#                 st.code(original)

#                 copy_html2 = f"""
#                 <div>
#                   <textarea id='toCopy2' style='width:100%;height:60px'>{original}</textarea>
#                   <button onclick="(async()=>{{ navigator.clipboard.writeText(document.getElementById('toCopy2').value); this.innerText='Copied'; }})()">Copy</button>
#                 </div>
#                 """
#                 components.html(copy_html2, height=120)

#             except Exception as e:
#                 st.error(f"Decryption failed: {e}")

# st.markdown("---")

# st.subheader("How it works")
# st.markdown(
#     """
#     - The app encodes your plaintext using Base64.
#     - A small random 3-letter prefix and a random 2-punctuation + 2-digit suffix are added to the Base64 string to create a "safe" token.
#     - For decryption the app strips the prefix (3 chars) and suffix (4 chars) then base64-decodes the middle chunk.

#     ⚠️ This scheme is NOT a replacement for real cryptography for sensitive data — it's a reversible obfuscation meant for learning and simple use-cases. For real security, use authenticated encryption (e.g. Fernet from the `cryptography` package).
#     """
# )

# st.caption("Built with ❤️ — Talha")
