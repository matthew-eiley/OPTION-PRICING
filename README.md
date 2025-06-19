# Python Option Pricing

This is a software and data engineering project which implements a suite of models for pricing financial options in Python. The focus is on building modular, transparent code while exploring advanced quantitative finance concepts.

## Overview
This project is intended to price a type of financial product called [options](https://www.investopedia.com/terms/o/option.asp). These are a type of [financial derivative](https://www.investopedia.com/terms/d/derivative.asp). The models are mostly different variations of the [Black-Scholes-Merton (BSM) model](https://www.investopedia.com/terms/b/blackscholes.asp) that is used to price [European options](https://www.investopedia.com/terms/e/europeanoption.asp).<br/><br/>
***Note that the 76 appended to some of the models below is to indicate (in honour of the Black76 model) that it is for a commodity option.***

### Option Pricing Models
| Pricing Models                                                          | Description                               |
| ----------------------------------------------------------------------- | ----------------------------------------- |
| [BlackScholes()](https://www.investopedia.com/terms/b/blackscholes.asp) | Stock options (no dividend yield)         |
| [Merton()](https://www.investopedia.com/terms/m/mertonmodel.asp)        | Index options (continuous dividend yield) |
| [Black76()](https://www.investopedia.com/terms/b/blacksmodel.asp)       | Commodity options                         |
| GarmanKohlhagen()                                                       | FX options                                |
| Asian76()                                                               | Asian options (on commodities)            |
| Kirks76()                                                               | Spread options (Kirk's approximation)     |
| American()                                                              | American options                          |
| American76()                                                            | American options (on commodities)         |

### Implied Volatility Calculations
| Implied Volatility Formula | Description                       |
| -------------------------- | --------------------------------- |
| EuroImpVol()               | European options                  |
| EuroImpVol76()             | European options (on commodities) |
| AmerImpVol()               | American options                  |
| AmerImpVol76()             | American options (on commodities) |

## Model Use

To access the user-interface, [click here.](https://github.com/matthew-eiley/OPTION-PRICING)

The inputs for the pricing formulas are:
```python
BlackScholes(option_type, x, fs, t, r, v)
Merton(option_type, x, fs, t, r, q, v)
Black76(option_type, x, fs, t, r, v)
GarmanKohlhagen(option_type, x, fs, t, b, r, rf, v)
Asian76(option_type, x, fs, t, ta, r, v)
Kirks76(option_type, x, f1, f2, t, r, v1, v2, corr)
American(option_type, x, fs, t, r, q, v)
American76(option_type, x, fs, t, r, v)
```
Similarly, the inputs for the implied volatility formulas are:
```python
EuroImpVol(option_type, x, fs, t, r, q, cp)
EuroImpVol76(option_type, x, fs, t, r, cp)
AmerImpVol(option_type, x, fs, t, r, q, cp)
AmerImpVol76(option_type, x, fs, t, r, cp)
```

### Inputs used by all
| Parameter | Description |
| :-------: | :---------- |
| `option_type` | Putt/Call indicator. `p` indicates a put and `c` indicates a call. |
| `fs` | Price of underlying. `fs` is used generically, but some models use `f` (forward price) or `s` (spot price). |
| `x` | Strike price. This is the exercise price. |
| `t` | Time to maturity. Given in years. |
| `r` | Risk-free interest rate. |
| `v` | Implied volatility. Annualized implied volatility. |

### Inputs used by some
| Parameter | Description |
| :-------: | :---------- |
| `q` | Continuous dividend. |
| `rf` | Foreign interest rate. |
| `ta` | Asian start time. This is the time that starts the averaging period. As `ta` approaches `t`, the Asian76 value should approach the Black76 value. |
| `cp` | Option price (used in implied volatility calculations). |
| `f1` | Price of underlying 1 in a spread. |
| `f2` | Price of underlying 2 in a spread. |
| `v1` | Implied volatility of first asset in a spread. |
| `v2` | Implied volatility of second asset in a spread. |
| `corr` | Correlation between the two assets in a spread. |

### Outputs
If using the program and not the UI, the output of each function is simply an array with the following elements:
| Index   | Description |
| ------- | :---------- |
| `[0]`   | Value |
| `[1]`   | Delta (sensitivity of value to cahnges in price) |
| `[2]`   | Gamma (sensitivity of delta to changes in price) |
| `[3]`   | Theta (sensitivity of value to changes in time to expiration) |
| `[4]`   | Vega (sensitivity of value to changes in volatility) |
| `[5]`   | Rho (sensitivity of value to changes in risk-free rates) |

## Theory

### Generalized Black-Scholes

The BSM model is what is typically used to price European options. The original BSM model was formulated in 1973 for non-dividend paying stocks. Since then, many extensions of this model have been created which are collectively referred to as the "Black-Scholes Genre" option models. In these other models, the original formula has been altered to price other options for other financial instruments like dividend paying stocks, commodity futures, and FX forwards. Mathematically, most of these models are quite similar, the main differences being whether or not the the asset has a [carrying cost](https://www.investopedia.com/terms/c/carrying-costs.asp) and how the present value of the asset is determined. 

The Black Scholes genre models are based on a number of assumptions about how financial markets operate:
1. **Arbitrage-Free:** Traders try to maximize personal profits and don't allow for arbitrage opportunities.
2. **Frictionless and Continuous:** It is possible to buy and sell any amount of the underlying at any time without any transaction costs.
3. **Risk Free Rates:** It is possible to borrow/lend money at a risk-free interest rate.
4. **Log-Normally Distributed Price Movements:** Prices are log-normally distributed and described by Geometric Brownian Motion.
5. **Constant Volatility:** Volatility is constant across the life of the option contract.

The traditional BSM model is used to price stock options based on the idea that stock prices follow a random path over time, starting from their current value. On average, prices are expected to rise at the risk-free interest rate. The Merton version adjusts the model to include dividends or other carrying costs. The Black-76 model changes the starting point from today’s price to a future (forward) price. Another variation, the Garman-Kohlhagen model, is used for pricing foreign exchange (FX) options. It accounts for the fact that each currency in a pair has its own interest rate.
- **Black-Scholes (Stocks):** This model is used for options on regular stocks, which are priced based on their current market value (the “spot price”). The model assumes the stock price grows over time at the risk-free rate.
- **Merton (Stocks with Dividends):** This version adjusts the Black-Scholes model for stocks that pay continuous dividends. Since option holders don’t receive dividends, the value of the option is slightly lower.
- **Black-76 (Commodities and Futures):** This model is for options on futures or commodities, where pricing is based on a future delivery price instead of today’s price. The forward price is discounted back to present value.
- **Garman-Kohlhagen (Foreign Exchange):** This model is used for FX options and adjusts for the fact that each currency in a pair has its own interest rate. Each currency’s future value is discounted using its respective rate.

The generalized BSM formulas can be seen below. While they looks complicated, most of the terms can either be found in the option contract or are prices easily available in the market. The only difficult term to calculate is implied volatility $V$, which is typically calculated using prices of other options that have recently been traded.
| Use                           | Formula                                                                                                               |
| :---------------------------: | :-------------------------------------------------------------------------------------------------------------------: |
| Call Price                    | $C = Fe^{(b-r)T} N(D_1) - Xe^{-rT} N(D_2)$                                                                            |
| Put Price                     | $P = Xe^{-rT} N(-D_2) - Fe^{(b-r)T} N(-D_1)$                                                                          |
| Intermediate<br/>Calculations | $D_1 = \frac{\ln\left(\frac{F}{X}\right) + T\left(b+\frac{V^2}{2}\right)}{V\cdot\sqrt{T}}$<br/>$D_2 = D_1 - V\sqrt{T}$|


**With the following symbol meanings:**
| Symbol     | Meaning                                                                                                                                |  
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| $C$        | The price of a European call option. The cost to buy the right to purchase the underlying asset at strike price $X$ at time $T$        |
| $P$        | The price of a European put option. The cost to buy the right to sell the underlying asset at strike price $X$ at time $T$.            |
| $F$        | The current price of the underlying asset on the valuation date. This may be a spot price (for stocks) or a futures price (for commodities), depending on the asset type.                                                                                                            | 
| $X$        | The strike (or exercise) price. The fixed price at which the option can be exercised.                                                  | 
| $T$        | Time to expiration, expressed in years, from the current date to the option’s maturity. $T = \frac{(t_1 - t_0)}{365}$                  | 
| $t_1$      | Expiration Date. The date on which the option must be exercised.                                                                       |
| $t_0$      | Valuation Date. The date on which the option is being valued.                                                                          | 
| $V$        | The volatility of the underlying asset’s returns, assumed constant and annualized; also commonly denoted as $\sigma$.                  | 
| $N()$      | The cumulative distribution function (CDF) of the standard normal distribution. It gives the probability that a normally distributed random variable is less than or equal to the given input.                                                                                             | 
| $D_1, D_2$ | Intermediate variables used in the Black-Scholes formula. They represent normalized distances between the forward price and strike, adjusted for volatility and time, and help determine the likelihood of the option finishing in the money.                                             |
| $r$        | The continuously compounded risk-free interest rate used to discount future cash flows.                                                |
| $b$        | The cost of carry. A rate that accounts for factors like dividends, storage costs, or foreign interest rates                           |

**With the cost of carry varying as follows:**
| Model            | Cost of Carry ($b$)   | 
|------------------|-----------------------| 
| Black Scholes    | $b = r$               | 
| Merton           | $b = r - q$           |
| Black 76         | $b = 0$               |
| Garman Kohlhagen | $b = r - r_f$         | 
| Asian            | $b = 0$, modified $V$ |

**With the symbol meanings:**
| Symbol  | Meaning                                                                                                                                    | 
|---------|--------------------------------------------------------------------------------------------------------------------------------------------| 
| $q$     | The continuous dividend yield of the underlying asset. It represents the annualized rate at which dividends are paid, expressed continuously, and is subtracted from the cost of carry when pricing options on dividend-paying stocks.                                                 |
| $r_f$   | The foreign risk-free interest rate used in foreign exchange (FX) option pricing. It reflects the continuously compounded interest rate of the foreign currency in a currency pair, and is used alongside the domestic rate $r$ to adjust for interest rate differentials.                        | 

### Asian Volatility Adjustment

Asian options, also known as average price options, base their payoff on the average price of the underlying over a set period rather than its price at expiration. This averaging reduces the impact of market manipulation or price spikes on the expiry date, making these options popular in volatile or strategically important markets like crude oil.

Because averaging lowers price variability, Ad volatisian options typically have lower effective volatility than comparable European options. The average of a set of lognormal distributions is not itself lognormally distributed, making calculations quite complicated. As such, for Asian options on futures, a modified Black-76 formula can be used, substituting the standard volatility with an adjusted average-price volatility, provided the averaging period begins in the future.
| Use                       | Formula                                                                                     |
| :-----------------------: | :-----------------------------------------------------------------------------------------: |
| Asian-Adjusted Volatility | $V_a = \sqrt{\frac{\ln(M)}{T}}$                                                             |
| Intermediate Calculation  | $M = \frac{2e^{V^2T} - 2e^{V^2T}\left[1+V^2\left(T-t\right)\right]}{V^4\left(T-t\right)^2}$ |

**With the symbol meanings:**
| Symbol | Meaning                                                                                                                                    | 
|--------|--------------------------------------------------------------------------------------------------------------------------------------------| 
| $V_a$  | The adjusted volatility used to price an Asian option, accounting for the smoothing effect of averaging prices over time. It replaces the standard volatility in the modified Black-76 formula.                                                                                                 |
| $M$    | An intermediate factor derived from the original volatility and timing inputs; it adjusts for the variance of the average price over the averaging period.                                                                                                                                               | 
| $V$    | The standard annualized volatility of the underlying asset, assumed constant. It reflects the price variability of the asset without adjustment for averaging.                                                                                                                             |
| $T$    | The time to option expiry, in years. It defines the total time horizon over which the option value is determined.                          | 
| $t$    | The start time of the averaging period, in years from valuation. Averaging begins at time $t$, and continues until maturity at $T$         |

### Spread Options and Kirk’s Approximation

Spread options derive their value from the difference between two commodity prices and are often used to model real-world physical assets as “real options.” For example, consider a power plant that converts natural gas into electricity. The plant earns a profit when the price of electricity exceeds the cost of the fuel by more than the plant’s operating cost. This difference — electricity price minus fuel cost — is the spread, and the plant will only operate if that spread exceeds a certain threshold, such as its variable operations and maintenance cost (VOM). In this context, a spread option models the decision to operate the plant, with the VOM acting as the strike price.

While there’s no exact closed-form solution for spread options, Kirk’s approximation offers a practical and accurate estimate. It transforms the spread into a ratio of two lognormal variables, leveraging the fact that this ratio is approximately lognormal, allowing the use of Black-Scholes-genre formulas to value the option as if it were based on a single underlying asset.

Accordingly, the payoff of a spread option is:
$$
C=\max\left[F_1-F_2-X, 0\right]
$$
$$
P=\max\left[X-\left(F_1-F_2\right), 0\right]
$$
**With the symbol meanings:**
| Symbol | Meaning                                     | 
|--------|---------------------------------------------| 
| $F_1$  | The price of asset 1 (the output commodity) |
| $F_2$  | The price of asset 2 (the input commodity)  | 

These formulas can (trivially) be algebraically manipulated to the following:
$$
C=\max\left[\frac{F_1}{F_2+X}-1, 0\right]\left(F_2+X\right)
$$
$$
P=\max\left[1-\frac{F_1}{F_2+X}, 0\right]\left(F_2+X\right)
$$
Allowing Kirk's approximation to be used to model the distribution of the spread as the ratio $\frac{F_1}{F_2+X}$. This ratio can now be converted into a formula very similar to the Generalized Black Scholes formula from above, with the simple addition of the $F_2+X$ multiplicand. 

The ratio of prices is to be used as $F=\frac{F_1}{F_2+X}$. It follows that the option is profitable ("in the money") whenever the ratio is greater than 1 (occuring when the price of the output commodity is greater than the total of the cost of the input commodity and the conversion cost). This necessitates a modification to the call and put price formulas as well as the $D_1$ formula, as the option is in the money when $F>1$, i.e. the strike price $X$ must be changed to $1$. 
| Use                           | Formula                                                                                                      |
| :---------------------------: | :----------------------------------------------------------------------------------------------------------: |
| Spread Option Call Price      | $C = \left(F_2+X\right)\left[Fe^{(b-r)T}N(D_1) - e^{-rT}N(D_2)\right]$                                       |
| Spread Option Put Price       | $P = \left(F_2+X\right)\left[e^{-rT}N(-D_2) - Fe^{(b-r)T} N(-D_1)\right]$                                    |
| Intermediate<br/>Calculations | $D_1 = \frac{\ln\left(F\right) + T\left(b+\frac{V^2}{2}\right)}{V\cdot\sqrt{T}}$<br/>$D_2 = D_1 - V\sqrt{T}$ |

Given these formulas, the main challenge in valuing spread options is determining the correct volatility to use in the pricing formula. Kirk’s approximation addresses this by assuming that the ratio of two lognormal variables is approximately normally distributed. This assumption allows the spread to be transformed and modeled using a modified Black-Scholes framework, making it possible to estimate an effective volatility for the option.
$$
V=\sqrt{V_1^2+\left(\frac{V_2 F_2}{F_2+X}\right)^2-\frac{2\rho V_1 V_2 F_2}{F_2+X}}
$$
**With the symbol meanings:**
| Symbol | Meaning                                 | 
|--------|-----------------------------------------| 
| $V$    | The effective volatility of the spread option, used as the input in the modified Black-Scholes-style pricing formula. |
| $V_1$  | The volatility of the first underlying asset (the output commodity) | 
| $V_2$  | The volatility of the second underlying asset (the input commodity) |
| $F_2$  | The price of asset 2 (the input commodity) | 
| $X$    | The strike price of the spread option, typically representing the fixed cost of conversion (VOM) |
| $\rho$ | The correlation coefficient between the returns of the two underlying assets, capturing how their prices move relative to each other | 

### American Options

American options differ from European options because they can be exercised at any time before expiration. This flexibility adds value, especially when early exercise is more profitable than selling the option – typically when the option is in the money, interest rates are high, or carrying costs are significant.

The cost of carry refers to the cash flows from holding an asset. For example, stocks pay dividends (positive carry), while commodities may incur storage costs (negative carry). Option holders do not receive these cash flows, only holders of the actual asset do. For call options on dividend-paying stocks, the effective cost of carry is $r-q$ where $r$ is the interest rate and $q$ is the dividend yield.

Early exercise is a tradeoff. Giving up an option’s remaining (extrinsic) value to gain immediate cash flow or asset exposure. For puts, early exercise is more attractive when interest rates are high and cost of carry is low or negative. For calls, it becomes valuable when dividends are significant and interest rates are low.

In commodity options, early exercise is rare. These are typically written on forwards or futures, which have no cost of carry and no intermediate cash flows. Early exercise only becomes attractive when interest rates are very high (often above 15–20%), allowing the immediate cash benefit to outweigh the remaining optionality.

There’s no exact formula for American option pricing, but models such as Bjerksund-Stensland (produced in 1993 and improved in 2002) provide efficient and accurate approximations.

#### Put/Call Duality Identity

It is possible to calculate the value of a put option using the call valuation formula, according to:
$$
P(S,X,T,r,b,V) = C(X,S,T,r-b,-b,V)
$$

#### Bjerksund Stensland 2002

**Reference:** [Bjerksund Stensland 2002](https://www.researchgate.net/publication/228801918_Closed_form_valuation_of_American_options)

There is no exact closed-form solution for pricing American options, but several closed-form approximations have been developed. One widely used method is the Bjerksund-Stensland model, originally introduced in 1993 and refined in 2002. The 2002 version, now the standard, estimates the value of an American option by calculating an early exercise boundary and approximating the probability of crossing it. This model uses the same inputs as the Generalized BSM framework:

| Symbol | Meaning               |  
| ------ | --------------------- |
| $F$    | Forward or spot price |
| $X$    | Strike price          |
| $T$    | Time to expiration    | 
| $r$    | Risk-free rate        | 
| $b$    | Cost of carry         | 
| $V$    | Volatility            |

##### Intermediate Calculation: Psi

The psi function is an intermediate calculation necessary for this approximation.
$$
\psi (F,t_2, \gamma, H, I_2, I_1, t_1, r, b, V)
$$

The psi function itself contains many of its own intermediate calculations:
$$A_1=V\ln(t_1)$$
$$A_2=V\ln(t_2)$$
$$B_1=t_1\cdot\left[b+\left(\gamma - 0.5\right)V^2\right]$$
$$B_2=t_2\cdot\left[b+\left(\gamma - 0.5\right)V^2\right]$$
$$d_1=\frac{\ln\left(\frac{F}{I_1}\right)+B_1}{A_1}$$
$$d_2=\frac{\ln\left(\frac{I_2^2}{I_1F}\right)+B_1}{A_1}$$
$$d_3=\frac{\ln\left(\frac{F}{I_1}\right)-B_1}{A_1}$$
$$d_4=\frac{\ln\left(\frac{I_2^2}{I_1F}\right)-B_1}{A_1}$$
$$e_1=\frac{\ln\left(\frac{F}{H}\right)+B_2}{A_2}$$
$$e_2=\frac{\ln\left(\frac{I_2^2}{HF}\right)+B_2}{A_2}$$
$$e_3=\frac{\ln\left(\frac{I_1^2}{HF}\right)+B_2}{A_2}$$
$$e_4=\frac{\ln\left(\frac{I_1^2F}{I_2^2H}\right)+B_2}{A_2}$$
$$\tau = \sqrt{\frac{t_1}{t_2}}$$
$$\lambda = -r+\gamma b+\frac{\gamma}{2}\left(\gamma -1\right)V^2$$
$$\kappa = \frac{2b}{V^2}+2\gamma -1$$

With all of these calculations, we can calculate psi as follows. Note that the function $M()$ will be described in two sections.

$$\psi = e^{\lambda t_2}F^\gamma M(-d_1, -e_1, \tau) - \left(\frac{I_2}{F}\right)^\kappa M(-d_2, -e_2, \tau) - \left(\frac{I_1}{F}\right)^\kappa M(-d32, -e_3, \tau) + \left(\frac{I_1}{I_2}\right)^\kappa M(-d_4, -e_4, \tau)$$

##### Intermediate Calculation: Phi

The phi function is another intermediate calculation necessary for this approximation.
$$
\phi (F, T, I, \gamma, r, b, V)
$$
With the symbol meanings:
| Symbol   | Meaning                                 |  
| -------- | --------------------------------------- |
| $F$      | Forward or spot price                   |
| $T$      | Time to expiration                      | 
| $I$      | Trigger price (as calculated in BS2002) |
| $\gamma$ | Modifier to $T$ (calculated in BS2002)  |
| $r$      | Risk-free rate                          | 
| $b$      | Cost of carry                           | 
| $V$      | Volatility                              |

The function is implemented as follows:
$$d_1 = -\frac{\ln\left(\frac{F}{H}\right)+T\left[b+\left(\gamma -0.5\right)V^2\right]}{V\sqrt{T}}$$
$$d_2 = d_1-\frac{2\ln\left(\frac{I}{F}\right)}{v\sqrt{T}}$$
$$\lambda = -r+\gamma b+\frac{\gamma}{2}\left(\gamma -1\right)V^2$$
$$\kappa = \frac{2b}{V^2}+2\gamma -1$$
$$\phi = e^{\lambda T}F^\gamma \left[N(d_1)-\left(\frac{I}{F}\right)^\kappa N(d_2)\right]$$

##### Intermediate Function: Normal Cumulative Density Function

The function $N()$ is the [NCDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function). It is part of `scipy.stats` so is be used "freely" (without definition) in this model.

##### Intermediate Function: Cumulative Bivariate Normal Distribution

The function $M()$ is the [CBND](https://mathworld.wolfram.com/BivariateNormalDistribution.html). It represents the bivariate normal density function integrated over $x$ and $y$ to calculate the joint probability that $x\lt a$ and $y\lt b$ as follows:
$$M(a,b,\rho) = \frac{1}{2\pi \sqrt{1-\rho^2}}\int_{-\infty}^a\int_{-\infty}^b \exp{\left[-\frac{x^2-2\rho xy+y^2}{2(1-\rho^2)}\right]}d_yd_x$$
With the symbol meanings:
| Symbol | Meaning                       |  
| ------ | ----------------------------- |
| $x$    | First variable                |
| $y$    | Second variable               | 
| $a$    | First variable's upper bound  |
| $b$    | Second variable's upper bound |
| $\rho$ | Correlation between variables | 

Though this equation has no closed-form solution, though several approximations exist and are included in the `numpy` library. The [Genz 2004 model](https://www.researchgate.net/publication/38389760_Approximations_to_multivariate_t_integrals_with_application_to_multiple_comparison_procedures) is used in this implementation and it has an accuracy of 14 decimal points.