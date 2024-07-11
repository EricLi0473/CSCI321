import mysql.connector
class WatchListSymbol:
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

    def fetchOne(self, sql, val,dictionary=True) -> dict:
        with self.mydb.cursor(dictionary=dictionary) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchone()
        return result

    def fetchAll(self, sql, val,dictionary=True) -> list:
        with self.mydb.cursor(dictionary=dictionary) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchall()
        return result

    def commit(self, sql, val):
        with self.mydb.cursor() as cursor:
            cursor.execute(sql, val)
            self.mydb.commit()
            return cursor.lastrowid

    def commitMany(self,sql,val):
        with self.mydb.cursor() as cursor:
            cursor.executemany(sql, val)
            self.mydb.commit()
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()


    def getWatchListSymbol_by_accountId(self,accountId):
        sql = "select * from watchList_symbol where accountId=%s"
        val = (accountId,)
        return self.fetchAll(sql, val)

    def updateWatchListSymbol_by_accountId(self,values:list[dict]):
        sql = """
        INSERT INTO watchList_symbol (watchList_symbol_id, accountId, symbol, priceInWatchList)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        accountId = VALUES(accountId),
        symbol = VALUES(symbol),
        priceInWatchList = VALUES(priceInWatchList)
        """
        val = [(item['watchList_symbol_id'], item['accountId'], item['symbol'], item['priceInWatchList']) for item in values]
        self.commitMany(sql, val)

if __name__ == '__main__':
    d = [{'watchList_symbol_id': 1, 'accountId': 1, 'symbol': 'AAPL', 'priceInWatchList': 150.0}, {'watchList_symbol_id': 2, 'accountId': 1, 'symbol': 'BILI', 'priceInWatchList': 200.0}]

    print(WatchListSymbol().getWatchListSymbol_by_accountId("2"))