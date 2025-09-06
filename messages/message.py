


import base64
import random
import os
import string
import json
from pathlib import Path
from loguru import logger
import argparse
import sys

def handle_exception(func):
    def wrapper(*args,**kwargs):
        functiomn = func(*args,**kwargs)
        return functiomn
    return wrapper

class Secret_Messenger:
    
    data = {}
    filepath = "C:/Users/talha/OneDrive/Desktop/cyberproject/messages/message.json"
    
    try :
        if Path(filepath).exists():
            with open(filepath,"r")as f:
                data = json.loads(f.read())    
        else:
            logger.error(f"No Such file found")    
    except Exception as e:
        logger.exception(f"Something Wrong {e}")
    
    @classmethod
    def update_data(cls):
        '''update data'''
        
        with  open(cls.filepath,"w") as f:
            f.write(json.dumps(cls.data))
    
    
    @classmethod
    def  data_save_in_json(cls,messagedata):
        '''data save in json file'''
        
        cls.data.update({"Encrypted Message " : "Decrypted Message"})
        cls.data.update(messagedata)
        cls.update_data()
        
    @property
    def encrypt_message(self):
        '''encrypt message'''
        message = input("Enter Simple message : ")
        encryyptmessage = base64.b64encode(message.encode()).decode() 
        Secret_Messenger.data_save_in_json({encryyptmessage:message})     
        return encryyptmessage
    
    @property
    def decrypt_message(self):
        message = input("Enter Encrypt message : ")
        decryptmessage = base64.b64decode(message.encode()).decode()
        Secret_Messenger.data_save_in_json({message:decryptmessage})  
        return decryptmessage
         
    @handle_exception
    def create_message(self):
        '''create message'''
        encrypt = True
        while True:
            option = input("Enter en for encrypt message and dc for decrypt message and q for quit : ")
            if option == "q":
                break
            elif option == "en":
                encrypt = True
            elif option == "dc":
                encrypt = False
            else:
                logger.debug(f"Enter vallid value")
                break
            
            if encrypt:
                encryyptmessage = self.encrypt_message
                logger.debug(f"Encrypt message : {encryyptmessage}")
            
            else:
                decryptmessage = self.decrypt_message
                logger.debug(f"Decrypt message : {decryptmessage}")


# Adding cli         
      
parse = argparse.ArgumentParser(description="Secret Messanger app")
parse.add_argument(
    "option",
    type=str ,
    # choices=["encrypt","decrypt","messenger"]
)      

parse.add_argument("--messenger",type=str)

args = parse.parse_args()

if __name__ == "__main__":
    f1 = Secret_Messenger()
    
    if args.option == "encrypt":
        logger.debug(f1.encrypt_message)
    
    elif args.option == "decrypt":
        logger.debug(f1.decrypt_message)
    
    else :
        f1.create_message()
    
    
    # if args.messenger:
    #     f1.create_message()
    