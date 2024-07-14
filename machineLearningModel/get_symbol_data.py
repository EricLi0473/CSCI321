import yfinance as yf
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class GetSymbolData():
    def __init__(self):
        pass

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

    def merge_data(self,df,yield_df,fed_funds_rate_df):
        merged_df = pd.merge(df, yield_df, on='ds', how='left')
        merged_df = pd.merge(merged_df, fed_funds_rate_df, on='ds', how='left')
        for col in ['treasury_yield', 'FEDERAL_FUNDS_RATE']:
            merged_df[col].fillna(method='ffill', inplace=True)
            merged_df[col].fillna(method='bfill', inplace=True)
        return merged_df
    def fetch_data(self,symbol):
        df = yf.download(symbol, period='5y')
        all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        df = df.reindex(all_dates)
        df = df.fillna(method='ffill')
        df.reset_index(inplace=True)
        df = df[['index', 'Close', 'Volume']]
        df.columns = ['ds', 'Adj Close', 'Volume']
        yield_df = self.fetch_treasury_yield()
        fed_funds_rate_df = self.fetch_fed_funds_rate()
        merged_df = self.merge_data(df,yield_df,fed_funds_rate_df)
        merged_df['ds'] = pd.to_datetime(merged_df['ds'])
        merged_df.set_index('ds', inplace=True)
        return merged_df

    def was_data(self,symbol):
        df = yf.download(symbol, period='5y')
        all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        df = df.reindex(all_dates)
        df = df.fillna(method='ffill')
        return df
if __name__ == '__main__':
    print(GetSymbolData().fetch_data('BILI'))
    print(GetSymbolData().was_data('BILI').info())
