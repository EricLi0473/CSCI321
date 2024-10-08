import mysql.connector
class Preference:
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
            return cursor.lastrowid
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()

    def get_preference_by_accountId(self, accountId):
        sql = "SELECT * FROM preferences LEFT JOIN account ON preferences.accountId = account.accountId WHERE preferences.accountId = %s "
        val = (accountId,)
        return self.fetchOne(sql, val)

    def set_preference_by_accountId(self, accountId, preferenceIndustry,preferenceCountry):
        sql = "INSERT INTO preferences(accountId, preferenceIndustry,preferenceCountry) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE preferenceIndustry=VALUES(preferenceIndustry),preferenceCountry=VALUES(preferenceCountry)"
        val = (accountId, preferenceIndustry, preferenceCountry)
        self.commit(sql, val)

    def update_ReceiveNotification_by_accountId(self, accountId, receiveNotification):
        sql = "UPDATE preferences SET receiveNotification = %s WHERE accountId = %s"
        val = (receiveNotification,accountId)
        self.commit(sql, val)
        return receiveNotification

if __name__ == "__main__":
    print(Preference().get_preference_by_accountId("2"))
