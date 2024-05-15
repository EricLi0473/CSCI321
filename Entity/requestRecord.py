import mysql.connector
# from aiosqlite import cursor


class RequestRecord:
    def __init__(self,requestId = None,keyHashedValue = None, requestTickerSymbol = None , requestTimeFrame = None, requestModel = None,
                 requestLayersNum = None,requestNeuronsPerLayer = None,requestForecastResult = None,requestDataTime = None):
        self.requestId = requestId
        self.keyHashedValue = keyHashedValue
        self.requestTickerSymbol = requestTickerSymbol
        self.requestTimeFrame = requestTimeFrame
        self.requestModel = requestModel
        self.requestLayersNum = requestLayersNum
        self.requestNeuronsPerLayer = requestNeuronsPerLayer
        self.requestForecastResult = requestForecastResult
        self.requestDataTime = requestDataTime

    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )

    def storeRequestRecord(self,keyHashedValue,requestTickerSymbol,requestTimeFrame,requestModel,requestLayersNum,requestNeuronsPerLayer,requestForecastResult) -> None:
        mydb = self.connectToDatabase()
        sql = "INSERT INTO requestrecord (keyHashedValue,requestTickerSymbol,requestTimeFrame,requestModel,requestLayersNum,requestNeuronsPerLayer,requestForecastResult) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (keyHashedValue,requestTickerSymbol,requestTimeFrame,requestModel,requestLayersNum,requestNeuronsPerLayer,requestForecastResult)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def getAllRequestRecord(self):
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM requestrecord"
        cursor = mydb.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        recordsList = []
        for _ in records:
            request_record = RequestRecord(*_)
            recordsList.append(request_record)
        return recordsList

# requestRecord = RequestRecord()
# requestRecord.storeRequestRecord("8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",'123456','123456','123456','123456','123456')
