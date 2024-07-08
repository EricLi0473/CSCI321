from Entity.account import *
import hashlib
class ResetPwd():
    def __init__(self):
        pass

    def reset_pwd(self,email,pwd):
        hashedPassword = hashlib.md5(pwd.encode()).hexdigest()
        return Account().reset_pwd(email,hashedPassword)