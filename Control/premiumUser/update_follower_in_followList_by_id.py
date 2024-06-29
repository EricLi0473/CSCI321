from Entity.followList import *
class UpdateFollowerInFollowListById:
    def __init__(self):
        pass

    def update_follower_in_followList_by_id(self, accountId,followedId,notifyMe):
        FollowList().update_follower_in_followList_by_id(accountId,followedId,notifyMe)