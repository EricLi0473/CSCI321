from Entity.account import *
class GetAllThresholdsByAccount:
    def __init__(self):
        pass

    def get_all_thresholds_by_account(self):
        return Account().get_AllThresholds_by_account()

if __name__ == '__main__':
    print(GetAllThresholdsByAccount().get_all_thresholds_by_account())