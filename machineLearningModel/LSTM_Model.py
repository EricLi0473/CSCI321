import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
import matplotlib.pyplot as plt
from machineLearningModel.get_symbol_data import *


class LSTM_Model:
    def __init__(self, symbol, df, n_days, layers, neurons):
        self.symbol = symbol
        self.df = df[["Adj Close", "Volume", "treasury_yield", "FEDERAL_FUNDS_RATE"]].copy()
        self.df.rename(columns={"Adj Close": "Price"}, inplace=True)
        self.n_days = n_days
        self.layers = layers
        self.neurons = neurons
        self.look_back = 60
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.data_normalized = self.scaler.fit_transform(self.df)
        self.model = self.build_model()
        self.full_index = self.df.index

    def create_dataset(self, dataset, look_back):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back)]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    def build_model(self):
        model = Sequential()
        model.add(Input(shape=(self.look_back, self.df.shape[1])))
        for i in range(self.layers):
            if i == 0:
                model.add(LSTM(self.neurons, return_sequences=True if self.layers > 1 else False))
            elif i == self.layers - 1:
                model.add(LSTM(self.neurons))
            else:
                model.add(LSTM(self.neurons, return_sequences=True))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def train_model(self):
        train_size = int(len(self.data_normalized) * 0.8)
        train, test = self.data_normalized[0:train_size, :], self.data_normalized[train_size:len(self.data_normalized),
                                                             :]

        trainX, trainY = self.create_dataset(train, self.look_back)
        testX, testY = self.create_dataset(test, self.look_back)

        trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], trainX.shape[2]))
        testX = np.reshape(testX, (testX.shape[0], testX.shape[1], testX.shape[2]))

        self.model.fit(trainX, trainY, epochs=10, batch_size=16, verbose=2)

        trainPredict = self.model.predict(trainX)
        testPredict = self.model.predict(testX)

        trainPredict = self.scaler.inverse_transform(
            np.concatenate([trainPredict, np.zeros((trainPredict.shape[0], self.df.shape[1] - 1))], axis=1))[:, 0]
        trainY = self.scaler.inverse_transform(
            np.concatenate([trainY.reshape(-1, 1), np.zeros((trainY.shape[0], self.df.shape[1] - 1))], axis=1))[:, 0]
        testPredict = self.scaler.inverse_transform(
            np.concatenate([testPredict, np.zeros((testPredict.shape[0], self.df.shape[1] - 1))], axis=1))[:, 0]
        testY = self.scaler.inverse_transform(
            np.concatenate([testY.reshape(-1, 1), np.zeros((testY.shape[0], self.df.shape[1] - 1))], axis=1))[:, 0]

        trainScore = np.sqrt(np.mean((trainPredict - trainY) ** 2))
        testScore = np.sqrt(np.mean((testPredict - testY) ** 2))

        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))

        return trainPredict, testPredict

    def plot_predictions(self, trainPredict, testPredict):
        trainPredictPlot = np.empty_like(self.data_normalized[:, 0])
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[self.look_back:len(trainPredict) + self.look_back] = trainPredict

        testPredictPlot = np.empty_like(self.data_normalized[:, 0])
        testPredictPlot[:, :] = np.nan
        testPredictPlot[len(trainPredict) + (self.look_back * 2) + 1:len(self.data_normalized) - 1] = testPredict

        plt.figure(figsize=(15, 6))
        plt.plot(self.full_index, self.scaler.inverse_transform(self.data_normalized)[:, 0], label='Actual Price')
        plt.plot(self.full_index, trainPredictPlot, label='Train Predictions')
        plt.plot(self.full_index, testPredictPlot, label='Test Predictions')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title('LSTM Model Predictions')
        plt.show()

    def predict_future(self):
        last_sequence = self.data_normalized[-self.look_back:]
        future_predictions = []

        for _ in range(self.n_days):
            next_pred = self.model.predict(last_sequence.reshape(1, self.look_back, self.df.shape[1]))
            next_pred_full = np.concatenate([next_pred, np.zeros((1, self.df.shape[1] - 1))], axis=1)
            future_predictions.append(next_pred[0, 0])
            last_sequence = np.append(last_sequence[1:], next_pred_full, axis=0)

        future_predictions = self.scaler.inverse_transform(
            np.concatenate([np.array(future_predictions).reshape(-1, 1), np.zeros((self.n_days, self.df.shape[1] - 1))],
                           axis=1))[:, 0]
        future_dates = [self.full_index[-1] + timedelta(days=i) for i in range(1, self.n_days + 1)]
        future_df = pd.DataFrame(
            {'Date': future_dates, 'Predicted': future_predictions})
        future_df.set_index('Date', inplace=True)
        window_size = 5
        future_df['SMA'] = future_df['Predicted'].rolling(window=window_size).mean()

        def generate_recommendation(row):
            if row['Predicted'] > row['SMA']:
                return 'Buy'
            elif row['Predicted'] < row['SMA']:
                return 'Sell'
            else:
                return 'Hold'

        future_df['Recommendation'] = future_df.apply(generate_recommendation, axis=1)


        # 使用过去的股票价格生成推荐
        self.df['Short_SMA'] = self.df['Price'].rolling(window=10).mean()
        self.df['Long_SMA'] = self.df['Price'].rolling(window=50).mean()

        future_df['Past_Short_SMA'] = self.df['Short_SMA'].iloc[-self.n_days:].values
        future_df['Past_Long_SMA'] = self.df['Long_SMA'].iloc[-self.n_days:].values

        def combined_recommendation(row):
            if row['Past_Short_SMA'] > row['Past_Long_SMA'] and row['Predicted'] > row['SMA']:
                return 'Buy'
            elif row['Past_Short_SMA'] < row['Past_Long_SMA'] and row['Predicted'] < row['SMA']:
                return 'Sell'
            else:
                return 'Hold'

        future_df['Recommendation'] = future_df.apply(combined_recommendation, axis=1)

        future_df = future_df.reset_index()
        future_df['Date'] = future_df['Date'].dt.strftime('%Y-%m-%d')
        result = future_df[['Date', 'Predicted', 'Recommendation']].to_dict(orient='records')
        for record in result:
            record['Predicted'] = round(record['Predicted'], 2)
        print(self.df.info())
        return result

    def predict(self):
        trainPredict, testPredict = self.train_model()
        # self.plot_predictions(trainPredict, testPredict)
        result = self.predict_future()

        return result


if __name__ == "__main__":
    df = GetSymbolData().fetch_data("AAPL")
    model = LSTM_Model('AAPL', df, n_days=10, layers=4, neurons=64)
    future_predictions = model.predict()
    for i in future_predictions:
        print(i)
# # 示例用法
# end_date = datetime.today().date()
# start_date = (end_date - timedelta(days=365 * 5))
# ticker_symbol = "AAPL"
# df = yf.download(ticker_symbol, start=start_date, end=end_date)
# all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
# df = df.reindex(all_dates)
# df = df.fillna(method='ffill')
# #
# model = LSTM_Model('AAPL', df, n_days=10, layers=4, neurons=64)
# future_predictions = model.predict()
# print(future_predictions)
