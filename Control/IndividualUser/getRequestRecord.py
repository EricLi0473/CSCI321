from Entity import requestRecord
from Entity.requestRecord import *
class GetRequestRecord():
    def __init__(self):
        pass
    def getRequestRecord(self,apikey) -> list[dict] or Exception:
        return RequestRecord().getRequestRecordByApiKey(apikey)
