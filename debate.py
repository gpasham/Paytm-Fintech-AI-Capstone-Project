import os

from stock_universe import STOCK_UNIVERSE


def get_stock_data(ticker):
    """Simulated local tool lookup for the debate agents."""
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Unknown ticker: {ticker}")
    return STOCK_UNIVERSE[ticker].copy()


def bull_agent(ticker, data):
    """Mock bull argument based on the ticker's actual universe data."""
    return (
        f"Bull: With an analyst expected return of "
        f"{data['analyst_expected_return']:.1%} against a beta of "
        f"{data['beta']:.2f}, {ticker} offers attractive risk-adjusted upside."
    )


def bear_agent(ticker, data):
    """Mock bear argument highlighting volatility risk."""
    return (
        f"Bear: The stock's standard deviation of {data['std_dev']:.1%} "
        f"indicates meaningful volatility, while its beta of {data['beta']:.2f} "
        f"also suggests exposure to market movements."
    )


def synthesizer(ticker, data, bull_argument, bear_argument):
    """Mock synthesizer producing a balanced 2–3 sentence summary."""
    return (
        f"Synthesizer: {ticker} presents a potentially attractive opportunity, "
        f"with an analyst expected return of {data['analyst_expected_return']:.1%} "
        f"and a beta of {data['beta']:.2f}. However, its {data['std_dev']:.1%} "
        f"standard deviation highlights meaningful volatility risk. Overall, "
        f"the stock offers upside potential but should be weighed against its "
        f"risk profile and an investor's tolerance for volatility."
    )


def debate(ticker):
    """Run the three-agent debate: bull -> bear -> synthesizer."""
    data = get_stock_data(ticker)

    # Graded baseline: deterministic templates; no LLM call.
    bull_argument = bull_agent(ticker, data)
    bear_argument = bear_agent(ticker, data)
    summary = synthesizer(ticker, data, bull_argument, bear_argument)

    return {
        "ticker": ticker,
        "stock_data": data,
        "bull_argument": bull_argument,
        "bear_argument": bear_argument,
        "synthesis": summary,
    }


def run_debate():
    # One valid ticker chosen from STOCK_UNIVERSE.
    ticker = "PAYTECH"
    return debate(ticker)


if __name__ == "__main__":
    result = run_debate()

    print("=" * 70)
    print(f"3-Agent Debate: {result['ticker']}")
    print("=" * 70)
    print(f"Stock data: {result['stock_data']}")
    print()
    print(result["bull_argument"])
    print()
    print(result["bear_argument"])
    print()
    print(result["synthesis"])
