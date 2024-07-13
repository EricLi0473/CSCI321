from Entity.predictiondata import *
class DeletePredictionDataByID:
    def __init__(self):
        pass

    def delete_prediction_data_by_id(self, predictionId):
        return PredictionData().delete_predictionData_by_id(predictionId)