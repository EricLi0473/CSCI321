import secrets
import string
import hashlib
from Entity.apiKey import *
class GenerateApiKeyController:
    def __init__(self):
        pass
    '''''
    return APIKey:string
    Store (hashed_api_key, keyOwnerName, keyOwnerOccupation):string into db
    '''''
    def generateApiKey(self,keyOwnerName,keyOwnerOccupation) -> str:
        # api_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        # hashed_api_key = hashlib.md5(api_key.encode()).hexdigest()
        # ApiKey().storeAnApiKey(hashed_api_key, keyOwnerName, keyOwnerOccupation)
        return "BYEEDmE66M7LV1xQ"

# print(GenerateApiKeyController().generateApiKey('admin', 'admin'))