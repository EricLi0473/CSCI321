from Entity.recommendationlist import *
from Control.User.stockDataController import *

import ast
class RecommendationListController:
    def __init__(self):
        pass

    def get_recommendationList_by_accountId(self, id) -> list[dict]:
        stockList = ast.literal_eval(RecommendationList().get_recommendations_by_id(id)['recommendedStock'])
        result = []
        tickers_string = " ".join(stockList)
        print(tickers_string)
        for stock in stockList:
            try:
                result.append(StockDataController().get_stock_info_medium(stock))

            except Exception:
                continue
        return result

    def insert_recommendation_by_accountId(self,id, countries,industry):
        stock_list = str(StockDataController().get_recommendation_stock_by_preference(countries,industry))
        RecommendationList().insert_recommendation_by_accountId(id, stock_list)

    def update_recommendation_by_accountId(self,id, countries,industry):
        stock_list = str(StockDataController().get_recommendation_stock_by_preference(countries,industry))
        RecommendationList().update_recommendation_by_accountId(id, stock_list)

if __name__ == '__main__':
    # print(RecommendationListController().get_recommendationList_by_accountId(1))
    print(RecommendationListController().get_recommendationList_by_accountId("1"))