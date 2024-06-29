from flask import jsonify, request, session
from Entity.watchlist import *


class AddWatchListController:
    def __init__(self):
        pass

    def add_to_watchlist(self, accountId, stockSymbol):
        Watchlist().add_to_watchlist(accountId, stockSymbol)
