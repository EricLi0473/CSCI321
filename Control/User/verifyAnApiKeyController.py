from Entity.apiKey import *
import hashlib
class verifyAnApiKeyController():
    def __init__(self):
        pass

    def verifyAnApiKey(self, apiKey) -> bool:
        return ApiKey().verifyAnApiKey(hashlib.md5(apiKey.encode()).hexdigest())

