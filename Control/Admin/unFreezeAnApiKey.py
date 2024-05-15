from Entity import apiKey
from Entity.apiKey import *
import hashlib
class UnFreezeAnApiKey:
    def __init__(self):
        pass
    def unFreeze_anApiKey(self,apiKey) -> None:
        ApiKey().unFreezeAnApiKey(hashlib.md5(apiKey.encode()).hexdigest())