from Entity.searchhistory import *
class RemoveSearchHistory():
    def __init__(self):
        pass

    def remove_searchHistory_by_id(self,id):
        SearchHistory().remove_searchHistory_by_id(id)