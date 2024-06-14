from Entity.individualAccount import *
class GetAccountInfo:
    def __init__(self):
        pass

    def getAccountInfo(self,accountId) -> dict or Exception:
        return IndividualAccount().findOneAccount(accountId)


