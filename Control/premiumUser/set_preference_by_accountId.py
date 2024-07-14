from Entity.preference import *
class Set_preference_by_accountId:
    def __init__(self):
        pass

    def set_preference_by_accountId(self,accountId, preferenceIndustry,preferenceCountry):
        Preference().set_preference_by_accountId(accountId, preferenceIndustry,preferenceCountry)

if __name__ == '__main__':
    Set_preference_by_accountId().set_preference_by_accountId("4","us","a")