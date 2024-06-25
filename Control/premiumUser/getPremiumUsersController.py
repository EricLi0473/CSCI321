from Entity.account import *
class GetPremiumUsersController:
    def __init__(self):
        pass

    def getPremiumUsers(self):
        return Account().get_premium_accountId()