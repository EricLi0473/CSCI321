from Entity.account import *
class GetAccountByAccountId:
    def __init__(self):
        pass
    def get_account_by_accountId(self, accountId):
        return Account().get_account_by_accountId(accountId)

if __name__ == '__main__':
    print(GetAccountByAccountId().get_account_by_accountId(1))