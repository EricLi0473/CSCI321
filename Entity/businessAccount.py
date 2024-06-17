import mysql.connector
from Entity.invitationCode import *
class BusinessAccount():
    def __init__(self):
        self.mydb = self.connectToDatabase()
    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )
    def fetchOne(self, sql, val) -> dict:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchone()
        return result

    def fetchAll(self, sql, val) -> list:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchall()
        return result

    def commit(self, sql, val):
        with self.mydb.cursor() as cursor:
            cursor.execute(sql, val)
            self.mydb.commit()

    def verifyAccount(self, userName, HashPassword) -> dict or Exception:
        sql = "SELECT * FROM businessaccount WHERE userName = %s"
        result = self.fetchOne(sql, (userName,))
        if result:
            if result['status'] == 'invalid':
                raise Exception("Your account has been banned.")
            elif result['hashedPassword'] == HashPassword:
                return result
            elif result['hashedPassword'] != HashPassword:
                raise Exception("incorrect password")
        else:
            raise Exception("Account does not exist")

    def signup(self, userName, apikey,hashedPassword,email,profile,invitationCode = None,companyId = None) -> dict or Exception:
        sql = "SELECT * FROM businessaccount WHERE userName = %s"
        if  self.fetchAll(sql, (userName,)):
            raise Exception("UserName already exists")
        #signup admin and dataManager when register a company account
        if invitationCode is None:
            sql = "insert into businessaccount(userName,apiKey,hashedPassword,email,profile,companyId) values (%s,%s,%s,%s,%s,%s)"
            val = (userName,apikey,hashedPassword,email,profile,companyId)
            accountId = self.commit(sql,val)
            sql = "SELECT * FROM businessaccount WHERE accountId = %s"
            return self.fetchOne(sql, (accountId,))
        #signup when using invitationCode
        sql = "insert into businessaccount(userName,apiKey,hashedPassword,email,profile,companyId) values (%s,%s,%s,%s,%s,%s)"
        companyId = InvitationCode().verifyInvite_AND_Return_CompanyId(invitationCode)
        val = (userName, apikey, hashedPassword, email, profile,
               companyId )
        accountId = self.commit(sql, val)
        sql = "select * from businessaccount where accountId = %s"
        return self.fetchOne(sql, (accountId,))

    def verifyApiKey(self, apiKey) -> bool or Exception:
        try:
            sql = "SELECT status FROM businessaccount WHERE apiKey = %s"
            result = self.fetchOne(sql, (apiKey,))
            if result["status"] != 'valid':
                return False
            else:
                return True
        except Exception as e:
            raise Exception(e)

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()
