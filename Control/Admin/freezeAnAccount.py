from Entity.account import *
class FreezeAnAccount:
    def __init__(self):
        pass
    def freeze_anAccount(self,accountId):
        Account().freezeAnAccount(accountId)