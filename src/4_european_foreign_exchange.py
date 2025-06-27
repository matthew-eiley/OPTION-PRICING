# IMPORT NECESSARY PACKAGES
from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np


######################################################################
# ============================ HELPERS ============================= #
######################################################################

def get_ds(S, K, T, rd, rf, sigma):
    d1 = (np.log(S/K) + (T*(rd-rf+((sigma**2)/2)))) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    return (d1, d2)


#################################################################################
# =============================== PRICING MODEL =============================== #
#################################################################################

def gk_price(S, K, T, rd, rf, sigma, option_type):
    d1 = get_ds(S, K, T, rd, rf, sigma)[0]
    d2 = get_ds(S, K, T, rd, rf, sigma)[1]
    match option_type:
        case 'c':
            ans = (S * np.exp(-1*rf*T) * norm.cdf(d1)) - (K * np.exp(-1*rd*T) * norm.cdf(d2))
            return round(ans, 2)
        case 'p':
            ans = (K * np.exp(-1*rd*T) * norm.cdf(-1*d2)) - (S * np.exp(-1*rf*T) * norm.cdf(-1*d1))
            return round(ans, 2)


####################################################################
# ====================== IMPLIED VOLATILITY ====================== #
####################################################################

def gk_implied_vol(price, S, K, T, rd, rf, option_type):
    def objective(sigma):
        return gk_price(S, K, T, rd, rf, sigma, option_type) - price
    ans = brentq(objective, 1e-6, 5.0)
    return round(ans*100, 2)


#############################################################################
# ================================ GREEKS ================================= #
#############################################################################

def gk_greeks(S, K, T, rd, rf, sigma, option_type):
    sol = {"delta":None, "gamma":None, "vega":None, "theta":None, "rho":None}
    d1 = get_ds(S, K, T, rd, rf, sigma)[0]
    d2 = get_ds(S, K, T, rd, rf, sigma)[1]
    
    match option_type:
        case 'c':
            delta = np.exp(-1*rf*T) * norm.cdf(d1)
            gamma = (np.exp(-1*rf*T) * norm.pdf(d1))/(S * sigma * np.sqrt(T))
            vega = S * np.exp(-1*rf*T) * norm.pdf(d1) * np.sqrt(T)
            theta = ((-1 * S * np.exp(-1*rf*T) * norm.pdf(d1) * sigma)/(2 * np.sqrt(T))) +\
                (rf * S * np.exp(-1*rf*T) * norm.cdf(d1)) -\
                (rd * K * np.exp(-1*rd*T) * norm.cdf(d2))
            rho = K * T * np.exp(-1*rd*T) * norm.cdf(d2)
        case 'p':
            delta = -1 * np.exp(-1*rf*T) * norm.cdf(-1*d1)
            gamma = (np.exp(-1*rf*T) * norm.pdf(d1))/(S * sigma * np.sqrt(T))
            vega = S * np.exp(-1*rf*T) * norm.pdf(d1) * np.sqrt(T)
            theta = ((-1 * S * np.exp(-1*rf*T) * norm.pdf(d1) * sigma)/(2 * np.sqrt(T))) -\
                (rf * S * np.exp(-1*rf*T) * norm.cdf(-1*d1)) +\
                (rd * K * np.exp(-1*rd*T) * norm.cdf(-1*d2))
            rho = -1 * K * T * np.exp(-1*rd*T) * norm.cdf(-1*d2)

    sol["delta"] = delta
    sol["gamma"] = gamma
    sol["vega"] = vega / 100
    sol["theta"] = theta / 365
    sol["rho"] = rho / 100
    
    return sol