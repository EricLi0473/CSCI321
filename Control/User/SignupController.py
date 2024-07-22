from Entity.account import *
import secrets
import string,random
import hashlib
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
class SignupController:
    def __init__(self):
        pass
    def individualSignUp(self,firstName,lastName,email,password,confirmPassword,age,sex,occupation,incomeLevel,netWorth,investmentExperience,riskTolerance,investmentGoals,profile,card_number=None) -> dict or Exception:
        api_key = ''.join(random.choices(string.ascii_letters, k=8))
        if card_number is not None:
            card_number = card_number[-4:]
            nextPaymentDate = (datetime.today() + relativedelta(months=1)).strftime('%Y-%m-%d %H:%M:%S')
        return Account().signUp(f"{lastName}"+" "+f"{firstName}",hashlib.md5(password.encode()).hexdigest(),email,profile,age,sex,occupation,incomeLevel,netWorth,investmentExperience,riskTolerance,investmentGoals,api_key,card_number,nextPaymentDate)


if __name__ == '__main__':
    SignupController().individualSignUp("Li","wei","1","1","1","10","male","a","100","100","novice","low","100","premium","99998888")

