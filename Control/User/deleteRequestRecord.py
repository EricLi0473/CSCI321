from Entity.requestRecord import *
class DeleteRequestRecord(object):
    def __init__(self):
        pass

    def deleteRequestRecord(self,requestId) -> None:
        RequestRecord().deleteRequestRecordById(requestId)