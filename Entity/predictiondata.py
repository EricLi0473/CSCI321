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

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()
    def insert_predictionData(self,symbol,min,avg,max,buy,hold,sell) -> None or Exception:
        sql = "INSERT INTO predictiondata (stockSymbol, minPredictedPrice, avgPredictedPrice, maxPredictedPrice, buyPercentage,holdPercentage,sellPercentage) VALUES (%s, %s, %s, %s, %s,%s,%s)"
        self.commit(sql, (symbol,min,avg,max,buy,hold,sell))
    def get_predictionData_by_symbol(self,symbol) -> dict:
        sql = "SELECT * FROM predictiondata WHERE stockSymbol=%s"
        result = self.fetchOne(sql, (symbol,))
        return result

if __name__ == "__main__":
    PredictionData().insert_predictionData("aapl","10.5","10.5","10.5","10.5","10.5","10.5")
    print(PredictionData().get_predictionData_by_symbol("AAPL"))