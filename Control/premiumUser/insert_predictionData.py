from Entity.predictiondata import *
class InsertPredictionData:
    def __init__(self):
        pass
    def insert_predictionData(self, symbol,min,avg,max,buy,hold,sell):
        PredictionData().insert_predictionData(symbol,min,avg,max,buy,hold,sell)