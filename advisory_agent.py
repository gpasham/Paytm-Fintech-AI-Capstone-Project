import os

from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES


def get_stock_data(ticker):
    """Simulated external-API tool call using the local stock universe."""
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Unknown ticker: {ticker}")
    return STOCK_UNIVERSE[ticker].copy()


ALLOCATION_RULES = {
    "Conservative": ("PAYBOND", "PAYGOLD", "PAYRETAIL"),
    "Moderate": ("PAYRETAIL", "PAYINFRA", "PAYGOLD"),
    "Aggressive": ("PAYTECH", "PAYFIN", "PAYINFRA"),
}


def calculate_portfolio(risk_tolerance, tickers):
    """Observe stock data and compute CAPM return and portfolio volatility."""
    weight = 1 / 3
    stock_data = {ticker: get_stock_data(ticker) for ticker in tickers}

    # CAPM expected return uses beta only; analyst_expected_return is ignored.
    capm_returns = {
        ticker: RISK_FREE_RATE
        + stock_data[ticker]["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
        for ticker in tickers
    }

    portfolio_return = sum(weight * capm_returns[ticker] for ticker in tickers)

    # Var(Rp) = sum(w_i^2 sigma_i^2)
    variance = sum(
        weight**2 * stock_data[ticker]["std_dev"]**2
        for ticker in tickers
    )

    # + 2 * sum(i<j) w_i*w_j*Cov(i,j), with rho = 0.3.
    rho = 0.3
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            sigma_i = stock_data[tickers[i]]["std_dev"]
            sigma_j = stock_data[tickers[j]]["std_dev"]
            covariance = rho * sigma_i * sigma_j
            variance += 2 * weight * weight * covariance

    portfolio_std_dev = variance**0.5

    return {
        "risk_tolerance": risk_tolerance,
        "tickers": list(tickers),
        "weights": {ticker: weight for ticker in tickers},
        "stock_data": stock_data,
        "capm_returns": capm_returns,
        "expected_portfolio_return": portfolio_return,
        "portfolio_variance": variance,
        "portfolio_std_dev": portfolio_std_dev,
    }


def mock_llm_sentence(investor_id, risk_tolerance, tickers, expected_return, volatility):
    """The only narrative-generation step gated by MOCK_LLM."""
    template = (
        f"For {risk_tolerance} investor {investor_id}, we recommend an allocation "
        f"across {', '.join(tickers)} with an expected portfolio return of "
        f"{expected_return:.1%} and volatility of {volatility:.1%}."
    )

    if os.getenv("MOCK_LLM", "1") != "0":
        return template

    # Optional extension point: without an actual LLM/API dependency, preserve
    # the exact same numbers and deterministic recommendation in this example.
    return template


def advisory_agent(investor):
    """
    Agent loop with explicit stages:
      1. Think
      2. Act
      3. Observe -> decide
    """
    investor_id = investor["investor_id"]
    risk_tolerance = investor["risk_tolerance"]

    # THINK: prescribed lookup table; no free-choice mapping.
    if risk_tolerance not in ALLOCATION_RULES:
        raise ValueError(f"Unsupported risk tolerance: {risk_tolerance}")

    tickers = ALLOCATION_RULES[risk_tolerance]

    # ACT: simulated tool calls, one for each prescribed ticker.
    stock_data = [get_stock_data(ticker) for ticker in tickers]

    # OBSERVE -> DECIDE: calculate using the observed tool data.
    result = calculate_portfolio(risk_tolerance, tickers)

    # Keep the explicitly observed tool-call results in the final record.
    result["tool_observations"] = {
        ticker: data for ticker, data in zip(tickers, stock_data)
    }
    result["investor_id"] = investor_id
    result["horizon_years"] = investor["horizon_years"]
    result["investment_amount_inr"] = investor["investment_amount_inr"]

    # Human-in-the-loop escalation threshold: strictly greater than 20%.
    if result["portfolio_std_dev"] > 0.20:
        result["status"] = "ESCALATED_TO_HUMAN_ADVISOR"
        result["recommendation"] = None
    else:
        result["status"] = "FINALIZED"
        result["recommendation"] = mock_llm_sentence(
            investor_id,
            risk_tolerance,
            tickers,
            result["expected_portfolio_return"],
            result["portfolio_std_dev"],
        )

    return result


def run_all_profiles():
    """Run the advisory loop for all five investor profiles."""
    return [advisory_agent(investor) for investor in INVESTOR_PROFILES]


if __name__ == "__main__":
    results = run_all_profiles()

    for result in results:
        print("=" * 70)
        print(f"Investor: {result['investor_id']}")
        print(f"Risk tolerance: {result['risk_tolerance']}")
        print(f"Allocation: {result['weights']}")
        print(
            f"CAPM expected return: "
            f"{result['expected_portfolio_return']:.4%}"
        )
        print(f"Portfolio variance: {result['portfolio_variance']:.6f}")
        print(f"Portfolio std dev: {result['portfolio_std_dev']:.4%}")
        print(f"Status: {result['status']}")

        if result["recommendation"]:
            print(f"Recommendation: {result['recommendation']}")
