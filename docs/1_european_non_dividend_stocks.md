# European Options on Non-Dividend-Paying Stocks
This is the classic case of a European option on a stock with no dividends. The Black-Scholes model
applies, providing a closed-form solution for call and put prices. Implied volatility is obtained 
by inverting the Black-Scholes formula numerically (since no closed-form solution exists for $\sigma$). 

FIND THE CODE ASSOCIATED WITH THIS README [HERE](../src/1_european_non_dividend_stocks.py)

## Pricing Model: Black-Scholes
The Black-Scholes (1973) formula uses the Black-Scholes-Merton differential equation to price European calls and puts on a non-dividend-paying underlying. This model assumes no dividends during the option’s life and that exercise can only occur at expiration (European-style). The model requires five inputs:
| Input | Description |
| ----- | ----------- |
| `S` |	Spot price of the underlying asset (i.e. current market price) |
| `K` | Strike price. The fixed price at which the option can be exercised |
| `T` |	Time to expiration, in years (e.g., 6 months = 0.5) |
| `r` |	Risk-free interest rate, continuously compounded (e.g., 5% = 0.05) |
| `sigma` |	Volatility of the underlying asset (annualized standard deviation) |
| `option_type` | Type of option: `c` for call, `p` for put |

The formulas are:
$$
C=SN(d_1)-Ke^{-rT}N(d_2)
$$
$$
P=Ke^{-rT}N(-d_2)-SN(-d_1)
$$
With:
$$
d_{1,2} = \frac{\ln\left(\frac{S}{K}\right)+T\left(r\pm \frac{\sigma ^2}{2}\right)}{\sigma \sqrt{T}}
$$
And $N(\cdot)$ as the standard normal cumulative distribution function.

#### Function Signature
Returns the theoretical option price for a call or put:

`bs_price(S, K, T, r, sigma, option_type) -> float`

## Implied Volatility

Black-Scholes implied volatility – Solve for $\sigma$ by numerically inverting the Black-Scholes pricing function. Given a market option price, this function finds the $\sigma$ that reproduces this price in the Black-Scholes formula. There is no closed-form solution for implied vol in the Black-Scholes model, so the Brent's (iterative) method is used.

#### Function Signature
Returns the implied volatility for the given Eruopean, non-dividend stock option:

`bs_implied_vol(price, S, K, T, r, option_type) -> float`

## Greeks

These are all first or second-order partial derivatives of the option pricing function $V(S,K,T,r,\sigma)$ to measure how the option's price reacts to changes in market inputs.

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