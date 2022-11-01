from typing import NoReturn, List
import yfinance as yf
import pandas as pd
import datetime as dt


# Create a class to hold data and methods for performing backtesting

class PortfolioBacktest:
    def __init__(self, start_date: str, end_date: str, stock_list: List[str], start_val: float) -> NoReturn:
        self.start_date = start_date
        self.end_date = end_date
        self.stock_list = stock_list
        self.start_val = start_val

    def _download_stock_data(self) -> NoReturn:
        df_list = []
        for stock in self.stock_list:
            df = yf.download(stock, start=self.start_date, end=self.end_date)
            df['Symbol'] = stock
            df_list.append(df)
        self.stock_data = pd.concat(df_list)
        self.divided_start_value = self.start_val / len(self.stock_list)
        
    def _calculate_drifting_values(self) -> NoReturn:
        input_df_list = [self.stock_data[self.stock_data['Symbol'] == stock] for stock in self.stock_list]
        processed_df_list = []
        for df in input_df_list:
            value_list = [self.divided_start_value]
            close_list = df['Adj Close'].to_list()
            for idx, close in enumerate(close_list):
                if idx > 0:
                    new_value = value_list[-1] * (close / close_list[idx-1])
                    value_list.append(new_value)
            processed_df_list.append(pd.DataFrame([{'Drifting Value': val} for val in value_list]))
        processed_df = pd.concat(processed_df_list)
        self.stock_data['Drifting Value'] = processed_df['Drifting Value'].values

    def run(self) -> NoReturn:
        self._download_stock_data()
        self._calculate_drifting_values()


# Example

# Get the day interval for 15 years
day_interval = 15 * 365.2425

# Calculate the date 15 years ago from today and convert to string
start_date = dt.datetime.strftime((dt.datetime.today() - dt.timedelta(days=day_interval)).date(), '%Y-%m-%d') 
end_date = dt.datetime.strftime(dt.datetime.today().date(), '%Y-%m-%d')

# Select a list of stocks in the portfolio
stocks = [
    'BHC',
    'HRI',
    'SWX',
    'XRX'
]

# Set the initial value for the portfolio
initial_value = 1000

# Instantiate a new object for backtesting
backtest = PortfolioBacktest(start_date, end_date, stocks, initial_value)

# Run backtest pipeline (this will download the data and perform testing)
backtest.run()

# Pull the backtest results into a DataFrame variable for inspection
df = backtest.stock_data

