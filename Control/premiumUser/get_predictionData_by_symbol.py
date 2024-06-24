from Entity.predictiondata import *
class GetPredictionDataBySymbol:
    def __init__(self):
        pass

    def get_predictionData_by_symbol(self, symbol):
        return PredictionData().get_predictionData_by_symbol(symbol)