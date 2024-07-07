from Entity.account import *
class UpdateProfileStatus():
    def __init__(self):
        pass

    def update_profile_status(self,accountId,status):
        return Account().update_profile_status(accountId,status)