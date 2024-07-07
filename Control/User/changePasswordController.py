from Entity.account import *
import hashlib
class ChangePasswordController:
    def __init__(self):
        pass

    def update_password_by_accountId(self,accountId,newPassword) -> str or Exception:
        return Account().update_password_by_accountId(accountId, hashlib.md5(newPassword.encode()).hexdigest())
