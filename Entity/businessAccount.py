import mysql.connector
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
    def fetchOne(self,sql,val) -> tuple:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchAll(self,sql,val) -> tuple:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        return result
    def verifyAccount(self, userName, HashPassword) -> dict or Exception:
        sql = "SELECT * FROM businessaccount WHERE userName = %s"
        result = self.fetchOne(sql, (userName,))
        if result:
            if result['status'] == 'invalid':
                raise Exception("Your account has been banned.")
            elif result['hashedPassword'] == HashPassword:
                result['accountType'] = 'business'
                return result
            elif result['hashedPassword'] != HashPassword:
                raise Exception("incorrect password")
        else:
            raise Exception("Account does not exist")
