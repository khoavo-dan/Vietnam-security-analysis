import pandas as pd
import numpy as np
from src.analysis.basis import dividend
# from src.analysis.cost_of_capital.capm import capm

def capm(Rf=0.0294, Rm=0.0979, beta=1.35):
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
    i = 0.045 #Vietnam current inflation
    Rf += i
    r_e = Rf+beta*(Rm-Rf)
    return r_e


def growth_rate(metric, number_of_years=5):
    """
    Growth rate
    """

    current_year = metric[-1]               # The current year
    past_year = metric[-number_of_years]    # The point in the past to compare

    if current_year*past_year>0:
        growth_rate = (current_year/past_year)**(1/(number_of_years-1))-1
    else:
        growth_rate = 0

    return growth_rate

def discounted_cash_flow(cash_flow, growth_rate, discount_rate, share_outstanding):
    """
    Discounted cash flow
    """

    discounted_cash_flow = [cash_flow *((1 + growth_rate) ** year)/ ((1 + discount_rate) ** year) for year, cash_flow in enumerate(cash_flow)]
    dcf = np.sum(discounted_cash_flow)/share_outstanding
    # print(cash_flow, growth_rate, discount_rate, share_outstanding)
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

    debt = report_data[f'{ticker}_balancesheet'].loc['Short-term borrowings']\
            + report_data[f'{ticker}_balancesheet'].loc['Long-term borrowings']\
            + report_data[f'{ticker}_balancesheet'].loc['Preferred shares']
    total_assets = report_data[f'{ticker}_balancesheet'].loc['TOTAL ASSETS']
    interest_expense = report_data[f'{ticker}_cashflow'].loc['Interest expense']
    depreciation = report_data[f'{ticker}_cashflow'].loc['Depreciation and amortisation']
    provision_expenses = report_data[f'{ticker}_cashflow'].loc['Provisions']
    cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets = report_data[f'{ticker}_cashflow'].loc['Purchases of fixed assets and other long term assets']
    cash_received_from_disposal_of_fixed_assets = report_data[f'{ticker}_cashflow'].loc['Proceeds from disposal of fixed assets']
    change_in_accounts_receivable = report_data[f'{ticker}_cashflow'].loc['(Increase)/decrease in receivables']
    change_in_inventory = report_data[f'{ticker}_cashflow'].loc['(Increase)/decrease in inventories']
    change_in_accounts_payable = report_data[f'{ticker}_cashflow'].loc['(Increase/(decrease) in payables']
    change_in_prepaid_expenses = report_data[f'{ticker}_cashflow'].loc['(Increase)/decrease in prepaid expenses']
    revenue = report_data[f'{ticker}_incomestatement'].loc['Sales']
    net_profit = report_data[f'{ticker}_incomestatement'].loc['Attributable to parent company']

    w_d = (debt / (debt + total_assets))[-1]                                # Calculate debt ratio
    if w_d != 0:
        r_d = np.mean(interest_expense[-3:])/np.mean(debt[-3:])             # Average interest rate in 3 years
    else:
        r_d = 0
    r_e = capm(Rf=0.0294, Rm=0.0979, beta=1)                                # Calculate discount rate using the Capital Asset Pricing Model (CAPM)
    w_e = 1 - w_d
    t = 0.2                                                                 # tax rate
    discount_rate = w_d*r_d*(1-t) + w_e*r_e                                 # Weighted average cost of capital
    # print(f' r_d: {r_d*100:.2f}\n r_e: {r_e*100:.2f}\n w_d: {w_d*100:.2f}\n w_e: {w_e*100:.2f} \n Discount rate: {discount_rate*100:.2f}')


    # Calculate Free float cashflow to firm
    non_cash_charge = depreciation + provision_expenses
    FCInv = cash_paid_for_purchase_of_fixed_assets_and_other_long_term_assets + cash_received_from_disposal_of_fixed_assets
    WCInv = change_in_accounts_receivable\
          + change_in_inventory\
          + change_in_accounts_payable\
          + change_in_prepaid_expenses

    fcff = np.array(
        net_profit + non_cash_charge - interest_expense * (1 - tax_rate) + FCInv + WCInv
    ) 
    # Interest extracted from P/L is negative, addition of a negative is (-)
    # FCInv & WCInv from cashflow and 

    # Assumption: Cash flow is constant for 10 years
    cash_flows = np.ones(10) * np.average(fcff[-3:])


    # Determine the minimum growth rate
    growth = min(
        growth_rate(metric=fcff, number_of_years=5),
        growth_rate(metric=revenue, number_of_years=5),
        growth_rate(metric=fcff, number_of_years=3)
    )

    # Calculate discounted cash flow (dcf)
    dcf = discounted_cash_flow(cash_flows, growth, discount_rate, share_outstanding[ticker])

    return dcf