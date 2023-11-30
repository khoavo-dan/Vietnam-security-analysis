from src.input import input_ticker
from src.experiment.security import Security
from src.analysis.basis import dividend
from src.analysis.basis import share_outstanding
from src.analysis.basis import earning_per_share
from src.analysis.cashflow import fcff
from src.analysis.working_capital import quarterly_ncav
from src.experiment.ratio import get_data_from_api

tickers = input_ticker()
reports = ['balancesheet', 'incomestatement', 'cashflow']

# Fetch the financial statements
annual_report_data = report.fetch_batch(tickers, reports, frequency='yearly', save_file=False)
quarterly_report_data = report.fetch_batch(tickers, reports, frequency='quarterly', save_file=False)
print('All FS successfully loaded')

data = get_data_from_api(tickers=tickers, url='https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}')
shares = {ticker : basis.share_outstanding(annual_report_data, ticker=ticker) for ticker in tickers}
price = {ticker : float(basis.price_board(ticker).cp) for ticker in tickers}
ncav = {ticker: quarterly_ncav(quarterly_report_data, ticker, share_outstanding, price) for ticker in tickers}
dcf = {ticker: fcff(annual_report_data, ticker=ticker, share_outstanding=share_outstanding, price=price) for ticker in tickers}
d = {ticker: dividend(ticker) for ticker in tickers}
eps = {ticker: earning_per_share(annual_report_data, ticker) for ticker in tickers}

class Stock:
    def __init__(self, ticker):
        self.pe = data[ticker]['pe']
        self.pb = data[ticker]['pb']
        self.roe = data[ticker]['roe']
        self.price = price['ticker']
        self.shares = shares['ticker']
        self.dividend_yield = d['ticker']
        self.eps = eps['ticker']
        self.dcf = dcf['ticker']
        self.ncav = ncav['ticker']