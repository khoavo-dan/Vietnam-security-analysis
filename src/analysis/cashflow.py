import pandas as pd
import numpy as np
# from src.analysis.cost_of_capital.capm import capm

def capm(Rf=0.294, Rm=0.979, beta=1):
    """
    Capital Asset Pricing Model
    r R e F = + β − i M [E(R ) RF ]
    where:
        [E(RM) − Rf] = Equity risk premium.
        RM = Expected return on the market.
        βi = Beta of stock. Beta measures the sensitivity of the stock’s returns to changes in market
        returns.
        RF = Risk‐free rate.
        r_e = Expected return on stock (cost of equity).
    """
    r_e = (Rf+beta*(Rm-Rf))
    return r_e


def growth_rate(metric, number_of_years=5):
    """
    Growth rate
    """
    return (metric[-1]/metric[-number_of_years])**(1/(number_of_years-1))-1

def discounted_cash_flow(cash_flow, growth_rate, discount_rate, share_outstanding):
    """
    Discounted cash flow
    """
    discounted_cash_flow = [cash_flow *((1 + growth_rate) ** year)/ ((1 + discount_rate) ** year) for year, cash_flow in enumerate(cash_flow)]
    dcf = np.sum(discounted_cash_flow)/share_outstanding
    return dcf

def fcff(report_data, ticker, share_outstanding, price, tax_rate=0.2):
    """
    FCFF is the cash flow available to the company’s suppliers of debt and equity capital
    after all operating expenses (including income taxes) have been paid and necessary
    investments in working capital and fixed capital have been made. FCFF can be computed starting with net income as
    FCFF = NI + NCC + Int(1 – Tax rate) – FCInv – WCInv
    where
    NI = Net income
    NCC = Non-cash charges (such as depreciation and amortisation)
    Int = Interest expense
    FCInv = Capital expenditures (fixed capital, such as equipment)
    WCInv = Working capital expenditures
    """
    # share_outstanding = share_outstanding[ticker]
    # price = price[ticker]
    # total_liabilities = report_data[f'{ticker}_balancesheet'].loc['total_liabilities']
    depreciation = report_data[f'{ticker}_cashflow'].loc['depreciation']
    provision_expenses = report_data[f'{ticker}_cashflow'].loc['provision_expenses']
    cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets = report_data[f'{ticker}_cashflow'].loc['cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets']
    cash_received_from_disposal_of_fixed_assets = report_data[f'{ticker}_cashflow'].loc['cash_received_from_disposal_of_fixed_assets']
    increase_decrease_in_accounts_receivable = report_data[f'{ticker}_cashflow'].loc['increase_decrease_in_accounts_receivable']
    increase_decrease_in_inventory = report_data[f'{ticker}_cashflow'].loc['increase_decrease_in_inventory']
    increase_decrease_in_accounts_payable = report_data[f'{ticker}_cashflow'].loc['increase_decrease_in_accounts_payable']
    increase_decrease_in_prepaid_expenses = report_data[f'{ticker}_cashflow'].loc['increase_decrease_in_prepaid_expenses']
    interest_expense = report_data[f'{ticker}_incomestatement'].loc['interest_expense']
    revenue = report_data[f'{ticker}_incomestatement'].loc['revenue']
    net_profit = report_data[f'{ticker}_incomestatement'].loc['profit_attributable_to_shareholders_of_the_parent_company']

    non_cash_charge = depreciation + provision_expenses
    FCInv = cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets + cash_received_from_disposal_of_fixed_assets
    WCInv = increase_decrease_in_accounts_receivable\
          + increase_decrease_in_inventory\
          + increase_decrease_in_accounts_payable\
          + increase_decrease_in_prepaid_expenses

    # # Calculate debt ratio
    # total_liabilities = liabilities
    # total_assets = total_assets
    # debt_ratio = total_liabilities / total_assets

    # Calculate fcff (cash flow)
    fcff = np.array(
        net_profit - interest_expense * (1 - tax_rate) + FCInv + WCInv
    )

    # Assumption: Cash flow is constant for 10 years
    cash_flows = np.ones(10) * fcff[-1]

    # Calculate discount rate using the Capital Asset Pricing Model (CAPM)
    discount_rate = capm(Rf=0.0294, Rm=0.1842, beta=1)

    # Calculate growth rates for different periods
    growth_rate_5YEARS = growth_rate(metric=fcff, number_of_years=5)
    growth_rate_5YEARS_revenue = growth_rate(metric=revenue, number_of_years=5)
    growth_rate_10YEARS = growth_rate(metric=fcff, number_of_years=10)

    # Determine the minimum growth rate
    growth = min(
        growth_rate_5YEARS,
        growth_rate_5YEARS_revenue,
        growth_rate_10YEARS
    )

    # Calculate discounted cash flow (dcf)
    dcf = discounted_cash_flow(cash_flows, growth, discount_rate, share_outstanding[ticker])

    return dcf
    # best_growth_rate = max(growth_rate_5YEARS, growth_rate_10YEARS)/2
    # worst_growth_rate = min(growth_rate_5YEARS, growth_rate_10YEARS)
    # dcf_worst = discounted_cash_flow(cash_flows, worst_growth_rate, discount_rate, share_outstanding[ticker])
    # dcf_best = discounted_cash_flow(cash_flows, best_growth_rate, discount_rate, share_outstanding[ticker])

    # if price != 0:
    #     print(f'    Discounted cash flow in the next 10 year (low scenario): {dcf_worst:,.2f}        P/L margin: {(dcf_worst/price[ticker]-1)*100:,.2f}%')
    #     print(f'    Discounted cash flow in the next 10 year (high scenario): {dcf_best:,.2f}        P/L margin: {(dcf_best/price[ticker]-1)*100:,.2f}%')
    # else:
    #     print (f'    Number_of_shares {number_of_shares[ticker]:,.2f}')
    #     print (f'    Discount_rate {discount_rate*100:,.2f}%')
    #     print(fcff[-1]/number_of_shares[ticker])
    #     print(fcff[-5])
    #     print (f'    Growth_rate {best_growth_rate*100:,.2f}%')
    #     print(f'    Free cash flow to firm (FCFF): {fcff[-1]:,.2f}')
    #     print(f'    FCFF per share: {fcff[-1]/number_of_shares[ticker]:,.2f}')
    #     print(f'    Discounted cash flow in the next 10 year (low scenario): {dcf_worst:,.2f}')
    #     print(f'    Discounted cash flow in the next 10 year (high scenario): {dcf_best:,.2f}')

    # cache = {}
    # for i in ['incomestatement', 'cashflow']:
    #     for j in report_data[f'{ticker}_{i}'].index:
    #         cache[str(j)] = np.array(report_data[f'{ticker}_{i}'].loc[j])

