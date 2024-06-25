from Entity.recommendationlist import *
from Control.User.stockDataController import *

import ast
class RecommendationListController:
    def __init__(self):
        pass

    def get_recommendationList_by_id(self, id) -> list[dict]:
        stockList = ast.literal_eval(RecommendationList().get_recommendations_by_id("1")['recommendedStock'])
        result = []
        for stock in stockList:
            result.append(StockDataController().get_stock_info_medium(stock))
        return result
if __name__ == '__main__':
    print(RecommendationListController().get_recommendationList_by_id(1))