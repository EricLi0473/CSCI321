import yfinance as yf
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tqdm import tqdm
from torch.utils.data import DataLoader, TensorDataset
from datetime import datetime, timedelta

class StockPredictor(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(StockPredictor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 2)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.gru(x, h0)
        out = self.fc(out[:, -1, :])
        return out

class GRU_Model:
    @staticmethod
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

    @staticmethod
    def preprocess_data(df):
        numeric_df = df.select_dtypes(include=[np.number])
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(numeric_df)
        return scaled_data, scaler

    @staticmethod
    def create_dataset(data, time_step=60):
        X, Y = [], []
        for i in range(len(data) - time_step):
            a = data[i:(i + time_step), :]
            X.append(a)
            Y.append(data[i + time_step, :])
        return np.array(X), np.array(Y)

    @staticmethod
    def predict_future_prices(symbol, df, forecast_days, layers, neurons):
        df = df[['Open', 'Close']].copy()

        scaled_data, scaler = GRU_Model.preprocess_data(df)

        time_step = 60  # 调整时间步长
        X, Y = GRU_Model.create_dataset(scaled_data, time_step)

        X = torch.tensor(X, dtype=torch.float32)
        Y = torch.tensor(Y, dtype=torch.float32)

        input_size = X.shape[2]

        model = StockPredictor(input_size, neurons, layers)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # 分离训练集和测试集
        train_size = int(len(X) * 0.8)
        test_size = len(X) - train_size
        train_X, test_X = X[:train_size], X[train_size:]
        train_Y, test_Y = Y[:train_size], Y[train_size:]

        train_dataset = TensorDataset(train_X, train_Y)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

        num_epochs = 10  # 调整训练轮数

        with tqdm(total=num_epochs, desc="Training Progress", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]") as pbar:
            for epoch in range(num_epochs):
                model.train()
                epoch_loss = 0
                for batch_X, batch_Y in train_loader:
                    outputs = model(batch_X)
                    optimizer.zero_grad()
                    loss = criterion(outputs, batch_Y)
                    loss.backward()
                    optimizer.step()
                    epoch_loss += loss.item()
                pbar.set_postfix(loss=epoch_loss / len(train_loader))
                pbar.update(1)

        # 计算测试集的MSE
        model.eval()
        with torch.no_grad():
            test_outputs = model(test_X)
            test_loss = criterion(test_outputs, test_Y).item()
        print(f"Testing MSE: {test_loss}")

        # 进行未来的预测
        future_inputs = X[-1].unsqueeze(0)
        predictions = []
        for _ in range(forecast_days):
            with torch.no_grad():
                future_pred = model(future_inputs)
                predictions.append(future_pred.squeeze().cpu().numpy())
                future_inputs = torch.cat((future_inputs[:, 1:, :], future_pred.unsqueeze(0)), dim=1)

        predictions = scaler.inverse_transform(predictions)
        future_dates = [df.index[-1] + timedelta(days=i+1) for i in range(forecast_days)]

        # 将预测结果和推荐加入结果字典
        future_df = pd.DataFrame(
            {'Date': future_dates, 'Predicted': predictions[:, 1]})
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
        future_df = future_df.reset_index()
        future_df['Date'] = future_df['Date'].dt.strftime('%Y-%m-%d')
        result = future_df[['Date', 'Predicted', 'Recommendation']].to_dict(orient='records')
        for record in result:
            record['Predicted'] = round(record['Predicted'],2)
        return result

    @staticmethod
    def plot_predictions(df, predictions):
        df['Date'] = df.index

        future_df = pd.DataFrame(predictions)
        future_df['Date'] = pd.to_datetime(future_df['Date'])

        plt.figure(figsize=(14, 7))

        plt.subplot(2, 1, 1)
        plt.plot(df['Date'], df['Open'], label='Historical Open Prices', color='blue')
        plt.plot(future_df['Date'], future_df['Predicted'], label='Predicted Open Prices', color='red')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Open Price Prediction')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(df['Date'], df['Close'], label='Historical Close Prices', color='blue')
        plt.plot(future_df['Date'], future_df['Predicted'], label='Predicted Close Prices', color='red')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Close Price Prediction')
        plt.legend()

        plt.tight_layout()
        plt.show()


# # 示例用法
# symbol = 'AAPL'  # 股票代码
# df = GRU_Model.get_stock_data(symbol)
# forecast_days = 30  # 预测天数
# layers = 2  # GRU层数
# neurons = 16  # 每层神经元数
#
# # 预测股票价格
# predictions = GRU_Model.predict_future_prices(symbol, df, forecast_days, layers, neurons)
#
# # 打印预测结果
# print(predictions)
#
# # 绘制预测结果
# GRU_Model.plot_predictions(df, predictions)
