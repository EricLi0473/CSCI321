import yfinance as yf
from prophet import Prophet
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def fetch_data(symbol, period):
    df = yf.download(symbol, period=period)
    df.reset_index(inplace=True)
    print(df.info())
    df = df[['Date', 'Close', 'Volume']]
    df.columns = ['ds', 'y', 'volume']
    return df


def fetch_sma(symbol):
    url = f"https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period=2000&series_type=open&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    sma_data = data['Technical Analysis: SMA']
    sma_df = pd.DataFrame.from_dict(sma_data, orient='index').reset_index()
    sma_df.columns = ['ds', 'SMA']
    sma_df['ds'] = pd.to_datetime(sma_df['ds'])
    sma_df['SMA'] = sma_df['SMA'].astype(float)
    return sma_df


def fetch_macd(symbol):
    url = f"https://www.alphavantage.co/query?function=MACD&symbol={symbol}&interval=daily&series_type=open&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    macd_data = data['Technical Analysis: MACD']
    macd_df = pd.DataFrame.from_dict(macd_data, orient='index').reset_index()
    macd_df.columns = ['ds', 'MACD', 'MACD_Signal', 'MACD_Hist']
    macd_df['ds'] = pd.to_datetime(macd_df['ds'])
    macd_df[['MACD', 'MACD_Signal', 'MACD_Hist']] = macd_df[['MACD', 'MACD_Signal', 'MACD_Hist']].astype(float)
    return macd_df


def fetch_stoch(symbol):
    url = f"https://www.alphavantage.co/query?function=STOCH&symbol={symbol}&interval=daily&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    stoch_data = data['Technical Analysis: STOCH']
    stoch_df = pd.DataFrame.from_dict(stoch_data, orient='index').reset_index()
    stoch_df.columns = ['ds', 'SlowK', 'SlowD']
    stoch_df['ds'] = pd.to_datetime(stoch_df['ds'])
    stoch_df['SlowK'] = stoch_df['SlowK'].astype(float)
    stoch_df['SlowD'] = stoch_df['SlowD'].astype(float)
    return stoch_df


def fetch_adx(symbol):
    url = f"https://www.alphavantage.co/query?function=ADX&symbol={symbol}&interval=daily&time_period=10&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    adx_data = data['Technical Analysis: ADX']
    adx_df = pd.DataFrame.from_dict(adx_data, orient='index').reset_index()
    adx_df.columns = ['ds', 'ADX']
    adx_df['ds'] = pd.to_datetime(adx_df['ds'])
    adx_df['ADX'] = adx_df['ADX'].astype(float)
    return adx_df


def fetch_treasury_yield():
    url = "https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    yield_data = data['data']
    yield_df = pd.DataFrame(yield_data)
    yield_df.columns = ['ds', 'value']
    yield_df['ds'] = pd.to_datetime(yield_df['ds'])

    # 清理数据中的无效字符，并转换为浮点数
    yield_df['value'] = yield_df['value'].str.replace('%', '')  # 去除百分号
    yield_df = yield_df[yield_df['value'].apply(lambda x: x.replace('.', '', 1).isdigit())]  # 过滤掉无效的值
    yield_df['value'] = yield_df['value'].astype(float)  # 转换为浮点数
    yield_df['treasury_yield'] = yield_df['value']  # 将清理后的数据重命名为'treasury_yield'
    yield_df = yield_df[['ds', 'treasury_yield']]  # 只保留'ds'和'treasury_yield'列
    return yield_df


def fetch_FEDERAL_FUNDS_RATE():
    url = "https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=1TI3ZQ9MXCZ08O3M"
    response = requests.get(url)
    data = response.json()
    yield_data = data['data']
    yield_df = pd.DataFrame(yield_data)
    yield_df.columns = ['ds', 'value']
    yield_df['ds'] = pd.to_datetime(yield_df['ds'])

    # 清理数据中的无效字符，并转换为浮点数
    yield_df['value'] = yield_df['value'].str.replace('%', '')  # 去除百分号
    yield_df = yield_df[yield_df['value'].apply(lambda x: x.replace('.', '', 1).isdigit())]  # 过滤掉无效的值
    yield_df['value'] = yield_df['value'].astype(float)  # 转换为浮点数
    yield_df['FEDERAL_FUNDS_RATE'] = yield_df['value']  # 将清理后的数据重命名为'FEDERAL_FUNDS_RATE'
    yield_df = yield_df[['ds', 'FEDERAL_FUNDS_RATE']]  # 只保留'ds'和'FEDERAL_FUNDS_RATE'列
    return yield_df


def merge_data(df, sma_df, macd_df, stoch_df, adx_df, yield_df, FEDERAL_FUNDS_RATE_df):
    merged_df = pd.merge(df, sma_df, on='ds', how='left')
    merged_df = pd.merge(merged_df, macd_df, on='ds', how='left')
    merged_df = pd.merge(merged_df, stoch_df, on='ds', how='left')
    merged_df = pd.merge(merged_df, adx_df, on='ds', how='left')
    merged_df = pd.merge(merged_df, yield_df, on='ds', how='left')
    merged_df = pd.merge(merged_df, FEDERAL_FUNDS_RATE_df, on='ds', how='left')
    # 填充缺失值
    for col in ['SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield',
                'FEDERAL_FUNDS_RATE']:
        merged_df[col].fillna(method='ffill', inplace=True)
        merged_df[col].fillna(method='bfill', inplace=True)
    return merged_df


def train_model(df):
    print(df.tail(10))  # 打印后几行以检查数据框
    print(df.columns)  # 打印列名以确认所有需要的列存在
    model = Prophet()
    model.add_regressor('treasury_yield')
    model.add_regressor('FEDERAL_FUNDS_RATE')
    model.add_regressor('volume')
    model.fit(df)
    return model


def predict(model, df, periods):
    future = model.make_future_dataframe(periods=periods)

    # 确保未来的数据也有相应的SMA、MACD、STOCH和ADX值（这里简单填充前值，你可以使用更复杂的逻辑）
    future = pd.merge(future, df[
        ['ds', 'volume', 'SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield',
         'FEDERAL_FUNDS_RATE']], on='ds', how='left')
    for col in ['volume', 'SMA', 'MACD', 'MACD_Signal', 'MACD_Hist', 'SlowK', 'SlowD', 'ADX', 'treasury_yield',
                'FEDERAL_FUNDS_RATE']:
        future[col].fillna(method='ffill', inplace=True)
        future[col].fillna(method='bfill', inplace=True)

    forecast = model.predict(future)
    return forecast


def plot_results(model, forecast):
    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)
    return fig1, fig2


if __name__ == "__main__":
    symbol = "SBUX"
    period = "5y"
    forecast_periods = 30

    df = fetch_data(symbol, period)
    sma_df = fetch_sma(symbol)
    macd_df = fetch_macd(symbol)
    stoch_df = fetch_stoch(symbol)
    adx_df = fetch_adx(symbol)
    yield_df = fetch_treasury_yield()
    FEDERAL_FUNDS_RATE_df = fetch_FEDERAL_FUNDS_RATE()
    df = merge_data(df, sma_df, macd_df, stoch_df, adx_df, yield_df, FEDERAL_FUNDS_RATE_df)
    print(df.info())
    model = train_model(df)
    forecast = predict(model, df, forecast_periods)

    fig1, fig2 = plot_results(model, forecast)

    print(forecast.tail(30))
    correlation_matrix = df.corr()

    # 绘制相关性矩阵的热图
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.show()
