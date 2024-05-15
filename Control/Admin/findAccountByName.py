from Entity.account import *
class FindAccountByName:
    def __init__(self):
        pass
    '''''
    return list:Object<Account>
    '''''
    def findAccountByName(self, accountName) -> list:
        return Account().getAccountByName(accountName)