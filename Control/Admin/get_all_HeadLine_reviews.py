from Entity.review import *
class GetAllHeadLineReviews():
    def __init__(self):
        pass

    def get_all_headline_reviews(self):
        return Review().get_all_HeadLine_reviews()

if __name__ == '__main__':
    print(GetAllHeadLineReviews().get_all_headline_reviews())