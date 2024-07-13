from Entity.predictiondata import *
class GetAllPredictionData:
    def __init__(self):
        pass

    def get_all_predictionData(self,date):
        return PredictionData().get_all_predictionData(date)