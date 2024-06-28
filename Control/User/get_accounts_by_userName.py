from Entity.account import *
class GetAccountsByUserName():
    def __init__(self):
        pass

    def get_accounts_by_userName(self, userName,exceptUser):
        return Account().get_accounts_by_userName(userName,exceptUser)