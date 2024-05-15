from Entity.apiKey import *
class FindApiKeysByHashedValue:
    def __init__(self):
        pass
    '''''
    fuzzy search, return [Object<APIkey>]
    '''''
    def findApiKeysByHashedValue(self, hashedValue):
        return ApiKey().getApiKeysByHashedValue(hashedValue)
