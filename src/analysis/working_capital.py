import numpy as np
from src.analysis import basis

def quarterly_ncav(report_data, ticker, share_outstanding):
    # cache = {}
    # for i in ['balancesheet','incomestatement']:
    #     for j in report_data[f'{ticker}_{i}'].index:
    #         cache[str(j)] = np.array(report_data[f'{ticker}_{i}'].loc[j])
    try:

        current_asset = report_data[f'{ticker}_balancesheet'].loc['CURRENT ASSETS']
        cash = report_data[f'{ticker}_balancesheet'].loc['Cash and cash equivalents']
        short_term_investments = report_data[f'{ticker}_balancesheet'].loc['Short-term investments'].iloc[0]
        receivables = report_data[f'{ticker}_balancesheet'].loc['Accounts receivable']
        inventory = report_data[f'{ticker}_balancesheet'].loc['Inventories'].iloc[0]
        liabilities = report_data[f'{ticker}_balancesheet'].loc['LIABILITIES']

        net_current_asset_value = current_asset - liabilities
        net_net_working_capital = (cash + short_term_investments + receivables*0.75 + inventory*0.5 - liabilities)/share_outstanding[ticker]

    except Exception as e:
        print(e)

    return net_net_working_capital[-1]
