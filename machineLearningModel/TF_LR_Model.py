import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import yfinance as yf
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class LinearRegression_Model:
    @staticmethod
    def get_stock_data(symbol):
        try:
            end_date = datetime.today().date()
            start_date = (end_date - timedelta(days=365 * 50))
            df = yf.download(symbol, start=start_date, end=end_date)
            all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            df = df.reindex(all_dates)
            df = df.fillna(method='ffill')
        except Exception:
            raise Exception(f"Stock with symbol '{symbol}' not found.")
        return df

    def __init__(self, tickerSymbol,df, forecast_out, layersNum=2, neuronsNum=8):
        self.tickerSymbol = tickerSymbol
        self.df = df
        self.forecast_out = forecast_out
        self.layersNum = layersNum
        self.neuronsNum = neuronsNum

    # Feature engineering and data preprocessing
    def prepare_data(self):
        df = self.df
        df['HL_PCT'] = (df['High'] - df['Adj Close']) / df['Adj Close'] * 100.0
        df['PCT_change'] = (df['Adj Close'] - df['Open']) / df['Open'] * 100.0
        df = df[['Adj Close', 'HL_PCT', 'PCT_change', 'Volume']]
        df['label'] = df['Adj Close'].shift(-self.forecast_out)
        df.dropna(inplace=True)
        X = np.array(df.drop(['label'], axis=1))
        X = preprocessing.scale(X)
        y = np.array(df['label'])
        return X, y

    # Linear regression modelling
    def build_model(self, input_shape):
        model = Sequential()
        model.add(Dense(self.neuronsNum, activation='relu', input_shape=input_shape))
        for _ in range(self.layersNum - 1):
            model.add(Dense(self.neuronsNum, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])
        return model

    # Forecasting stock prices
    def predict_stock_price(self):
        try:
            # Prepare data
            df = self.df

            if len(df) < 3650:
                batch_size = 32
            elif len(df) < 7300:
                batch_size = 64
            else:
                batch_size = 128

            X, y = self.prepare_data()

            # Delineate training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Modelling
            input_shape = (X_train.shape[1],)
            model = self.build_model(input_shape)

            # Training models
            model.fit(X_train, y_train, epochs=100, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1)

            # Assessment models
            loss = model.evaluate(X_test, y_test, verbose=0)
            print("Test Loss:", loss)

            # Make projections
            forecast_set = model.predict(X[-self.forecast_out:])
            forecast_set = forecast_set.flatten()

            future_dates = pd.date_range(start=df.index[-1], periods=self.forecast_out + 1)[1:]

            # Combine dates and predictions into a DataFrame
            predictions_df = pd.DataFrame({'Date': future_dates, f'TF_LR Predicted Price for {self.tickerSymbol}': forecast_set})
            predictions_df.set_index('Date', inplace=True)
            json_string = predictions_df.to_json(date_format='iso').replace('T00:00:00.000', '')
        except Exception as e:
            raise e
        return json_string

# Examples of use
# symbol = "bili"
# forecast_out = 5
# layersNum = 3
# neuronsNum = 8
#
# df = LinearRegression_Model.get_stock_data(symbol)
# forecast_prices = LinearRegression_Model(df, forecast_out, layersNum, neuronsNum).predict_stock_price()
# print(forecast_prices)
