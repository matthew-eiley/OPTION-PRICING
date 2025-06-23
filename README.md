# Python Option Pricing Engine

A modular Python-based library for pricing plain-vanilla financial options and calculating implied volatility across asset classes. This tool supports multiple pricing models and allows users to invert models to extract market-implied volatility. Designed with clarity, transparency, and quantitative rigor in mind.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Key Concepts](#key-concepts)
3. [Supported Option Types](#supported-option-types)
4. [Pricing Models](#pricing-models)
5. [Implied Volatility](#implied-volatility)
6. [Function Signatures](#function-signatures)
7.  [References](#references)

---

## Introduction

This Python module implements pricing and implied volatility models for a variety of vanilla options, including:

- European equity options (with and without dividends)
- Commodity options (spot and futures)
- FX (currency) options
- Asian (average price) options
- Spread options
- American options with early exercise

The project aims to strike a balance between mathematical accuracy and accessibility for learners and practitioners.

---

## Key Concepts

### What is an Option?

An **option** is a financial derivative giving the holder the right—but not the obligation—to buy or sell an asset at a pre-agreed price (strike price) on or before a specific date.

- A **Call** allows buying the asset.
- A **Put** allows selling the asset.

### European vs American

- **European Options**: Exercisable only at expiration.
- **American Options**: Exercisable at any time before expiration.

### What is Implied Volatility?

Volatility is a measure of uncertainty or risk. **Implied volatility (IV)** is the market's forecast of a likely movement in a security’s price. It is **not directly observable** and must be solved for using the observed market price of the option and inverting a pricing model.

---

## Supported Option Types

| Option Type                        | Style      | Underlying            | Dividend/Carry Support | Pricing Model               |
|-----------------------------------|------------|------------------------|------------------------|-----------------------------|
| Equity (non-dividend)             | European   | Stock                 | No                     | Black-Scholes               |
| Equity (dividend-paying)          | European   | Stock                 | Yes                    | Black-Scholes-Merton        |
| Commodity Futures                 | European   | Futures/Forwards      | N/A                    | Black-76                    |
| FX (currency)                     | European   | Foreign Exchange Rate | Yes                    | Garman-Kohlhagen            |
| Asian (average price)             | European   | Spot/Futures          | Optional               | Turnbull-Wakeman            |
| Spread (between assets)           | European   | Two Commodities       | N/A                    | Kirk’s Approximation        |
| American (with dividends)         | American   | Stock                 | Yes                    | Bjerksund-Stensland 2002    |
| American (commodities)           | American   | Spot/Futures          | Yes                    | Binomial or Bjerksund-Stensland |

---

## Pricing Models

### 1. **Black-Scholes (1973)**
Used for non-dividend European equity options.  
- Assumes lognormal distribution of returns, constant volatility, and risk-free interest rate.

### 2. **Black-Scholes-Merton**
Extends Black-Scholes to include continuous dividend yield.

### 3. **Black-76**
For European options on futures or forwards.  
- Treats the futures price as the underlying.

### 4. **Garman-Kohlhagen**
An FX-specific model accounting for domestic and foreign interest rates.

### 5. **Turnbull-Wakeman**
An approximation for arithmetic-average Asian options.

### 6. **Kirk’s Approximation**
Used to price spread options between two assets (e.g., Brent vs. WTI oil).

### 7. **Bjerksund-Stensland 2002**
Closed-form approximation for American options with dividends or cost-of-carry.

### 8. **Binomial Tree (CRR)**
Flexible lattice-based model for American options, especially on commodities or futures.

---

## 🔍 Implied Volatility

For every pricing model, an **implied volatility function** is implemented. These numerically invert the pricing formulas using methods like:

- Newton-Raphson
- Bisection
- Brent’s Method

Each IV function solves for `σ` such that `model_price(σ) ≈ observed_market_price`


This allows traders and developers to infer market expectations about volatility.

---

## Function Signatures

Here are standard function interfaces:

```python
# Black-Scholes Price and IV
bs_price(S, K, T, r, sigma, option_type)
bs_implied_vol(price, S, K, T, r, option_type)

# BSM with Dividend Yield
bsm_div_price(S, K, T, r, q, sigma, option_type)
bsm_div_implied_vol(price, S, K, T, r, q, option_type)

# Black-76 (Futures)
black76_price(F, K, T, r, sigma, option_type)
black76_implied_vol(price, F, K, T, r, option_type)

# FX Options
garman_kohlhagen_price(S, K, T, r_dom, r_for, sigma, option_type)
garman_kohlhagen_implied_vol(price, S, K, T, r_dom, r_for, option_type)

# Asian Options (Turnbull-Wakeman)
asian_price_TW(S_or_F, K, T, sigma, r, q, option_type)
asian_implied_vol(price, S_or_F, K, T, r, q, option_type)

# Spread Options (Kirk's Approximation)
spread_price_kirk(F1, F2, K, T, vol1, vol2, rho, r, option_type)
spread_implied_comb_vol(price, F1, F2, K, T, vol1, vol2, r, option_type)

# American Options
american_price_bjs(S, K, T, r, q, sigma, option_type)
american_implied_vol(price, S, K, T, r, q, option_type)

# American Commodity Options
american_commodity_price(S_or_F, K, T, r, y, sigma, option_type)
american_commodity_implied_vol(price, S_or_F, K, T, r, y, option_type)
```

## References
This implementation is based on industry-standard models:

Black-Scholes (1973)

Merton's dividend model

Black-76 (1976)

Garman-Kohlhagen (1983)

Turnbull & Wakeman (1991)

Kirk (1995)

Bjerksund-Stensland (2002)