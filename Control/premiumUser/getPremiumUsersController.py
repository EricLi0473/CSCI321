from Entity.account import *
class GetPremiumUsersController:
    def __init__(self):
        pass

    def getPremiumUsers(self):
        return Account().get_premium_accountId()

if __name__ == '__main__':
    print(GetPremiumUsersController().getPremiumUsers())