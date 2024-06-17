import mysql.connector
import ast
import time
import json

class RequestRecord:
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

    def storeRequestRecord1(self, keyHashedValue, requestTickerSymbol, requestTimeFrame, requestModel, requestLayersNum,
                           requestNeuronsPerLayer, requestForecastResult) -> None:
        sql = "INSERT INTO requestrecord (keyHashedValue, requestTickerSymbol, requestTimeFrame, requestModel, requestLayersNum, requestNeuronsPerLayer, requestForecastResult) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (
        keyHashedValue, requestTickerSymbol, requestTimeFrame, requestModel, requestLayersNum, requestNeuronsPerLayer,
        requestForecastResult)
        self.commit(sql, val)

    def getAllRequestRecord(self):
        sql = "SELECT * FROM requestrecord"
        records = self.fetchAll(sql, ())
        return records

    def getRequestRecordByApiKey(self, apikey) -> list[dict] or Exception:
        sql = "SELECT * FROM requestrecord where apikey = %s"
        result = self.fetchAll(sql, (apikey,))
        for record in result:
            if record["forecastResult"] != 'waiting':
                record["forecastResult"] = ast.literal_eval(record["forecastResult"])
        return result

    def deleteRequestRecordById(self, requestId) -> None:
        sql = "DELETE FROM requestrecord WHERE requestId = %s"
        self.commit(sql, (requestId,))

    def storeRequestRecord(self,apikey,tickerSymbol,timeFrame,model,layersNum,neuronsPerLayer,forecastResult = "waiting"):
        sql = "INSERT INTO requestrecord (apikey,tickerSymbol,timeFrame,model,layersNum,neuronsPerLayer,forecastResult) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (apikey, tickerSymbol, timeFrame, model, layersNum, neuronsPerLayer,forecastResult)
        id = self.commit(sql, val)
        return id
    def updateResult(self,requestId,forecastResult):
        try:
            forecastResult = json.dumps(forecastResult)
            sql = "UPDATE requestrecord SET forecastResult = %s WHERE requestId = %s"
            val = (forecastResult, requestId)
            self.commit(sql, val)
        except Exception as e:
            pass
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()
# 示例代码
# request_record_instance = RequestRecord()
# for i in range(0, 100):
#     print(i)
#     print(request_record_instance.getRequestRecordByApiKey("abcdefg"))
#     time.sleep(0.1)
