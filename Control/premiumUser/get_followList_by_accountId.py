from Entity.followList import *
class GetFollowListByAccountId(object):
    def __init__(self):
        pass

    def get_followList_by_accountId(self, accountId):
        return FollowList().get_followList_by_accountId(accountId)

    def get_followList_by_accountId_List(self, accountId) -> list:
        Follow_List = FollowList().get_followList_by_accountId(accountId)
        list = []
        for follower in Follow_List:
            list.append(follower['accountAccountId'])
        return list
if __name__ == '__main__':
    print(GetFollowListByAccountId().get_followList_by_accountId_List("1"))