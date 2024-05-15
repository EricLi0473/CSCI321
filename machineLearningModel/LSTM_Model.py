import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from datetime import datetime, timedelta
import yfinance as yf

def get_stock_data(symbol):
    try:
        end_date = datetime.today().date()
        start_date = (end_date - timedelta(days=365 * 5))
        df = yf.download(symbol, start=start_date, end=end_date)
        all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        df = df.reindex(all_dates)
        df = df.fillna(method='ffill')
    except Exception:
        raise Exception(f"Stock with symbol '{symbol}' not found.")
    return df

class LSTM_Model:
    def __init__(self, tickerSymbol,df, forecast_day, layers, neurons_per_layer):
        self.tickerSymbol = tickerSymbol
        self.df = df
        self.forecast_day = forecast_day
        self.layers = layers
        self.neurons_per_layer = neurons_per_layer
        self.scaler = MinMaxScaler(feature_range=(0, 1))  # Add scaler attribute
        self.preprocess_data()

    def preprocess_data(self):
        OHLC_avg = self.df[['Adj Close', 'Open', 'High', 'Low']].mean(axis=1)
        OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg), 1))
        self.scaled_data = self.scaler.fit_transform(OHLC_avg)  # Use scaler to fit and transform data
        self.build_model()

    def new_dataset(self, dataset, step_size):
        data_X, data_Y = [], []
        for i in range(len(dataset) - step_size - 1):
            a = dataset[i:(i + step_size), 0]
            data_X.append(a)
            data_Y.append(dataset[i + step_size, 0])
        return np.array(data_X), np.array(data_Y)

    def build_model(self):
        self.model = Sequential()
        self.model.add(LSTM(self.neurons_per_layer, input_shape=(1, 1), return_sequences=True))
        for _ in range(self.layers - 2):
            self.model.add(LSTM(self.neurons_per_layer, return_sequences=True))
        self.model.add(LSTM(self.neurons_per_layer))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.train_model()

    def train_model(self):
        for _ in range(self.forecast_day):
            trainX, trainY = self.new_dataset(self.scaled_data, 1)  # Use scaled data
            trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            self.model.fit(trainX, trainY, epochs=10, batch_size=64, verbose=2)

            last_val = self.scaled_data[-1]
            next_val = self.model.predict(np.reshape(last_val, (1, 1, 1)))
            self.scaled_data = np.append(self.scaled_data, next_val[0])
            self.scaled_data = self.scaled_data.reshape(-1, 1)
            self.predict()

    def predict(self):
        next_val = self.scaler.inverse_transform(self.scaled_data[-self.forecast_day:])  # Use same scaler object
        next_val = next_val.flatten()
        future_dates = pd.date_range(start=self.df.index[-1], periods=self.forecast_day + 1)[1:]
        predictions_df = pd.DataFrame({'Date': future_dates, f'LSTM Predicted Price for {self.tickerSymbol} ': next_val})
        predictions_df.set_index('Date', inplace=True)
        json_string = predictions_df.to_json(date_format='iso').replace('T00:00:00.000', '')
        return json_string



# df = pd.read_csv('D:/Users/cesir/PycharmProjects/flaskProject/bili.csv')
# df = get_stock_data("aapl")
#
# stock_predictor = LSTM_Model(df, forecast_day=5, layers=2, neurons_per_layer=16)
# result = stock_predictor.predict()
# print("Next n Days Value:", result)
