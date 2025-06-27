# IMPORT NECESSARY PACKAGES
from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np


######################################################################
# ============================ HELPERS ============================= #
######################################################################

def get_ds(F, K, T, r, sigma):
    d1 = (np.log(F/K) + (T*((sigma**2)/2))) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    return (d1, d2)


#################################################################################
# =============================== PRICING MODEL =============================== #
#################################################################################

def b76_price(F, K, T, r, sigma, option_type):
    d1 = get_ds(F, K, T, r, sigma)[0]
    d2 = get_ds(F, K, T, r, sigma)[1]
    match option_type:
        case 'c':
            ans = np.exp(-1*r*T) * ((F * norm.cdf(d1)) - (K * norm.cdf(d2)))
            return round(ans, 2)
        case 'p':
            ans = np.exp(-1*r*T) * ((K * norm.cdf(-1*d2)) - (F * norm.cdf(-1*d1)))
            return round(ans, 2)


####################################################################
# ====================== IMPLIED VOLATILITY ====================== #
####################################################################

def b76_implied_vol(price, F, K, T, r, option_type):
    def objective(sigma):
        return b76_price(F, K, T, r, sigma, option_type) - price
    ans = brentq(objective, 1e-6, 5.0)
    return round(ans*100, 2)


#############################################################################
# ================================ GREEKS ================================= #
#############################################################################

def b76_greeks(F, K, T, r, sigma, option_type):
    sol = {"delta":None, "gamma":None, "vega":None, "theta":None, "rho":None}
    d1 = get_ds(F, K, T, r, sigma)[0]
    d2 = get_ds(F, K, T, r, sigma)[1]
    
    match option_type:
        case 'c':
            delta = np.exp(-1*r*T) * norm.cdf(d1)
            gamma = (np.exp(-1*r*T) * norm.pdf(d1))/(F * sigma * np.sqrt(T))
            vega = F * np.exp(-1*r*T) * norm.pdf(d1) * np.sqrt(T)
            theta = ((-1 * F * np.exp(-1*r*T) * norm.pdf(d1) * sigma)/(2 * np.sqrt(T))) +\
                (r * K * np.exp(-1*r*T) * norm.cdf(d2))
            rho = T * np.exp(-1*r*T) * ((K * norm.cdf(d2)) - (F * norm.cdf(d1)))
        case 'p':
            delta = -1 * np.exp(-1*r*T) * norm.cdf(-1*d1)
            gamma = (np.exp(-1*r*T) * norm.pdf(d1))/(F * sigma * np.sqrt(T))
            vega = F * np.exp(-1*r*T) * norm.pdf(d1) * np.sqrt(T)
            theta = ((-1 * F * np.exp(-1*r*T) * norm.pdf(d1) * sigma)/(2 * np.sqrt(T))) -\
                (r * K * np.exp(-1*r*T) * norm.cdf(-1*d2))
            rho = T * np.exp(-1*r*T) * ((-1 * K * norm.cdf(-1*d2)) + (F * norm.cdf(-1*d1)))

    sol["delta"] = delta
    sol["gamma"] = gamma
    sol["vega"] = vega / 100
    sol["theta"] = theta / 365
    sol["rho"] = rho / 100
    
    return sol