from Entity.followList import *
class GetAccountListByFollowedId():
    def __init__(self):
        pass

    def get_accountList_by_followedId(self, followedId):
        return FollowList().get_accountList_by_followedId(followedId)

if __name__ == '__main__':
    print(GetAccountListByFollowedId().get_accountList_by_followedId(1))