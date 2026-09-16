# Paytm Investment Advisory & Risk Analysis Tasks

The implementations use deterministic mock logic for the recorded baseline runs.

## Recorded Run Configuration

The recorded run transcripts were generated with:

```text
MOCK_LLM=1
```

This means the baseline runs **did not make external LLM/API calls**. The narrative portions that support an optional LLM extension use deterministic templates, while the quantitative calculations and disclosure-signal extraction are performed locally.

### Recorded baseline outputs

| Task | Recorded mode | External LLM call |
|---|---|---|
| `advisory_agent.py` | `MOCK_LLM=1` | No |
| `extract_disclosure.py` | Mock baseline | No |
| `debate.py` | Mock baseline | No |
| `dcf_calculator.py` | Deterministic calculation | No |

The disclosure extractor's baseline keyword/regex logic and the portfolio calculations do not require an LLM.

## Files

```text
stock_universe.py
investor_profiles.py
disclosure_snippets.py
advisory_agent.py
extract_disclosure.py
debate.py
dcf_calculator.py
blockchain_risk_note.md
```

## Requirements

- Run the scripts from the directory containing the files.

## How to Run

### 1. Advisory Agent

```bash
MOCK_LLM=1 python advisory_agent.py
```

On Windows PowerShell:

```powershell
$env:MOCK_LLM="1"
python advisory_agent.py
```

The script:

1. Builds the prescribed portfolio from the investor's risk profile.
2. Retrieves stock data from the local stock universe.
3. Calculates CAPM expected returns.
4. Calculates portfolio expected return and volatility.
5. Escalates portfolios whose standard deviation exceeds 20%.
6. Produces the advisory narrative using the mock baseline.

Expected baseline pattern:

- Conservative investors: finalized
- Moderate investors: finalized
- Aggressive investors: escalated to a human advisor

### 2. Disclosure Extraction

```bash
python extract_disclosure.py
```

The baseline extractor identifies:

- Risk flags such as litigation, regulatory exposure, and customer concentration
- Hedging language
- Sentiment: `confident`, `cautious`, or `neutral`

The recorded signal output is stored in:

```text
disclosure_signal_outputs.json
```

### 3. Multi-Agent Debate

```bash
python debate.py
```

The script runs a three-agent mock debate for the selected ticker:

- Bull
- Bear
- Synthesizer

The baseline output uses the actual stock-universe values for beta, analyst expected return, and standard deviation.

### 4. DCF Calculator

```bash
python dcf_calculator.py
```

The recorded output is stored in:

```text
dcf_output.json
```

### 5. Blockchain Risk Note

`blockchain_risk_note.md` is a written risk-analysis deliverable and does not require execution.

It covers:

- Fiat-collateralized vs. algorithmic stablecoins
- Tokenomics and DAO-governance risks
- Crypto allocation recommendation
- CAPM/portfolio considerations
- Survivorship bias and transaction costs
- T.A.N.G. social-engineering risks
- Real-time bank-side defenses

## Reproducing the Baseline

From the project directory:

```bash
python extract_disclosure.py
python debate.py
python dcf_calculator.py
```

For the advisory agent, explicitly enable mock mode:

```bash
MOCK_LLM=1 python advisory_agent.py
```

This reproduces the intended deterministic workflow without requiring external credentials or API access.

## Key Design Principle

The project separates:

**Think → Act → Observe → Decide**

The advisory workflow first determines the portfolio from the investor profile, then retrieves local market inputs, calculates portfolio-level risk/return, and finally decides whether to finalize or escalate.
