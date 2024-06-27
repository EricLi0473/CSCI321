from Entity.watchlist import *
import json
class UpdateWatchlist():
    def __init__(self):
        pass

    def update_Watchlist(self,accountId,stockSymbol:list):
        Watchlist().update_watchlist(accountId,json.dumps(stockSymbol))

if __name__ == '__main__':
    UpdateWatchlist().update_Watchlist("1",["bili","sbux"])