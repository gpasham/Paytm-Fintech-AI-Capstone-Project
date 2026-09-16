from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN

# Illustrative assumptions; all cash flows are INR million.
EBIT = 100.0
TAX_RATE = 0.25
D_AND_A = 20.0
CAPEX = 25.0
DELTA_NWC = 10.0

# FCFF = EBIT * (1 - tax rate) + D&A - CapEx - ΔNet Working Capital
BASE_FCFF = EBIT * (1 - TAX_RATE) + D_AND_A - CAPEX - DELTA_NWC

# Cost of equity: CAPM using PAYINFRA beta.
BETA_TICKER = "PAYINFRA"
BETA = STOCK_UNIVERSE[BETA_TICKER]["beta"]
COST_OF_EQUITY = RISK_FREE_RATE + BETA * (MARKET_RETURN - RISK_FREE_RATE)

# Illustrative capital structure: 70% equity / 30% debt.
PRETAX_COST_OF_DEBT = 0.085
AFTER_TAX_COST_OF_DEBT = PRETAX_COST_OF_DEBT * (1 - TAX_RATE)
EQUITY_WEIGHT = 0.70
DEBT_WEIGHT = 0.30
WACC = EQUITY_WEIGHT * COST_OF_EQUITY + DEBT_WEIGHT * AFTER_TAX_COST_OF_DEBT

# Five-year growth fades from 12% to 5%; terminal growth is 4%.
GROWTH_RATES = [0.12, 0.10, 0.08, 0.06, 0.05]
TERMINAL_GROWTH = 0.04

# Illustrative EV/EBITDA cross-check.
EBITDA = 90.0
EBITDA_MULTIPLE = 12.0


def project_fcffs():
    fcffs = []
    current = BASE_FCFF
    for growth in GROWTH_RATES:
        current *= 1 + growth
        fcffs.append(current)
    return fcffs


def dcf(discount_rate=WACC, terminal_growth=TERMINAL_GROWTH):
    if discount_rate <= terminal_growth:
        raise ValueError("Discount rate must exceed terminal growth.")

    fcffs = project_fcffs()
    pv_fcffs = [
        fcf / (1 + discount_rate) ** year
        for year, fcf in enumerate(fcffs, 1)
    ]
    terminal_value = (
        fcffs[-1] * (1 + terminal_growth)
        / (discount_rate - terminal_growth)
    )
    pv_terminal_value = terminal_value / (1 + discount_rate) ** 5

    return {
        "projected_fcffs": fcffs,
        "pv_fcffs": pv_fcffs,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": sum(pv_fcffs) + pv_terminal_value,
    }


def self_check_terminal_growth():
    # Required: WACC - terminal growth >= 1pp in the worst sensitivity cell.
    wacc_values = [WACC - 0.01, WACC, WACC + 0.01]
    growth_values = [
        TERMINAL_GROWTH - 0.01,
        TERMINAL_GROWTH,
        TERMINAL_GROWTH + 0.01,
    ]
    worst_gap = min(w - g for w in wacc_values for g in growth_values)
    assert worst_gap >= 0.01, "Required WACC/growth constraint failed."
    return worst_gap


def sensitivity_table():
    self_check_terminal_growth()
    wacc_values = [WACC - 0.01, WACC, WACC + 0.01]
    growth_values = [
        TERMINAL_GROWTH - 0.01,
        TERMINAL_GROWTH,
        TERMINAL_GROWTH + 0.01,
    ]
    return {
        f"{wacc:.2%}": {
            f"{growth:.2%}": dcf(wacc, growth)["enterprise_value"]
            for growth in growth_values
        }
        for wacc in wacc_values
    }


def ev_ebitda_cross_check():
    return EBITDA * EBITDA_MULTIPLE


def run_valuation():
    return {
        "base_case": dcf(),
        "sensitivity": sensitivity_table(),
        "worst_case_WACC_minus_terminal_growth": self_check_terminal_growth(),
        "ev_ebitda": ev_ebitda_cross_check(),
    }


if __name__ == "__main__":
    result = run_valuation()

    print(f"Base FCFF: INR {BASE_FCFF:.2f}m")
    print(f"Cost of equity: {COST_OF_EQUITY:.2%}")
    print(f"WACC: {WACC:.2%}")
    print(f"Terminal growth: {TERMINAL_GROWTH:.2%}")
    print(f"Worst-case WACC - g: {result['worst_case_WACC_minus_terminal_growth']:.2%}")
    print(f"DCF enterprise value: INR {result['base_case']['enterprise_value']:.2f}m")
    print(f"EV/EBITDA enterprise value: INR {result['ev_ebitda']:.2f}m")
    print("\nSensitivity table — EV (INR million):")
    for wacc, row in result["sensitivity"].items():
        print(wacc, row)
