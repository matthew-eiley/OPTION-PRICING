# IMPORT NECESSARY PACKAGES
from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np


######################################################################
# ============================ HELPERS ============================= #
######################################################################

def get_ds(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (T*(r+((sigma**2)/2)))) / (sigma * np.sqrt(T))
    d2= d1 - (sigma * np.sqrt(T))
    return (d1, d2)


#################################################################################
# =============================== PRICING MODEL =============================== #
#################################################################################

def bs_price(S, K, T, r, sigma, option_type):
    d1 = get_ds(S, K, T, r, sigma)[0]
    d2 = get_ds(S, K, T, r, sigma)[1]
    match option_type:
        case 'c':
            return (S * norm.cdf(d1)) - (K * np.exp(-1*r*T) * norm.cdf(d2))
        case 'p':
            return (K * np.exp(-1*r*T) * norm.cdf(-1*d2)) - (S * norm.cdf(-1*d1))

  
###############################################################
# =================== IMPLIED VOLATILITY ==================== #
###############################################################

def bs_implied_vol(price, S, K, T, r, option_type):
    def objective(sigma):
        return bs_price(S, K, T, r, sigma, option_type) - price
    return brentq(objective, 1e-6, 5.0)

#############################################################################
# ================================ GREEKS ================================= #
#############################################################################

def bs_greeks(S, K, T, r, sigma, option_type):
    sol = {"delta":None, "gamma":None, "vega":None, "theta":None, "rho":None}
    d1 = get_ds(S, K, T, r, sigma)[0]
    d2 = get_ds(S, K, T, r, sigma)[1]
    
    match option_type:
        case 'c':
            delta = norm.cdf(d1)
            gamma = norm.pdf(d1)/(S * sigma * np.sqrt(T))
            vega = S * norm.pdf(d1) * np.sqrt(T)
            theta = (-1 * ((S * norm.pdf(d1) * sigma)/(2 * np.sqrt(T)))) -\
                (r * K * np.exp(-1*r*T) * norm.cdf(d2))
            rho = K * T * np.exp(-1*r*T) * norm.cdf(d2)
        case 'p':
            delta = norm.cdf(d1) - 1
            gamma = norm.pdf(d1)/(S * sigma * np.sqrt(T))
            vega = S * norm.pdf(d1) * np.sqrt(T)
            theta = (-1 * ((S * norm.pdf(d1) * sigma)/(2 * np.sqrt(T)))) +\
                (r * K * np.exp(-1*r*T) * norm.cdf(-1*d2))
            rho = -1 * K * T * np.exp(-1*r*T) * norm.cdf(-1*d2)

    sol["delta"] = delta
    sol["gamma"] = gamma
    sol["vega"] = vega / 100
    sol["theta"] = theta / 365
    sol["rho"] = rho / 100
    
    return sol