from Entity.review import *
class Insert_review_by_id():
    def __init__(self):
        pass

    def insert_review_by_id(self, accountId,rating,reviewText):
        Review().insert_review_by_id(accountId,rating,reviewText)