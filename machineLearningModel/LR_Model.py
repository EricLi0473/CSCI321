import yfinance as yf 
import numpy as np
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import pickle

def getStockByTickerSymbol(Tickersymbol:str) -> pd.DataFrame:
    end_date = datetime.today().date()
    start_date = (end_date - timedelta(days=365 * 5))
    df = yf.download(Tickersymbol, start=start_date, end=end_date)
    # df = df.sort_index(ascending=False)
    # 重新索引数据框，包含所有日期
    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(all_dates)

    # 使用前一天的收盘价填充缺失值
    df = df.fillna(method='ffill')
    return df

def showPredictGraph(df:pd.DataFrame):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df, marker='o')
    plt.title('Predicted Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Predicted Price')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()


class LinearRegression_Model:
    def __init__(self) -> None:
        pass

    def getStockPrediction(self,df:pd.DataFrame,forecast_out:int) -> pd.DataFrame:
        df = df[["Adj Close"]]

        #Create another column (the target or dependent variable) shifted 'n' units up
        df['Prediction'] = df[["Adj Close"]].shift(-forecast_out)

        ### Create the indenpendent data set (X) ####
        #Convert the dataframe to a numpy array
        X = np.array(df.drop(['Prediction'],axis=1))
        #Remove the last 'n' rows
        X = X[:-forecast_out]

        ### Create the dependent data set (y) ###
        #Convert the dataframe to a numpy array(All of the values including the NaN's)
        y = np.array(df['Prediction'])
        # Get all of the y values except the last 'n' rows
        y = y[:-forecast_out]

        #Split the data into 80% training and 20% testing
        x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
        #Create and train the Linear Regression Model
        # lr = LinearRegression()
        lr = Ridge(alpha=0.1)
        #Train the model
        lr.fit(x_train,y_train)
        lr_coefficient = lr.score(x_test,y_test)
        # print(lr_coefficient)
  
        #Set x_forecast equal to the last 'n' rows of the original data set from Adj Close column
        x_forecast = np.array(df.drop(["Prediction"],axis=1))[-forecast_out:]

        #Print the linear regressor predictions for the next 'n' days
        lr_prediction = lr.predict(x_forecast)


        # Get future dates for prediction
        future_dates = pd.date_range(start=df.index[-1], periods=forecast_out + 1)[1:]

        # Combine dates and predictions into a DataFrame
        predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': lr_prediction})
        predictions_df.set_index('Date', inplace=True)
        return predictions_df
    

lr = LinearRegression_Model()
result = lr.getStockPrediction(getStockByTickerSymbol("AAPL"),100)
# print(result)
### transfer to json string
print(result.to_json(date_format='iso').replace('T00:00:00.000', ''))
