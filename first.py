
import base64
import random
from loguru import logger
import string 


def handle_exception(func):
    
    def wrapper(*args,**kwargs):
        try :
            function = func(*args,**kwargs)
            return function
        
        except Exception as e:
            logger.exception(f"Something Wrong :{e}")
    return wrapper

@handle_exception
def check_password_categry(password):
    
    for i in password:
        if (i in string.ascii_letters) and len(password) < 8:
            categry = "Weak"
        elif (i in string.ascii_letters or i in string.digits) and len(password) < 8:
            categry = "Medium"
            
        elif (i in string.ascii_letters or i in string.digits or i in string.punctuation) and len(password) > 12:
            categry = "Strong"
        else:
            categry = "Normal"
    
    return categry
            
    

class SecurePassword :
    
    def __init__(self):
        logger.debug(f"Secure Your Password")
    
    @staticmethod
    @handle_exception
    def encrypt_password():
        '''encrypt your password'''
        
        ra = "".join(random.choices(string.ascii_lowercase,k=3))
        punc= "".join(random.choices(string.punctuation,k=2))
        digi = "".join(random.choices(string.digits,k=2))
        password  = input("Enter password : ")
        
        categry = check_password_categry(password)
        logger.debug(f"Categry : {categry}")
        
        encrypt_password = base64.b64encode(password.encode()).decode()
        logger.debug(encrypt_password)
        safe_password = ra + encrypt_password[1:] + punc + encrypt_password[0]+ digi
        
        logger.debug(f"Encrypted password : {safe_password}")

    
    @staticmethod
    @handle_exception
    def decode_password():
        '''decode your password'''
        
        
        password  = input("Enter password : ")
        safe_password = password[-3] + password[3:-5]
        logger.debug(safe_password)
        decrypt_password = base64.b64decode(safe_password.encode()).decode()
        logger.debug(decrypt_password)
        
        


if __name__ == "__main__":
    f1 = SecurePassword()
    option = input("Enter en for encode and dc for decode and q for quit : ")
    
    if option == "en":
        f1.encrypt_password()  
    elif option == "dc":
        f1.decode_password()
    
    elif option == "q":
        pass