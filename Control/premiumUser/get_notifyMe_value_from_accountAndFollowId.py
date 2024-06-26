from Entity.followList import *
class GetNotifyMeValueFromAccountAndFollowId():
    def __init__(self):
        pass

    def get_notifyMe_value_from_accountAndFollowId(self,accountId,followId):
        return FollowList().get_notifyMe_value_from_accountAndFollowId(accountId,followId)

if __name__ == '__main__':
    print(GetNotifyMeValueFromAccountAndFollowId().get_notifyMe_value_from_accountAndFollowId(1,2))
