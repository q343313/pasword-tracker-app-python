

import base64
import json
from pathlib import Path
from loguru import logger
import argparse
import sys
import streamlit as st


def handle_exception(func):
    """Decorator to log exceptions gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            return None
    return wrapper


class SecretMessenger:
    """A simple messenger for encrypting and decrypting messages."""

    FILEPATH = Path("C:/Users/talha/OneDrive/Desktop/cyberproject/messages/message.json")
    data = {}

    try:
        if FILEPATH.exists():
            with open(FILEPATH, "r") as f:
                data = json.loads(f.read())
        else:
            logger.warning(f"No file found at {FILEPATH}, starting with empty data.")
            
    except Exception as e:
        logger.exception(f"Error loading data: {e}")
        data = {}

    @classmethod
    def update_data(cls):
        """Update the JSON file with the current data."""
        with open(cls.FILEPATH, "w") as f:
            f.write(json.dumps(cls.data))
            logger.info("Data updated successfully.")
     
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

    @handle_exception
    def create_message(self):
        """Interactive CLI loop for encryption and decryption."""
        while True:
            option = input("Enter 'en' to encrypt, 'dc' to decrypt, or 'q' to quit: ").strip().lower()

            if option == "q":
                logger.info("Exiting messenger.")
                break
            elif option == "en":
                message = input("Enter plain message: ").strip()
                encrypted = self.encrypt_message(message)
                self.save_message({encrypted: message})
                logger.success(f"Encrypted Message: {encrypted}")
            elif option == "dc":
                encrypted = input("Enter encrypted message: ").strip()
                try:
                    decrypted = self.decrypt_message(encrypted)
                    self.save_message({encrypted: decrypted})
                    logger.success(f"Decrypted Message: {decrypted}")
                except Exception:
                    logger.error("Invalid encrypted message provided.")
            else:
                logger.warning("Invalid option. Please enter 'en', 'dc', or 'q'.")


# Secret App Cli
def main():
    parser = argparse.ArgumentParser(description="Secret Messenger CLI App")
    parser.add_argument("option", type=str, choices=["encrypt", "decrypt", "messenger"],
                        help="Choose an operation: encrypt, decrypt, messenger")
    parser.add_argument("--message", type=str, help="Message to encrypt or decrypt")

    args = parser.parse_args()
    messenger = SecretMessenger()

    if args.option == "encrypt":
        if not args.message:
            logger.error("Please provide a message using --message for encryption.")
            sys.exit(1)
        encrypted = messenger.encrypt_message(args.message)
        messenger.save_message({encrypted: args.message})
        logger.success(f"Encrypted: {encrypted}")

    elif args.option == "decrypt":
        if not args.message:
            logger.error("Please provide an encrypted message using --message for decryption.")
            sys.exit(1)
        try:
            decrypted = messenger.decrypt_message(args.message)
            messenger.save_message({args.message: decrypted})
            logger.success(f"Decrypted: {decrypted}")
        except Exception:
            logger.error("Failed to decrypt. Ensure the input is a valid Base64 encoded string.")

    elif args.option == "messenger":
        messenger.create_message()


# Design Ui Using Streamlib
def run_app():
    st.set_page_config(page_title="Secret Messenger", page_icon="🕵️", layout="centered")
    st.title(" Secret Messenger Web App")
    st.caption("Encrypt and Decrypt messages securely with Base64.")

    messenger = SecretMessenger()

    # Sidebar for navigation
    option = st.sidebar.radio("Choose Action", ["Encrypt Message", "Decrypt Message", "Saved Messages"])

    if option == "Encrypt Message":
        st.subheader("Encrypt your message")
        message = st.text_area("Enter your message:", placeholder="Type something here...")
        if st.button("Encrypt"):
            if message.strip():
                encrypted = messenger.encrypt_message(message)
                messenger.save_message({encrypted: message})
                st.success("Message Encrypted Successfully!")
                st.code(encrypted, language="text")
            else:
                st.warning("Please enter a message to encrypt.")

    elif option == "Decrypt Message":
        st.subheader("Decrypt your message")
        encrypted_message = st.text_area("Enter encrypted message:", placeholder="Paste Base64 text here...")
        if st.button("Decrypt"):
            if encrypted_message.strip():
                try:
                    decrypted = messenger.decrypt_message(encrypted_message)
                    messenger.save_message({encrypted_message: decrypted})
                    st.success("Message Decrypted Successfully!")
                    st.code(decrypted, language="text")
                except Exception:
                    st.error("Invalid encrypted message. Please check your input.")
            else:
                st.warning("Please enter an encrypted message.")

    elif option == "Saved Messages":
        st.subheader("Encrypted & Decrypted Message History")
        if messenger.data:
            for enc, dec in messenger.data.items():
                with st.expander(f"{enc[:30]}..."):
                    st.write(f"**Encrypted:** {enc}")
                    st.write(f"**Decrypted:** {dec}")
        else:
            st.info("No saved messages found yet.")    

if __name__ == "__main__":
    # main()
    run_app()
    
    # command in cmd
    # for encryption
    # py fullmessageapp.py encrypt --message "Take message"

    # for decryptionn
    # py fullmessageapp.py decrypt --message "Take message"
    
    # for messenger
    # py fullmessageapp.py messenger