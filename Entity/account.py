import mysql.connector

class Account:
    def __init__(self, accountId=None, accountName=None, accountHashPassword=None, accountEmail=None,accountBio=None,accountProfile=None,accountStatus=None,accountCreateDate=None
                 ,keyHashedValue=None):
        self.accountId = accountId
        self.accountName = accountName
        self.accountHashPassword = accountHashPassword
        self.accountEmail = accountEmail
        self.accountBio = accountBio
        self.accountProfile = accountProfile
        self.accountStatus = accountStatus
        self.accountCreateDate = accountCreateDate
        self.keyHashedValue = keyHashedValue



    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )

    def getTheProfile(self, userName):
        mydb = self.connectToDatabase()
        sql = "SELECT profile FROM individualaccount WHERE userName = %s "
        val = (userName,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        if cursor.fetchone() is None:
            sql = "SELECT profile FROM businessaccount WHERE userName = %s "
            cursor.execute(sql, val)
            result = cursor.fetchone()
            cursor.close()
            if cursor.fetchone() is None:
                return None
            else:
                return 'business'
        cursor.close()
        return 'individual'

    def verifyAccount(self, accountName, accountHashPassword) -> bool and str:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM account WHERE accountName = %s"
        val = (accountName,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        if result:
            if result[6] == 'invalid':
                return False,"Your account has been banned."
            elif result[2] == accountHashPassword:
                return True,Account(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8])
            elif result[2] != accountHashPassword:
                return False,"incorrect password"
        else:
            return False,"Account does not exist"

    def getAllAccounts(self) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM account"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        accountsList = []
        for _ in result:
            accountItem = Account(*_)
            accountsList.append(accountItem)
        return accountsList

    def updateAccount(self,accountId, accountName,accountHashedPassword,accountEmail,accountBio,accountStatus) -> bool:
        try:
            mydb = self.connectToDatabase()
            sql = 'UPDATE account SET accountName = %s, accountHashedPassword = %s, accountEmail = %s, accountBio = %s, accountStatus = %s WHERE accountId = %s'
            val = (accountName,accountHashedPassword,accountEmail,accountBio,accountStatus,accountId)
            cursor = mydb.cursor()
            cursor.execute(sql, val)
            mydb.commit()
            return True
        except Exception:
            return False

    def getAccountByName(self, accountName) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM account WHERE accountName LIKE %s"
        cursor = mydb.cursor()
        cursor.execute(sql, ('%' + accountName + '%',))
        result = cursor.fetchall()
        accountsData = [Account(*_) for _ in result]
        cursor.close()
        return accountsData
    def freezeAnAccount(self,accountId) -> None:
        mydb = self.connectToDatabase()
        sql = "UPDATE account SET accountStatus = 'invalid' WHERE accountId = %s "
        val = (accountId,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def unFreezeAnAccount(self,accountId) -> None:
        mydb = self.connectToDatabase()
        sql = "UPDATE account SET accountStatus = 'valid' WHERE accountId = %s "
        val = (accountId,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def deleteAnAccountById(self, accountId) -> bool and str:
        try:
            mydb = self.connectToDatabase()
            sql = "DELETE FROM account WHERE accountId = %s"
            val = (accountId,)
            cursor = mydb.cursor()
            cursor.execute(sql, val)
            mydb.commit()
            cursor.close()
        except Exception:
            return False,"Account does not exist"
        else:
            return True,"Account deleted"
    def createAnAccount(self,accountName,accountHashedPassword,accountEmail,accountBio,accountProfile,accountStatus,keyHashedValue) -> bool and str:
        try:
            mydb = self.connectToDatabase()
            sql = ' INSERT INTO account (accountName, accountHashedPassword, accountEmail, accountBio, accountProfile, accountStatus, keyHashedValue) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            val = (accountName,accountHashedPassword,accountEmail,accountBio,accountProfile,accountStatus,keyHashedValue)
            cursor = mydb.cursor()
            cursor.execute(sql, val)
            mydb.commit()
            cursor.close()
        except Exception:
            return False, "Account creation failed, check your key value."
        else:
            return True, "Account created"

