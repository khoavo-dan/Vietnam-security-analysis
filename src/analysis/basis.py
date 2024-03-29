from pandas import json_normalize
import numpy as np
import requests
import json

def price_board (symbol_ls):
    """
    This function returns the trading price board of a target stocks list.
    Args:
        symbol_ls (:obj:`str`, required): STRING list of symbols separated by "," without any space. Ex: "TCB,SSI,BID"
    """
    data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}'.format(symbol_ls)).json()
    df = json_normalize(data['data'])
    df = df[['t', 'cp', 'fv', 'mav', 'nstv', 'nstp', 'rsi', 'macdv', 'macdsignal', 'tsignal', 'avgsignal', 'ma20', 'ma50', 'ma100', 'session', 'mscore', 'pe', 'pb', 'roe', 'oscore', 'ev', 'mw3d', 'mw1m', 'mw3m', 'mw1y', 'rs3d', 'rs1m', 'rs3m', 'rs1y', 'rsavg', 'hp1m', 'hp3m', 'hp1y', 'lp1m', 'lp3m', 'lp1y', 'hp1yp', 'lp1yp', 'delta1m', 'delta1y', 'bv', 'av', 'hmp', 'seq', 'vnid3d', 'vnid1m', 'vnid3m', 'vnid1y', 'vnipe', 'vnipb']]

    return df

def share_outstanding(report_data, ticker):
    eps = report_data[f'{ticker}_incomestatement'].loc['EPS']
    attributable_net_profit = report_data[f'{ticker}_incomestatement'].loc['Attributable to parent company']
    shares_outstanding = attributable_net_profit/eps

    return shares_outstanding[-1]

def share_outstanding_1(report_data):
    eps = np.array(report_data.loc[(slice(None),'EPS'),:])
    attributable_net_profit = np.array(report_data.loc[(slice(None),'Attributable to parent company'),:])
    shares_outstanding = attributable_net_profit/eps

    return shares_outstanding

def eps(report_data, ticker, year):
    basicEPS = report_data[f'{ticker}_incomestatement'].loc['EPS']
    return np.mean(basicEPS[-year:])

def dividend(symbol):
    data = requests.get('https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{}/dividend-payment-histories?page=0&size=20'.format(symbol)).json()
    df = json_normalize(data['listDividendPaymentHis']).drop(columns=['no', 'ticker'])
    dividend_yield = np.array(df['cashDividendPercentage'])
    d_yield = np.mean(dividend_yield[-3:])
    return d_yield

