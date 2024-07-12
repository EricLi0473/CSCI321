import yfinance as yf
from prophet import Prophet
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Prophet_model:
    def __init__(self, symbol, days, period="5y"):
        self.symbol = symbol
        self.period = period
        self.days = days
        self.df = self.fetch_data()
        self.sma_df = self.fetch_sma()
        self.macd_df = self.fetch_macd()
        self.stoch_df = self.fetch_stoch()
        self.adx_df = self.fetch_adx()
        self.yield_df = self.fetch_treasury_yield()
        self.fed_funds_rate_df = self.fetch_fed_funds_rate()
        self.merged_df = self.merge_data()
        self.model = self.train_model()

    def fetch_data(self):
        df = yf.download(self.symbol, period=self.period)
        df.reset_index(inplace=True)
        df = df[['Date', 'Close', 'Volume']]
        df.columns = ['ds', 'y', 'volume']
        return df

    def fetch_sma(self):
        url = f"https://www.alphavantage.co/query?function=SMA&symbol={self.symbol}&interval=daily&time_period=2000&series_type=open&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        sma_data = data['Technical Analysis: SMA']
        sma_df = pd.DataFrame.from_dict(sma_data, orient='index').reset_index()
        sma_df.columns = ['ds', 'SMA']
        sma_df['ds'] = pd.to_datetime(sma_df['ds'])
        sma_df['SMA'] = sma_df['SMA'].astype(float)
        return sma_df

    def fetch_macd(self):
        url = f"https://www.alphavantage.co/query?function=MACD&symbol={self.symbol}&interval=daily&series_type=open&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        macd_data = data['Technical Analysis: MACD']
        macd_df = pd.DataFrame.from_dict(macd_data, orient='index').reset_index()
        macd_df.columns = ['ds', 'MACD', 'MACD_Signal', 'MACD_Hist']
        macd_df['ds'] = pd.to_datetime(macd_df['ds'])
        macd_df[['MACD', 'MACD_Signal', 'MACD_Hist']] = macd_df[['MACD', 'MACD_Signal', 'MACD_Hist']].astype(float)
        return macd_df

    def fetch_stoch(self):
        url = f"https://www.alphavantage.co/query?function=STOCH&symbol={self.symbol}&interval=daily&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        stoch_data = data['Technical Analysis: STOCH']
        stoch_df = pd.DataFrame.from_dict(stoch_data, orient='index').reset_index()
        stoch_df.columns = ['ds', 'SlowK', 'SlowD']
        stoch_df['ds'] = pd.to_datetime(stoch_df['ds'])
        stoch_df['SlowK'] = stoch_df['SlowK'].astype(float)
        stoch_df['SlowD'] = stoch_df['SlowD'].astype(float)
        return stoch_df

    def fetch_adx(self):
        url = f"https://www.alphavantage.co/query?function=ADX&symbol={self.symbol}&interval=daily&time_period=10&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        adx_data = data['Technical Analysis: ADX']
        adx_df = pd.DataFrame.from_dict(adx_data, orient='index').reset_index()
        adx_df.columns = ['ds', 'ADX']
        adx_df['ds'] = pd.to_datetime(adx_df['ds'])
        adx_df['ADX'] = adx_df['ADX'].astype(float)
        return adx_df

    def fetch_treasury_yield(self):
        url = "https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        yield_data = data['data']
        yield_df = pd.DataFrame(yield_data)
        yield_df.columns = ['ds', 'value']
        yield_df['ds'] = pd.to_datetime(yield_df['ds'])
        yield_df['value'] = yield_df['value'].str.replace('%', '')
        yield_df = yield_df[yield_df['value'].apply(lambda x: x.replace('.', '', 1).isdigit())]
        yield_df['value'] = yield_df['value'].astype(float)
        yield_df['treasury_yield'] = yield_df['value']
        yield_df = yield_df[['ds', 'treasury_yield']]
        return yield_df

    def fetch_fed_funds_rate(self):
        url = "https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=1TI3ZQ9MXCZ08O3M"
        response = requests.get(url)
        data = response.json()
        yield_data = data['data']
        yield_df = pd.DataFrame(yield_data)
        yield_df.columns = ['ds', 'value']
        yield_df['ds'] = pd.to_datetime(yield_df['ds'])
        yield_df['value'] = yield_df['value'].str.replace('%', '')
        yield_df = yield_df[yield_df['value'].apply(lambda x: x.replace('.', '', 1).isdigit())]
        yield_df['value'] = yield_df['value'].astype(float)
        yield_df['FEDERAL_FUNDS_RATE'] = yield_df['value']
        yield_df = yield_df[['ds', 'FEDERAL_FUNDS_RATE']]
        return yield_df

    def merge_data(self):
        merged_df = pd.merge(self.df, self.sma_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.macd_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.stoch_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.adx_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.yield_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.fed_funds_rate_df, on='ds', how='left')
        for col in ['SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield', 'FEDERAL_FUNDS_RATE']:
            merged_df[col].fillna(method='ffill', inplace=True)
            merged_df[col].fillna(method='bfill', inplace=True)
        return merged_df

    def train_model(self):
        model = Prophet()
        model.add_regressor('treasury_yield')
        model.add_regressor('FEDERAL_FUNDS_RATE')
        model.add_regressor('volume')
        model.fit(self.merged_df)
        return model

    def predict(self):
        future = self.model.make_future_dataframe(periods=self.days)
        future = pd.merge(future, self.merged_df[
            ['ds', 'volume', 'SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield', 'FEDERAL_FUNDS_RATE']], on='ds', how='left')
        for col in ['volume', 'SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield', 'FEDERAL_FUNDS_RATE']:
            future[col].fillna(method='ffill', inplace=True)
            future[col].fillna(method='bfill', inplace=True)
        forecast = self.model.predict(future)
        recommendations = self.make_recommendations(forecast)
        return recommendations


    def show_graph(self):
        correlation_matrix = self.merged_df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.show()

    def calculate_rsi(self, data, window):
        delta = data['yhat'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def make_recommendations(self, forecast):
        window_length = 3
        forecast['rsi'] = self.calculate_rsi(forecast, window_length)
        recommendations = []
        forecast_data = forecast.tail(self.days+1)
        for i in range(1, len(forecast_data)):
            current_row = forecast_data.iloc[i]
            date = current_row['ds'].strftime('%Y-%m-%d')
            predicted = current_row['yhat']
            rsi = current_row['rsi']
            if rsi < 30:
                recommendation = 'Buy'
            elif rsi > 70:
                recommendation = 'Sell'
            else:
                recommendation = 'Hold'
            recommendations.append({
                'Date': date,
                'Predicted': round(predicted, 2),
                'Recommendation': recommendation
            })
        return recommendations


# 使用示例
if __name__ == "__main__":
    symbol = "MCD"
    days = 30
    stock_prophet = Prophet_model(symbol, days)
    recommendations = stock_prophet.predict()
    for rec in recommendations:
        print(rec)
    stock_prophet.show_graph()
