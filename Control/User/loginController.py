# import hashlib
# from Entity.account import *
# from Entity.businessAccount import *
# from Entity.individualAccount import *


class LoginController:
    def __init__(self):
        pass

    def login(self,username,password) -> dict or Exception:
        if username is None or password is None:
            raise Exception('please enter both username and password')
        password = hashlib.md5(password.encode()).hexdigest()
        profile = Account().getTheProfile(username)
        if profile is None:
            raise Exception("Account not found")
        elif profile == 'individual':
            return IndividualAccount().verifyAccount(username,password)
        elif profile == 'business':
            pass

