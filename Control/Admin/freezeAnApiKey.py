from Entity import apiKey
from Entity.apiKey import *
import hashlib
class FreezeAnApiKey:
    def __init__(self):
        pass

    def freeze_anApiKey(self,apiKey) -> None:
        ApiKey().freezeAnApiKey(hashlib.md5(apiKey.encode()).hexdigest())
