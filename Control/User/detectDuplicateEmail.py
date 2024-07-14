from Entity.account import *
class DetectDuplicateEmail:
    def __init__(self):
        pass

    def detectDuplicateEmail(self,email):
        return Account().detectDuplicateEmail(email)