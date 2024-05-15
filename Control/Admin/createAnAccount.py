from Entity.account import *
import hashlib
class CreateAccount:
    def __init__(self):
        pass
    '''''
    return (True,str)(False,str)
    '''''
    def createAnAccount(self,accountName,accountPassword,accountEmail,accountBio,accountProfile,accountStatus,keyValue):
        return Account().createAnAccount(accountName,hashlib.md5(accountPassword.encode()).hexdigest(),accountEmail,accountBio,accountProfile,accountStatus,hashlib.md5(keyValue.encode()).hexdigest())


