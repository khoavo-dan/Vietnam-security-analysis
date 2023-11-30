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
        r
        e = Expected return on stock (cost of equity).
    """
    r_e = (Rf+beta*(Rm-Rf))
    return r_e

def bond_yield_plus_risk_premium(bond_yield, risk_premium):
    """
    """
    r_e = (bond_yield + risk_premium)
    return r_e


def growth_rate(d, eps, roe):
    """
    Growth rate
    g = (d/eps) * roe
    d = Next year dividend
    eps = Earnings per share
    roe = Return on equity
    """
    g = (d/eps) * roe

    return g
