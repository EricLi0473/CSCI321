from Entity.account import *
from Entity.followList import *
class UpdatePersonalInfoController:
    def update_personal_info(self, account):
        try:
            accountId = account['accountId']
            userName = account["userName"]
            email = account['email']
            bio = account['bio']
            age = account['age']
            sex  = account['sex']
            occupation = account['occupation']
            incomeLevel = account['incomeLevel']
            netWorth = account['netWorth']
            investmentExperience = account['investmentExperience']
            riskTolerance = account['riskTolerance']
            investmentGoals = account['investmentGoals']
            profile = account['profile']
            isPrivateAccount = account['isPrivateAccount']
            mlViewLeft = account['mlViewLeft']

            # if private account, delete all followers
            if isPrivateAccount == 1:
                FollowList().remove_all_follower(accountId)

            return Account().update_Account(
                accountId, userName, email, bio, age, sex, occupation,
                incomeLevel, netWorth, investmentExperience, riskTolerance, investmentGoals, profile,
                isPrivateAccount,mlViewLeft
            )
        except Exception as e:
            print(f"Error in update_personal_info: {e}")
            return False


if __name__ == "__main__":
    print(UpdatePersonalInfoController().update_personal_info({
        "accountId": 4,
        "userName": "UpdatedDummyName",
        "email": "updateddummyemail@example.com",
        "bio": "Updated bio.",
        "age": 31,
        "sex": "female",
        "occupation": "UpdatedOccupation",
        "incomeLevel": 60000,
        "netWorth": 250000,
        "investmentExperience": "intermediate",
        "riskTolerance": "high",
        "investmentGoals": "Buy a house",
        "profile": "premium"
    }))

