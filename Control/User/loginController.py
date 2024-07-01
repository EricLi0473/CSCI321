import hashlib
from Entity.account import *
# from Entity.businessAccount import *
# from Entity.individualAccount import *


class LoginController:
    def __init__(self):
        pass

    def login(self,email,password) -> dict or Exception:
        if email is None or password is None:
            raise Exception('please enter both username and password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        return Account().verifyAccount(email, hashed_password)

