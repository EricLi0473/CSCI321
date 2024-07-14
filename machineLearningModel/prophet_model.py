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
        merged_df = pd.merge(self.df, self.yield_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, self.fed_funds_rate_df, on='ds', how='left')
        for col in ['treasury_yield', 'FEDERAL_FUNDS_RATE']:
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
            ['ds', 'volume',  'treasury_yield', 'FEDERAL_FUNDS_RATE']], on='ds', how='left')
        for col in ['volume',  'treasury_yield', 'FEDERAL_FUNDS_RATE']:
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
