import statistics
from collections import Counter
from Entity.predictiondata import *
class storePredictionResultController():
    def __init__(self):
        pass

    @staticmethod
    def store_prediction_result(symbol, prediction_result):
        db = PredictionData()

        predicted_prices = [pred['Predicted'] for pred in prediction_result]
        min_price = round(min(predicted_prices),2)
        avg_price = round(statistics.mean(predicted_prices),2)
        max_price = round(max(predicted_prices),2)

        recommendations = [pred['Recommendation'] for pred in prediction_result]
        recommendation_counts = Counter(recommendations)
        most_frequent_recommendation = recommendation_counts.most_common(1)[0][0]

        buy_count = recommendation_counts.get('Buy', 0)
        hold_count = recommendation_counts.get('Hold', 0)
        sell_count = recommendation_counts.get('Sell', 0)

        total_count = len(prediction_result)
        buy_percentage = round((buy_count / total_count),1)
        hold_percentage = round((hold_count / total_count),1)
        sell_percentage = round((sell_count / total_count),1)
        time_range = total_count

        prediction_id = db.insert_or_update_predictionData(
            symbol,
            min_price,
            avg_price,
            max_price,
            buy_percentage,
            hold_percentage,
            sell_percentage,
            time_range,
            most_frequent_recommendation
        )
        return prediction_id


# testing purpose
if __name__ == "__main__":
    print(
    storePredictionResultController().store_prediction_result(
        "aapl",
        [
            {'Date': '2024-06-29', 'Predicted': 171.28, 'Recommendation': 'Hold'},
            {'Date': '2024-06-30', 'Predicted': 172.95, 'Recommendation': 'Hold'},
            {'Date': '2024-07-01', 'Predicted': 177.53, 'Recommendation': 'Hold'},
            {'Date': '2024-07-02', 'Predicted': 177.63, 'Recommendation': 'Hold'},
            {'Date': '2024-07-03', 'Predicted': 177.63, 'Recommendation': 'Buy'}
        ]
    )
    )