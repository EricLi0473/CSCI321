from Entity.followList import *
class InsertFollowListById:
    def __init__(self):
        pass

    def insert_followList_by_id(self, accountID, followedId):
        FollowList().insert_followList_by_id(accountID, followedId)