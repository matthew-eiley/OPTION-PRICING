# European Options on Commodities (Futures/Forwards)

This case focuses on European options where the underlying is a commodity futures or forward contract. These are typically priced using the Black-76 model, which applies the Black-Scholes framework to futures prices rather than spot prices. The payoff is discounted at the risk-free rate, and implied volatility is computed by numerically inverting the pricing formula.

FIND THE CODE ASSOCIATED WITH THIS README [HERE](../src/3_european_commodities.py)

## Pricing Model: Black-76
The Black-76 (1976) model is a lognormal pricing model designed for options on futures or forward contracts. Instead of the spot price $S$, the model uses the futures or forward price $F$ as the input, since futures already account for cost-of-carry. The model assumes no early exercise and European-style expiration. This model requires five inputs:
| Input | Description |
| ----- | ----------- |
| `F` |	Current futures/forward price of the underlying commodity (contract delivering at or after option maturity) |
| `K` | Strike price. The fixed price at which the option can be exercised |
| `T` |	Time to expiration, in years (e.g., 6 months = 0.5) |
| `r` |	Risk-free interest rate, continuously compounded (e.g., 5% = 0.05) |
| `sigma` |	Volatility of the underlying asset (annualized standard deviation) |
| `option_type` | Type of option: `c` for call, `p` for put |

The formulas are:
$$
C=e^{-rT}\left[FN(d_1)-KN(d_2)\right]
$$
$$
P=e^{-rT}\left[KN(-d_2)-FN(-d_1)\right]
$$
With:
$$
d_{1,2} = \frac{\ln\left(\frac{F}{K}\right)\pm T\left(\frac{\sigma ^2}{2}\right)}{\sigma \sqrt{T}}
$$
And $N(\cdot)$ as the standard normal cumulative distribution function. 

#### Function Signature
Returns the theoretical option price for a European call or put on a futures/forward:

`b76_price(F, K, T, r, sigma, option_type) -> float`

## Implied Volatility

Black-76 implied volatility is computed by numerically inverting the Black-76 pricing formula. Given an option’s market price, this function finds the value of $\sigma$ such that the Black-76 model reproduces the observed price. Like the standard Black-Scholes model, there is no closed-form solution, so Brent’s method is used.

#### Function Signature
Returns the implied volatility for a European option on a futures or forward:
`b76_implied_vol(price, F, K, T, r, option_type) -> float`

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