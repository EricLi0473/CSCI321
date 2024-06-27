from Entity.followList import *
class Get_who_follows_me_by_accountID():
    def __init__(self):
        pass

    def get_who_follows_me_by_accountID(self,accontId):
        return FollowList().get_who_follows_me_by_accountID(accontId)