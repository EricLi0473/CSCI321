from Entity.account import *
class DeleteAccountByAccountId:
    def __init__(self):
        pass
    def deleteAccountById(self, accountId) -> bool and str:
        return Account().deleteAnAccountById(accountId)