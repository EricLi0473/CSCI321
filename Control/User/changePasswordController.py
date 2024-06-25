
import hashlib
class ChangePasswordController:
    def __init__(self):
        pass

    def changeIndividualPassword(self,userName,oldPassword,newPassword) -> str or Exception:
        return IndividualAccount().updatePasswordByName(userName,hashlib.md5(newPassword.encode()).hexdigest())
