from Entity.searchhistory import *
class InsertSearchHistoryById:
    def __init__(self):
        pass

    def insert_searchHistory_by_id(self,accountID,stockSymbol):
        return SearchHistory().insert_searchHistory_by_id(accountID,stockSymbol)

if __name__ == '__main__':
    InsertSearchHistoryById().insert_searchHistory_by_id('1','AAPL')
