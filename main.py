from src import report
from src.input import input_ticker
from src.analysis import working_capital
from src.analysis import cashflow
from src.analysis import basis
from src.analysis.basis import dividend
from src.experiment.ratio import get_data_from_api
import time

# Initialize an empty list to store ticker symbols
tickers = input_ticker()

# Define the tickers and reports and the frequency
reports = ['balancesheet', 'incomestatement', 'cashflow']

# Fetch the financial statements
annual_report_data = report.fetch_batch(tickers, reports, frequency='yearly', save_file=False)
quarterly_report_data = report.fetch_batch(tickers, reports, frequency='quarterly', save_file=False)
print('All FS successfully loaded')

data = get_data_from_api(tickers=tickers, url='https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}')
share_outstanding = {ticker : basis.share_outstanding(annual_report_data, ticker=ticker) for ticker in tickers}
price = {ticker : float(basis.price_board(ticker).cp) for ticker in tickers}
ncav = {ticker: working_capital.quarterly_ncav(quarterly_report_data, ticker, share_outstanding, price) for ticker in tickers}
dcf = {ticker: cashflow.fcff(annual_report_data, ticker=ticker, share_outstanding=share_outstanding, price=price) for ticker in tickers}
d = {ticker: dividend(ticker)*10000 for ticker in tickers}
eps = {ticker: basis.earning_per_share(annual_report_data, ticker) for ticker in tickers}
roe = {ticker : data[ticker]['data'][0]['roe'] for ticker in tickers}
r_e = 0.11
g = {ticker: (1-d[ticker]/eps[ticker])*roe[ticker] for ticker in tickers }
# dividend_discount = {ticker: d[ticker]/(r_e-g[ticker]) for ticker in tickers}

end_str = "\n--------------------------------------------------------------\n"
sep_str ="\t"

for ticker in tickers:
    print(f'{ticker}')
    print(f'{sep_str}Current price:                                {price[ticker]:>10,.2f}')
    print(f'{sep_str}Net curent asset value per share (ncav):      {ncav[ticker][0]:>10,.2f}')
    # print(f'{sep_str}Dividend discount: {sep_str}{dividend_discount[ticker]:>10,.2f}')

    if price[ticker]!=0:
        print(f'{sep_str}Net-net working capital per share (nnwc):     {ncav[ticker][1]:>10,.2f}        P/L margin: {(ncav[ticker][1]/price[ticker]-1)*100:>10,.2f}%')
        print(f'{sep_str}Discounted cash flow in the next 10 year:     {dcf[ticker]:>10,.2f}        P/L margin: {(dcf[ticker]/price[ticker]-1)*100:>10,.2f}%', end=end_str)

# Fetch the financial statements
# for frequency in frequencies:
#     report_data = load.fetch_batch_fs(tickers, reports, frequency)
#     print(f'{frequency.title()} FS successfully loaded')
#     # local_storing.save_file(frequency, report_data)
#     if frequency=='yearly':
#         no_shares = {ticker : net_net_working_capital.number_of_shares(report_data, ticker=ticker) for ticker in tickers}

#     if frequency=='quarterly':
#         for ticker in tickers:
#             try:
#                 net_net_working_capital.quarterly_ncav(report_data, ticker=ticker, number_of_shares=no_shares)
#             except: pass
