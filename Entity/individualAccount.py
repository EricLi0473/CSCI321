import mysql.connector
class IndividualAccount():
    def __init__(self):
        self.mydb = self.connectToDatabase()
    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321",
            auth_plugin = 'mysql_native_password'
        )
    def fetchOne(self,sql,val) -> dict:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchAll(self,sql,val) -> dict:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self,sql,val):
        cursor = self.mydb.cursor()
        cursor.execute(sql, val)
        self.mydb.commit()
        return cursor.lastrowid
    def verifyAccount(self, userName, HashPassword) -> dict or Exception:
        sql = "SELECT * FROM individualaccount WHERE userName = %s"
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

    def signup(self, userName, apikey,hashedPassword,email,profile) -> dict or Exception:
        sql = "SELECT * FROM individualaccount WHERE userName = %s"
        if  self.fetchAll(sql, (userName,)):
            raise Exception("UserName already exists")
        sql = "INSERT INTO individualaccount (userName,apikey,hashedPassword,email,profile) values (%s,%s,%s,%s,%s)"
        last_id = self.commit(sql, (userName, apikey, hashedPassword, email, profile))
        sql = "SELECT * FROM individualaccount WHERE accountId = %s"
        result = self.fetchOne(sql, (last_id,))
        return result

    def findOneAccount(self,accountId) -> dict or Exception:
        sql = "SELECT * FROM individualaccount WHERE accountId = %s"
        result = self.fetchOne(sql, (accountId,))
        if not result:
            raise Exception("Account does not exist")
        return result
