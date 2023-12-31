# Data Validator
import re

class DataValidator:
    def __init__(self):
        pass

    def validate_user(self, user: str, email: str, password: str):
        if self.validate_username(user) and self.validate_email(email) and self.validate_password(password):
            print("User validated")
            return True
        else:
            print("User not validated")
            return False
        
    def validate_username(self, user: str):
        return 3 < len(user) < 12 and any(char.isalnum() or char.isprintable() or char.isalpha() for char in user) \
                and ' ' not in user and all(ord(char) < 128 for char in user)
    
    def validate_email(self, email: str):
        email_patern = re.compile(r"[^@]+@[^@]+\.[a-zA-Z]{2,}")
        return email_patern.match(email)
    
    def validate_password(self, password: str):
        return 8 < len(password) < 60 and any(char.isalnum() or char.isalpha() or char.isprintable() or char.isspace()
                                          for char in password) and all(ord(char) < 128 for char in password)
