


import base64
import json
from pathlib import Path
from loguru import logger
import streamlit as st


class SecretMessenger:
    """A simple messenger for encrypting and decrypting messages."""

    FILEPATH = Path("C:/Users/talha/OneDrive/Desktop/cyberproject/messages/message.json")
    data = {}

    try:
        if FILEPATH.exists():
            with open(FILEPATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            logger.warning(f"No file found at {FILEPATH}, starting with empty data.")
            data = {}
    except Exception as e:
        logger.exception(f"Error loading data: {e}")
        data = {}

    @classmethod
    def update_data(cls):
        """Update the JSON file with the current data."""
        try:
            with open(cls.FILEPATH, "w", encoding="utf-8") as f:
                json.dump(cls.data, f, indent=4)
            logger.info("Data updated successfully.")
        except Exception as e:
            logger.exception(f"Error saving data: {e}")

    @classmethod
    def save_message(cls, message_map: dict):
        """Save encrypted-decrypted message pairs to JSON file."""
        cls.data.update(message_map)
        cls.update_data()

    @staticmethod
    def encrypt_message(message: str):
        """Encrypt a plain text message using Base64."""
        return base64.b64encode(message.encode()).decode()

    @staticmethod
    def decrypt_message(encoded_message: str):
        """Decrypt a Base64 encoded message."""
        return base64.b64decode(encoded_message.encode()).decode()


# -------------------- Streamlit App ----------------------

def run_app():
    st.set_page_config(page_title="🔐 Secret Messenger", page_icon="🕵️", layout="centered")
    st.title("🔐 Secret Messenger Web App")
    st.caption("Encrypt and Decrypt messages securely with Base64.")

    messenger = SecretMessenger()

    # Sidebar for navigation
    option = st.sidebar.radio("Choose Action", ["Encrypt Message", "Decrypt Message", "Saved Messages"])

    if option == "Encrypt Message":
        st.subheader("✉️ Encrypt your message")
        message = st.text_area("Enter your message:", placeholder="Type something here...")
        if st.button("Encrypt"):
            if message.strip():
                encrypted = messenger.encrypt_message(message)
                messenger.save_message({encrypted: message})
                st.success("✅ Message Encrypted Successfully!")
                st.code(encrypted, language="text")
            else:
                st.warning("⚠️ Please enter a message to encrypt.")

    elif option == "Decrypt Message":
        st.subheader("🔓 Decrypt your message")
        encrypted_message = st.text_area("Enter encrypted message:", placeholder="Paste Base64 text here...")
        if st.button("Decrypt"):
            if encrypted_message.strip():
                try:
                    decrypted = messenger.decrypt_message(encrypted_message)
                    messenger.save_message({encrypted_message: decrypted})
                    st.success("✅ Message Decrypted Successfully!")
                    st.code(decrypted, language="text")
                except Exception:
                    st.error("❌ Invalid encrypted message. Please check your input.")
            else:
                st.warning("⚠️ Please enter an encrypted message.")

    elif option == "Saved Messages":
        st.subheader("📂 Encrypted & Decrypted Message History")
        if messenger.data:
            for enc, dec in messenger.data.items():
                with st.expander(f"🔐 {enc[:30]}..."):
                    st.write(f"**Encrypted:** {enc}")
                    st.write(f"**Decrypted:** {dec}")
        else:
            st.info("No saved messages found yet.")


if __name__ == "__main__":
    run_app()
