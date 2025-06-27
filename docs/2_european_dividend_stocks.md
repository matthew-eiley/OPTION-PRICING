# European Options on Dividend-Paying Stocks
This case extends the standard Black-Scholes model to account for continuous dividend yield. The Black-Scholes-Merton model (also called the "dividend-adjusted" model) provides a closed-form solution for European options on dividend-paying stocks. Implied volatility is obtained by numerically inverting this dividend-augmented pricing formula (since no closed-form solution exists for $\sigma$).

FIND THE CODE ASSOCIATED WITH THIS README [HERE](../src/2_european_dividend_stocks.py)

## Pricing Model: Black-Scholes-Merton
The Black-Scholes-Merton (1973) formula adjusts the classic Black-Scholes framework by incorporating a continuous dividend yield $q$. Dividends reduce the effective cost of holding the stock, which lowers the present value of the underlying. In practice, this is modeled by replacing $S$ with $Se^{-qT} in the pricing formula. This model assumes exercise only at expiration (European-style). This model requires six inputs:
| Input | Description |
| ----- | ----------- |
| `S` |	Spot price of the underlying asset (i.e. current market price) |
| `K` | Strike price. The fixed price at which the option can be exercised |
| `T` |	Time to expiration, in years (e.g., 6 months = 0.5) |
| `r` |	Risk-free interest rate, continuously compounded (e.g., 5% = 0.05) |
| `q` |	Continuous dividend yield (e.g., 2% = 0.02) |
| `sigma` |	Volatility of the underlying asset (annualized standard deviation) |
| `option_type` | Type of option: `c` for call, `p` for put |

The formulas are:
$$
C=Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)
$$
$$
P=Ke^{-rT}N(-d_2)-Se^{-qT}N(-d_1)
$$
With:
$$
d_{1,2} = \frac{\ln\left(\frac{S}{K}\right)+T\left(r-q\pm \frac{\sigma ^2}{2}\right)}{\sigma \sqrt{T}}
$$
And $N(\cdot)$ as the standard normal cumulative distribution function. This model reduces to the standard Black-Scholes formula when $q=0$.

#### Function Signature
Returns the theoretical option price for a call or put (with continuous dividend yield):

`bsm_price(S, K, T, r, q, sigma, option_type) -> float`

## Implied Volatility

Dividend-adjusted implied volatility – This is calculated by numerically inverting the Black-Scholes-Merton pricing function. Given a market option price and a known dividend yield $q$, this function finds the value of $\sigma$ that reproduces that price. As with the original model, there is no closed-form solution for implied volatility, so Brent's root-finding method is used.

#### Function Signature
Returns the implied volatility for the given Eruopean, dividend-yielding stock option:

`bsm_implied_vol(price, S, K, T, r, q, option_type) -> float`

## Greeks

These are all first or second-order partial derivatives of the dividend-adjusted option pricing function $V(S,K,T,r,q, \sigma)$ to measure how the option's price reacts to changes in market inputs, now incorporating a continuous dividend yield $q$.

- **Delta ($\Delta$):** Sensitivity of the option’s price to changes in the underlying asset price.
- **Gamma ($\Gamma$):** The rate of change of delta with respect to the underlying price (i.e. how stable delta is).
- **Vega ($\nu$):** Sensitivity of the option’s price to changes in volatility ($\sigma$).
- **Theta ($\Theta$):** Sensitivity of the option’s price to the passage of time (i.e., time decay).
- **Rho ($\rho$):** Sensitivity of the option’s price to changes in the risk-free interest rate.

These measures are defined as follows:
$$\Delta = \frac{\partial V}{\partial S}$$
$$\Gamma = \frac{\partial^2 V}{\partial S^2}$$
$$\nu = \frac{\partial V}{\partial \sigma}$$
$$\Theta = -\frac{\partial V}{\partial T}$$
$$\rho = \frac{\partial V}{\partial r}$$

The only new variable introduced in these calculations is $n(\cdot)$, which is the standard normal probability density function.
#### Function Signature
Returns a dictionary of the greeks for the given option:

`bs_implied_vol(price, S, K, T, r, option_type) -> dict`

`{"delta": , "gamma": , "vega": , "theta": , "rho": ,}`