import datetime
import json
import mysql.connector
class PredictionData:
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

    def commitNReturnRowID(self, sql, val):
        with self.mydb.cursor() as cursor:
            cursor.execute(sql, val)
            self.mydb.commit()
            return cursor.lastrowid

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()
    def insert_predictionData(self,id,symbol,min,avg,max,buy,hold,sell, timeRange, target,accountId,model,rawData) -> None or Exception:
        sql = """
        UPDATE predictiondata 
        SET 
            stockSymbol = %s,
            minPredictedPrice = %s,
            avgPredictedPrice = %s,
            maxPredictedPrice = %s,
            buyPercentage = %s,
            holdPercentage = %s,
            sellPercentage = %s,
            timeRange = %s,
            target = %s,
            accountId = %s,
            model = %s,
            rawData = %s,
            requestDate = CURRENT_TIMESTAMP
        WHERE predictionId = %s
        """
        lastId = self.commitNReturnRowID(sql, (symbol, min, avg, max, buy, hold, sell, timeRange, target, accountId, model, rawData, id))
        return lastId

    def get_predictionData_by_symbol(self,symbol) -> dict:
        sql = "SELECT * FROM predictiondata WHERE stockSymbol=%s AND rawData IS NOT NULL ORDER BY requestDate DESC LIMIT 1;"
        result = self.fetchOne(sql, (symbol,))
        if result is None:
            return {}
        elif result and 'rawData' in result:
            result['rawData'] = json.loads(result['rawData'])
        return result
    def get_all_predictionData(self,date:str ) -> list:
        sql = "SELECT * FROM predictiondata JOIN account on predictiondata.accountId = account.accountId WHERE requestDate >= %s ORDER BY requestDate DESC;"
        results =  self.fetchAll(sql, (date,))
        if results is None:
            return []
        for result in results:
            if result['rawData'] is not None:
                result['rawData'] = json.loads(result['rawData'])
        return results
    def get_all_precessing_predictionData(self) -> list:
        sql = "SELECT * FROM predictiondata WHERE rawData IS NULL"
        return self.fetchAll(sql, "")
    def get_predictionData_by_accountId(self,accountId,date:str ) -> list:
        sql = "SELECT * FROM predictiondata WHERE accountId=%s AND requestDate >= %s ORDER BY requestDate DESC"
        results =  self.fetchAll(sql, (accountId,date))
        if results is None:
            return []
        for result in results:
            if result['rawData'] is not None:
                result['rawData'] = json.loads(result['rawData'])
        return results


    def  pre_store_prediction_result(self,symbol,timeRange,accountId,model) -> int:
        sql = "INSERT INTO predictiondata(stockSymbol, timeRange, accountId, model) VALUES (%s, %s, %s, %s)"
        values = (symbol, timeRange, accountId, model)
        lastId = self.commitNReturnRowID(sql, values)
        return lastId

    def delete_predictionData_by_id(self,predictionId):
        sql = "DELETE FROM predictiondata WHERE predictionId=%s"
        values = (predictionId,)
        self.commit(sql, values)
if __name__ == "__main__":
    # PredictionData().insert_predictionData(13,"AAPL",1,2,3,4,5,6,15,"Buy","1","LSTM","raw")
    print(PredictionData().get_all_precessing_predictionData())
    # print(PredictionData().pre_store_prediction_result("AAPL",14,1,"LSTM"))
    # print(PredictionData().get_predictionData_by_symbol("AAPL"))
