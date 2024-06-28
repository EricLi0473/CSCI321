from Entity.followList import *
class RemoveFollowerInFollowListById:
    def __init__(self):
        pass

    def remove_follower_in_followList_by_id(self, accountID, followedID):
        FollowList().remove_follower_in_followList_by_id(accountID, followedID)