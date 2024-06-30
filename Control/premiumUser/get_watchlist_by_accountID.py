from Entity.watchlist import *
import json
class GetWatchlistByAccountID():
    def __init__(self):
        pass

    def get_watchlist_by_accountID(self, accountID):
        try:
            return json.loads(Watchlist().get_watchlist_by_accountID(accountID)['stockSymbol'])
        except Exception:
            # If the user does not have a favourite
            return []

    def get_watchlist_by_accountId_full(self, accountID):
        return Watchlist().get_watchlist_by_accountID(accountID)

if __name__ == '__main__':
    print(GetWatchlistByAccountID().get_watchlist_by_accountID("1"))