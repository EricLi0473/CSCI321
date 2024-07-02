import datetime

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
    def insert_predictionData(self,symbol,min,avg,max,buy,hold,sell, timeRange, target) -> None or Exception:
        sql = "INSERT INTO predictiondata (stockSymbol, minPredictedPrice, avgPredictedPrice, maxPredictedPrice, buyPercentage,holdPercentage,sellPercentage, timeRange, target) VALUES (%s, %s, %s, %s, %s,%s,%s, %s,%s)"
        self.commit(sql, (symbol,min,avg,max,buy,hold,sell, timeRange, target))
    def get_predictionData_by_symbol(self,symbol) -> dict:
        sql = "SELECT * FROM predictiondata WHERE stockSymbol=%s"
        result = self.fetchOne(sql, (symbol,))
        if result is None:
            return {}
        return result

    def insert_or_update_predictionData(self, symbol, min_price, avg_price, max_price, buy, hold, sell, time_range, target):
        current_time = datetime.datetime.now()

        existing_prediction = self.get_predictionData_by_symbol(symbol)

        if existing_prediction:
            # Update existing row
            sql = """
            UPDATE predictiondata
            SET 
                requestDate = %s,
                minPredictedPrice = %s,
                avgPredictedPrice = %s,
                maxPredictedPrice = %s,
                buyPercentage = %s,
                holdPercentage = %s,
                sellPercentage = %s,
                timeRange = %s,
                target = %s
            WHERE stockSymbol = %s
            """
            values = (current_time, min_price, avg_price, max_price, buy, hold, sell, time_range, target, symbol)
            self.commit(sql, values)
            return existing_prediction['predictionId']
        else:
            # Insert new row
            sql = """
            INSERT INTO predictiondata (stockSymbol, requestDate, minPredictedPrice, avgPredictedPrice, maxPredictedPrice, buyPercentage, holdPercentage, sellPercentage, timeRange, target)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (symbol, current_time, min_price, avg_price, max_price, buy, hold, sell, time_range, target)
            prediction_id = self.commitNReturnRowID(sql, values)
            return prediction_id

# if __name__ == "__main__":
    # print("test inserORUpdate")
    # print(PredictionData().insert_or_update_predictionData("aapl", "10", "10", "10", "10", "10", "10", 10, "Buy"))
    # print(PredictionData().insert_or_update_predictionData("L222", "10", "10", "10", "10", "10", "10", 10, "Buy"))
    # print(PredictionData().insert_or_update_predictionData("L444", "10", "10", "10", "10", "10", "10", 10, "Buy"))
    # print(PredictionData().insert_or_update_predictionData("L555", "10", "10", "10", "10", "10", "10", 10, "Buy"))

    # PredictionData().insert_predictionData("aapl","10.5","10.5","10.5","10.5","10.5","10.5")
    # print(PredictionData().get_predictionData_by_symbol("aapl"))