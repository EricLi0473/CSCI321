import mysql.connector
class ThresholdSettings:
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

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()

    def get_threshold_settings_by_id(self, id):
        sql = "SELECT * FROM thresholdsettings WHERE accountId = %s"
        val = (id,)
        return self.fetchAll(sql, val)

    def remove_threshold_settings_by_thresholdId(self, thresholdId):
        sql = "DELETE FROM thresholdsettings WHERE thresholdId = %s"
        val = (thresholdId,)
        self.commit(sql, val)

    # integrate insert and update
    def insert_threshold_settings_by_id(self, accountId,stockSymbol,changePercentage):
        sql = "INSERT INTO thresholdsettings (accountId, stockSymbol, changePercentage) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE changePercentage = VALUES(changePercentage)"
        val = (accountId, stockSymbol, changePercentage)
        self.commit(sql, val)


    def remove_threshold_settings_by_info(self,accountId,stockSymbol):
        sql = "DELETE FROM thresholdsettings WHERE accountId = %s AND stockSymbol = %s"
        val = (accountId, stockSymbol)
        self.commit(sql, val)

if __name__ == "__main__":
    settings = ThresholdSettings()
    print(settings.insert_threshold_settings_by_id("1","a",1.111))
