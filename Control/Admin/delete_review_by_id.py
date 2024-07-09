from Entity.review import *
class DeleteReviewById:
    def __init__(self):
        pass

    def delete_review_by_id(self, review_id):
        Review().delete_review_by_id(review_id)
