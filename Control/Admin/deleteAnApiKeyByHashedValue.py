from Entity.apiKey import *
class DeleteApiKeyByHashedValue():
    def __init__(self):
        pass
    '''''
    return (True,str)
           (False,str)
    '''''
    def deleteApiKeyByHashedValue(self,keyHashedValue) -> bool and str:
        return ApiKey().deleteApiKeyByHashedValue(keyHashedValue)