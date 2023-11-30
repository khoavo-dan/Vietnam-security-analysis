import numpy as np
from src.analysis import basis

def quarterly_ncav(report_data, ticker, share_outstanding, price):
    # cache = {}
    # for i in ['balancesheet','incomestatement']:
    #     for j in report_data[f'{ticker}_{i}'].index:
    #         cache[str(j)] = np.array(report_data[f'{ticker}_{i}'].loc[j])


    current_asset = report_data[f'{ticker}_balancesheet'].loc['current_assets']
    cash = report_data[f'{ticker}_balancesheet'].loc['cash_and_cash_equivalents']
    short_term_investments = report_data[f'{ticker}_balancesheet'].loc['short-term_net_investment_value']
    receivables = report_data[f'{ticker}_balancesheet'].loc['accounts_receivable']
    inventory = report_data[f'{ticker}_balancesheet'].loc['inventory,_net']
    liabilities = report_data[f'{ticker}_balancesheet'].loc['liabilities']

    net_current_asset_value = current_asset - liabilities
    net_net_working_capital = cash + short_term_investments + receivables*0.75 + inventory*0.5 - liabilities
    ncav = net_current_asset_value[-1]/share_outstanding[ticker]
    nnwc = net_net_working_capital[-1]/share_outstanding[ticker]

    # if price != 0:
    #     print(f'{ticker} \n    Current price: {price}')
    #     print(f'    Net curent asset value per share (ncav): {ncav:,.2f}')
    #     print(f'    Net-net working capital per share (nnwc): {nnwc:,.2f}        P/L margin: {(nnwc/price[ticker]-1)*100:.2f}%')
    # else:
    #     print(f'    Net curent asset value per share (ncav): {ncav:,.2f}')
    #     print(f'    Net-net working capital per share (nnwc): {nnwc:,.2f}')

    return ncav, nnwc
