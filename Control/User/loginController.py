import hashlib
from Entity.account import *


class LoginController:
    def __init__(self):
        pass
    '''''
    return ('True',Account:Object)  or ('False',"reason":str)
    '''''
    def verifyAccount(self,accountName,accountPassword) -> bool and str:
        return Account().verifyAccount(accountName,hashlib.md5(accountPassword.encode()).hexdigest())


# verify =  LoginController().verifyAccount("li","123456")
# if verify[0]:
#     print("Login Successful")
# elif verify[0] is False:
#     print(verify[1])

