from Entity.searchhistory import *
class Get_searchHistory_by_id():
    def __init__(self):
        pass

    def get_searchHistory_by_id(self,accountId):
        return SearchHistory().get_searchHistory_by_id(accountId)