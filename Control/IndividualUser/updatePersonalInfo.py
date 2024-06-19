from Entity.individualAccount import IndividualAccount

class UpdatePersonalInfo:
    def __init__(self):
        pass

    def updatePersonalInfo(self,accountId,userName,email,bio) -> bool or Exception:
       return IndividualAccount().updateAccount(accountId,userName,email,bio)
