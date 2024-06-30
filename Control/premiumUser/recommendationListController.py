from Entity.recommendationlist import *
from Control.User.stockDataController import *
import time
import ast
import json
class RecommendationListController:
    def __init__(self):
        pass

    def get_recommendationList_by_accountId(self, id) -> list[dict]:
        return json.loads(RecommendationList().get_recommendations_by_id(id)['recommendedStock'])

    def insert_recommendation_by_accountId(self,id, countries:list,industry:list):
        stock_list = StockDataController().get_recommendation_stock_by_preference(countries,industry)
        result = []

        for stock in stock_list:
            try:
                result.append(StockDataController().get_stock_info_medium(stock))
            except Exception:
                continue

        RecommendationList().insert_recommendation_by_accountId(id, json.dumps(result))

    def update_recommendation_by_accountId(self,id, countries:list,industry:list):
        stock_list = StockDataController().get_recommendation_stock_by_preference(countries,industry)
        result = []

        for stock in stock_list:
            try:
                result.append(StockDataController().get_stock_info_medium(stock))
            except Exception:
                continue
        RecommendationList().update_recommendation_by_accountId(id, json.dumps(result))

if __name__ == '__main__':
    print(RecommendationListController().get_recommendationList_by_accountId(1))