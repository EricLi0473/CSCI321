import mysql.connector
class Watchlist():
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

    def get_watchlist_by_accountID(self,accountId):
        sql = "select * from watchlist where accountId=%s"
        val = (accountId,)
        return self.fetchOne(sql, val)

    def update_watchlist(self, accountId, stockSymbol):
        sql = '''INSERT INTO watchlist (accountId, stockSymbol)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE
stockSymbol = VALUES(stockSymbol);'''
        val = (accountId,stockSymbol)
        self.commit(sql, val)

    def is_stock_in_watchlist(self, accountId, stockSymbol):
        try:
            cursor = self.mydb.cursor(dictionary=True)
            sql = "SELECT * FROM watchlist WHERE accountId = %s AND stockSymbol = %s"
            cursor.execute(sql, (accountId, stockSymbol))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except mysql.connector.Error as e:
            print("Database error:", e)
            return False

    def add_to_watchlist(self, accountId, stockSymbol):
        if not self.is_stock_in_watchlist(accountId, stockSymbol):
            try:
                cursor = self.mydb.cursor()
                sql = "INSERT INTO watchlist (accountId, stockSymbol) VALUES (%s, %s)"
                cursor.execute(sql, (accountId, stockSymbol))
                self.mydb.commit()
                cursor.close()
                return True
            except mysql.connector.Error as e:
                print("Database error:", e)
                return False
        else:
            return False

if __name__ == "__main__":
    Watchlist().get_watchlist_by_accountID("1")