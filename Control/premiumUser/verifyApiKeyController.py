from Entity.account import *
class VerifyApiKeyController():
    def __init__(self):
        pass

    def verifyApiKey(self,key):
        account = Account().verify_AccountBy_apikey(key)
        if account:
            return account
        else:
            raise Exception("Please enter right api key")

if __name__ == '__main__':
    print(VerifyApiKeyController().verifyApiKey("1"))
