from Entity.preference import *
from Control.premiumUser.recommendationListController import *
class UpdatePreferenceByAccountId():
    def __init__(self):
        pass

    # Automatically determines whether to update or create a new preference, and updates the recommendationLIst.
    def update_preference_by_accountId(self, accountId, countries:list,industries:list):
        countriesStr = ",".join(countries)
        industriesStr = ",".join(industries)
        Preference().set_preference_by_accountId(accountId, countriesStr, industriesStr)
        RecommendationListController().insert_recommendation_by_accountId(accountId, industries,countries )

    def update_ReceiveNotification_by_accountId(self,accountId,receiveNotification) -> int:
        print(receiveNotification)
        if receiveNotification == "true":
            receiveNotification = 1
        elif receiveNotification == "false":
            receiveNotification = 0
        return Preference().update_ReceiveNotification_by_accountId(accountId, receiveNotification)
if __name__ == '__main__':
    # UpdatePreferenceByAccountId().update_preference_by_accountId("3",["us","hk"],["Technology"])
    UpdatePreferenceByAccountId().update_ReceiveNotification_by_accountId("1",0)