from Entity.preference import *
class GetPreferenceByAccountId():
    def __init__(self):
        pass

    def get_preference_by_accountId(self,accountId):
        try:
            data =  Preference().get_preference_by_accountId(accountId)
            data['preferenceIndustry'] = data['preferenceIndustry'].split(',')
            data['preferenceCountry'] = data['preferenceCountry'].split(',')
            return data
        except Exception:
            return {'preferenceIndustry':["Technology"],'preferenceCountry':["us"]}

if __name__ == '__main__':
    print(GetPreferenceByAccountId().get_preference_by_accountId("1"))