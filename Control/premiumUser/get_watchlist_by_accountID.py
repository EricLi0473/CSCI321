from Entity.watchlist import *
import json
class GetWatchlistByAccountID():
    def __init__(self):
        pass

    def get_watchlist_by_accountID(self, accountID):
        return json.loads(Watchlist().get_watchlist_by_accountID(accountID)['stockSymbol'])


if __name__ == '__main__':
    print(GetWatchlistByAccountID().get_watchlist_by_accountID("1"))