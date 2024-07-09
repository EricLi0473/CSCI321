
from Entity.review import *
class Get_all_reviews:
    def __init__(self):
        pass

    def get_all_reviews(self):
        return Review().get_all_reviews()

if __name__ == '__main__':
    print(Get_all_reviews().get_all_reviews())