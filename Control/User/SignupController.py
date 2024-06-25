
import secrets
import string
import hashlib
import re
class SignupController:
    def __init__(self):
        pass
    def individualSignUp(self,profile,username,email,password,againPassword,invitationCode = None,) -> dict or Exception:
        print(profile,username,email,password,againPassword,invitationCode)
        if profile == 'default' or not username or not email or not password or not againPassword:
            raise Exception('Please fill the from')
        if password != againPassword:
            raise Exception('Reentered passwords do not match')
        pattern = re.compile(r'^(?=.*[A-Z]).{8,}$')
        if not pattern.match(password):
            raise Exception('Password does not match')
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not pattern.match(email):
            raise Exception('Email does not match')
        api_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        hashedPassword = hashlib.md5(password.encode()).hexdigest()
        if profile == 'Free':
            return IndividualAccount().signup(username,api_key,hashedPassword,email,"free")
        elif profile == 'premium' and invitationCode is None:
            return IndividualAccount().signup(username,api_key,hashedPassword,email,"premium")
        elif profile == 'premium' and invitationCode is not None:
            return BusinessAccount().signup(profile,api_key,hashedPassword,email,"premium",invitationCode)
#{'invitationCode' = 'xx','account':[{'username':'xx','password':'xx'},{'username':'xx','password':'xx'}]}
    def businessSignUp(self,cName,cType,cMail,cPhone,cCount = 10) -> dict:
        invitationCode = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))