from Entity.followList import *
class GetFollowListByAccountId(object):
    def __init__(self):
        pass

    def get_followList_by_accountId(self, accountId):
        return FollowList().get_followList_by_accountId(accountId)

if __name__ == '__main__':
    print(GetFollowListByAccountId().get_followList_by_accountId("1"))