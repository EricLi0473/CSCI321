import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from Entity.apiKey import *
from machineLearningModel.TF_LR_Model import *
from machineLearningModel.LSTM_Model import *
from Entity.requestRecord import *
import hashlib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
class MlController:
    def __init__(self):
        pass

    @staticmethod
    def verifyTickerSymbol(symbol) -> pd.DataFrame or Exception:
        try:
            end_date = datetime.today().date()
            start_date = (end_date - timedelta(days=2))
            df = yf.download(symbol, start=start_date, end=end_date)
            all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            df = df.reindex(all_dates)
            df = df.fillna(method='ffill')
        except Exception:
            raise Exception(f"Stock with symbol ' {symbol} ' not found.")
        return df

    @staticmethod
    def get_stock_data(symbol) -> pd.DataFrame or Exception:
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

    def getMLResultByParameters(self,inputApikey,tickerSymbol,modelName,timeFrame,layersNum,neuronsPerLayer) -> str or Exception:
        try:
            timeFrame=int(timeFrame)
            layersNum=int(layersNum)
            neuronsPerLayer=int(neuronsPerLayer)
            if ApiKey().verifyAnApiKey(hashlib.md5(inputApikey.encode()).hexdigest()) is False:
                raise Exception("Invalid API Key")
            MlController.verifyTickerSymbol(tickerSymbol)
            df = MlController.get_stock_data(tickerSymbol)
            if modelName.lower() == 'lr':
                forecastResult =  LinearRegression_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict_stock_price()
            elif modelName.lower() == 'lstm':
                forecastResult = LSTM_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict()
            RequestRecord().storeRequestRecord(hashlib.md5(inputApikey.encode()).hexdigest(), tickerSymbol, timeFrame, modelName, layersNum, neuronsPerLayer, forecastResult)
            ApiKey().apiKeyUsageCountPlusOne(hashlib.md5(inputApikey.encode()).hexdigest())
            return forecastResult
        except Exception as e:
            raise e

    def getMLResultByUploadData(self,df,inputApikey,tickerSymbol,modelName,timeFrame,layersNum,neuronsPerLayer) ->str or Exception:
        try:
            timeFrame=int(timeFrame)
            layersNum=int(layersNum)
            neuronsPerLayer=int(neuronsPerLayer)
            if ApiKey().verifyAnApiKey(hashlib.md5(inputApikey.encode()).hexdigest()) is False:
                raise Exception("Invalid API Key")
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
            if modelName.lower() == 'lr':
                forecastResult =  LinearRegression_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict_stock_price()
            elif modelName.lower() == 'lstm':
                forecastResult = LSTM_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict()
            RequestRecord().storeRequestRecord(hashlib.md5(inputApikey.encode()).hexdigest(), tickerSymbol, timeFrame, modelName, layersNum, neuronsPerLayer, forecastResult)
            ApiKey().apiKeyUsageCountPlusOne(hashlib.md5(inputApikey.encode()).hexdigest())
            return forecastResult
        except Exception as e:
            raise e

    def getMLResultByApi(self, inputApikey, tickerSymbol, modelName, timeFrame, layersNum,
                                neuronsPerLayer) -> str or Exception:
        try:
            if tickerSymbol is None:
                raise Exception("Please enter the ticker symbol.")
            if ApiKey().verifyAnApiKey(hashlib.md5(inputApikey.encode()).hexdigest()) is False:
                raise Exception("You have entered an invalid API Key.")
            MlController.verifyTickerSymbol(tickerSymbol)
            df = MlController.get_stock_data(tickerSymbol)
            if modelName.lower() not in ['lr', 'lstm', 'gru']:
                raise Exception("Unsupported model types, we only support 'lr', 'lstm', and 'gru'.")
            timeFrame = int(timeFrame)
            layersNum = int(layersNum)
            neuronsPerLayer = int(neuronsPerLayer)
            if timeFrame < 0 or timeFrame > 100:
                raise ValueError("Timeframe must be between 0 and 100")
            if modelName.lower() == 'lr':
                forecastResult =  LinearRegression_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict_stock_price()
            elif modelName.lower() == 'lstm':
                forecastResult = LSTM_Model(tickerSymbol,df,timeFrame,layersNum,neuronsPerLayer).predict()
            RequestRecord().storeRequestRecord(hashlib.md5(inputApikey.encode()).hexdigest(), tickerSymbol, timeFrame, modelName, layersNum, neuronsPerLayer, forecastResult)
            ApiKey().apiKeyUsageCountPlusOne(hashlib.md5(inputApikey.encode()).hexdigest())
            return forecastResult
        except ValueError:
            raise Exception("Please fill in the numbers variable in the timeframe, layers or neurons.")
        except Exception as e:
            raise e
# from io import StringIO
# df = MlController.get_stock_data("aapl")
# print(df.info())
# dfStr = df.to_csv()
#
# newdf = pd.read_csv(StringIO(dfStr))
# newdf["Date"] = pd.to_datetime(newdf["Unnamed: 0"])
# newdf.set_index("Date", inplace=True)
# newdf.drop(columns=['Unnamed: 0'], inplace=True)
# print(newdf.info())
# mlController = mlController()
# try:
#     print(MlController().getMLResultByParameters("123456", "bili", "lstm", "10", "2", "8"))
# except Exception as e:
#     print(e)

