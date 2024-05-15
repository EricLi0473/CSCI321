import mysql.connector
class UploadedStockData:
    def __init__(self,stockId = None,uploadedTickerSymbol = None,keyHashedValue = None,stockStrSeries = None,uploadDataTime = None):
        self.stockId = stockId
        self.uploadedTickerSymbol = uploadedTickerSymbol
        self.keyHashedValue = keyHashedValue
        self.stockStrSeries = stockStrSeries
        self.uploadDataTime = uploadDataTime
    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )
    def storeStockData(self,uploadedTickerSymbol,keyHashedValue,stockStrSeries) -> None:
        mydb = self.connectToDatabase()
        sql = "INSERT INTO uploadedstockdata (uploadedTickerSymbol,keyHashedValue,stockStrSeries) VALUES (%s,%s,%s)"
        val = (uploadedTickerSymbol,keyHashedValue,stockStrSeries)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def getAllStockData(self) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM uploadedstockdata"
        cursor = mydb.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        stocksData = [UploadedStockData(*record) for record in records]
        cursor.close()
        return stocksData

    def getStockDataById(self,stockId) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM uploadedstockdata WHERE stockId = %s"
        val = (stockId,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        return UploadedStockData(*result)

    def getStockDataBySymbol(self,uploadedTickerSymbol) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM uploadedstockdata WHERE uploadedTickerSymbol = %s"
        val = (uploadedTickerSymbol,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        records = cursor.fetchall()
        stocksData = [UploadedStockData(*record) for record in records]
        cursor.close()
        return stocksData
