import mysql.connector
from pandas.io import sql


class SearchHistory:
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


    def get_searchHistory_by_id(self,accountId):
        sql = "SELECT * FROM searchHistory WHERE accountId = %s ORDER BY searchDate DESC"
        val = (accountId,)
        return self.fetchAll(sql, val)

    def insert_searchHistory_by_id(self,accountId,stockSymbol):
        sql = "INSERT INTO searchHistory (accountId, stockSymbol) VALUES (%s, %s) ON DUPLICATE KEY UPDATE searchDate = CURRENT_TIMESTAMP;"
        val = (accountId, stockSymbol)
        self.commit(sql, val)

    def remove_searchHistory_by_id(self,searchId):
        sql = "DELETE FROM searchHistory WHERE searchId = %s"
        val = (searchId,)
        self.commit(sql, val)

if __name__ == '__main__':
    print(SearchHistory().insert_searchHistory_by_id("1","AAPL"))