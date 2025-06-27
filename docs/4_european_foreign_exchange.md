# European Options on Foreign Exchange (FX)

This section focuses on European options where the underlying is a foreign currency exchange rate. These are priced using the Garman-Kohlhagen model (1983), an extension of the Black-Scholes framework that accounts for two interest rates: one domestic and one foreign. The foreign interest rate is modeled as a continuous dividend yield on the foreign currency. Implied volatility is computed by numerically inverting the Garman-Kohlhagen pricing formula.

FIND THE CODE ASSOCIATED WITH THIS README [HERE](../src/4_european_foreign_exchange.py)

## Pricing Model: Garman-Kohlhagen

The Garman–Kohlhagen model adapts Black-Scholes to price options on currency pairs by introducing two risk-free rates:
- $r_d$: domestic interest rate (currency in which the option is settled)
- $r_f$: foreign interest rate (currency being bought or sold)

The spot FX rate $S$ is quoted in domestic currency per one unit of foreign currency (e.g., USD per EUR). The formula resembles the Black-Scholes-Merton model with $r_f$ acting as a dividend yield on the foreign currency. The model requires six inputs:

| Input | Description |
| ----- | ----------- |
| `S` |	Spot FX rate (domestic per 1 unit foreign, e.g., USD/EUR) |
| `K` | Strike price (same unit as $S$) |
| `T` |	Time to expiration, in years (e.g., 6 months = 0.5) |
| `rd` |	Domestic interest rate, continuously compounded (e.g., 5% = 0.05) |
| `rf` |	Foreign interest rate, continuously compounded (e.g., 2% = 0.02) |
| `sigma` |	Volatility of the FX rate (annualized standard deviation) |
| `option_type` | Type of option: `c` for call, `p` for put |

The formulas are:
$$
C=Se^{-r_fT}N(d_1)-Ke^{-r_dT}N(d_2)
$$
$$
P=Ke^{-r_dT}N(-d_2)-Se^{-r_fT}N(-d_1)
$$
With:
$$
d_{1,2} = \frac{\ln\left(\frac{S}{K}\right)+T\left(r_d-r_f\pm \frac{\sigma ^2}{2}\right)}{\sigma \sqrt{T}}
$$
And $N(\cdot)$ as the standard normal cumulative distribution function. 

#### Function Signature
Returns the theoretical FX option price (payoff settled in domestic currency):

`gk_price(S, K, T, rd, rf, sigma, option_type) -> float`

## Implied Volatility

FX implied volatility is the volatility value that, when plugged into the Garman-Kohlhagen pricing formula, yields the market-observed price of the FX option. This is computed using Brent’s method.

#### Function Signature
Returns the implied volatility for the given FX option:
`gk_implied_vol(price, S, K, T, rd, rf, option_type) -> float`

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
$$\rho_d = \frac{\partial V}{\partial r_d}$$
$$\rho_f = \frac{\partial V}{\partial r_f}$$

The only new variable introduced in these calculations is $n(\cdot)$, which is the standard normal probability density function.

#### Function Signature
Returns a dictionary of the greeks for the given option:

`gk_greeks(S, K, T, rd, rf, sigma, option_type) -> dict`

`{"delta": , "gamma": , "vega": , "theta": , "rho": ,}`