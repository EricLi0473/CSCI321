from Entity.review import *
class GetReviewByAccountId():
    def __init__(self):
        pass

    def get_review_by_accountId(self, accountId):
        return Review().get_review_by_accountId(accountId)