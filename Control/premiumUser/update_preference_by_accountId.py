from Entity.preference import *
from Control.premiumUser.recommendationListController import *
class UpdatePreferenceByAccountId():
    def __init__(self):
        pass

    # Automatically determines whether to update or create a new preference, and updates the recommendationLIst.
    def update_preference_by_accountId(self, accountId, countries:list,industries:list):
        countriesStr = ",".join(countries)
        industriesStr = ",".join(industries)
        if not Preference().get_preference_by_accountId(accountId):
            Preference().set_preference_by_accountId(accountId, countriesStr, industriesStr)
            RecommendationListController().insert_recommendation_by_accountId(accountId, countries, industries)
        else:
            Preference().update_preference_by_accountId(accountId, countriesStr, industriesStr)
            RecommendationListController().update_recommendation_by_accountId(accountId, countries, industries)
if __name__ == '__main__':
    UpdatePreferenceByAccountId().update_preference_by_accountId("3",["us","hk"],["Technology"])