from Entity.preference import *
class GetPreferenceByAccountId():
    def __init__(self):
        pass

    def get_preference_by_accountId(self,accountId):
        return Preference().get_preference_by_accountId(accountId)

if __name__ == '__main__':
    print(GetPreferenceByAccountId().get_preference_by_accountId("1"))