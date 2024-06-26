from machineLearningModel.TF_LR_Model import LinearRegression_Model
from machineLearningModel.LSTM_Model import LSTM_Model
from machineLearningModel.GRU_Model import GRU_Model
from Entity.individualAccount import *

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class RequestForPrediction:
    def __init__(self):
        pass
    def verifyTickerSymbol(self,symbol) -> None:
        try:
            end_date = datetime.today().date()
            start_date = (end_date - timedelta(days=10))
            df = yf.download(symbol, start=start_date, end=end_date)
            all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            df = df.reindex(all_dates)
            df = df.fillna(method='ffill')
        except Exception:
            raise Exception(f"Stock with symbol ' {symbol} ' not found.")


    def get_stock_data(self,symbol) -> pd.DataFrame or Exception:
        try:
            end_date = datetime.today().date()
            start_date = (end_date - timedelta(days=365 * 5))
            df = yf.download(symbol, start=start_date, end=end_date)
            all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            df = df.reindex(all_dates)
            df = df.fillna(method='ffill')
        except Exception:
            raise Exception(f"Stock with symbol ' {symbol} ' not found.")
        return df
    def verifyInput(self,apikey,tickerSymbol,timeRange,model,layers,neurons,method=None):
        #if api
        print(apikey,tickerSymbol,timeRange,model,layers,neurons,method)
        if method == 'api':
            timeRange = 5 if timeRange is None else timeRange
            layers = 2 if layers is None else layers
            neurons = 16 if neurons is None else neurons
            model = "LR" if model is None else model
            if IndividualAccount().verifyApiKey(apikey) == False and BusinessAccount().verifyApiKey(apikey) == False:
                raise Exception("Invalid API key or Your member rank is not available for API function")

        if tickerSymbol is None:
            raise Exception(f"Please provide ticker symbol.")
        models = ["LSTM","GRU","LR"]
        if model not in models:
            raise Exception("Invalid Model")
        try:
            timeRange = int(timeRange)
            if timeRange < 1 or timeRange > 100:
                raise Exception("Invalid Time Range")
        except ValueError:
            raise Exception("Invalid Time Range, need to be an integer")
        self.verifyTickerSymbol(tickerSymbol)
        try:
            layers = int(layers)
            if layers < 0:
                raise Exception("Invalid number of layers")
        except Exception:
            raise Exception("Invalid Layer, need to be an integer")
        try:
            neurons = int(neurons)
            if neurons < 0:
                raise Exception("Invalid number of neurons")
        except Exception:
            raise Exception("Invalid neurons, need to be an integer")
        return True

    def getPrediction(self,apikey,tickerSymbol,timeRange,model,layers,neurons,method = None):
        #verify input
        # self.verifyInput(tickerSymbol, timeRange, model, layers, neurons)
        timeRange = int(timeRange)
        layers = int(layers)
        neurons = int(neurons)
        id = RequestRecord().storeRequestRecord(apikey,tickerSymbol,timeRange,model,layers,neurons)
        # get stock data frame,
        if method is None or method == 'api':
            df = self.get_stock_data(tickerSymbol)
        if model == "GRU":
            result = GRU_Model.predict_future_prices(tickerSymbol, df, timeRange, layers, neurons)
        elif model == "LSTM":
            result = LSTM_Model(tickerSymbol,df,timeRange,layers,neurons).predict()
        elif model == "LR":
            result = LinearRegression_Model(tickerSymbol,df,timeRange,layers,neurons).predict_stock_price()
        RequestRecord().updateResult(id,result)
        return result

# Request = RequestForPrediction()
# Request.getPrediction("abcdefg","aapl","5","LR","2","16")
