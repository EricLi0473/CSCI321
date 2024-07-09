from Entity.account import *
class VerifyAccountByEmail:
    def __init__(self):
        pass

    def verify_account_by_email(self, email):
        return Account().verify_account_by_email(email)