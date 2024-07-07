
from Entity.review import *
class Reviews():
    def __init__(self):
        pass

    def get_all_reviews(self):
        return Review().get_all_reviews()

if __name__ == '__main__':
    print(Reviews().get_all_reviews())