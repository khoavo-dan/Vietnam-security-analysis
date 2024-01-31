import numpy as np
from src.analysis import basis

def quarterly_ncav(report_data, ticker, share_outstanding, price):
    # cache = {}
    # for i in ['balancesheet','incomestatement']:
    #     for j in report_data[f'{ticker}_{i}'].index:
    #         cache[str(j)] = np.array(report_data[f'{ticker}_{i}'].loc[j])
    try:

        current_asset = report_data[f'{ticker}_balancesheet'].loc['CURRENT ASSETS']
        cash = report_data[f'{ticker}_balancesheet'].loc['Cash and cash equivalents']
        short_term_investments = report_data[f'{ticker}_balancesheet'].loc['Short-term investments']
        receivables = report_data[f'{ticker}_balancesheet'].loc['Accounts receivable']
        inventory = report_data[f'{ticker}_balancesheet'].loc['Inventories'].iloc[0]
        liabilities = report_data[f'{ticker}_balancesheet'].loc['LIABILITIES']

        net_current_asset_value = current_asset - liabilities
        net_net_working_capital = cash + short_term_investments + receivables*0.75 + inventory*0.5 - liabilities
        ncav = net_current_asset_value[-1]/share_outstanding[ticker]
        nnwc = net_net_working_capital[-1]/share_outstanding[ticker]

    except Exception as e:
        print(e)
    # if price != 0:
    #     print(f'{ticker} \n    Current price: {price}')
    #     print(f'    Net curent asset value per share (ncav): {ncav:,.2f}')
    #     print(f'    Net-net working capital per share (nnwc): {nnwc:,.2f}        P/L margin: {(nnwc/price[ticker]-1)*100:.2f}%')
    # else:
    #     print(f'    Net curent asset value per share (ncav): {ncav:,.2f}')
    #     print(f'    Net-net working capital per share (nnwc): {nnwc:,.2f}')

    return ncav, nnwc
