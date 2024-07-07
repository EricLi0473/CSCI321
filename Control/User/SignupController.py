from Entity.account import *
import secrets
import string
import hashlib
import re
class SignupController:
    def __init__(self):
        pass
    def individualSignUp(self,firstName,lastName,email,password,confirmPassword,age,sex,occupation,incomeLevel,netWorth,investmentExperience,riskTolerance,investmentGoals,profile) -> dict or Exception:
        return Account().signUp(f"{lastName}"+" "+f"{firstName}",hashlib.md5(password.encode()).hexdigest(),email,profile,age,sex,occupation,incomeLevel,netWorth,investmentExperience,riskTolerance,investmentGoals)


