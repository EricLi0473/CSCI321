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
            auth_plugin='mysql_native_password'
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
        sql = "SELECT * FROM individualaccount WHERE userName = %s"
        result = self.fetchOne(sql, (userName,))
        if result:
            if result['status'] == 'invalid':
                raise Exception("Your account has been banned.")
            elif result['hashedPassword'] == HashPassword:
                return result
            else:
                raise Exception("Incorrect password")
        else:
            raise Exception("Account does not exist")

    def signup(self, userName, apikey, hashedPassword, email, profile) -> dict or Exception:
        sql = "SELECT * FROM individualaccount WHERE userName = %s"
        if self.fetchAll(sql, (userName,)):
            raise Exception("UserName already exists")
        sql = "INSERT INTO individualaccount (userName, apikey, hashedPassword, email, profile) VALUES (%s, %s, %s, %s, %s)"
        last_id = self.commit(sql, (userName, apikey, hashedPassword, email, profile))
        sql = "SELECT * FROM individualaccount WHERE accountId = %s"
        result = self.fetchOne(sql, (last_id,))
        return result

    def findOneAccount(self, accountId) -> dict or Exception:
        sql = "SELECT * FROM individualaccount WHERE accountId = %s"
        result = self.fetchOne(sql, (accountId,))
        if not result:
            raise Exception("Account does not exist")
        return result

    def updateAccount(self, user):
        self.collection.update_one({'accountId': user['accountId']}, {"$set": user})
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()


# 示例代码
# account_instance = IndividualAccount()
# for i in range(0, 100):
#
#     print(account_instance.findOneAccount("1"))
