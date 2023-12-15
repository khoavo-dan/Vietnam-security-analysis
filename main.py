from src import report
from src.input import input_ticker
from src.analysis import working_capital
from src.analysis import cashflow
from src.analysis import basis
from src.analysis.basis import dividend
from src.experiment.ratio import get_data_from_api
import time
import numpy as np

# Initialize an empty list to store ticker symbols
tickers = input_ticker()

# Define the tickers and reports and the frequency
reports = ['balancesheet', 'incomestatement', 'cashflow']

# Fetch the financial statements
annual_report_data = report.fetch_batch(tickers, reports, frequency='yearly', save_file=False)
quarterly_report_data = report.fetch_batch(tickers, reports, frequency='quarterly', save_file=False)
print('All FS successfully loaded')

data = get_data_from_api(tickers=tickers, url='https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}')

# Define empty dictionaries for the results
share_outstanding = {}
price = {}
ncav = {}
dcf = {}


end_str = "\n--------------------------------------------------------------\n"
sep_str ="\t"

# Process each ticker individually with error handling
for ticker in tickers:
    try:
        # Get share outstanding data
        share_outstanding[ticker] = basis.share_outstanding(annual_report_data, ticker=ticker)

        # Get price data
        price[ticker] = float(basis.price_board(ticker).cp)
        pb = float(basis.price_board(ticker).pb)
        d = dividend(ticker)
        eps = basis.eps(annual_report_data, ticker)
        roe = data[ticker]['data'][0]['roe']

        # Calculate ncav
        ncav[ticker] = working_capital.quarterly_ncav(quarterly_report_data, ticker, share_outstanding, price)

        # Calculate dcf
        dcf[ticker] = cashflow.fcff(annual_report_data, ticker=ticker, share_outstanding=share_outstanding, price=price)

        print(f'{ticker}')
        print(f'{sep_str}Current price:                                 {price[ticker]:>10,.2f}')
        # print(f'{sep_str}Dividend discount:                            {dividend_discount[ticker]:>10,.2f}')

        if price[ticker]!=0:
            print(f'{sep_str}Earning yield (3 year):                        {eps/price[ticker]*100:>10,.2f} %')
            print(f'{sep_str}Dividend yield (3 years):                      {d*pb*100:>10,.2f} %')
            print(f'{sep_str}Net-net working capital per share (nnwc):      {ncav[ticker][1]:>10,.2f}       P/L margin: {(ncav[ticker][1]/price[ticker]-1)*100:>10,.2f} %')
            print(f'{sep_str}Discounted cashflow in the next 10 year:       {dcf[ticker]:>10,.2f}       P/L margin: {(dcf[ticker]/price[ticker]-1)*100:>10,.2f} %', end=end_str)

        else:
            print(f'{sep_str}Net-net working capital per share (nnwc):      {ncav[ticker][1]:>10,.2f}')
            print(f'{sep_str}Discounted cashflow in the next 10 year:       {dcf[ticker]:>10,.2f}', end=end_str)

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        # You can handle the error for this specific ticker here if needed

# r_e = 0.11
# g = {ticker: (1-d[ticker][0]/eps[ticker])*roe[ticker] for ticker in tickers }
# dividend_discount = {ticker: d[ticker][1]/(r_e-g[ticker]) for ticker in tickers}

# ncav = np.array([working_capital.quarterly_ncav(quarterly_report_data, ticker, share_outstanding, price) for ticker in tickers])
# dcf = np.array([cashflow.fcff(annual_report_data, ticker=ticker, share_outstanding=share_outstanding, price=price) for ticker in tickers])
# d = np.array([dividend(ticker)*10000 for ticker in tickers])
# eps = np.array([basis.earning_per_share(annual_report_data, ticker) for ticker in tickers])
# roe = np.array([data[ticker]['data'][0]['roe'] for ticker in tickers])
# r_e = 0.11
# g = np.array([(1-d[ticker]/eps[ticker])*roe[ticker] for ticker in tickers ])

