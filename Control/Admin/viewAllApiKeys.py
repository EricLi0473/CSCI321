from Entity.apiKey import *
class ViewAllApiKeys():
    def __init__(self):
        pass
    '''''
    return List: Object < ApiKey >
    '''''
    def viewAllApiKeys(self):
        return ApiKey().getAllApiKeysInfo()