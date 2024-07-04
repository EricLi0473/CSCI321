from Entity.preference import *
class GetPreferenceByAccountId():
    def __init__(self):
        pass

    def get_preference_by_accountId(self,accountId):
        data =  Preference().get_preference_by_accountId(accountId)
        data['preferenceIndustry'] = data['preferenceIndustry'].split(',')
        data['preferenceCountry'] = data['preferenceCountry'].split(',')
        return data

if __name__ == '__main__':
    print(GetPreferenceByAccountId().get_preference_by_accountId("1")["preferenceIndustry"])